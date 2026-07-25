"""Deterministic in-memory evaluation of the existing R1 and R2 pipeline."""

import re
from enum import StrEnum
from types import MappingProxyType
from typing import Annotated, Final

from pydantic import (
    Field,
    PrivateAttr,
    StrictBool,
    StrictInt,
    StrictStr,
    computed_field,
    field_validator,
    model_validator,
)

from local_ai_guild.contracts import (
    BoundaryModel,
    RefusalReason,
    RefusedRoutingDecision,
    SuccessfulRoutingDecision,
    ToolIdentifier,
)
from local_ai_guild.evidence import R1_EVIDENCE_REGISTRY
from local_ai_guild.mock_router import route_user_input
from local_ai_guild.policy import (
    ALLOW_EVIDENCE_BY_TOOL,
    APPROVAL_EVIDENCE_BY_TOOL,
    POLICY_EVIDENCE_REGISTRY,
    PolicyIssueCode,
    PolicyOutcome,
    PolicyProfile,
    _policy_profile_is_consistent,
    build_policy_evaluation_envelope,
)

_CASE_IDENTIFIER_PATTERN: Final = r"^[a-z][a-z0-9_-]*:[a-z0-9][a-z0-9._-]*$"

type CaseIdentifier = Annotated[
    StrictStr,
    Field(min_length=3, max_length=128, pattern=_CASE_IDENTIFIER_PATTERN),
]
type EvaluationInput = (
    Annotated[StrictStr, Field(max_length=256)]
    | Annotated[StrictInt, Field(ge=-1_000_000, le=1_000_000)]
)
type StableIdentifiers = Annotated[tuple[StrictStr, ...], Field(min_length=1)]


class RoutingOutcome(StrEnum):
    """Stable routing outcomes compared by R3."""

    ROUTED = "routed"
    REFUSED = "refused"


class EvaluationInputError(TypeError):
    """A bounded rejection for unvalidated evaluation input."""


_ROUTING_EVIDENCE_BY_TOOL: Final = MappingProxyType(
    {
        ToolIdentifier.PROJECT_STATUS: ("rule:project-status-v1",),
        ToolIdentifier.SEARCH_PUBLIC_DOCS: ("rule:search-public-docs-v1",),
        ToolIdentifier.READ_PUBLIC_DOC: ("rule:read-public-doc-v1",),
    }
)
_ROUTING_EVIDENCE_BY_REASON: Final = MappingProxyType(
    {
        RefusalReason.UNKNOWN_REQUEST: ("rule:refuse-unknown-request-v1",),
        RefusalReason.INVALID_REQUEST: ("rule:refuse-invalid-request-v1",),
        RefusalReason.INVALID_ARGUMENTS: ("rule:refuse-invalid-arguments-v1",),
    }
)
_ALLOW_POLICY_EVIDENCE_BY_TOOL: Final = MappingProxyType(
    {tool: (reference.identifier,) for tool, reference in ALLOW_EVIDENCE_BY_TOOL.items()}
)
_APPROVAL_POLICY_EVIDENCE_BY_TOOL: Final = MappingProxyType(
    {tool: (reference.identifier,) for tool, reference in APPROVAL_EVIDENCE_BY_TOOL.items()}
)
_ROUTING_REFUSAL_POLICY_EVIDENCE: Final = ("policy:refuse-routing-refusal-v1",)
_NOT_ALLOWLISTED_POLICY_EVIDENCE: Final = ("policy:refuse-unallowlisted-tool-v1",)


def _is_case_identifier(value: object) -> bool:
    return (
        type(value) is str
        and 3 <= len(value) <= 128
        and re.fullmatch(_CASE_IDENTIFIER_PATTERN, value) is not None
        and value.partition(":")[0] == "eval"
    )


def _identifiers_are_valid(
    values: object,
    namespace: str,
    registry: object,
) -> bool:
    return (
        type(values) is tuple
        and bool(values)
        and all(
            type(value) is str and value.partition(":")[0] == namespace and value in registry
            for value in values
        )
        and len(set(values)) == len(values)
    )


class ExpectedEvaluationResult(BoundaryModel):
    """Stable expected R1/R2 behavior for one authorized synthetic case."""

    routing_outcome: RoutingOutcome
    routing_reason: RefusalReason | None = None
    routed_tool: ToolIdentifier | None = None
    routing_evidence_identifiers: StableIdentifiers
    policy_outcome: PolicyOutcome
    policy_issue_codes: tuple[PolicyIssueCode, ...] = ()
    policy_evidence_identifiers: StableIdentifiers

    @model_validator(mode="after")
    def fields_must_be_internally_consistent(self) -> "ExpectedEvaluationResult":
        """Reject contradictory routing, policy, issue, and evidence expectations."""
        if not _expected_result_is_consistent(self):
            raise ValueError("expected evaluation result fields are inconsistent")
        return self


def _expected_result_is_consistent(expected: object) -> bool:
    if type(expected) is not ExpectedEvaluationResult:
        return False
    routing_outcome = getattr(expected, "routing_outcome", None)
    routing_reason = getattr(expected, "routing_reason", None)
    routed_tool = getattr(expected, "routed_tool", None)
    routing_evidence = getattr(expected, "routing_evidence_identifiers", None)
    policy_outcome = getattr(expected, "policy_outcome", None)
    policy_issues = getattr(expected, "policy_issue_codes", None)
    policy_evidence = getattr(expected, "policy_evidence_identifiers", None)

    if (
        type(routing_outcome) is not RoutingOutcome
        or type(policy_outcome) is not PolicyOutcome
        or type(policy_issues) is not tuple
        or any(type(code) is not PolicyIssueCode for code in policy_issues)
        or len(set(policy_issues)) != len(policy_issues)
        or not _identifiers_are_valid(routing_evidence, "rule", R1_EVIDENCE_REGISTRY)
        or not _identifiers_are_valid(policy_evidence, "policy", POLICY_EVIDENCE_REGISTRY)
    ):
        return False

    if routing_outcome is RoutingOutcome.ROUTED:
        if routing_reason is not None or type(routed_tool) is not ToolIdentifier:
            return False
        if routing_evidence != _ROUTING_EVIDENCE_BY_TOOL[routed_tool]:
            return False
    elif routing_outcome is RoutingOutcome.REFUSED:
        if type(routing_reason) is not RefusalReason or routed_tool is not None:
            return False
        if routing_evidence != _ROUTING_EVIDENCE_BY_REASON[routing_reason]:
            return False
        return (
            policy_outcome is PolicyOutcome.REFUSE
            and policy_issues == (PolicyIssueCode.ROUTING_WAS_REFUSED,)
            and policy_evidence == _ROUTING_REFUSAL_POLICY_EVIDENCE
        )
    else:
        return False

    if policy_outcome is PolicyOutcome.ALLOW:
        return not policy_issues and policy_evidence == _ALLOW_POLICY_EVIDENCE_BY_TOOL[routed_tool]
    if policy_outcome is PolicyOutcome.REQUIRE_HUMAN_APPROVAL:
        return (
            policy_issues == (PolicyIssueCode.HUMAN_APPROVAL_REQUIRED,)
            and policy_evidence == _APPROVAL_POLICY_EVIDENCE_BY_TOOL[routed_tool]
        )
    if policy_outcome is PolicyOutcome.REFUSE:
        return (
            policy_issues == (PolicyIssueCode.TOOL_NOT_ALLOWLISTED,)
            and policy_evidence == _NOT_ALLOWLISTED_POLICY_EVIDENCE
        )
    return False


class EvaluationCase(BoundaryModel):
    """One bounded public or synthetic input and its deterministic expectation."""

    identifier: CaseIdentifier
    description: StrictStr = Field(min_length=1, max_length=160)
    input: EvaluationInput
    policy_profile: PolicyProfile
    expected: ExpectedEvaluationResult

    @field_validator("identifier")
    @classmethod
    def identifier_must_use_eval_namespace(cls, value: str) -> str:
        if not _is_case_identifier(value):
            raise ValueError("evaluation case identifier must use the eval namespace")
        return value

    @field_validator("description")
    @classmethod
    def description_must_be_bounded_plain_text(cls, value: str) -> str:
        if value != value.strip() or any(
            ord(character) < 32 or ord(character) == 127 for character in value
        ):
            raise ValueError("evaluation case description must be bounded plain text")
        return value

    @field_validator("policy_profile", mode="before")
    @classmethod
    def profile_must_be_an_exact_instance(cls, value: object) -> object:
        if type(value) is not PolicyProfile:
            raise ValueError("evaluation case requires an exact policy profile")
        return value

    @field_validator("expected", mode="before")
    @classmethod
    def expected_must_be_an_exact_instance(cls, value: object) -> object:
        if type(value) is not ExpectedEvaluationResult:
            raise ValueError("evaluation case requires an exact expected result")
        return value

    @model_validator(mode="after")
    def fields_must_be_internally_consistent(self) -> "EvaluationCase":
        """Bind the expected policy outcome to the exact immutable profile."""
        if not _evaluation_case_is_consistent(self):
            raise ValueError("evaluation case fields are inconsistent")
        return self


def _evaluation_case_is_consistent(case: object) -> bool:
    if type(case) is not EvaluationCase:
        return False
    identifier = getattr(case, "identifier", None)
    description = getattr(case, "description", None)
    case_input = getattr(case, "input", None)
    profile = getattr(case, "policy_profile", None)
    expected = getattr(case, "expected", None)
    if (
        not _is_case_identifier(identifier)
        or type(description) is not str
        or not 1 <= len(description) <= 160
        or description != description.strip()
        or any(ord(character) < 32 or ord(character) == 127 for character in description)
        or not (
            (type(case_input) is str and len(case_input) <= 256)
            or (type(case_input) is int and -1_000_000 <= case_input <= 1_000_000)
        )
        or not _policy_profile_is_consistent(profile)
        or not _expected_result_is_consistent(expected)
    ):
        return False

    if (
        expected.routing_outcome is RoutingOutcome.REFUSED
        or expected.routed_tool not in profile.allowlisted_tools
    ):
        required_outcome = PolicyOutcome.REFUSE
    elif expected.routed_tool in profile.approval_required_tools:
        required_outcome = PolicyOutcome.REQUIRE_HUMAN_APPROVAL
    else:
        required_outcome = PolicyOutcome.ALLOW
    return expected.policy_outcome is required_outcome


class EvaluationMismatchCode(StrEnum):
    """Stable bounded mismatch categories in comparison order."""

    ROUTING_OUTCOME_MISMATCH = "routing_outcome_mismatch"
    ROUTING_REASON_MISMATCH = "routing_reason_mismatch"
    ROUTED_TOOL_MISMATCH = "routed_tool_mismatch"
    ROUTING_EVIDENCE_MISMATCH = "routing_evidence_mismatch"
    POLICY_OUTCOME_MISMATCH = "policy_outcome_mismatch"
    POLICY_ISSUE_MISMATCH = "policy_issue_mismatch"
    POLICY_EVIDENCE_MISMATCH = "policy_evidence_mismatch"
    INVALID_CASE = "invalid_case"
    EVALUATION_ERROR = "evaluation_error"


class _BuilderAuthority(StrEnum):
    """Private deterministic builder capabilities, never serialized."""

    RESULT = "result"
    SUMMARY = "summary"


_MISMATCH_DEFINITIONS: Final = (
    (
        EvaluationMismatchCode.ROUTING_OUTCOME_MISMATCH,
        ("The routing outcome did not match the case expectation"),
    ),
    (
        EvaluationMismatchCode.ROUTING_REASON_MISMATCH,
        ("The routing refusal reason did not match the case expectation"),
    ),
    (
        EvaluationMismatchCode.ROUTED_TOOL_MISMATCH,
        ("The routed tool did not match the case expectation"),
    ),
    (
        EvaluationMismatchCode.ROUTING_EVIDENCE_MISMATCH,
        ("The routing evidence did not match the case expectation"),
    ),
    (
        EvaluationMismatchCode.POLICY_OUTCOME_MISMATCH,
        ("The policy outcome did not match the case expectation"),
    ),
    (
        EvaluationMismatchCode.POLICY_ISSUE_MISMATCH,
        ("The policy issues did not match the case expectation"),
    ),
    (
        EvaluationMismatchCode.POLICY_EVIDENCE_MISMATCH,
        ("The policy evidence did not match the case expectation"),
    ),
    (EvaluationMismatchCode.INVALID_CASE, "The evaluation case is invalid"),
    (EvaluationMismatchCode.EVALUATION_ERROR, "The evaluation could not be completed"),
)


def _build_mismatch_messages(
    definitions: object,
) -> MappingProxyType[EvaluationMismatchCode, str]:
    """Build the complete message registry without hidden duplicate codes."""
    if type(definitions) is not tuple or any(
        type(item) is not tuple
        or len(item) != 2
        or type(item[0]) is not EvaluationMismatchCode
        or type(item[1]) is not str
        or not 1 <= len(item[1]) <= 96
        for item in definitions
    ):
        raise RuntimeError("evaluation mismatch definitions are invalid")
    codes = tuple(item[0] for item in definitions)
    if len(set(codes)) != len(codes) or set(codes) != set(EvaluationMismatchCode):
        raise RuntimeError("evaluation mismatch definitions must be unique and complete")
    return MappingProxyType(dict(definitions))


_MISMATCH_MESSAGES: Final = _build_mismatch_messages(_MISMATCH_DEFINITIONS)


class EvaluationMismatch(BoundaryModel):
    """One bounded mismatch without raw input or arbitrary error content."""

    code: EvaluationMismatchCode

    @computed_field(return_type=str)
    @property
    def message(self) -> str:
        """Derive the only permitted message from the stable mismatch code."""
        return _MISMATCH_MESSAGES[self.code]


EVALUATION_MISMATCH_REGISTRY: Final = MappingProxyType(
    {code: EvaluationMismatch(code=code) for code in _MISMATCH_MESSAGES}
)
_MISMATCH_ORDER: Final = (
    EvaluationMismatchCode.ROUTING_OUTCOME_MISMATCH,
    EvaluationMismatchCode.ROUTING_REASON_MISMATCH,
    EvaluationMismatchCode.ROUTED_TOOL_MISMATCH,
    EvaluationMismatchCode.ROUTING_EVIDENCE_MISMATCH,
    EvaluationMismatchCode.POLICY_OUTCOME_MISMATCH,
    EvaluationMismatchCode.POLICY_ISSUE_MISMATCH,
    EvaluationMismatchCode.POLICY_EVIDENCE_MISMATCH,
    EvaluationMismatchCode.INVALID_CASE,
    EvaluationMismatchCode.EVALUATION_ERROR,
)
if len(_MISMATCH_ORDER) != len(EVALUATION_MISMATCH_REGISTRY) or set(_MISMATCH_ORDER) != set(
    EVALUATION_MISMATCH_REGISTRY
):
    raise RuntimeError("evaluation mismatch order must be unique and complete")
_MISMATCH_ORDER_INDEX: Final = MappingProxyType(
    {code: index for index, code in enumerate(_MISMATCH_ORDER)}
)
_RESULT_BUILDER_AUTHORITY: Final = _BuilderAuthority.RESULT
_SUMMARY_BUILDER_AUTHORITY: Final = _BuilderAuthority.SUMMARY


class EvaluationCaseResult(BoundaryModel):
    """Bounded actual R1/R2 behavior for one case, with no raw input."""

    case_identifier: CaseIdentifier
    passed: StrictBool
    mismatches: tuple[EvaluationMismatch, ...] = ()
    actual_routing_outcome: RoutingOutcome
    actual_routing_reason: RefusalReason | None = None
    actual_routed_tool: ToolIdentifier | None = None
    actual_routing_evidence_identifiers: StableIdentifiers
    actual_policy_outcome: PolicyOutcome
    actual_policy_issue_codes: tuple[PolicyIssueCode, ...] = ()
    actual_policy_evidence_identifiers: StableIdentifiers
    _builder_authority: _BuilderAuthority | None = PrivateAttr(default=None)
    _bound_case_identifier: str | None = PrivateAttr(default=None)
    _bound_expected: ExpectedEvaluationResult | None = PrivateAttr(default=None)

    def __init__(self, **data: object) -> None:
        """Permit construction only through the deterministic evaluator."""
        authority = data.pop("_builder_authority", None)
        expected = data.pop("_bound_expected", None)
        if authority is not _RESULT_BUILDER_AUTHORITY or not _expected_result_is_consistent(
            expected
        ):
            raise EvaluationInputError(
                "Evaluation case results are created only by the deterministic evaluator"
            )
        super().__init__(**data)
        if _expected_mismatch_codes(
            routing_outcome=self.actual_routing_outcome,
            routing_reason=self.actual_routing_reason,
            routed_tool=self.actual_routed_tool,
            routing_evidence=self.actual_routing_evidence_identifiers,
            policy_outcome=self.actual_policy_outcome,
            policy_issues=self.actual_policy_issue_codes,
            policy_evidence=self.actual_policy_evidence_identifiers,
            expected=expected,
        ) != tuple(mismatch.code for mismatch in self.mismatches):
            raise EvaluationInputError("The deterministic evaluation result is inconsistent")
        self._builder_authority = authority
        self._bound_case_identifier = self.case_identifier
        self._bound_expected = expected
        if not _trusted_case_result_is_consistent(self):
            raise EvaluationInputError("The deterministic evaluation result is inconsistent")

    @field_validator("case_identifier")
    @classmethod
    def identifier_must_use_eval_namespace(cls, value: str) -> str:
        if not _is_case_identifier(value):
            raise ValueError("evaluation result identifier must use the eval namespace")
        return value

    @field_validator("mismatches", mode="before")
    @classmethod
    def mismatches_must_be_exact_instances(cls, value: object) -> object:
        if type(value) is not tuple or any(type(item) is not EvaluationMismatch for item in value):
            raise ValueError("evaluation result mismatches must be exact typed instances")
        return value

    @model_validator(mode="after")
    def fields_must_be_internally_consistent(self) -> "EvaluationCaseResult":
        if not _case_result_fields_are_consistent(self):
            raise ValueError("evaluation case result fields are inconsistent")
        return self


def _case_result_fields_are_consistent(result: object) -> bool:
    if type(result) is not EvaluationCaseResult:
        return False
    identifier = getattr(result, "case_identifier", None)
    passed = getattr(result, "passed", None)
    mismatches = getattr(result, "mismatches", None)
    routing_outcome = getattr(result, "actual_routing_outcome", None)
    routing_reason = getattr(result, "actual_routing_reason", None)
    routed_tool = getattr(result, "actual_routed_tool", None)
    routing_evidence = getattr(result, "actual_routing_evidence_identifiers", None)
    policy_outcome = getattr(result, "actual_policy_outcome", None)
    policy_issues = getattr(result, "actual_policy_issue_codes", None)
    policy_evidence = getattr(result, "actual_policy_evidence_identifiers", None)
    mismatch_codes = (
        tuple(getattr(mismatch, "code", None) for mismatch in mismatches)
        if type(mismatches) is tuple
        else ()
    )

    if (
        not _is_case_identifier(identifier)
        or type(passed) is not bool
        or type(mismatches) is not tuple
        or any(type(mismatch) is not EvaluationMismatch for mismatch in mismatches)
        or any(type(code) is not EvaluationMismatchCode for code in mismatch_codes)
        or any(
            EVALUATION_MISMATCH_REGISTRY.get(code) is not mismatch
            for code, mismatch in zip(mismatch_codes, mismatches, strict=True)
        )
        or passed != (len(mismatches) == 0)
        or len(set(mismatch_codes)) != len(mismatch_codes)
        or tuple(sorted(mismatch_codes, key=_MISMATCH_ORDER_INDEX.__getitem__)) != mismatch_codes
        or type(routing_outcome) is not RoutingOutcome
        or type(policy_outcome) is not PolicyOutcome
        or type(policy_issues) is not tuple
        or any(type(code) is not PolicyIssueCode for code in policy_issues)
        or len(set(policy_issues)) != len(policy_issues)
        or not _identifiers_are_valid(routing_evidence, "rule", R1_EVIDENCE_REGISTRY)
        or not _identifiers_are_valid(policy_evidence, "policy", POLICY_EVIDENCE_REGISTRY)
    ):
        return False

    if routing_outcome is RoutingOutcome.ROUTED:
        if routing_reason is not None or type(routed_tool) is not ToolIdentifier:
            return False
        if routing_evidence != _ROUTING_EVIDENCE_BY_TOOL[routed_tool]:
            return False
    elif routing_outcome is RoutingOutcome.REFUSED:
        if type(routing_reason) is not RefusalReason or routed_tool is not None:
            return False
        if routing_evidence != _ROUTING_EVIDENCE_BY_REASON[routing_reason]:
            return False
        return (
            policy_outcome is PolicyOutcome.REFUSE
            and policy_issues == (PolicyIssueCode.ROUTING_WAS_REFUSED,)
            and policy_evidence == _ROUTING_REFUSAL_POLICY_EVIDENCE
        )
    else:
        return False

    if policy_outcome is PolicyOutcome.ALLOW:
        return not policy_issues and policy_evidence == _ALLOW_POLICY_EVIDENCE_BY_TOOL[routed_tool]
    if policy_outcome is PolicyOutcome.REQUIRE_HUMAN_APPROVAL:
        return (
            policy_issues == (PolicyIssueCode.HUMAN_APPROVAL_REQUIRED,)
            and policy_evidence == _APPROVAL_POLICY_EVIDENCE_BY_TOOL[routed_tool]
        )
    if policy_outcome is PolicyOutcome.REFUSE:
        return (
            policy_issues == (PolicyIssueCode.TOOL_NOT_ALLOWLISTED,)
            and policy_evidence == _NOT_ALLOWLISTED_POLICY_EVIDENCE
        )
    return False


def _expected_mismatch_codes(
    *,
    routing_outcome: RoutingOutcome,
    routing_reason: RefusalReason | None,
    routed_tool: ToolIdentifier | None,
    routing_evidence: tuple[str, ...],
    policy_outcome: PolicyOutcome,
    policy_issues: tuple[PolicyIssueCode, ...],
    policy_evidence: tuple[str, ...],
    expected: ExpectedEvaluationResult,
) -> tuple[EvaluationMismatchCode, ...]:
    """Compare one internally consistent actual result in the documented order."""
    codes: list[EvaluationMismatchCode] = []
    if routing_outcome is not expected.routing_outcome:
        codes.append(EvaluationMismatchCode.ROUTING_OUTCOME_MISMATCH)
    else:
        if (
            routing_outcome is RoutingOutcome.REFUSED
            and routing_reason is not expected.routing_reason
        ):
            codes.append(EvaluationMismatchCode.ROUTING_REASON_MISMATCH)
        if routing_outcome is RoutingOutcome.ROUTED and routed_tool is not expected.routed_tool:
            codes.append(EvaluationMismatchCode.ROUTED_TOOL_MISMATCH)
    if routing_evidence != expected.routing_evidence_identifiers:
        codes.append(EvaluationMismatchCode.ROUTING_EVIDENCE_MISMATCH)
    if policy_outcome is not expected.policy_outcome:
        codes.append(EvaluationMismatchCode.POLICY_OUTCOME_MISMATCH)
    if policy_issues != expected.policy_issue_codes:
        codes.append(EvaluationMismatchCode.POLICY_ISSUE_MISMATCH)
    if policy_evidence != expected.policy_evidence_identifiers:
        codes.append(EvaluationMismatchCode.POLICY_EVIDENCE_MISMATCH)
    return tuple(codes)


def _trusted_case_result_is_consistent(result: object) -> bool:
    """Recheck fields plus the evaluator-owned, non-serialized case binding."""
    if not _case_result_fields_are_consistent(result):
        return False
    expected = getattr(result, "_bound_expected", None)
    return (
        getattr(result, "_builder_authority", None) is _RESULT_BUILDER_AUTHORITY
        and getattr(result, "_bound_case_identifier", None) == result.case_identifier
        and _expected_result_is_consistent(expected)
        and _expected_mismatch_codes(
            routing_outcome=result.actual_routing_outcome,
            routing_reason=result.actual_routing_reason,
            routed_tool=result.actual_routed_tool,
            routing_evidence=result.actual_routing_evidence_identifiers,
            policy_outcome=result.actual_policy_outcome,
            policy_issues=result.actual_policy_issue_codes,
            policy_evidence=result.actual_policy_evidence_identifiers,
            expected=expected,
        )
        == tuple(mismatch.code for mismatch in result.mismatches)
    )


class EvaluationSummary(BoundaryModel):
    """Deterministic in-memory aggregate for one non-empty ordered case tuple."""

    total_case_count: StrictInt = Field(ge=1)
    passed_case_count: StrictInt = Field(ge=0)
    failed_case_count: StrictInt = Field(ge=0)
    case_results: Annotated[tuple[EvaluationCaseResult, ...], Field(min_length=1)]
    succeeded: StrictBool
    _builder_authority: _BuilderAuthority | None = PrivateAttr(default=None)
    _bound_case_identifiers: tuple[str, ...] = PrivateAttr(default=())

    def __init__(self, **data: object) -> None:
        """Permit construction only through the deterministic batch evaluator."""
        authority = data.pop("_builder_authority", None)
        if authority is not _SUMMARY_BUILDER_AUTHORITY:
            raise EvaluationInputError(
                "Evaluation summaries are created only by the deterministic evaluator"
            )
        super().__init__(**data)
        self._builder_authority = authority
        self._bound_case_identifiers = tuple(result.case_identifier for result in self.case_results)
        if not _trusted_summary_is_consistent(self):
            raise EvaluationInputError("The deterministic evaluation summary is inconsistent")

    @field_validator("case_results", mode="before")
    @classmethod
    def results_must_be_exact_instances(cls, value: object) -> object:
        if type(value) is not tuple or any(
            type(item) is not EvaluationCaseResult for item in value
        ):
            raise ValueError("evaluation summary requires exact typed case results")
        return value

    @model_validator(mode="after")
    def counts_must_match_results(self) -> "EvaluationSummary":
        if not _summary_fields_are_consistent(self):
            raise ValueError("evaluation summary counts or identifiers are inconsistent")
        return self


def _summary_fields_are_consistent(summary: object) -> bool:
    """Recheck summary fields and every evaluator-bound result."""
    if type(summary) is not EvaluationSummary:
        return False
    results = getattr(summary, "case_results", None)
    if (
        type(results) is not tuple
        or not results
        or any(not _trusted_case_result_is_consistent(result) for result in results)
    ):
        return False
    passed = sum(result.passed for result in results)
    failed = len(results) - passed
    identifiers = tuple(result.case_identifier for result in results)
    return (
        type(getattr(summary, "total_case_count", None)) is int
        and type(getattr(summary, "passed_case_count", None)) is int
        and type(getattr(summary, "failed_case_count", None)) is int
        and type(getattr(summary, "succeeded", None)) is bool
        and summary.total_case_count == len(results)
        and summary.passed_case_count == passed
        and summary.failed_case_count == failed
        and summary.total_case_count == summary.passed_case_count + summary.failed_case_count
        and summary.succeeded is (failed == 0)
        and len(set(identifiers)) == len(identifiers)
    )


def _trusted_summary_is_consistent(summary: object) -> bool:
    """Recheck a summary's private builder authority and ordered case binding."""
    if not _summary_fields_are_consistent(summary):
        return False
    identifiers = tuple(result.case_identifier for result in summary.case_results)
    return (
        getattr(summary, "_builder_authority", None) is _SUMMARY_BUILDER_AUTHORITY
        and getattr(summary, "_bound_case_identifiers", None) == identifiers
    )


def _mismatch(code: EvaluationMismatchCode) -> EvaluationMismatch:
    return EVALUATION_MISMATCH_REGISTRY[code]


def evaluate_case(case: object) -> EvaluationCaseResult:
    """Evaluate one exact validated case without execution, parsing, or persistence."""
    if not _evaluation_case_is_consistent(case):
        raise EvaluationInputError("An exact validated evaluation case is required")

    decision = route_user_input(case.input)
    envelope = build_policy_evaluation_envelope(decision, case.policy_profile)
    routing_decision = envelope.routing.decision
    if type(routing_decision) is SuccessfulRoutingDecision:
        routing_outcome = RoutingOutcome.ROUTED
        routing_reason = None
        routed_tool = routing_decision.proposal.tool
    elif type(routing_decision) is RefusedRoutingDecision:
        routing_outcome = RoutingOutcome.REFUSED
        routing_reason = routing_decision.reason
        routed_tool = None
    else:
        raise EvaluationInputError("The deterministic evaluation could not be completed")

    routing_evidence = tuple(reference.identifier for reference in envelope.routing.evidence)
    policy_outcome = envelope.policy.outcome
    policy_issues = tuple(issue.code for issue in envelope.policy.issues)
    policy_evidence = tuple(reference.identifier for reference in envelope.policy.evidence)

    expected = case.expected
    mismatch_codes = _expected_mismatch_codes(
        routing_outcome=routing_outcome,
        routing_reason=routing_reason,
        routed_tool=routed_tool,
        routing_evidence=routing_evidence,
        policy_outcome=policy_outcome,
        policy_issues=policy_issues,
        policy_evidence=policy_evidence,
        expected=expected,
    )
    mismatches = tuple(_mismatch(code) for code in mismatch_codes)
    return EvaluationCaseResult(
        case_identifier=case.identifier,
        passed=not mismatches,
        mismatches=mismatches,
        actual_routing_outcome=routing_outcome,
        actual_routing_reason=routing_reason,
        actual_routed_tool=routed_tool,
        actual_routing_evidence_identifiers=routing_evidence,
        actual_policy_outcome=policy_outcome,
        actual_policy_issue_codes=policy_issues,
        actual_policy_evidence_identifiers=policy_evidence,
        _builder_authority=_RESULT_BUILDER_AUTHORITY,
        _bound_expected=expected,
    )


def evaluate_cases(cases: object) -> EvaluationSummary:
    """Evaluate a non-empty exact tuple, preserving case and result order."""
    if type(cases) is not tuple or not cases:
        raise EvaluationInputError("A non-empty tuple of evaluation cases is required")
    if any(not _evaluation_case_is_consistent(case) for case in cases):
        raise EvaluationInputError("Every evaluation case must be an exact validated instance")
    identifiers = tuple(case.identifier for case in cases)
    if len(set(identifiers)) != len(identifiers):
        raise EvaluationInputError("Evaluation case identifiers must be unique")

    results = tuple(evaluate_case(case) for case in cases)
    passed = sum(result.passed for result in results)
    failed = len(results) - passed
    return EvaluationSummary(
        total_case_count=len(results),
        passed_case_count=passed,
        failed_case_count=failed,
        case_results=results,
        succeeded=failed == 0,
        _builder_authority=_SUMMARY_BUILDER_AUTHORITY,
    )
