"""Tests for the deterministic, non-executing R3 evaluation harness."""

import json

import pytest
from pydantic import ValidationError

from local_ai_guild.contracts import RefusalReason, ToolIdentifier
from local_ai_guild.evaluation import (
    EVALUATION_MISMATCH_REGISTRY,
    EvaluationCase,
    EvaluationCaseResult,
    EvaluationInputError,
    EvaluationMismatch,
    EvaluationMismatchCode,
    EvaluationSummary,
    ExpectedEvaluationResult,
    RoutingOutcome,
    _build_mismatch_messages,
    _trusted_case_result_is_consistent,
    _trusted_summary_is_consistent,
    evaluate_case,
    evaluate_cases,
)
from local_ai_guild.evaluation_cases import (
    EMPTY_POLICY_PROFILE,
    R3_EVALUATION_CASES,
)
from local_ai_guild.policy import (
    DEFAULT_POLICY_PROFILE,
    PolicyIssueCode,
    PolicyOutcome,
    PolicyProfile,
)


def status_allowed_expectation() -> ExpectedEvaluationResult:
    return ExpectedEvaluationResult(
        routing_outcome=RoutingOutcome.ROUTED,
        routed_tool=ToolIdentifier.PROJECT_STATUS,
        routing_evidence_identifiers=("rule:project-status-v1",),
        policy_outcome=PolicyOutcome.ALLOW,
        policy_evidence_identifiers=("policy:allow-project-status-v1",),
    )


def status_case(
    *,
    identifier: str = "eval:synthetic-status-v1",
    expected: ExpectedEvaluationResult | None = None,
) -> EvaluationCase:
    return EvaluationCase(
        identifier=identifier,
        description="Synthetic status evaluation case",
        input="status",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=expected or status_allowed_expectation(),
    )


def result_fields(result: EvaluationCaseResult) -> dict[str, object]:
    return {
        "case_identifier": result.case_identifier,
        "passed": result.passed,
        "mismatches": result.mismatches,
        "actual_routing_outcome": result.actual_routing_outcome,
        "actual_routing_reason": result.actual_routing_reason,
        "actual_routed_tool": result.actual_routed_tool,
        "actual_routing_evidence_identifiers": (result.actual_routing_evidence_identifiers),
        "actual_policy_outcome": result.actual_policy_outcome,
        "actual_policy_issue_codes": result.actual_policy_issue_codes,
        "actual_policy_evidence_identifiers": result.actual_policy_evidence_identifiers,
    }


def test_r3_boundary_models_are_strict_frozen_and_forbid_extras() -> None:
    models = (
        ExpectedEvaluationResult,
        EvaluationCase,
        EvaluationMismatch,
        EvaluationCaseResult,
        EvaluationSummary,
    )
    for model in models:
        assert model.model_config["strict"] is True
        assert model.model_config["extra"] == "forbid"
        assert model.model_config["frozen"] is True

    with pytest.raises(ValidationError):
        EvaluationCase(
            identifier="eval:extra-field-v1",
            description="Synthetic extra-field case",
            input="status",
            policy_profile=DEFAULT_POLICY_PROFILE,
            expected=status_allowed_expectation(),
            unexpected=True,  # type: ignore[call-arg]
        )


@pytest.mark.parametrize(
    "identifier",
    [
        "",
        "ab",
        f"eval:{'a' * 124}",
        " eval:status-v1",
        "eval:status-v1 ",
        "Eval:status-v1",
        "eval:Status-v1",
        "eval:with whitespace",
        "eval:with\tcontrol",
        "eval:with\nnewline",
        "1eval:status-v1",
        ":missing-namespace",
        "eval:",
        "eval:multiple:colons",
        "rule:status-v1",
        "https:example.com",
        "http:example.com",
        "file:case.json",
        "c:case.json",
        "eval/path",
        r"eval:path\case",
        "arbitrary evaluation prose",
    ],
)
def test_case_identifier_rejects_invalid_forms(identifier: str) -> None:
    with pytest.raises(ValidationError):
        status_case(identifier=identifier)


def test_case_identifier_accepts_bounded_eval_namespace() -> None:
    assert status_case().identifier == "eval:synthetic-status-v1"


def test_case_rejects_raw_nested_models_and_is_frozen() -> None:
    expected = status_allowed_expectation()
    with pytest.raises(ValidationError):
        EvaluationCase(
            identifier="eval:raw-profile-v1",
            description="Synthetic raw-profile case",
            input="status",
            policy_profile=DEFAULT_POLICY_PROFILE.model_dump(),
            expected=expected,
        )
    with pytest.raises(ValidationError):
        EvaluationCase(
            identifier="eval:raw-expected-v1",
            description="Synthetic raw-expected case",
            input="status",
            policy_profile=DEFAULT_POLICY_PROFILE,
            expected=expected.model_dump(),
        )
    with pytest.raises(ValidationError):
        EvaluationCase(
            identifier="eval:control-description-v1",
            description="Synthetic\x00description",
            input="status",
            policy_profile=DEFAULT_POLICY_PROFILE,
            expected=expected,
        )

    case = status_case()
    with pytest.raises(ValidationError):
        case.identifier = "eval:mutated-v1"  # type: ignore[misc]


def test_case_binds_expected_policy_outcome_to_profile() -> None:
    with pytest.raises(ValidationError):
        EvaluationCase(
            identifier="eval:contradictory-profile-v1",
            description="Synthetic contradictory-profile case",
            input="status",
            policy_profile=EMPTY_POLICY_PROFILE,
            expected=status_allowed_expectation(),
        )


@pytest.mark.parametrize(
    "fields",
    [
        {
            "routing_outcome": RoutingOutcome.ROUTED,
            "routing_evidence_identifiers": ("rule:project-status-v1",),
            "policy_outcome": PolicyOutcome.ALLOW,
            "policy_evidence_identifiers": ("policy:allow-project-status-v1",),
        },
        {
            "routing_outcome": RoutingOutcome.REFUSED,
            "routing_reason": RefusalReason.UNKNOWN_REQUEST,
            "routed_tool": ToolIdentifier.PROJECT_STATUS,
            "routing_evidence_identifiers": ("rule:refuse-unknown-request-v1",),
            "policy_outcome": PolicyOutcome.REFUSE,
            "policy_issue_codes": (PolicyIssueCode.ROUTING_WAS_REFUSED,),
            "policy_evidence_identifiers": ("policy:refuse-routing-refusal-v1",),
        },
        {
            "routing_outcome": RoutingOutcome.REFUSED,
            "routing_reason": RefusalReason.UNKNOWN_REQUEST,
            "routing_evidence_identifiers": ("rule:refuse-unknown-request-v1",),
            "policy_outcome": PolicyOutcome.ALLOW,
            "policy_evidence_identifiers": ("policy:allow-project-status-v1",),
        },
        {
            "routing_outcome": RoutingOutcome.ROUTED,
            "routing_evidence_identifiers": ("rule:read-public-doc-v1",),
            "policy_outcome": PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
            "policy_issue_codes": (PolicyIssueCode.HUMAN_APPROVAL_REQUIRED,),
            "policy_evidence_identifiers": ("policy:require-approval-read-public-doc-v1",),
        },
        {
            "routing_outcome": RoutingOutcome.ROUTED,
            "routed_tool": ToolIdentifier.PROJECT_STATUS,
            "routing_evidence_identifiers": ("policy:allow-project-status-v1",),
            "policy_outcome": PolicyOutcome.ALLOW,
            "policy_evidence_identifiers": ("policy:allow-project-status-v1",),
        },
        {
            "routing_outcome": RoutingOutcome.ROUTED,
            "routed_tool": ToolIdentifier.PROJECT_STATUS,
            "routing_evidence_identifiers": ("rule:project-status-v1",),
            "policy_outcome": PolicyOutcome.ALLOW,
            "policy_evidence_identifiers": ("rule:project-status-v1",),
        },
        {
            "routing_outcome": RoutingOutcome.ROUTED,
            "routed_tool": ToolIdentifier.PROJECT_STATUS,
            "routing_evidence_identifiers": (
                "rule:project-status-v1",
                "rule:project-status-v1",
            ),
            "policy_outcome": PolicyOutcome.ALLOW,
            "policy_evidence_identifiers": ("policy:allow-project-status-v1",),
        },
        {
            "routing_outcome": RoutingOutcome.ROUTED,
            "routed_tool": ToolIdentifier.PROJECT_STATUS,
            "routing_evidence_identifiers": ("rule:project-status-v1",),
            "policy_outcome": PolicyOutcome.ALLOW,
            "policy_evidence_identifiers": (
                "policy:allow-project-status-v1",
                "policy:allow-project-status-v1",
            ),
        },
    ],
)
def test_expected_result_rejects_contradictory_fields(fields: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        ExpectedEvaluationResult(**fields)  # type: ignore[arg-type]


def test_expected_result_rejects_raw_enum_strings_and_extra_fields() -> None:
    with pytest.raises(ValidationError):
        ExpectedEvaluationResult(
            routing_outcome="routed",  # type: ignore[arg-type]
            routed_tool=ToolIdentifier.PROJECT_STATUS,
            routing_evidence_identifiers=("rule:project-status-v1",),
            policy_outcome=PolicyOutcome.ALLOW,
            policy_evidence_identifiers=("policy:allow-project-status-v1",),
        )
    with pytest.raises(ValidationError):
        ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.ROUTED,
            routed_tool=ToolIdentifier.PROJECT_STATUS,
            routing_evidence_identifiers=("rule:project-status-v1",),
            policy_outcome=PolicyOutcome.ALLOW,
            policy_evidence_identifiers=("policy:allow-project-status-v1",),
            execution_result="forbidden",  # type: ignore[call-arg]
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("routing_evidence_identifiers", ("rule:syntactically-valid-unknown-v1",)),
        ("routing_evidence_identifiers", ("rule:search-public-docs-v1",)),
        ("policy_evidence_identifiers", ("policy:syntactically-valid-unknown-v1",)),
        ("policy_evidence_identifiers", ("policy:allow-read-public-doc-v1",)),
        ("policy_issue_codes", (PolicyIssueCode.HUMAN_APPROVAL_REQUIRED,)),
        (
            "policy_issue_codes",
            (
                PolicyIssueCode.TOOL_NOT_ALLOWLISTED,
                PolicyIssueCode.TOOL_NOT_ALLOWLISTED,
            ),
        ),
    ],
)
def test_expected_result_rejects_unknown_or_semantically_wrong_registered_values(
    field: str,
    value: object,
) -> None:
    fields = status_allowed_expectation().model_dump()
    fields[field] = value
    with pytest.raises(ValidationError):
        ExpectedEvaluationResult(**fields)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "case_input",
    [
        [],
        {},
        {"synthetic": "value"},
        RuntimeError("SYNTHETIC_EXCEPTION_MARKER"),
        object(),
        json,
        lambda: None,
    ],
)
def test_case_input_rejects_arbitrary_objects_and_collections(case_input: object) -> None:
    with pytest.raises(ValidationError):
        EvaluationCase(
            identifier="eval:bounded-input-v1",
            description="Synthetic bounded-input rejection case",
            input=case_input,  # type: ignore[arg-type]
            policy_profile=DEFAULT_POLICY_PROFILE,
            expected=status_allowed_expectation(),
        )


def test_unchecked_case_and_expected_instances_are_revalidated_by_evaluator() -> None:
    marker = "PRIVATE_UNCHECKED_EXPECTATION_MARKER"
    corrupt_expected = status_allowed_expectation().model_copy(
        update={"routing_evidence_identifiers": (marker,)}
    )
    corrupt_case = EvaluationCase.model_construct(
        identifier="eval:unchecked-case-v1",
        description="Synthetic unchecked case",
        input="status",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=corrupt_expected,
    )

    with pytest.raises(EvaluationInputError) as captured:
        evaluate_case(corrupt_case)
    assert marker not in str(captured.value)


def test_raw_subclass_and_unchecked_policy_profiles_are_rejected() -> None:
    class ProfileSubclass(PolicyProfile):
        pass

    subclass = ProfileSubclass(
        allowlisted_tools=frozenset({ToolIdentifier.PROJECT_STATUS}),
        approval_required_tools=frozenset(),
    )
    with pytest.raises(ValidationError):
        EvaluationCase(
            identifier="eval:profile-subclass-v1",
            description="Synthetic profile-subclass case",
            input="status",
            policy_profile=subclass,
            expected=status_allowed_expectation(),
        )

    corrupt_profiles = (
        PolicyProfile.model_construct(
            allowlisted_tools=[ToolIdentifier.PROJECT_STATUS],
            approval_required_tools=[],
        ),
        PolicyProfile.model_construct(
            allowlisted_tools=frozenset({"project_status"}),
            approval_required_tools=frozenset(),
        ),
        PolicyProfile.model_construct(
            allowlisted_tools=frozenset(),
            approval_required_tools=frozenset({ToolIdentifier.PROJECT_STATUS}),
        ),
    )
    for index, profile in enumerate(corrupt_profiles):
        corrupt_case = EvaluationCase.model_construct(
            identifier=f"eval:unchecked-profile-{index}-v1",
            description="Synthetic unchecked-profile case",
            input="status",
            policy_profile=profile,
            expected=status_allowed_expectation(),
        )
        with pytest.raises(EvaluationInputError, match="exact validated"):
            evaluate_case(corrupt_case)


def test_mismatch_messages_are_derived_and_registry_owned_in_results() -> None:
    code = EvaluationMismatchCode.ROUTING_OUTCOME_MISMATCH
    with pytest.raises(ValidationError):
        EvaluationMismatch(code=code, message="PRIVATE_CALLER_MESSAGE")  # type: ignore[call-arg]

    lookalike = EvaluationMismatch(code=code)
    assert lookalike.message == EVALUATION_MISMATCH_REGISTRY[code].message
    assert lookalike is not EVALUATION_MISMATCH_REGISTRY[code]

    passing = evaluate_case(status_case())
    corrupted = passing.model_copy(update={"passed": False, "mismatches": (lookalike,)})
    assert not _trusted_case_result_is_consistent(corrupted)


def test_mismatch_registry_builder_rejects_duplicate_or_incomplete_codes() -> None:
    code = EvaluationMismatchCode.ROUTING_OUTCOME_MISMATCH
    with pytest.raises(RuntimeError, match="unique and complete"):
        _build_mismatch_messages(((code, "First"), (code, "Second")))


def test_case_results_are_builder_controlled_and_bound_to_expectation() -> None:
    passing = evaluate_case(status_case())
    fields = result_fields(passing)

    with pytest.raises(EvaluationInputError, match="created only"):
        EvaluationCaseResult(**fields)  # type: ignore[arg-type]

    assert _trusted_case_result_is_consistent(passing)
    assert "_bound_expected" not in passing.model_dump()
    assert "_builder_authority" not in passing.model_dump()


def test_case_result_relabeling_and_forged_pass_are_detected() -> None:
    passing = evaluate_case(status_case())
    unbound = EvaluationCaseResult.model_construct(**result_fields(passing))
    assert not _trusted_case_result_is_consistent(unbound)

    relabeled = passing.model_copy(update={"case_identifier": "eval:relabeled-synthetic-v1"})
    assert not _trusted_case_result_is_consistent(relabeled)

    wrong_expectation = ExpectedEvaluationResult(
        routing_outcome=RoutingOutcome.ROUTED,
        routed_tool=ToolIdentifier.READ_PUBLIC_DOC,
        routing_evidence_identifiers=("rule:read-public-doc-v1",),
        policy_outcome=PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
        policy_issue_codes=(PolicyIssueCode.HUMAN_APPROVAL_REQUIRED,),
        policy_evidence_identifiers=("policy:require-approval-read-public-doc-v1",),
    )
    failing = evaluate_case(status_case(expected=wrong_expectation))
    forged_pass = failing.model_copy(update={"passed": True, "mismatches": ()})
    assert not _trusted_case_result_is_consistent(forged_pass)


def test_case_result_detects_raw_duplicate_and_out_of_order_mismatches() -> None:
    passing = evaluate_case(status_case())
    routing = EVALUATION_MISMATCH_REGISTRY[EvaluationMismatchCode.ROUTING_EVIDENCE_MISMATCH]
    policy = EVALUATION_MISMATCH_REGISTRY[EvaluationMismatchCode.POLICY_EVIDENCE_MISMATCH]

    raw = passing.model_copy(update={"passed": False, "mismatches": (routing.model_dump(),)})
    duplicate = passing.model_copy(update={"passed": False, "mismatches": (routing, routing)})
    out_of_order = passing.model_copy(update={"passed": False, "mismatches": (policy, routing)})
    assert not _trusted_case_result_is_consistent(raw)
    assert not _trusted_case_result_is_consistent(duplicate)
    assert not _trusted_case_result_is_consistent(out_of_order)


@pytest.mark.parametrize(
    "updates",
    [
        {
            "actual_routing_outcome": RoutingOutcome.REFUSED,
            "actual_routing_reason": RefusalReason.UNKNOWN_REQUEST,
            "actual_routed_tool": ToolIdentifier.PROJECT_STATUS,
        },
        {
            "actual_routing_outcome": RoutingOutcome.REFUSED,
            "actual_routing_reason": None,
            "actual_routed_tool": None,
        },
        {"actual_routing_evidence_identifiers": ("policy:allow-project-status-v1",)},
        {"actual_routing_evidence_identifiers": ("rule:unknown-registered-shape-v1",)},
        {
            "actual_routing_evidence_identifiers": (
                "rule:project-status-v1",
                "rule:project-status-v1",
            )
        },
        {
            "actual_policy_evidence_identifiers": (
                "policy:allow-project-status-v1",
                "policy:allow-project-status-v1",
            )
        },
        {"actual_policy_issue_codes": ("tool_not_allowlisted",)},
    ],
)
def test_case_result_detects_malformed_actual_envelopes(
    updates: dict[str, object],
) -> None:
    corrupted = evaluate_case(status_case()).model_copy(update=updates)
    assert not _trusted_case_result_is_consistent(corrupted)


def test_summaries_are_builder_controlled_and_detect_forged_state() -> None:
    first = evaluate_case(status_case(identifier="eval:first-status-v1"))
    second = evaluate_case(status_case(identifier="eval:second-status-v1"))
    summary = evaluate_cases(
        (
            status_case(identifier="eval:first-status-v1"),
            status_case(identifier="eval:second-status-v1"),
        )
    )

    with pytest.raises(EvaluationInputError, match="created only"):
        EvaluationSummary(
            total_case_count=1,
            passed_case_count=1,
            failed_case_count=0,
            case_results=(first,),
            succeeded=True,
        )

    assert _trusted_summary_is_consistent(summary)
    assert not _trusted_summary_is_consistent(summary.model_copy(update={"total_case_count": 3}))
    assert not _trusted_summary_is_consistent(
        summary.model_copy(update={"case_results": (first, first)})
    )
    assert not _trusted_summary_is_consistent(
        summary.model_copy(update={"case_results": (second, first)})
    )

    forged_result = first.model_copy(update={"case_identifier": "eval:forged-status-v1"})
    forged_green = summary.model_copy(
        update={
            "total_case_count": 1,
            "passed_case_count": 1,
            "failed_case_count": 0,
            "case_results": (forged_result,),
            "succeeded": True,
        }
    )
    assert not _trusted_summary_is_consistent(forged_green)

    raw_summary = EvaluationSummary.model_construct(
        total_case_count=1,
        passed_case_count=1,
        failed_case_count=0,
        case_results=(first.model_dump(),),
        succeeded=True,
    )
    assert not _trusted_summary_is_consistent(raw_summary)


def test_evaluate_case_rejects_raw_subclass_and_arbitrary_objects_without_echo() -> None:
    marker = "PRIVATE_EVALUATOR_OBJECT_MARKER"

    class MarkerObject:
        def __repr__(self) -> str:
            return marker

    class CaseSubclass(EvaluationCase):
        pass

    for value in (
        {marker: "attacker field"},
        MarkerObject(),
    ):
        with pytest.raises(EvaluationInputError) as captured:
            evaluate_case(value)
        assert marker not in str(captured.value)

    with pytest.raises(ValidationError):
        CaseSubclass(
            identifier="eval:subclass-v1",
            description="Synthetic subclass case",
            input="status",
            policy_profile=DEFAULT_POLICY_PROFILE,
            expected=status_allowed_expectation(),
        )


@pytest.mark.parametrize(
    "cases",
    [
        [],
        (),
        [status_case()],
        {status_case()},
        {"eval:case": status_case()},
        (case for case in (status_case(),)),
        ({"identifier": "eval:raw-v1"},),
        (object(),),
    ],
)
def test_evaluate_cases_rejects_non_exact_or_empty_batches(cases: object) -> None:
    with pytest.raises(EvaluationInputError):
        evaluate_cases(cases)


def test_evaluate_cases_rejects_tuple_subclass() -> None:
    class CaseTuple(tuple[EvaluationCase, ...]):
        pass

    with pytest.raises(EvaluationInputError):
        evaluate_cases(CaseTuple((status_case(),)))


def test_evaluate_case_rejects_unchecked_subclass_instance() -> None:
    class CaseSubclass(EvaluationCase):
        pass

    unchecked = CaseSubclass.model_construct(
        identifier="eval:unchecked-subclass-v1",
        description="Synthetic unchecked-subclass case",
        input="status",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=status_allowed_expectation(),
    )
    with pytest.raises(EvaluationInputError, match="exact validated"):
        evaluate_case(unchecked)


def test_evaluate_cases_rejects_duplicate_identifiers_without_echo() -> None:
    case = status_case(identifier="eval:duplicate-marker-v1")
    with pytest.raises(EvaluationInputError) as captured:
        evaluate_cases((case, case))
    assert case.identifier not in str(captured.value)


def test_all_versioned_cases_pass_in_declared_order() -> None:
    summary = evaluate_cases(R3_EVALUATION_CASES)

    assert len(R3_EVALUATION_CASES) == 10
    assert summary.total_case_count == 10
    assert summary.passed_case_count == 10
    assert summary.failed_case_count == 0
    assert summary.succeeded is True
    assert tuple(result.case_identifier for result in summary.case_results) == tuple(
        case.identifier for case in R3_EVALUATION_CASES
    )
    assert all(result.passed and not result.mismatches for result in summary.case_results)


def test_mismatch_comparison_order_is_stable() -> None:
    read_approval = ExpectedEvaluationResult(
        routing_outcome=RoutingOutcome.ROUTED,
        routed_tool=ToolIdentifier.READ_PUBLIC_DOC,
        routing_evidence_identifiers=("rule:read-public-doc-v1",),
        policy_outcome=PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
        policy_issue_codes=(PolicyIssueCode.HUMAN_APPROVAL_REQUIRED,),
        policy_evidence_identifiers=("policy:require-approval-read-public-doc-v1",),
    )
    result = evaluate_case(status_case(expected=read_approval))

    assert tuple(mismatch.code for mismatch in result.mismatches) == (
        EvaluationMismatchCode.ROUTED_TOOL_MISMATCH,
        EvaluationMismatchCode.ROUTING_EVIDENCE_MISMATCH,
        EvaluationMismatchCode.POLICY_OUTCOME_MISMATCH,
        EvaluationMismatchCode.POLICY_ISSUE_MISMATCH,
        EvaluationMismatchCode.POLICY_EVIDENCE_MISMATCH,
    )


def test_routing_outcome_mismatch_suppresses_reason_and_tool_mismatches() -> None:
    case = EvaluationCase(
        identifier="eval:suppressed-inapplicable-v1",
        description="Synthetic inapplicable-mismatch suppression case",
        input="unknown synthetic command",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=status_allowed_expectation(),
    )
    result = evaluate_case(case)
    codes = tuple(mismatch.code for mismatch in result.mismatches)

    assert codes == (
        EvaluationMismatchCode.ROUTING_OUTCOME_MISMATCH,
        EvaluationMismatchCode.ROUTING_EVIDENCE_MISMATCH,
        EvaluationMismatchCode.POLICY_OUTCOME_MISMATCH,
        EvaluationMismatchCode.POLICY_ISSUE_MISMATCH,
        EvaluationMismatchCode.POLICY_EVIDENCE_MISMATCH,
    )
    assert EvaluationMismatchCode.ROUTING_REASON_MISMATCH not in codes
    assert EvaluationMismatchCode.ROUTED_TOOL_MISMATCH not in codes


def test_marker_inputs_do_not_enter_results_or_summary() -> None:
    markers = (
        "PRIVATE_UNKNOWN_COMMAND_MARKER",
        "PRIVATE_SEARCH_QUERY_MARKER",
        "PRIVATE_DOCUMENT_PATH_MARKER",
    )
    unknown = EvaluationCase(
        identifier="eval:marker-unknown-v1",
        description="Synthetic unknown-command marker case",
        input=markers[0],
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.REFUSED,
            routing_reason=RefusalReason.UNKNOWN_REQUEST,
            routing_evidence_identifiers=("rule:refuse-unknown-request-v1",),
            policy_outcome=PolicyOutcome.REFUSE,
            policy_issue_codes=(PolicyIssueCode.ROUTING_WAS_REFUSED,),
            policy_evidence_identifiers=("policy:refuse-routing-refusal-v1",),
        ),
    )
    search = EvaluationCase(
        identifier="eval:marker-search-v1",
        description="Synthetic search-query marker case",
        input=f"search docs: {markers[1]}",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.ROUTED,
            routed_tool=ToolIdentifier.SEARCH_PUBLIC_DOCS,
            routing_evidence_identifiers=("rule:search-public-docs-v1",),
            policy_outcome=PolicyOutcome.ALLOW,
            policy_evidence_identifiers=("policy:allow-search-public-docs-v1",),
        ),
    )
    document = EvaluationCase(
        identifier="eval:marker-document-v1",
        description="Synthetic document-path marker case",
        input=f"read doc: docs/{markers[2]}.md",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.ROUTED,
            routed_tool=ToolIdentifier.READ_PUBLIC_DOC,
            routing_evidence_identifiers=("rule:read-public-doc-v1",),
            policy_outcome=PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
            policy_issue_codes=(PolicyIssueCode.HUMAN_APPROVAL_REQUIRED,),
            policy_evidence_identifiers=("policy:require-approval-read-public-doc-v1",),
        ),
    )

    summary_json = evaluate_cases((unknown, search, document)).model_dump_json()
    assert all(marker not in summary_json for marker in markers)


def test_invalid_input_object_cannot_enter_a_case_or_evaluator_error() -> None:
    marker = "PRIVATE_INVALID_REQUEST_OBJECT_MARKER"

    class InvalidRequest:
        def __repr__(self) -> str:
            return marker

    with pytest.raises(ValidationError):
        EvaluationCase(
            identifier="eval:invalid-object-v1",
            description="Synthetic invalid-object case",
            input=InvalidRequest(),
            policy_profile=DEFAULT_POLICY_PROFILE,
            expected=status_allowed_expectation(),
        )
    with pytest.raises(EvaluationInputError) as captured:
        evaluate_case(InvalidRequest())
    assert marker not in str(captured.value)


def test_serialization_and_evaluation_are_byte_deterministic() -> None:
    case = R3_EVALUATION_CASES[-1]
    first_case = case.model_dump_json()
    second_case = case.model_dump_json()
    first_summary = evaluate_cases(R3_EVALUATION_CASES).model_dump_json()
    second_summary = evaluate_cases(R3_EVALUATION_CASES).model_dump_json()

    assert first_case == second_case
    assert first_summary == second_summary
    assert json.loads(first_case)["policy_profile"]["allowlisted_tools"] == [
        "project_status",
        "search_public_docs",
    ]


def test_failing_evaluation_serialization_is_byte_deterministic() -> None:
    wrong_expectation = ExpectedEvaluationResult(
        routing_outcome=RoutingOutcome.ROUTED,
        routed_tool=ToolIdentifier.READ_PUBLIC_DOC,
        routing_evidence_identifiers=("rule:read-public-doc-v1",),
        policy_outcome=PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
        policy_issue_codes=(PolicyIssueCode.HUMAN_APPROVAL_REQUIRED,),
        policy_evidence_identifiers=("policy:require-approval-read-public-doc-v1",),
    )
    case = status_case(expected=wrong_expectation)

    first = evaluate_case(case).model_dump_json()
    second = evaluate_case(case).model_dump_json()
    assert first == second
    assert tuple(mismatch["code"] for mismatch in json.loads(first)["mismatches"]) == (
        EvaluationMismatchCode.ROUTED_TOOL_MISMATCH,
        EvaluationMismatchCode.ROUTING_EVIDENCE_MISMATCH,
        EvaluationMismatchCode.POLICY_OUTCOME_MISMATCH,
        EvaluationMismatchCode.POLICY_ISSUE_MISMATCH,
        EvaluationMismatchCode.POLICY_EVIDENCE_MISMATCH,
    )


def test_markers_do_not_enter_bounded_builder_or_evaluator_errors() -> None:
    marker = "PRIVATE_BOUNDARY_ERROR_MARKER"

    class MarkerObject:
        def __repr__(self) -> str:
            return marker

    corrupt_case = EvaluationCase.model_construct(
        identifier="eval:marker-corrupt-v1",
        description="Synthetic marker-corrupt case",
        input="status",
        policy_profile=MarkerObject(),
        expected=status_allowed_expectation(),
    )
    corrupt_identifier = EvaluationCase.model_construct(
        identifier=f"eval:{marker}",
        description="Synthetic invalid-identifier marker case",
        input="status",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=status_allowed_expectation(),
    )
    calls = (
        lambda: evaluate_case(MarkerObject()),
        lambda: evaluate_case({marker: MarkerObject()}),
        lambda: evaluate_case(corrupt_case),
        lambda: evaluate_case(corrupt_identifier),
        lambda: evaluate_cases((corrupt_case,)),
        lambda: EvaluationCaseResult(marker=MarkerObject()),  # type: ignore[call-arg]
        lambda: EvaluationSummary(marker=MarkerObject()),  # type: ignore[call-arg]
    )
    for call in calls:
        with pytest.raises(EvaluationInputError) as captured:
            call()
        assert marker not in str(captured.value)


def test_primary_r3_json_schemas_generate_in_memory() -> None:
    assert EvaluationCase.model_json_schema()["title"] == "EvaluationCase"
    assert EvaluationCaseResult.model_json_schema()["title"] == "EvaluationCaseResult"
    assert EvaluationSummary.model_json_schema()["title"] == "EvaluationSummary"


def test_results_and_summaries_have_no_input_execution_or_timing_fields() -> None:
    result_fields = set(EvaluationCaseResult.model_fields)
    summary_fields = set(EvaluationSummary.model_fields)

    assert "input" not in result_fields
    assert "query" not in result_fields
    assert "path" not in result_fields
    assert not {"executed", "execution", "duration", "timestamp"} & result_fields
    assert not {"input", "executed", "execution", "duration", "timestamp"} & summary_fields
