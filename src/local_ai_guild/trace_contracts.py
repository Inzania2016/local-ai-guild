"""Strict contracts for the fixed O2 R2 evidence-trace pilot."""

import re
from enum import StrEnum
from typing import Annotated, Final, Literal

from pydantic import (
    Field,
    PrivateAttr,
    StrictBool,
    StrictInt,
    StrictStr,
    field_validator,
    model_validator,
)

from local_ai_guild.contracts import BoundaryModel

_IDENTIFIER_PATTERN: Final = r"^[a-z][a-z0-9_]*:[a-z0-9][a-z0-9._-]*-v[1-9][0-9]*$"
_GIT_SHA_PATTERN: Final = r"^[0-9a-f]{40}$"
_REPOSITORY_CITATION_PATTERN: Final = re.compile(
    r"^(?P<path>[A-Za-z0-9][A-Za-z0-9._/-]*?)"
    r"(?:@(?P<revision>[0-9a-f]{7,40}))?"
    r":(?P<start>[1-9][0-9]*)-(?P<end>[1-9][0-9]*)$"
)
_GIT_LOCATOR_PATTERN: Final = re.compile(r"^git:(?P<sha>[0-9a-f]{40})$")
_REPOSITORY_PATH_PATTERN: Final = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._-]*(?:/[A-Za-z0-9][A-Za-z0-9._-]*)*$"
)
_MAX_IDENTIFIER_LENGTH: Final = 128
_MAX_LOCATOR_LENGTH: Final = 200

type DurableIdentifier = Annotated[
    StrictStr,
    Field(min_length=5, max_length=_MAX_IDENTIFIER_LENGTH, pattern=_IDENTIFIER_PATTERN),
]
type TraceIdentifier = Annotated[
    StrictStr,
    Field(min_length=5, max_length=_MAX_IDENTIFIER_LENGTH, pattern=_IDENTIFIER_PATTERN),
]
type GitSha = Annotated[
    StrictStr,
    Field(min_length=40, max_length=40, pattern=_GIT_SHA_PATTERN),
]
type NonEmptyReferences = Annotated[tuple[DurableIdentifier, ...], Field(min_length=1)]
type NonEmptyEvidence = Annotated[tuple["EvidenceLocator", ...], Field(min_length=1)]


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


def _repository_path_is_valid(value: object) -> bool:
    if (
        type(value) is not str
        or not 1 <= len(value) <= 180
        or value != value.strip()
        or "\\" in value
        or ":" in value
        or value.startswith("/")
        or re.fullmatch(_REPOSITORY_PATH_PATTERN, value) is None
    ):
        return False
    return all(segment not in {".", ".."} for segment in value.split("/"))


def _repository_citation_is_valid(value: object) -> bool:
    if (
        type(value) is not str
        or not 1 <= len(value) <= _MAX_LOCATOR_LENGTH
        or value != value.strip()
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        return False
    match = _REPOSITORY_CITATION_PATTERN.fullmatch(value)
    if match is None:
        return False
    path = match.group("path")
    if not _repository_path_is_valid(path):
        return False
    return int(match.group("start")) <= int(match.group("end"))


class EvidenceKind(StrEnum):
    """Bounded kinds of declared trace evidence."""

    REPOSITORY_SOURCE = "repository_source"
    GIT_COMMIT = "git_commit"
    VERIFICATION_RECORD = "verification_record"
    DETERMINISTIC_RESULT = "deterministic_result"
    HUMAN_APPROVAL_RECORD = "human_approval_record"


class EvidenceProvenance(StrEnum):
    """Origin classification kept separate from epistemic status."""

    REPOSITORY_DOCUMENT = "repository_document"
    GIT_HISTORY = "git_history"
    DETERMINISTIC_TOOL = "deterministic_tool"
    HUMAN_RECORD = "human_record"


class EpistemicStatus(StrEnum):
    """Bounded epistemic classifications for declared evidence."""

    OBSERVED_FACT = "observed_fact"
    RETRIEVED_FACT = "retrieved_fact"
    INFERENCE = "inference"
    HYPOTHESIS = "hypothesis"


class RealizationStatus(StrEnum):
    """Lifecycle state independent of verification and approval."""

    PLANNED = "planned"
    AUTHORIZED = "authorized"
    WORKING_TREE = "working_tree"
    COMMITTED = "committed"
    PUBLISHED = "published"
    NOT_APPLICABLE = "not_applicable"


class AutomatedVerificationStatus(StrEnum):
    """Automated verification state."""

    NOT_CHECKED = "not_checked"
    AUTOMATED_FAILED = "automated_failed"
    AUTOMATED_PASSED = "automated_passed"
    NOT_APPLICABLE = "not_applicable"


class HumanVerificationStatus(StrEnum):
    """Human verification state, never inferred from automation."""

    NOT_CHECKED = "not_checked"
    HUMAN_REQUIRED = "human_required"
    HUMAN_FAILED = "human_failed"
    HUMAN_PASSED = "human_passed"
    NOT_APPLICABLE = "not_applicable"


class ApprovalStatus(StrEnum):
    """Approval state independent of implementation and verification."""

    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVOKED = "revoked"
    UNKNOWN_FROM_REPOSITORY = "unknown_from_repository"


class ApprovalEvidenceStatus(StrEnum):
    """Whether repository evidence for an approval is present."""

    NOT_REQUIRED = "not_required"
    RECORDED = "recorded"
    NOT_RECORDED_IN_REPOSITORY = "not_recorded_in_repository"


class AuthorityKind(StrEnum):
    """Bounded authority-source classifications."""

    EXPLICIT_HUMAN_INSTRUCTION = "explicit_human_instruction"
    APPROVED_WORK_PACKET = "approved_work_packet"
    SECURITY_POLICY = "security_policy"
    VERIFICATION_POLICY = "verification_policy"
    PROJECT_STATE = "project_state"
    DECISION_RECORD = "decision_record"


class AuthorityEvidenceStatus(StrEnum):
    """Repository confirmation state for an authority source."""

    CONFIRMED_FROM_REPOSITORY = "confirmed_from_repository"
    UNCONFIRMED_FROM_REPOSITORY = "unconfirmed_from_repository"


class ConstraintKind(StrEnum):
    """Bounded constraint classifications."""

    SCOPE = "scope"
    SECURITY = "security"
    DATA_BOUNDARY = "data_boundary"
    EXECUTION_BOUNDARY = "execution_boundary"
    CLAIM_BOUNDARY = "claim_boundary"


class ArtifactKind(StrEnum):
    """Bounded implementation-artifact classifications."""

    SOURCE = "source"
    TEST = "test"
    DOCUMENTATION = "documentation"
    SCRIPT = "script"


class VerificationMethod(StrEnum):
    """Bounded deterministic verification methods."""

    PYTEST = "pytest"
    RUFF = "ruff"
    FORMAT_CHECK = "format_check"
    CLI_SMOKE = "cli_smoke"
    DIFF_CHECK = "diff_check"
    SOURCE_SCAN = "source_scan"
    ADVERSARIAL_REVIEW = "adversarial_review"
    COMBINED_CLOSEOUT = "combined_closeout"


class VerificationOutcome(StrEnum):
    """Bounded verification outcomes."""

    PASSED = "passed"
    FAILED = "failed"
    MIXED = "mixed"


class VerificationComponent(StrEnum):
    """Component checks declared by the combined R2 closeout."""

    RUFF = "ruff"
    FORMAT = "format"
    PYTEST = "pytest"
    CLI = "cli"
    DIFF = "diff"
    REDACTION_SCAN = "redaction_scan"
    DEPENDENCY_CHECK = "dependency_check"
    PARSER_BYPASS_SCAN = "parser_bypass_scan"
    EXECUTION_SURFACE_SCAN = "execution_surface_scan"


class ApprovalGateKind(StrEnum):
    """Bounded progression and mutation gates."""

    PACKET_START = "packet_start"
    REPOSITORY_WRITE = "repository_write"
    COMMIT = "commit"
    PUBLICATION = "publication"
    CLOUD_DELEGATION = "cloud_delegation"
    RUNTIME_INSTALLATION = "runtime_installation"


class EvidenceLocator(BoundaryModel):
    """One bounded declared repository citation; it is never resolved dynamically."""

    kind: EvidenceKind
    locator: StrictStr = Field(min_length=1, max_length=_MAX_LOCATOR_LENGTH)
    scope: StrictStr = Field(min_length=1, max_length=160)
    epistemic_status: EpistemicStatus
    provenance: EvidenceProvenance

    @field_validator("scope")
    @classmethod
    def scope_must_be_plain_text(cls, value: str) -> str:
        if not _is_plain_text(value, maximum=160):
            raise ValueError("evidence scope must be bounded plain text")
        return value

    @model_validator(mode="after")
    def locator_and_metadata_must_agree(self) -> "EvidenceLocator":
        if self.kind is EvidenceKind.GIT_COMMIT:
            if (
                _GIT_LOCATOR_PATTERN.fullmatch(self.locator) is None
                or self.provenance is not EvidenceProvenance.GIT_HISTORY
                or self.epistemic_status is not EpistemicStatus.OBSERVED_FACT
            ):
                raise ValueError("Git evidence metadata is inconsistent")
        elif not _repository_citation_is_valid(self.locator):
            raise ValueError("repository evidence locator is invalid")
        elif self.kind is EvidenceKind.HUMAN_APPROVAL_RECORD:
            if (
                self.provenance is not EvidenceProvenance.HUMAN_RECORD
                or self.epistemic_status
                not in {EpistemicStatus.OBSERVED_FACT, EpistemicStatus.RETRIEVED_FACT}
            ):
                raise ValueError("human approval evidence must use human-record provenance")
        elif self.kind is EvidenceKind.DETERMINISTIC_RESULT:
            if (
                self.provenance is not EvidenceProvenance.DETERMINISTIC_TOOL
                or self.epistemic_status is not EpistemicStatus.OBSERVED_FACT
            ):
                raise ValueError("deterministic evidence must use deterministic-tool provenance")
        elif self.kind is EvidenceKind.VERIFICATION_RECORD:
            allowed_verification_pair = (
                (
                    self.provenance is EvidenceProvenance.REPOSITORY_DOCUMENT
                    and self.epistemic_status is EpistemicStatus.RETRIEVED_FACT
                )
                or (
                    self.provenance is EvidenceProvenance.DETERMINISTIC_TOOL
                    and self.epistemic_status is EpistemicStatus.OBSERVED_FACT
                )
                or (
                    self.provenance is EvidenceProvenance.HUMAN_RECORD
                    and self.epistemic_status
                    in {EpistemicStatus.OBSERVED_FACT, EpistemicStatus.RETRIEVED_FACT}
                )
            )
            if not allowed_verification_pair:
                raise ValueError("verification evidence metadata is inconsistent")
        elif (
            self.provenance is not EvidenceProvenance.REPOSITORY_DOCUMENT
            or self.epistemic_status is EpistemicStatus.OBSERVED_FACT
        ):
            raise ValueError("repository-source evidence metadata is inconsistent")
        return self


class EmbeddedRequirement(BoundaryModel):
    """A strict requirement value embedded in a WorkPacket."""

    identifier: DurableIdentifier
    statement: StrictStr = Field(min_length=1, max_length=180)
    required: StrictBool
    evidence: NonEmptyEvidence

    @field_validator("identifier")
    @classmethod
    def identifier_must_use_requirement_namespace(cls, value: str) -> str:
        if not _identifier_has_namespace(value, "requirement"):
            raise ValueError("requirement identifier namespace is invalid")
        return value

    @field_validator("statement")
    @classmethod
    def statement_must_be_plain_text(cls, value: str) -> str:
        if not _is_plain_text(value, maximum=180):
            raise ValueError("requirement statement must be bounded plain text")
        return value

    @field_validator("evidence", mode="before")
    @classmethod
    def evidence_must_be_exact_instances(cls, value: object) -> object:
        if type(value) is not tuple or any(type(item) is not EvidenceLocator for item in value):
            raise ValueError("requirement evidence must be exact typed instances")
        return value


class _TraceRecordBase(BoundaryModel):
    """Shared strict fields for the ten approved record contracts."""

    identifier: DurableIdentifier
    title: StrictStr = Field(min_length=1, max_length=160)
    evidence: tuple[EvidenceLocator, ...]

    @field_validator("title")
    @classmethod
    def title_must_be_plain_text(cls, value: str) -> str:
        if not _is_plain_text(value, maximum=160):
            raise ValueError("record title must be bounded plain text")
        return value

    @field_validator("evidence", mode="before")
    @classmethod
    def evidence_must_be_exact_instances(cls, value: object) -> object:
        if type(value) is not tuple or any(type(item) is not EvidenceLocator for item in value):
            raise ValueError("record evidence must be exact typed instances")
        return value


class Goal(_TraceRecordBase):
    """One R2 goal."""

    record_type: Literal["goal"] = "goal"
    description: StrictStr | None = Field(default=None, min_length=1, max_length=240)

    @model_validator(mode="after")
    def fields_must_be_consistent(self) -> "Goal":
        if not _identifier_has_namespace(self.identifier, "goal"):
            raise ValueError("goal identifier namespace is invalid")
        if self.description is not None and not _is_plain_text(self.description, maximum=240):
            raise ValueError("goal description must be bounded plain text")
        if not self.evidence or not any(
            item.kind is EvidenceKind.REPOSITORY_SOURCE for item in self.evidence
        ):
            raise ValueError("goal requires repository-source evidence")
        return self


class WorkPacket(_TraceRecordBase):
    """The completed R2 work packet and its embedded requirements."""

    record_type: Literal["work_packet"] = "work_packet"
    requirements: Annotated[tuple[EmbeddedRequirement, ...], Field(min_length=1)]
    governed_by: NonEmptyReferences
    constrained_by: NonEmptyReferences
    advances_goal: NonEmptyReferences
    realization_status: RealizationStatus
    automated_verification_status: AutomatedVerificationStatus
    human_verification_status: HumanVerificationStatus
    approval_status: ApprovalStatus
    approval_evidence_status: ApprovalEvidenceStatus

    @field_validator("requirements", mode="before")
    @classmethod
    def requirements_must_be_exact_instances(cls, value: object) -> object:
        if type(value) is not tuple or any(type(item) is not EmbeddedRequirement for item in value):
            raise ValueError("work packet requirements must be exact typed instances")
        return value

    @model_validator(mode="after")
    def fields_must_be_consistent(self) -> "WorkPacket":
        if not _identifier_has_namespace(self.identifier, "work_packet"):
            raise ValueError("work-packet identifier namespace is invalid")
        if len({item.identifier for item in self.requirements}) != len(self.requirements):
            raise ValueError("embedded requirement identifiers must be unique")
        if not all(
            _references_are_unique(references)
            for references in (self.governed_by, self.constrained_by, self.advances_goal)
        ):
            raise ValueError("work-packet relationship references must be unique")
        if self.human_verification_status in {
            HumanVerificationStatus.HUMAN_FAILED,
            HumanVerificationStatus.HUMAN_PASSED,
        } and not _has_human_verification_record(self.evidence):
            raise ValueError("human verification status requires human verification evidence")
        if not _approval_fields_are_consistent(
            self.approval_status, self.approval_evidence_status, self.evidence
        ):
            raise ValueError("work-packet approval fields are inconsistent")
        return self


class AuthoritySource(_TraceRecordBase):
    """A repository authority source, not an approval event."""

    record_type: Literal["authority_source"] = "authority_source"
    authority_kind: AuthorityKind
    scope: StrictStr = Field(min_length=1, max_length=180)
    precedence: StrictInt = Field(ge=1, le=10)
    evidence_status: AuthorityEvidenceStatus

    @field_validator("scope")
    @classmethod
    def scope_must_be_plain_text(cls, value: str) -> str:
        if not _is_plain_text(value, maximum=180):
            raise ValueError("authority scope must be bounded plain text")
        return value

    @model_validator(mode="after")
    def fields_must_be_consistent(self) -> "AuthoritySource":
        if not _identifier_has_namespace(self.identifier, "authority"):
            raise ValueError("authority identifier namespace is invalid")
        if self.evidence_status is AuthorityEvidenceStatus.CONFIRMED_FROM_REPOSITORY:
            if not self.evidence:
                raise ValueError("confirmed authority requires repository evidence")
        elif self.evidence:
            raise ValueError("unconfirmed authority must not claim confirming evidence")
        return self


class Constraint(_TraceRecordBase):
    """One bounded R2 constraint."""

    record_type: Literal["constraint"] = "constraint"
    constraint_kind: ConstraintKind

    @model_validator(mode="after")
    def fields_must_be_consistent(self) -> "Constraint":
        if not _identifier_has_namespace(self.identifier, "constraint"):
            raise ValueError("constraint identifier namespace is invalid")
        if not self.evidence or not any(
            item.kind is EvidenceKind.REPOSITORY_SOURCE for item in self.evidence
        ):
            raise ValueError("constraint requires repository-source evidence")
        return self


class Decision(_TraceRecordBase):
    """One R2 design decision and its declared implementation."""

    record_type: Literal["decision"] = "decision"
    selected_by: DurableIdentifier
    implemented_by: NonEmptyReferences

    @model_validator(mode="after")
    def fields_must_be_consistent(self) -> "Decision":
        if not _identifier_has_namespace(self.identifier, "decision"):
            raise ValueError("decision identifier namespace is invalid")
        if not self.evidence or not any(
            item.kind is EvidenceKind.REPOSITORY_SOURCE and item.locator.startswith("DECISIONS.md:")
            for item in self.evidence
        ):
            raise ValueError("decision requires a decision-record citation")
        if not _references_are_unique(self.implemented_by):
            raise ValueError("implemented-by references must be unique")
        return self


class ImplementationArtifact(_TraceRecordBase):
    """One repository artifact declared by the R2 trace."""

    record_type: Literal["implementation_artifact"] = "implementation_artifact"
    artifact_kind: ArtifactKind
    repository_path: StrictStr = Field(min_length=1, max_length=180)
    implements: NonEmptyReferences
    verified_by: NonEmptyReferences
    published_in: NonEmptyReferences

    @field_validator("repository_path")
    @classmethod
    def repository_path_must_be_relative(cls, value: str) -> str:
        if not _repository_path_is_valid(value):
            raise ValueError("artifact repository path is invalid")
        return value

    @model_validator(mode="after")
    def fields_must_be_consistent(self) -> "ImplementationArtifact":
        if not _identifier_has_namespace(self.identifier, "artifact"):
            raise ValueError("artifact identifier namespace is invalid")
        if not all(
            _references_are_unique(references)
            for references in (self.implements, self.verified_by, self.published_in)
        ):
            raise ValueError("artifact relationship references must be unique")
        return self


class VerificationResult(_TraceRecordBase):
    """One bounded recorded R2 verification result."""

    record_type: Literal["verification_result"] = "verification_result"
    method: VerificationMethod
    result: VerificationOutcome
    verifies: NonEmptyReferences
    automated_verification_status: AutomatedVerificationStatus
    human_verification_status: HumanVerificationStatus
    limitations: Annotated[tuple[StrictStr, ...], Field(min_length=1)]
    component_checks: Annotated[tuple[VerificationComponent, ...], Field(min_length=1)]

    @field_validator("limitations")
    @classmethod
    def limitations_must_be_bounded(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if type(value) is not tuple or any(not _is_plain_text(item, maximum=180) for item in value):
            raise ValueError("verification limitations must be bounded statements")
        return value

    @model_validator(mode="after")
    def fields_must_be_consistent(self) -> "VerificationResult":
        if not _identifier_has_namespace(self.identifier, "verification"):
            raise ValueError("verification identifier namespace is invalid")
        if self.result is VerificationOutcome.PASSED and (
            self.automated_verification_status is not AutomatedVerificationStatus.AUTOMATED_PASSED
        ):
            raise ValueError("passed result requires automated-passed status")
        if self.result in {VerificationOutcome.FAILED, VerificationOutcome.MIXED} and (
            self.automated_verification_status is not AutomatedVerificationStatus.AUTOMATED_FAILED
        ):
            raise ValueError("failed or mixed result requires automated-failed status")
        if self.human_verification_status in {
            HumanVerificationStatus.HUMAN_FAILED,
            HumanVerificationStatus.HUMAN_PASSED,
        } and not _has_human_verification_record(self.evidence):
            raise ValueError("human verification status requires human verification evidence")
        if not any(
            item.kind in {EvidenceKind.VERIFICATION_RECORD, EvidenceKind.DETERMINISTIC_RESULT}
            for item in self.evidence
        ):
            raise ValueError("verification requires verification evidence")
        if not _references_are_unique(self.verifies):
            raise ValueError("verification targets must be unique")
        return self


class ApprovalGate(_TraceRecordBase):
    """One explicit R2 approval gate and its repository evidence state."""

    record_type: Literal["approval_gate"] = "approval_gate"
    gate_kind: ApprovalGateKind
    required_authority: DurableIdentifier
    approval_status: ApprovalStatus
    approval_evidence_status: ApprovalEvidenceStatus

    @model_validator(mode="after")
    def fields_must_be_consistent(self) -> "ApprovalGate":
        if not _identifier_has_namespace(self.identifier, "approval_gate"):
            raise ValueError("approval-gate identifier namespace is invalid")
        if not _approval_fields_are_consistent(
            self.approval_status, self.approval_evidence_status, self.evidence
        ):
            raise ValueError("approval-gate fields are inconsistent")
        return self


class Commit(_TraceRecordBase):
    """One declared Git publication identity."""

    record_type: Literal["commit"] = "commit"
    sha: GitSha
    publishes: NonEmptyReferences
    authorized_by_gate: DurableIdentifier
    realization_status: RealizationStatus

    @model_validator(mode="after")
    def fields_must_be_consistent(self) -> "Commit":
        if not _identifier_has_namespace(self.identifier, "commit"):
            raise ValueError("commit identifier namespace is invalid")
        expected_locator = f"git:{self.sha}"
        if self.realization_status is not RealizationStatus.PUBLISHED or not any(
            item.kind is EvidenceKind.GIT_COMMIT and item.locator == expected_locator
            for item in self.evidence
        ):
            raise ValueError("commit publication fields are inconsistent")
        if not _references_are_unique(self.publishes):
            raise ValueError("commit publication targets must be unique")
        return self


class NextAction(_TraceRecordBase):
    """The documented action following R2, without automatic authorization."""

    record_type: Literal["next_action"] = "next_action"
    enabled_by: NonEmptyReferences
    blocked_by: tuple[DurableIdentifier, ...]

    @model_validator(mode="after")
    def fields_must_be_consistent(self) -> "NextAction":
        if not _identifier_has_namespace(self.identifier, "next_action"):
            raise ValueError("next-action identifier namespace is invalid")
        if not _references_are_unique(self.enabled_by) or not _references_are_unique(
            self.blocked_by
        ):
            raise ValueError("next-action relationship references must be unique")
        return self


type TraceRecord = Annotated[
    Goal
    | WorkPacket
    | AuthoritySource
    | Constraint
    | Decision
    | ImplementationArtifact
    | VerificationResult
    | ApprovalGate
    | Commit
    | NextAction,
    Field(discriminator="record_type"),
]

_EXACT_RECORD_TYPES: Final = (
    Goal,
    WorkPacket,
    AuthoritySource,
    Constraint,
    Decision,
    ImplementationArtifact,
    VerificationResult,
    ApprovalGate,
    Commit,
    NextAction,
)


class TraceDocument(BoundaryModel):
    """One fixed, ordered R2 trace document."""

    schema_version: Literal["0.1"]
    trace_identifier: TraceIdentifier
    subject_record_identifier: DurableIdentifier
    records: Annotated[tuple[TraceRecord, ...], Field(min_length=1)]
    _bound_trace_identifier: str | None = PrivateAttr(default=None)
    _bound_record_identifiers: tuple[str, ...] = PrivateAttr(default=())

    def __init__(self, **data: object) -> None:
        super().__init__(**data)
        self._bound_trace_identifier = self.trace_identifier
        self._bound_record_identifiers = tuple(record.identifier for record in self.records)

    @field_validator("trace_identifier")
    @classmethod
    def identifier_must_use_trace_namespace(cls, value: str) -> str:
        if not _identifier_has_namespace(value, "trace"):
            raise ValueError("trace identifier namespace is invalid")
        return value

    @field_validator("records", mode="before")
    @classmethod
    def records_must_be_exact_instances(cls, value: object) -> object:
        if type(value) is not tuple or any(type(item) not in _EXACT_RECORD_TYPES for item in value):
            raise ValueError("trace records must be exact typed instances")
        return value

    @model_validator(mode="after")
    def document_must_have_one_unique_subject(self) -> "TraceDocument":
        identifiers = tuple(record.identifier for record in self.records)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("trace record identifiers must be unique")
        requirement_identifiers = tuple(
            requirement.identifier
            for record in self.records
            if type(record) is WorkPacket
            for requirement in record.requirements
        )
        durable_identifiers = (self.trace_identifier, *identifiers, *requirement_identifiers)
        if len(set(durable_identifiers)) != len(durable_identifiers):
            raise ValueError("all trace-document durable identifiers must be globally unique")
        subjects = tuple(
            record
            for record in self.records
            if type(record) is WorkPacket and record.identifier == self.subject_record_identifier
        )
        if len(subjects) != 1:
            raise ValueError("trace subject must identify exactly one work packet")
        return self


def _approval_fields_are_consistent(
    status: object,
    evidence_status: object,
    evidence: object,
) -> bool:
    if (
        type(status) is not ApprovalStatus
        or type(evidence_status) is not ApprovalEvidenceStatus
        or type(evidence) is not tuple
    ):
        return False
    has_human_record = any(
        type(item) is EvidenceLocator and item.kind is EvidenceKind.HUMAN_APPROVAL_RECORD
        for item in evidence
    )
    if status is ApprovalStatus.APPROVED:
        return evidence_status is ApprovalEvidenceStatus.RECORDED and has_human_record
    if status is ApprovalStatus.UNKNOWN_FROM_REPOSITORY:
        return (
            evidence_status is ApprovalEvidenceStatus.NOT_RECORDED_IN_REPOSITORY
            and not has_human_record
        )
    if status is ApprovalStatus.NOT_REQUIRED:
        return evidence_status is ApprovalEvidenceStatus.NOT_REQUIRED and not has_human_record
    if evidence_status is ApprovalEvidenceStatus.RECORDED:
        return has_human_record
    return not has_human_record


def _has_human_verification_record(evidence: object) -> bool:
    return type(evidence) is tuple and any(
        type(item) is EvidenceLocator
        and item.kind is EvidenceKind.VERIFICATION_RECORD
        and item.provenance is EvidenceProvenance.HUMAN_RECORD
        for item in evidence
    )


def _references_are_unique(references: object) -> bool:
    return type(references) is tuple and len(set(references)) == len(references)


def _model_public_fields_are_reconstructable(value: BoundaryModel) -> bool:
    try:
        data = {name: getattr(value, name) for name in type(value).model_fields}
        reconstructed = type(value)(**data)
    except (AttributeError, TypeError, ValueError):
        return False
    return reconstructed == value


def _evidence_is_consistent(value: object) -> bool:
    return type(value) is EvidenceLocator and _model_public_fields_are_reconstructable(value)


def _requirement_is_consistent(value: object) -> bool:
    return (
        type(value) is EmbeddedRequirement
        and type(getattr(value, "evidence", None)) is tuple
        and all(_evidence_is_consistent(item) for item in value.evidence)
        and _model_public_fields_are_reconstructable(value)
    )


def _record_is_consistent(value: object) -> bool:
    if type(value) not in _EXACT_RECORD_TYPES:
        return False
    evidence = getattr(value, "evidence", None)
    if type(evidence) is not tuple or any(not _evidence_is_consistent(item) for item in evidence):
        return False
    if type(value) is WorkPacket and (
        type(getattr(value, "requirements", None)) is not tuple
        or any(not _requirement_is_consistent(item) for item in value.requirements)
    ):
        return False
    return _model_public_fields_are_reconstructable(value)


def trace_document_is_consistent(value: object) -> bool:
    """Recheck an exact trace and its private order binding after unsafe corruption."""
    if type(value) is not TraceDocument:
        return False
    schema_version = getattr(value, "schema_version", None)
    trace_identifier = getattr(value, "trace_identifier", None)
    subject_identifier = getattr(value, "subject_record_identifier", None)
    if (
        schema_version != "0.1"
        or not _identifier_has_namespace(trace_identifier, "trace")
        or not _identifier_has_namespace(subject_identifier, "work_packet")
    ):
        return False
    records = getattr(value, "records", None)
    if (
        type(records) is not tuple
        or not records
        or any(not _record_is_consistent(record) for record in records)
    ):
        return False
    identifiers = tuple(record.identifier for record in records)
    if (
        len(set(identifiers)) != len(identifiers)
        or getattr(value, "_bound_trace_identifier", None) != trace_identifier
        or getattr(value, "_bound_record_identifiers", None) != identifiers
    ):
        return False
    try:
        reconstructed = TraceDocument(
            schema_version=schema_version,
            trace_identifier=trace_identifier,
            subject_record_identifier=subject_identifier,
            records=records,
        )
    except (AttributeError, TypeError, ValueError):
        return False
    return reconstructed == value
