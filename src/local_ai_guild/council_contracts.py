"""Strict runtime-neutral contracts for a minimum portable Council proceeding."""

import re
from enum import StrEnum
from typing import Annotated, Final, Literal

from pydantic import Field, PrivateAttr, StrictBool, StrictStr, field_validator, model_validator

from local_ai_guild.contracts import BoundaryModel

_IDENTIFIER_PATTERN: Final = r"^[a-z][a-z0-9_]*:[a-z0-9][a-z0-9._-]*-v[1-9][0-9]*$"
_DIGEST_PATTERN: Final = r"^sha256:[0-9a-f]{64}$"
_DETAIL_CODE_PATTERN: Final = r"^[a-z][a-z0-9_]{2,63}$"
_MAX_IDENTIFIER_LENGTH: Final = 128

type CouncilIdentifier = Annotated[
    StrictStr,
    Field(min_length=5, max_length=_MAX_IDENTIFIER_LENGTH, pattern=_IDENTIFIER_PATTERN),
]
type ContentDigest = Annotated[
    StrictStr,
    Field(min_length=71, max_length=71, pattern=_DIGEST_PATTERN),
]
type DetailCode = Annotated[
    StrictStr,
    Field(min_length=3, max_length=64, pattern=_DETAIL_CODE_PATTERN),
]
type NonEmptyIdentifiers = Annotated[tuple[CouncilIdentifier, ...], Field(min_length=1)]
type NonEmptyStatements = Annotated[tuple[StrictStr, ...], Field(min_length=1)]


def _is_plain_text(value: object, *, maximum: int) -> bool:
    return (
        type(value) is str
        and 1 <= len(value) <= maximum
        and value == value.strip()
        and all(ord(character) >= 32 and ord(character) != 127 for character in value)
    )


def _identifier_has_namespace(value: object, namespace: str) -> bool:
    return (
        type(value) is str
        and len(value) <= _MAX_IDENTIFIER_LENGTH
        and re.fullmatch(_IDENTIFIER_PATTERN, value) is not None
        and value.partition(":")[0] == namespace
    )


def _statements_are_bounded(value: object, *, maximum: int = 180) -> bool:
    return (
        type(value) is tuple
        and len(value) == len(set(value))
        and all(_is_plain_text(item, maximum=maximum) for item in value)
    )


def _identifiers_are_unique(value: object) -> bool:
    return type(value) is tuple and len(value) == len(set(value))


class RoleKind(StrEnum):
    """Council-owned actor classifications independent of runtime identities."""

    HUMAN_AUTHORITY = "human_authority"
    COUNCIL_MEMBER = "council_member"
    DETERMINISTIC_VERIFIER = "deterministic_verifier"


class CouncilPermission(StrEnum):
    """Portable institutional capabilities, not runtime-native permissions."""

    READ_PACKET = "read_packet"
    READ_EVIDENCE = "read_evidence"
    SUBMIT_POSITION = "submit_position"
    REVIEW_POSITION = "review_position"
    SUBMIT_VERIFICATION = "submit_verification"
    REQUEST_DECISION = "request_decision"


class PositionDisposition(StrEnum):
    """One frozen position's recommendation."""

    APPROVE = "approve"
    MODIFY = "modify"
    DEFER = "defer"
    REJECT = "reject"


class PositionIntegrityStatus(StrEnum):
    """Whether the declared digest has been confirmed as the frozen version."""

    FROZEN = "frozen"
    UNCONFIRMED = "unconfirmed"


class ReviewAssessment(StrEnum):
    """Bounded cross-review assessment."""

    AGREES = "agrees"
    CHALLENGES = "challenges"
    MIXED = "mixed"


class EvidenceProvenance(StrEnum):
    """Origin classification kept separate from epistemic classification."""

    REPOSITORY_DOCUMENT = "repository_document"
    SYNTHETIC_ASSERTION = "synthetic_assertion"
    DETERMINISTIC_TOOL = "deterministic_tool"
    HUMAN_RECORD = "human_record"
    RUNTIME_OBSERVATION = "runtime_observation"


class EpistemicClassification(StrEnum):
    """Bounded claim status that does not itself establish authority."""

    OBSERVED_FACT = "observed_fact"
    RETRIEVED_FACT = "retrieved_fact"
    INFERENCE = "inference"
    HYPOTHESIS = "hypothesis"


class EvidenceKind(StrEnum):
    """Portable evidence classifications."""

    SOURCE = "source"
    POSITION_SUPPORT = "position_support"
    VERIFICATION_OUTPUT = "verification_output"
    HUMAN_RECORD = "human_record"
    RUNTIME_OBSERVATION = "runtime_observation"


class VerificationMethod(StrEnum):
    """Bounded verification methods that never imply approval."""

    DETERMINISTIC_CHECK = "deterministic_check"
    HUMAN_REVIEW = "human_review"


class VerificationOutcome(StrEnum):
    """Verification result independent of approval state."""

    PASSED = "passed"
    FAILED = "failed"
    MIXED = "mixed"


class DecisionOutcome(StrEnum):
    """Human decision outcomes preserved by the Council."""

    APPROVED = "approved"
    MODIFIED = "modified"
    DEFERRED = "deferred"
    REJECTED = "rejected"


class KnowledgeClass(StrEnum):
    """Target classes from the knowledge-promotion policy."""

    AUTHORITATIVE_KNOWLEDGE = "authoritative_knowledge"
    CURRENT_OPERATIONAL_STATE = "current_operational_state"
    VERIFIED_EVIDENCE = "verified_evidence"
    APPROVED_DECISION = "approved_decision"


class FreshnessPolicy(StrEnum):
    """Portable freshness handling without timestamps."""

    CURRENT_UNTIL_SUPERSEDED = "current_until_superseded"
    REVIEW_BEFORE_USE = "review_before_use"
    EXPIRES_BY_POLICY = "expires_by_policy"


class RuntimeEventKind(StrEnum):
    """Bounded operational semantics reported by any candidate runtime."""

    SESSION_STARTED = "session_started"
    POSITION_EXPORTED = "position_exported"
    TOOL_DENIED = "tool_denied"
    SESSION_TERMINATED = "session_terminated"


class RuntimeEventOutcome(StrEnum):
    """Portable runtime-event outcomes."""

    OBSERVED = "observed"
    SUCCEEDED = "succeeded"
    DENIED = "denied"
    FAILED = "failed"


class RoleContract(BoundaryModel):
    """Council-owned role purpose, duties, and institutional capabilities."""

    identifier: CouncilIdentifier
    title: StrictStr = Field(min_length=1, max_length=120)
    role_kind: RoleKind
    purpose: StrictStr = Field(min_length=1, max_length=200)
    obligations: NonEmptyStatements
    permissions: tuple[CouncilPermission, ...]
    prohibited_behaviors: NonEmptyStatements
    independent: StrictBool
    may_approve: StrictBool

    @model_validator(mode="after")
    def fields_must_be_portable_and_consistent(self) -> "RoleContract":
        if not _identifier_has_namespace(self.identifier, "role"):
            raise ValueError("role identifier namespace is invalid")
        if not all(
            (
                _is_plain_text(self.title, maximum=120),
                _is_plain_text(self.purpose, maximum=200),
                _statements_are_bounded(self.obligations),
                _statements_are_bounded(self.prohibited_behaviors),
                len(self.permissions) == len(set(self.permissions)),
            )
        ):
            raise ValueError("role fields must be bounded and unique")
        if self.may_approve is not (self.role_kind is RoleKind.HUMAN_AUTHORITY):
            raise ValueError("only a human-authority role may approve")
        return self


class CouncilWorkPacket(BoundaryModel):
    """One bounded Council question and its required institutional procedure."""

    identifier: CouncilIdentifier
    title: StrictStr = Field(min_length=1, max_length=140)
    question: StrictStr = Field(min_length=1, max_length=240)
    scope: StrictStr = Field(min_length=1, max_length=200)
    constraints: NonEmptyStatements
    required_outputs: NonEmptyStatements
    evidence_standard: StrictStr = Field(min_length=1, max_length=180)
    participant_role_ids: NonEmptyIdentifiers

    @model_validator(mode="after")
    def fields_must_be_bounded(self) -> "CouncilWorkPacket":
        if not _identifier_has_namespace(self.identifier, "work_packet"):
            raise ValueError("work-packet identifier namespace is invalid")
        if not all(
            (
                _is_plain_text(self.title, maximum=140),
                _is_plain_text(self.question, maximum=240),
                _is_plain_text(self.scope, maximum=200),
                _statements_are_bounded(self.constraints),
                _statements_are_bounded(self.required_outputs),
                _is_plain_text(self.evidence_standard, maximum=180),
                _identifiers_are_unique(self.participant_role_ids),
            )
        ):
            raise ValueError("work-packet fields must be bounded and unique")
        return self


class FrozenPosition(BoundaryModel):
    """One immutable position reference exported before peer review."""

    identifier: CouncilIdentifier
    work_packet_id: CouncilIdentifier
    author_role_id: CouncilIdentifier
    content_digest: ContentDigest
    disposition: PositionDisposition
    summary: StrictStr = Field(min_length=1, max_length=240)
    produced_independently: StrictBool
    integrity_status: PositionIntegrityStatus

    @model_validator(mode="after")
    def fields_must_be_bounded(self) -> "FrozenPosition":
        if not _identifier_has_namespace(self.identifier, "position"):
            raise ValueError("position identifier namespace is invalid")
        if not _is_plain_text(self.summary, maximum=240):
            raise ValueError("position summary must be bounded plain text")
        return self


class CrossReview(BoundaryModel):
    """One review of a referenced frozen position by an identified role."""

    identifier: CouncilIdentifier
    frozen_position_id: CouncilIdentifier
    reviewer_role_id: CouncilIdentifier
    assessment: ReviewAssessment
    evidence_ids: tuple[CouncilIdentifier, ...]
    findings: NonEmptyStatements

    @model_validator(mode="after")
    def fields_must_be_bounded(self) -> "CrossReview":
        if not _identifier_has_namespace(self.identifier, "review"):
            raise ValueError("review identifier namespace is invalid")
        if not _identifiers_are_unique(self.evidence_ids) or not _statements_are_bounded(
            self.findings
        ):
            raise ValueError("review fields must be bounded and unique")
        return self


class CouncilEvidence(BoundaryModel):
    """One evidence declaration with separate provenance and epistemic status."""

    identifier: CouncilIdentifier
    kind: EvidenceKind
    locator: StrictStr = Field(min_length=1, max_length=180)
    claim: StrictStr = Field(min_length=1, max_length=240)
    provenance: EvidenceProvenance
    epistemic_classification: EpistemicClassification

    @model_validator(mode="after")
    def fields_must_be_bounded(self) -> "CouncilEvidence":
        if not _identifier_has_namespace(self.identifier, "evidence"):
            raise ValueError("evidence identifier namespace is invalid")
        if not _is_plain_text(self.locator, maximum=180) or not _is_plain_text(
            self.claim, maximum=240
        ):
            raise ValueError("evidence fields must be bounded plain text")
        if (
            self.kind is EvidenceKind.RUNTIME_OBSERVATION
            and self.provenance is not EvidenceProvenance.RUNTIME_OBSERVATION
        ) or (
            self.provenance is EvidenceProvenance.RUNTIME_OBSERVATION
            and self.kind is not EvidenceKind.RUNTIME_OBSERVATION
        ):
            raise ValueError("runtime observation kind and provenance must agree")
        return self


class VerificationRecord(BoundaryModel):
    """A verification result that has no approval field or approval authority."""

    identifier: CouncilIdentifier
    work_packet_id: CouncilIdentifier
    subject_ids: NonEmptyIdentifiers
    verifier_role_id: CouncilIdentifier
    method: VerificationMethod
    outcome: VerificationOutcome
    evidence_ids: NonEmptyIdentifiers
    limitations: NonEmptyStatements

    @model_validator(mode="after")
    def fields_must_be_bounded(self) -> "VerificationRecord":
        if not _identifier_has_namespace(self.identifier, "verification"):
            raise ValueError("verification identifier namespace is invalid")
        if not all(
            (
                _identifiers_are_unique(self.subject_ids),
                _identifiers_are_unique(self.evidence_ids),
                _statements_are_bounded(self.limitations),
            )
        ):
            raise ValueError("verification fields must be bounded and unique")
        return self


class ApprovalRequest(BoundaryModel):
    """A request for a named human decision; it does not execute approval."""

    identifier: CouncilIdentifier
    work_packet_id: CouncilIdentifier
    required_human_role_id: CouncilIdentifier
    question: StrictStr = Field(min_length=1, max_length=240)
    alternatives: NonEmptyStatements
    evidence_ids: NonEmptyIdentifiers
    request_state: Literal["requested"] = "requested"

    @model_validator(mode="after")
    def fields_must_be_bounded(self) -> "ApprovalRequest":
        if not _identifier_has_namespace(self.identifier, "approval_request"):
            raise ValueError("approval-request identifier namespace is invalid")
        if not all(
            (
                _is_plain_text(self.question, maximum=240),
                _statements_are_bounded(self.alternatives),
                _identifiers_are_unique(self.evidence_ids),
            )
        ):
            raise ValueError("approval-request fields must be bounded and unique")
        return self


class DissentStatement(BoundaryModel):
    """One preserved material dissent attached to a decision."""

    role_id: CouncilIdentifier
    frozen_position_id: CouncilIdentifier
    summary: StrictStr = Field(min_length=1, max_length=200)

    @field_validator("summary")
    @classmethod
    def summary_must_be_plain_text(cls, value: str) -> str:
        if not _is_plain_text(value, maximum=200):
            raise ValueError("dissent summary must be bounded plain text")
        return value


class DecisionRecord(BoundaryModel):
    """One durable human decision that preserves material dissent."""

    identifier: CouncilIdentifier
    work_packet_id: CouncilIdentifier
    approval_request_id: CouncilIdentifier | None
    decided_by_role_id: CouncilIdentifier
    outcome: DecisionOutcome
    rationale: StrictStr = Field(min_length=1, max_length=240)
    evidence_ids: NonEmptyIdentifiers
    dissent: tuple[DissentStatement, ...]

    @field_validator("dissent", mode="before")
    @classmethod
    def dissent_must_be_exact_instances(cls, value: object) -> object:
        if type(value) is not tuple or any(type(item) is not DissentStatement for item in value):
            raise ValueError("decision dissent must contain exact typed instances")
        return value

    @model_validator(mode="after")
    def fields_must_be_bounded(self) -> "DecisionRecord":
        if not _identifier_has_namespace(self.identifier, "decision"):
            raise ValueError("decision identifier namespace is invalid")
        if (
            not _is_plain_text(self.rationale, maximum=240)
            or not _identifiers_are_unique(self.evidence_ids)
            or len({(item.role_id, item.frozen_position_id) for item in self.dissent})
            != len(self.dissent)
        ):
            raise ValueError("decision fields must be bounded and unique")
        return self


class KnowledgePromotionRequest(BoundaryModel):
    """A proposal for human-governed promotion, never a mutation command."""

    identifier: CouncilIdentifier
    work_packet_id: CouncilIdentifier
    candidate_digest: ContentDigest
    target_class: KnowledgeClass
    evidence_ids: tuple[CouncilIdentifier, ...]
    review_ids: tuple[CouncilIdentifier, ...]
    approval_request_id: CouncilIdentifier | None
    rationale: StrictStr = Field(min_length=1, max_length=240)
    freshness_policy: FreshnessPolicy
    request_state: Literal["proposed"] = "proposed"

    @model_validator(mode="after")
    def fields_must_be_bounded(self) -> "KnowledgePromotionRequest":
        if not _identifier_has_namespace(self.identifier, "promotion_request"):
            raise ValueError("promotion-request identifier namespace is invalid")
        if (
            not _identifiers_are_unique(self.evidence_ids)
            or not _identifiers_are_unique(self.review_ids)
            or not _is_plain_text(self.rationale, maximum=240)
        ):
            raise ValueError("promotion-request fields must be bounded and unique")
        return self


class RuntimeEvent(BoundaryModel):
    """Portable operational telemetry correlated only through a Council identifier."""

    identifier: CouncilIdentifier
    correlation_id: CouncilIdentifier
    event_kind: RuntimeEventKind
    outcome: RuntimeEventOutcome
    detail_code: DetailCode

    @model_validator(mode="after")
    def identifier_must_be_runtime_event(self) -> "RuntimeEvent":
        if not _identifier_has_namespace(self.identifier, "runtime_event"):
            raise ValueError("runtime-event identifier namespace is invalid")
        return self


_PROCEEDING_COLLECTIONS: Final = (
    ("roles", RoleContract),
    ("positions", FrozenPosition),
    ("reviews", CrossReview),
    ("evidence", CouncilEvidence),
    ("verifications", VerificationRecord),
    ("approval_requests", ApprovalRequest),
    ("decisions", DecisionRecord),
    ("knowledge_promotions", KnowledgePromotionRequest),
    ("runtime_events", RuntimeEvent),
)


class CouncilProceeding(BoundaryModel):
    """One exact in-memory Council proceeding with no persistence or loader."""

    identifier: CouncilIdentifier
    work_packet: CouncilWorkPacket
    roles: Annotated[tuple[RoleContract, ...], Field(min_length=1)]
    positions: tuple[FrozenPosition, ...]
    reviews: tuple[CrossReview, ...]
    evidence: tuple[CouncilEvidence, ...]
    verifications: tuple[VerificationRecord, ...]
    approval_requests: tuple[ApprovalRequest, ...]
    decisions: tuple[DecisionRecord, ...]
    knowledge_promotions: tuple[KnowledgePromotionRequest, ...]
    runtime_events: tuple[RuntimeEvent, ...]
    _bound_identifiers: tuple[str, ...] = PrivateAttr(default=())

    def __init__(self, **data: object) -> None:
        super().__init__(**data)
        self._bound_identifiers = _proceeding_identifiers(self)

    @field_validator("work_packet", mode="before")
    @classmethod
    def work_packet_must_be_exact(cls, value: object) -> object:
        if type(value) is not CouncilWorkPacket:
            raise ValueError("proceeding work packet must be an exact typed instance")
        return value

    @field_validator(*tuple(name for name, _ in _PROCEEDING_COLLECTIONS), mode="before")
    @classmethod
    def collections_must_contain_exact_types(
        cls,
        value: object,
        info: object,
    ) -> object:
        expected_type = dict(_PROCEEDING_COLLECTIONS)[info.field_name]
        if type(value) is not tuple or any(type(item) is not expected_type for item in value):
            raise ValueError("proceeding collections must contain exact typed instances")
        return value

    @model_validator(mode="after")
    def identifier_must_be_proceeding(self) -> "CouncilProceeding":
        if not _identifier_has_namespace(self.identifier, "proceeding"):
            raise ValueError("proceeding identifier namespace is invalid")
        return self


def _proceeding_records(proceeding: CouncilProceeding) -> tuple[BoundaryModel, ...]:
    return (
        proceeding.work_packet,
        *proceeding.roles,
        *proceeding.positions,
        *proceeding.reviews,
        *proceeding.evidence,
        *proceeding.verifications,
        *proceeding.approval_requests,
        *proceeding.decisions,
        *proceeding.knowledge_promotions,
        *proceeding.runtime_events,
    )


def _proceeding_identifiers(proceeding: CouncilProceeding) -> tuple[str, ...]:
    return (
        proceeding.identifier,
        *(record.identifier for record in _proceeding_records(proceeding)),
    )


def _model_is_reconstructable(value: BoundaryModel) -> bool:
    try:
        reconstructed = type(value)(
            **{name: getattr(value, name) for name in type(value).model_fields}
        )
    except (AttributeError, TypeError, ValueError):
        return False
    return reconstructed == value


def _record_is_reconstructable(value: BoundaryModel) -> bool:
    if type(value) is DecisionRecord and (
        type(getattr(value, "dissent", None)) is not tuple
        or any(
            type(item) is not DissentStatement or not _model_is_reconstructable(item)
            for item in value.dissent
        )
    ):
        return False
    return _model_is_reconstructable(value)


def council_proceeding_is_consistent(value: object) -> bool:
    """Recheck exact nested types and private order binding after unsafe corruption."""
    if type(value) is not CouncilProceeding:
        return False
    try:
        records = _proceeding_records(value)
        identifiers = _proceeding_identifiers(value)
    except (AttributeError, TypeError):
        return False
    collections_are_exact = all(
        type(getattr(value, name, None)) is tuple
        and all(type(item) is expected for item in getattr(value, name))
        for name, expected in _PROCEEDING_COLLECTIONS
    )
    return (
        type(getattr(value, "identifier", None)) is str
        and _identifier_has_namespace(value.identifier, "proceeding")
        and type(getattr(value, "work_packet", None)) is CouncilWorkPacket
        and collections_are_exact
        and len(records) >= 2
        and all(_record_is_reconstructable(record) for record in records)
        and getattr(value, "_bound_identifiers", None) == identifiers
        and _model_is_reconstructable(value)
    )
