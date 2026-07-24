"""Typed, synthetic evidence references for validated R1 routing decisions."""

from collections.abc import Mapping
from enum import StrEnum
from types import MappingProxyType
from typing import Annotated, Final

from pydantic import Field, StrictStr, field_validator, model_validator

from local_ai_guild.contracts import (
    BoundaryModel,
    ProjectStatusArguments,
    ProjectStatusProposal,
    ReadPublicDocArguments,
    ReadPublicDocProposal,
    RefusalReason,
    RefusedRoutingDecision,
    RoutingDecision,
    SearchPublicDocsArguments,
    SearchPublicDocsProposal,
    SuccessfulRoutingDecision,
    ToolIdentifier,
    ValidationIssue,
)
from local_ai_guild.validation import SAFE_LOCATION_PARTS, _safe_validation_message


class EvidenceKind(StrEnum):
    """Evidence categories implemented in R2."""

    ROUTING_RULE = "routing_rule"
    POLICY_RULE = "policy_rule"


class EvidenceProvenance(StrEnum):
    """Public-repository-safe evidence provenance metadata."""

    PUBLIC = "public"
    SYNTHETIC = "synthetic"


class EvidenceReference(BoundaryModel):
    """A typed deterministic reference, not proof of external truth."""

    identifier: StrictStr = Field(
        min_length=3,
        max_length=128,
        pattern=r"^[a-z][a-z0-9_-]*:[a-z0-9][a-z0-9._-]*$",
    )
    kind: EvidenceKind
    provenance: EvidenceProvenance

    @model_validator(mode="after")
    def namespace_must_match_kind(self) -> "EvidenceReference":
        """Keep routing and policy namespaces unambiguous."""
        namespace = self.identifier.partition(":")[0]
        expected_namespace = {
            EvidenceKind.ROUTING_RULE: "rule",
            EvidenceKind.POLICY_RULE: "policy",
        }[self.kind]
        if namespace != expected_namespace:
            raise ValueError("evidence identifier namespace must match evidence kind")
        return self


def _synthetic_evidence_registry(
    identifiers: tuple[str, ...],
    kind: EvidenceKind,
) -> Mapping[str, EvidenceReference]:
    """Build a registry without allowing duplicate identifiers to be hidden."""
    if len(set(identifiers)) != len(identifiers):
        raise RuntimeError("evidence registry identifiers must be unique")
    references = tuple(
        EvidenceReference(
            identifier=identifier,
            kind=kind,
            provenance=EvidenceProvenance.SYNTHETIC,
        )
        for identifier in identifiers
    )
    registry = {reference.identifier: reference for reference in references}
    if len(registry) != len(identifiers):
        raise RuntimeError("evidence registry identifiers must be unique")
    return MappingProxyType(registry)


R1_EVIDENCE_REGISTRY: Final[Mapping[str, EvidenceReference]] = _synthetic_evidence_registry(
    (
        "rule:project-status-v1",
        "rule:search-public-docs-v1",
        "rule:read-public-doc-v1",
        "rule:refuse-unknown-request-v1",
        "rule:refuse-invalid-request-v1",
        "rule:refuse-invalid-arguments-v1",
    ),
    EvidenceKind.ROUTING_RULE,
)

_SUCCESS_EVIDENCE_BY_TOOL: Final[Mapping[ToolIdentifier, tuple[str, ...]]] = MappingProxyType(
    {
        ToolIdentifier.PROJECT_STATUS: ("rule:project-status-v1",),
        ToolIdentifier.SEARCH_PUBLIC_DOCS: ("rule:search-public-docs-v1",),
        ToolIdentifier.READ_PUBLIC_DOC: ("rule:read-public-doc-v1",),
    }
)
_REFUSAL_EVIDENCE_BY_REASON: Final[Mapping[RefusalReason, tuple[str, ...]]] = MappingProxyType(
    {
        RefusalReason.UNKNOWN_REQUEST: ("rule:refuse-unknown-request-v1",),
        RefusalReason.INVALID_REQUEST: ("rule:refuse-invalid-request-v1",),
        RefusalReason.INVALID_ARGUMENTS: ("rule:refuse-invalid-arguments-v1",),
    }
)
_SAFE_VALIDATION_CODES: Final = frozenset(
    {
        "extra_forbidden",
        "greater_than_equal",
        "int_type",
        "less_than_equal",
        "literal_error",
        "missing",
        "string_too_long",
        "string_too_short",
        "string_type",
        "union_tag_invalid",
        "union_tag_not_found",
        "value_error",
    }
)


class EvidenceEnvelopeError(ValueError):
    """A bounded error that never interpolates caller-controlled data."""


type TypedEvidence = Annotated[tuple[EvidenceReference, ...], Field(min_length=1)]


class RoutingDecisionEnvelope(BoundaryModel):
    """A validated R1 decision paired with its registered typed evidence."""

    decision: RoutingDecision
    evidence: TypedEvidence

    @field_validator("decision", mode="before")
    @classmethod
    def decision_must_be_an_exact_validated_instance(cls, value: object) -> object:
        """Reject raw dictionaries, proposals, arbitrary objects, and subclasses."""
        if type(value) not in (SuccessfulRoutingDecision, RefusedRoutingDecision):
            raise ValueError("decision must be an exact validated R1 routing decision")
        return value

    @field_validator("evidence", mode="before")
    @classmethod
    def evidence_must_be_typed_instances(cls, value: object) -> object:
        """Reject raw evidence dictionaries and mutable collections."""
        if type(value) is not tuple or any(type(item) is not EvidenceReference for item in value):
            raise ValueError("routing evidence must contain typed evidence references")
        return value

    @model_validator(mode="after")
    def evidence_must_match_decision(self) -> "RoutingDecisionEnvelope":
        """Reject missing, duplicate, unknown, or inconsistent evidence."""
        if not _routing_envelope_is_consistent(self):
            raise ValueError("routing evidence must match the validated decision and registry")
        return self


def _expected_routing_identifiers(decision: object) -> tuple[str, ...] | None:
    """Return the one R1 evidence sequence valid for an exact decision."""
    if type(decision) is SuccessfulRoutingDecision:
        proposal = getattr(decision, "proposal", None)
        expected = {
            ProjectStatusProposal: (
                ToolIdentifier.PROJECT_STATUS,
                ProjectStatusArguments,
            ),
            SearchPublicDocsProposal: (
                ToolIdentifier.SEARCH_PUBLIC_DOCS,
                SearchPublicDocsArguments,
            ),
            ReadPublicDocProposal: (
                ToolIdentifier.READ_PUBLIC_DOC,
                ReadPublicDocArguments,
            ),
        }.get(type(proposal))
        if expected is None:
            return None
        expected_tool, expected_arguments = expected
        if (
            getattr(proposal, "tool", None) is not expected_tool
            or type(getattr(proposal, "arguments", None)) is not expected_arguments
        ):
            return None
        return _SUCCESS_EVIDENCE_BY_TOOL[expected_tool]
    if type(decision) is RefusedRoutingDecision:
        reason = getattr(decision, "reason", None)
        if type(reason) is not RefusalReason:
            return None
        return _REFUSAL_EVIDENCE_BY_REASON[reason]
    return None


def _arguments_are_validated(proposal: object) -> bool:
    """Recheck the small R1 argument shapes without parsing or filesystem I/O."""
    if type(proposal) not in (
        ProjectStatusProposal,
        SearchPublicDocsProposal,
        ReadPublicDocProposal,
    ):
        return False
    arguments = getattr(proposal, "arguments", None)
    if type(proposal) is ProjectStatusProposal:
        return type(arguments) is ProjectStatusArguments and not arguments.__dict__
    if type(proposal) is SearchPublicDocsProposal:
        query = getattr(arguments, "query", None)
        max_results = getattr(arguments, "max_results", None)
        if (
            type(arguments) is not SearchPublicDocsArguments
            or type(query) is not str
            or type(max_results) is not int
            or not 1 <= max_results <= 10
        ):
            return False
        try:
            return (
                SearchPublicDocsArguments.query_must_not_be_blank(query) == query
                and len(query) <= 200
            )
        except ValueError:
            return False
    if type(proposal) is ReadPublicDocProposal:
        if (
            type(arguments) is not ReadPublicDocArguments
            or type(getattr(arguments, "path", None)) is not str
        ):
            return False
        try:
            return (
                ReadPublicDocArguments.path_must_be_safe_public_markdown(arguments.path)
                == arguments.path
            )
        except ValueError:
            return False
    return False


def _refusal_issues_are_redaction_safe(decision: RefusedRoutingDecision) -> bool:
    """Reject caller-authored issue content that is outside the R1 safe vocabulary."""
    issues = getattr(decision, "issues", None)
    if type(issues) is not tuple or any(type(issue) is not ValidationIssue for issue in issues):
        return False
    if getattr(decision, "reason", None) is RefusalReason.UNKNOWN_REQUEST:
        return not issues
    if not issues:
        return False
    for issue in issues:
        location = getattr(issue, "location", None)
        code = getattr(issue, "code", None)
        message = getattr(issue, "message", None)
        if (
            type(location) is not tuple
            or type(code) is not str
            or code not in _SAFE_VALIDATION_CODES
            or type(message) is not str
            or message != _safe_validation_message(code)
        ):
            return False
        if any(
            not (
                type(part) is int
                or (type(part) is str and (part in SAFE_LOCATION_PARTS or part == "<redacted>"))
            )
            for part in location
        ):
            return False
    return True


def _routing_envelope_is_consistent(envelope: object) -> bool:
    """Recheck trusted-envelope invariants without parsing or coercion."""
    if type(envelope) is not RoutingDecisionEnvelope:
        return False
    decision = getattr(envelope, "decision", None)
    if type(decision) not in (SuccessfulRoutingDecision, RefusedRoutingDecision):
        return False
    if type(decision) is SuccessfulRoutingDecision:
        if getattr(decision, "outcome", None) != "routed" or not _arguments_are_validated(
            getattr(decision, "proposal", None)
        ):
            return False
    elif (
        getattr(decision, "outcome", None) != "refused"
        or type(getattr(decision, "reason", None)) is not RefusalReason
        or not _refusal_issues_are_redaction_safe(decision)
    ):
        return False
    identifiers = getattr(decision, "evidence_references", None)
    if (
        type(identifiers) is not tuple
        or not identifiers
        or any(type(identifier) is not str for identifier in identifiers)
        or len(set(identifiers)) != len(identifiers)
        or identifiers != _expected_routing_identifiers(decision)
    ):
        return False
    evidence = getattr(envelope, "evidence", None)
    if (
        type(evidence) is not tuple
        or len(evidence) != len(identifiers)
        or any(type(reference) is not EvidenceReference for reference in evidence)
    ):
        return False
    return all(
        R1_EVIDENCE_REGISTRY.get(identifier) is reference
        for identifier, reference in zip(identifiers, evidence, strict=True)
    )


def build_routing_decision_envelope(decision: object) -> RoutingDecisionEnvelope:
    """Resolve an exact validated R1 decision; subclasses are rejected deliberately."""
    if type(decision) not in (SuccessfulRoutingDecision, RefusedRoutingDecision):
        raise EvidenceEnvelopeError("A validated R1 routing decision is required")
    if type(decision) is SuccessfulRoutingDecision:
        if getattr(decision, "outcome", None) != "routed" or not _arguments_are_validated(
            getattr(decision, "proposal", None)
        ):
            raise EvidenceEnvelopeError("A validated R1 routing decision is required")
    elif (
        getattr(decision, "outcome", None) != "refused"
        or type(getattr(decision, "reason", None)) is not RefusalReason
        or not _refusal_issues_are_redaction_safe(decision)
    ):
        raise EvidenceEnvelopeError("A validated R1 routing decision is required")

    identifiers = getattr(decision, "evidence_references", None)
    if (
        type(identifiers) is not tuple
        or not identifiers
        or any(type(identifier) is not str for identifier in identifiers)
        or len(set(identifiers)) != len(identifiers)
        or identifiers != _expected_routing_identifiers(decision)
    ):
        raise EvidenceEnvelopeError("Routing evidence is inconsistent")

    resolved: list[EvidenceReference] = []
    for identifier in identifiers:
        reference = R1_EVIDENCE_REGISTRY.get(identifier)
        if reference is None:
            raise EvidenceEnvelopeError("Routing evidence identifier is not registered")
        resolved.append(reference)

    return RoutingDecisionEnvelope(decision=decision, evidence=tuple(resolved))
