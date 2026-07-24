"""Deterministic deny-by-default policy checks with no execution capability."""

from collections.abc import Mapping
from enum import StrEnum
from types import MappingProxyType
from typing import Annotated, Final

from pydantic import Field, StrictStr, field_serializer, field_validator, model_validator

from local_ai_guild.contracts import (
    BoundaryModel,
    RefusedRoutingDecision,
    ToolIdentifier,
)
from local_ai_guild.evidence import (
    EvidenceKind,
    EvidenceReference,
    RoutingDecisionEnvelope,
    _routing_envelope_is_consistent,
    _synthetic_evidence_registry,
    build_routing_decision_envelope,
)


class PolicyOutcome(StrEnum):
    """R2 outcomes; none performs an action."""

    ALLOW = "allow"
    REFUSE = "refuse"
    REQUIRE_HUMAN_APPROVAL = "require_human_approval"


class PolicyIssueCode(StrEnum):
    """Stable, non-user-derived policy issue codes."""

    ROUTING_WAS_REFUSED = "routing_was_refused"
    TOOL_NOT_ALLOWLISTED = "tool_not_allowlisted"
    HUMAN_APPROVAL_REQUIRED = "human_approval_required"
    INVALID_POLICY_INPUT = "invalid_policy_input"


class PolicyIssue(BoundaryModel):
    """Bounded policy metadata without proposal arguments or request content."""

    code: PolicyIssueCode
    message: StrictStr = Field(min_length=1, max_length=160)


class PolicyProfile(BoundaryModel):
    """An immutable allowlist and approval requirement profile."""

    allowlisted_tools: frozenset[ToolIdentifier]
    approval_required_tools: frozenset[ToolIdentifier]

    @model_validator(mode="after")
    def approval_tools_must_be_allowlisted(self) -> "PolicyProfile":
        """Prevent contradictory approval requirements outside the allowlist."""
        if not self.approval_required_tools.issubset(self.allowlisted_tools):
            raise ValueError("approval-required tools must be allowlisted")
        return self

    @field_serializer("allowlisted_tools", "approval_required_tools", when_used="json")
    def serialize_tool_sets(
        self,
        value: frozenset[ToolIdentifier],
    ) -> tuple[str, ...]:
        """Serialize immutable sets in a deterministic order."""
        return tuple(sorted(tool.value for tool in value))


DEFAULT_POLICY_PROFILE: Final = PolicyProfile(
    allowlisted_tools=frozenset(ToolIdentifier),
    approval_required_tools=frozenset({ToolIdentifier.READ_PUBLIC_DOC}),
)


POLICY_EVIDENCE_REGISTRY: Final[Mapping[str, EvidenceReference]] = _synthetic_evidence_registry(
    (
        "policy:refuse-routing-refusal-v1",
        "policy:refuse-unallowlisted-tool-v1",
        "policy:allow-project-status-v1",
        "policy:allow-search-public-docs-v1",
        "policy:allow-read-public-doc-v1",
        "policy:require-approval-project-status-v1",
        "policy:require-approval-search-public-docs-v1",
        "policy:require-approval-read-public-doc-v1",
    ),
    EvidenceKind.POLICY_RULE,
)

ALLOW_EVIDENCE_BY_TOOL: Final[Mapping[ToolIdentifier, EvidenceReference]] = MappingProxyType(
    {
        ToolIdentifier.PROJECT_STATUS: POLICY_EVIDENCE_REGISTRY["policy:allow-project-status-v1"],
        ToolIdentifier.SEARCH_PUBLIC_DOCS: POLICY_EVIDENCE_REGISTRY[
            "policy:allow-search-public-docs-v1"
        ],
        ToolIdentifier.READ_PUBLIC_DOC: POLICY_EVIDENCE_REGISTRY["policy:allow-read-public-doc-v1"],
    }
)

APPROVAL_EVIDENCE_BY_TOOL: Final[Mapping[ToolIdentifier, EvidenceReference]] = MappingProxyType(
    {
        ToolIdentifier.PROJECT_STATUS: POLICY_EVIDENCE_REGISTRY[
            "policy:require-approval-project-status-v1"
        ],
        ToolIdentifier.SEARCH_PUBLIC_DOCS: POLICY_EVIDENCE_REGISTRY[
            "policy:require-approval-search-public-docs-v1"
        ],
        ToolIdentifier.READ_PUBLIC_DOC: POLICY_EVIDENCE_REGISTRY[
            "policy:require-approval-read-public-doc-v1"
        ],
    }
)

type PolicyEvidence = Annotated[tuple[EvidenceReference, ...], Field(min_length=1)]


def _same_instances(actual: tuple[object, ...], expected: tuple[object, ...]) -> bool:
    return len(actual) == len(expected) and all(
        item is expected_item for item, expected_item in zip(actual, expected, strict=True)
    )


class PolicyDecision(BoundaryModel):
    """A deterministic policy outcome that never represents execution."""

    outcome: PolicyOutcome
    issues: tuple[PolicyIssue, ...] = ()
    evidence: PolicyEvidence
    tool: ToolIdentifier | None = None

    @field_validator("issues", mode="before")
    @classmethod
    def issues_must_be_typed_instances(cls, value: object) -> object:
        """Reject caller-written issue dictionaries and mutable collections."""
        if type(value) is not tuple or any(type(item) is not PolicyIssue for item in value):
            raise ValueError("policy issues must contain typed policy issue instances")
        return value

    @field_validator("evidence", mode="before")
    @classmethod
    def evidence_must_be_typed_instances(cls, value: object) -> object:
        """Reject caller-written evidence dictionaries and mutable collections."""
        if type(value) is not tuple or any(type(item) is not EvidenceReference for item in value):
            raise ValueError("policy evidence must contain typed evidence references")
        return value

    @model_validator(mode="after")
    def evidence_must_be_registered_policy_rules(self) -> "PolicyDecision":
        """Restrict policy evidence to immutable deterministic constants."""
        if not _policy_decision_is_internally_consistent(self):
            raise ValueError("policy decision fields are inconsistent")
        return self


class PolicyInputError(TypeError):
    """A constant bounded rejection for unvalidated policy input."""


ROUTING_REFUSED_ISSUE: Final = PolicyIssue(
    code=PolicyIssueCode.ROUTING_WAS_REFUSED,
    message="Routing refused the request before policy evaluation",
)
NOT_ALLOWLISTED_ISSUE: Final = PolicyIssue(
    code=PolicyIssueCode.TOOL_NOT_ALLOWLISTED,
    message="The routed tool is not allowlisted by this policy profile",
)
APPROVAL_REQUIRED_ISSUE: Final = PolicyIssue(
    code=PolicyIssueCode.HUMAN_APPROVAL_REQUIRED,
    message="The routed tool requires human approval",
)


def _policy_profile_is_consistent(profile: object) -> bool:
    """Recheck profile invariants without parsing or collection coercion."""
    if type(profile) is not PolicyProfile:
        return False
    allowlisted = getattr(profile, "allowlisted_tools", None)
    approval_required = getattr(profile, "approval_required_tools", None)
    return (
        type(allowlisted) is frozenset
        and type(approval_required) is frozenset
        and all(type(tool) is ToolIdentifier for tool in allowlisted)
        and all(type(tool) is ToolIdentifier for tool in approval_required)
        and approval_required.issubset(allowlisted)
    )


def _policy_decision_is_internally_consistent(decision: object) -> bool:
    """Require constants selected from the immutable policy registries."""
    if type(decision) is not PolicyDecision:
        return False
    issues = getattr(decision, "issues", None)
    evidence = getattr(decision, "evidence", None)
    outcome = getattr(decision, "outcome", None)
    tool = getattr(decision, "tool", None)
    if (
        type(issues) is not tuple
        or any(type(issue) is not PolicyIssue for issue in issues)
        or type(evidence) is not tuple
        or not evidence
        or any(type(reference) is not EvidenceReference for reference in evidence)
    ):
        return False
    identifiers = tuple(getattr(reference, "identifier", None) for reference in evidence)
    if any(type(identifier) is not str for identifier in identifiers):
        return False
    if len(set(identifiers)) != len(identifiers) or any(
        POLICY_EVIDENCE_REGISTRY.get(identifier) is not reference
        for identifier, reference in zip(identifiers, evidence, strict=True)
    ):
        return False

    if outcome is PolicyOutcome.ALLOW:
        reference = ALLOW_EVIDENCE_BY_TOOL.get(tool)
        return (
            type(tool) is ToolIdentifier
            and not issues
            and reference is not None
            and _same_instances(evidence, (reference,))
        )
    if outcome is PolicyOutcome.REQUIRE_HUMAN_APPROVAL:
        reference = APPROVAL_EVIDENCE_BY_TOOL.get(tool)
        return (
            type(tool) is ToolIdentifier
            and _same_instances(issues, (APPROVAL_REQUIRED_ISSUE,))
            and reference is not None
            and _same_instances(evidence, (reference,))
        )
    if outcome is not PolicyOutcome.REFUSE:
        return False
    if tool is None:
        return _same_instances(issues, (ROUTING_REFUSED_ISSUE,)) and _same_instances(
            evidence,
            (POLICY_EVIDENCE_REGISTRY["policy:refuse-routing-refusal-v1"],),
        )
    return (
        type(tool) is ToolIdentifier
        and _same_instances(issues, (NOT_ALLOWLISTED_ISSUE,))
        and _same_instances(
            evidence,
            (POLICY_EVIDENCE_REGISTRY["policy:refuse-unallowlisted-tool-v1"],),
        )
    )


def _policy_matches_routing_and_profile(
    policy: object,
    routing: object,
    profile: object,
) -> bool:
    """Bind a policy result to the exact routing envelope and immutable profile."""
    if (
        not _policy_decision_is_internally_consistent(policy)
        or not _routing_envelope_is_consistent(routing)
        or not _policy_profile_is_consistent(profile)
    ):
        return False
    routing_decision = routing.decision
    if type(routing_decision) is RefusedRoutingDecision:
        return (
            policy.outcome is PolicyOutcome.REFUSE
            and policy.tool is None
            and _same_instances(policy.issues, (ROUTING_REFUSED_ISSUE,))
        )

    tool = routing_decision.proposal.tool
    if tool not in profile.allowlisted_tools:
        return (
            policy.outcome is PolicyOutcome.REFUSE
            and policy.tool is tool
            and _same_instances(policy.issues, (NOT_ALLOWLISTED_ISSUE,))
        )
    if tool in profile.approval_required_tools:
        return (
            policy.outcome is PolicyOutcome.REQUIRE_HUMAN_APPROVAL
            and policy.tool is tool
            and _same_instances(policy.issues, (APPROVAL_REQUIRED_ISSUE,))
        )
    return policy.outcome is PolicyOutcome.ALLOW and policy.tool is tool and not policy.issues


class PolicyEvaluationEnvelope(BoundaryModel):
    """A routing envelope, exact profile, and their non-executing policy result."""

    routing: RoutingDecisionEnvelope
    profile: PolicyProfile
    policy: PolicyDecision

    @field_validator("routing", mode="before")
    @classmethod
    def routing_must_be_an_exact_validated_instance(cls, value: object) -> object:
        """Reject raw dictionaries, arbitrary objects, and subclasses."""
        if type(value) is not RoutingDecisionEnvelope:
            raise ValueError("routing must be an exact validated routing envelope")
        return value

    @field_validator("profile", mode="before")
    @classmethod
    def profile_must_be_an_exact_validated_instance(cls, value: object) -> object:
        """Reject raw dictionaries, arbitrary objects, and subclasses."""
        if type(value) is not PolicyProfile:
            raise ValueError("profile must be an exact validated policy profile")
        return value

    @field_validator("policy", mode="before")
    @classmethod
    def policy_must_be_an_exact_validated_instance(cls, value: object) -> object:
        """Reject raw dictionaries, arbitrary objects, and subclasses."""
        if type(value) is not PolicyDecision:
            raise ValueError("policy must be an exact validated policy decision")
        return value

    @model_validator(mode="after")
    def policy_must_match_routing_and_profile(self) -> "PolicyEvaluationEnvelope":
        """Prevent contradictory or profile-unbound nested objects."""
        if not _policy_matches_routing_and_profile(self.policy, self.routing, self.profile):
            raise ValueError("policy must match the routing envelope and policy profile")
        return self


def evaluate_policy(
    envelope: object,
    profile: PolicyProfile = DEFAULT_POLICY_PROFILE,
) -> PolicyDecision:
    """Evaluate exact validated inputs; subclasses are rejected deliberately."""
    if not _routing_envelope_is_consistent(envelope):
        raise PolicyInputError("A validated routing decision envelope is required")
    if not _policy_profile_is_consistent(profile):
        raise PolicyInputError("A validated policy profile is required")

    decision = envelope.decision
    if type(decision) is RefusedRoutingDecision:
        return PolicyDecision(
            outcome=PolicyOutcome.REFUSE,
            issues=(ROUTING_REFUSED_ISSUE,),
            evidence=(POLICY_EVIDENCE_REGISTRY["policy:refuse-routing-refusal-v1"],),
        )

    tool = decision.proposal.tool
    if tool not in profile.allowlisted_tools:
        return PolicyDecision(
            outcome=PolicyOutcome.REFUSE,
            issues=(NOT_ALLOWLISTED_ISSUE,),
            evidence=(POLICY_EVIDENCE_REGISTRY["policy:refuse-unallowlisted-tool-v1"],),
            tool=tool,
        )

    if tool in profile.approval_required_tools:
        return PolicyDecision(
            outcome=PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
            issues=(APPROVAL_REQUIRED_ISSUE,),
            evidence=(APPROVAL_EVIDENCE_BY_TOOL[tool],),
            tool=tool,
        )

    return PolicyDecision(
        outcome=PolicyOutcome.ALLOW,
        evidence=(ALLOW_EVIDENCE_BY_TOOL[tool],),
        tool=tool,
    )


def build_policy_evaluation_envelope(
    decision: object,
    profile: PolicyProfile = DEFAULT_POLICY_PROFILE,
) -> PolicyEvaluationEnvelope:
    """Wrap an exact R1 decision and profile; subclasses and raw data are rejected."""
    routing_envelope = build_routing_decision_envelope(decision)
    policy_decision = evaluate_policy(routing_envelope, profile)
    return PolicyEvaluationEnvelope(
        routing=routing_envelope,
        profile=profile,
        policy=policy_decision,
    )
