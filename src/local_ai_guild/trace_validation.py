"""Deterministic semantic validation for the fixed O2 R2 trace."""

from enum import StrEnum
from types import MappingProxyType
from typing import Final

from pydantic import PrivateAttr, StrictBool, StrictInt, computed_field, field_validator

from local_ai_guild.contracts import BoundaryModel
from local_ai_guild.trace_contracts import (
    ApprovalEvidenceStatus,
    ApprovalGate,
    ApprovalStatus,
    AuthorityEvidenceStatus,
    AuthorityKind,
    AuthoritySource,
    AutomatedVerificationStatus,
    Commit,
    Constraint,
    Decision,
    DurableIdentifier,
    EmbeddedRequirement,
    EvidenceProvenance,
    Goal,
    ImplementationArtifact,
    NextAction,
    TraceDocument,
    TraceIdentifier,
    VerificationOutcome,
    VerificationResult,
    WorkPacket,
    trace_document_is_consistent,
)
from local_ai_guild.trace_loading import load_r2_trace


class TraceValidationError(TypeError):
    """Bounded rejection of a raw, subclassed, or corrupted trace."""


class FindingSeverity(StrEnum):
    """Bounded finding severities."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class FindingCode(StrEnum):
    """Semantic conditions the O2 validator can detect without external resolution."""

    MISSING_AUTHORITY_EVIDENCE = "missing_authority_evidence"
    MISSING_APPROVAL_EVIDENCE = "missing_approval_evidence"
    DANGLING_REFERENCE = "dangling_reference"
    WRONG_TARGET_TYPE = "wrong_target_type"
    MISSING_REQUIRED_RELATIONSHIP = "missing_required_relationship"
    UNSUPPORTED_VERIFICATION_CLAIM = "unsupported_verification_claim"
    UNSUPPORTED_AUTHORITY_CLAIM = "unsupported_authority_claim"
    ILLEGAL_STATUS_COMBINATION = "illegal_status_combination"
    COMMIT_DOES_NOT_PROVE_AUTHORIZATION = "commit_does_not_prove_authorization"
    COMMIT_DOES_NOT_PROVE_CORRECTNESS = "commit_does_not_prove_correctness"
    REPOSITORY_ASSERTION_NOT_EXTERNAL_TRUTH = "repository_assertion_not_external_truth"
    SELF_REFERENCE = "self_reference"


class RelationshipKind(StrEnum):
    """Schema-owned relationship metadata used in findings."""

    ADVANCES_GOAL = "advances_goal"
    GOVERNED_BY = "governed_by"
    CONSTRAINED_BY = "constrained_by"
    SELECTED_BY = "selected_by"
    IMPLEMENTED_BY = "implemented_by"
    IMPLEMENTS = "implements"
    VERIFIED_BY = "verified_by"
    PUBLISHED_IN = "published_in"
    VERIFIES = "verifies"
    REQUIRED_AUTHORITY = "required_authority"
    PUBLISHES = "publishes"
    AUTHORIZED_BY_GATE = "authorized_by_gate"
    ENABLED_BY = "enabled_by"
    BLOCKED_BY = "blocked_by"
    AUTHORITY_EVIDENCE = "authority_evidence"
    APPROVAL_EVIDENCE = "approval_evidence"
    PUBLICATION_SUPPORT = "publication_support"
    VERIFICATION_SUPPORT = "verification_support"
    ASSERTION_SCOPE = "assertion_scope"
    AUTHORIZATION_CLAIM = "authorization_claim"
    CORRECTNESS_CLAIM = "correctness_claim"


class _BuilderAuthority(StrEnum):
    FINDING = "finding"
    RESULT = "result"


_FINDING_DEFINITIONS: Final = (
    (
        FindingCode.MISSING_AUTHORITY_EVIDENCE,
        FindingSeverity.ERROR,
        "A required authority source lacks repository evidence",
    ),
    (
        FindingCode.MISSING_APPROVAL_EVIDENCE,
        FindingSeverity.ERROR,
        "No first-class repository approval record is declared for this gate",
    ),
    (
        FindingCode.DANGLING_REFERENCE,
        FindingSeverity.ERROR,
        "A declared relationship target is absent from the trace",
    ),
    (
        FindingCode.WRONG_TARGET_TYPE,
        FindingSeverity.ERROR,
        "A declared relationship target has an unsupported record type",
    ),
    (
        FindingCode.MISSING_REQUIRED_RELATIONSHIP,
        FindingSeverity.ERROR,
        "A status assertion lacks its required supporting relationship",
    ),
    (
        FindingCode.UNSUPPORTED_VERIFICATION_CLAIM,
        FindingSeverity.ERROR,
        "A verification result lacks a supported trace target",
    ),
    (
        FindingCode.UNSUPPORTED_AUTHORITY_CLAIM,
        FindingSeverity.ERROR,
        "An approval gate does not identify a confirmed human authority",
    ),
    (
        FindingCode.ILLEGAL_STATUS_COMBINATION,
        FindingSeverity.ERROR,
        "A publication relationship contradicts its declared approval status",
    ),
    (
        FindingCode.COMMIT_DOES_NOT_PROVE_AUTHORIZATION,
        FindingSeverity.INFO,
        "Commit identity does not establish publication authorization",
    ),
    (
        FindingCode.COMMIT_DOES_NOT_PROVE_CORRECTNESS,
        FindingSeverity.INFO,
        "Commit identity does not establish implementation correctness",
    ),
    (
        FindingCode.REPOSITORY_ASSERTION_NOT_EXTERNAL_TRUTH,
        FindingSeverity.INFO,
        "Repository assertions are not proof of external truth",
    ),
    (
        FindingCode.SELF_REFERENCE,
        FindingSeverity.ERROR,
        "A record must not support itself through a declared relationship",
    ),
)


def _build_finding_registry(
    definitions: object,
) -> tuple[
    MappingProxyType[FindingCode, FindingSeverity],
    MappingProxyType[FindingCode, str],
]:
    """Build complete immutable registries with explicit duplicate detection."""
    if type(definitions) is not tuple or any(
        type(item) is not tuple
        or len(item) != 3
        or type(item[0]) is not FindingCode
        or type(item[1]) is not FindingSeverity
        or type(item[2]) is not str
        or not 1 <= len(item[2]) <= 96
        for item in definitions
    ):
        raise RuntimeError("trace finding definitions are invalid")
    codes = tuple(item[0] for item in definitions)
    if len(set(codes)) != len(codes) or set(codes) != set(FindingCode):
        raise RuntimeError("trace finding definitions must be unique and complete")
    return (
        MappingProxyType({code: severity for code, severity, _ in definitions}),
        MappingProxyType({code: message for code, _, message in definitions}),
    )


FINDING_SEVERITIES, FINDING_MESSAGES = _build_finding_registry(_FINDING_DEFINITIONS)
FINDING_ORDER: Final = (
    FindingCode.MISSING_AUTHORITY_EVIDENCE,
    FindingCode.MISSING_APPROVAL_EVIDENCE,
    FindingCode.DANGLING_REFERENCE,
    FindingCode.WRONG_TARGET_TYPE,
    FindingCode.MISSING_REQUIRED_RELATIONSHIP,
    FindingCode.UNSUPPORTED_VERIFICATION_CLAIM,
    FindingCode.UNSUPPORTED_AUTHORITY_CLAIM,
    FindingCode.ILLEGAL_STATUS_COMBINATION,
    FindingCode.COMMIT_DOES_NOT_PROVE_AUTHORIZATION,
    FindingCode.COMMIT_DOES_NOT_PROVE_CORRECTNESS,
    FindingCode.REPOSITORY_ASSERTION_NOT_EXTERNAL_TRUTH,
    FindingCode.SELF_REFERENCE,
)
if len(set(FINDING_ORDER)) != len(FindingCode) or set(FINDING_ORDER) != set(FindingCode):
    raise RuntimeError("trace finding order must be unique and complete")
_FINDING_ORDER_INDEX: Final = MappingProxyType(
    {code: index for index, code in enumerate(FINDING_ORDER)}
)
_RELATIONSHIP_ORDER: Final = (
    RelationshipKind.ADVANCES_GOAL,
    RelationshipKind.GOVERNED_BY,
    RelationshipKind.CONSTRAINED_BY,
    RelationshipKind.SELECTED_BY,
    RelationshipKind.IMPLEMENTED_BY,
    RelationshipKind.IMPLEMENTS,
    RelationshipKind.VERIFIED_BY,
    RelationshipKind.PUBLISHED_IN,
    RelationshipKind.VERIFIES,
    RelationshipKind.REQUIRED_AUTHORITY,
    RelationshipKind.PUBLISHES,
    RelationshipKind.AUTHORIZED_BY_GATE,
    RelationshipKind.ENABLED_BY,
    RelationshipKind.BLOCKED_BY,
    RelationshipKind.AUTHORITY_EVIDENCE,
    RelationshipKind.APPROVAL_EVIDENCE,
    RelationshipKind.PUBLICATION_SUPPORT,
    RelationshipKind.VERIFICATION_SUPPORT,
    RelationshipKind.ASSERTION_SCOPE,
    RelationshipKind.AUTHORIZATION_CLAIM,
    RelationshipKind.CORRECTNESS_CLAIM,
)
if len(set(_RELATIONSHIP_ORDER)) != len(RelationshipKind) or set(_RELATIONSHIP_ORDER) != set(
    RelationshipKind
):
    raise RuntimeError("trace relationship order must be unique and complete")
_RELATIONSHIP_ORDER_INDEX: Final = MappingProxyType(
    {relationship: index for index, relationship in enumerate(_RELATIONSHIP_ORDER)}
)
_FINDING_BUILDER_AUTHORITY: Final = _BuilderAuthority.FINDING
_RESULT_BUILDER_AUTHORITY: Final = _BuilderAuthority.RESULT


class TraceFinding(BoundaryModel):
    """One evaluator-built bounded finding with registry-owned metadata."""

    code: FindingCode
    subject_identifier: DurableIdentifier
    relationship: RelationshipKind | None = None
    _builder_authority: _BuilderAuthority | None = PrivateAttr(default=None)
    _bound_code: FindingCode | None = PrivateAttr(default=None)
    _bound_subject: str | None = PrivateAttr(default=None)
    _bound_relationship: RelationshipKind | None = PrivateAttr(default=None)

    def __init__(self, **data: object) -> None:
        authority = data.pop("_builder_authority", None)
        if authority is not _FINDING_BUILDER_AUTHORITY:
            raise TraceValidationError(
                "Trace findings are created only by the deterministic validator"
            )
        super().__init__(**data)
        self._builder_authority = authority
        self._bound_code = self.code
        self._bound_subject = self.subject_identifier
        self._bound_relationship = self.relationship

    @computed_field(return_type=FindingSeverity)
    @property
    def severity(self) -> FindingSeverity:
        """Derive severity from the complete immutable registry."""
        return FINDING_SEVERITIES[self.code]

    @computed_field(return_type=str)
    @property
    def message(self) -> str:
        """Derive the only permitted message from the complete registry."""
        return FINDING_MESSAGES[self.code]


def _finding_is_consistent(value: object) -> bool:
    return (
        type(value) is TraceFinding
        and type(getattr(value, "code", None)) is FindingCode
        and type(getattr(value, "subject_identifier", None)) is str
        and (
            getattr(value, "relationship", None) is None
            or type(value.relationship) is RelationshipKind
        )
        and getattr(value, "_builder_authority", None) is _FINDING_BUILDER_AUTHORITY
        and getattr(value, "_bound_code", None) is value.code
        and getattr(value, "_bound_subject", None) == value.subject_identifier
        and getattr(value, "_bound_relationship", None) is value.relationship
        and value.severity is FINDING_SEVERITIES[value.code]
        and value.message is FINDING_MESSAGES[value.code]
    )


class TraceValidationResult(BoundaryModel):
    """Evaluator-built result for one exact ordered TraceDocument."""

    trace_identifier: TraceIdentifier
    subject_record_identifier: DurableIdentifier
    trace_complete: StrictBool
    error_count: StrictInt
    warning_count: StrictInt
    info_count: StrictInt
    findings: tuple[TraceFinding, ...]
    record_count: StrictInt
    _builder_authority: _BuilderAuthority | None = PrivateAttr(default=None)
    _bound_trace_identifier: str | None = PrivateAttr(default=None)
    _bound_record_identifiers: tuple[str, ...] = PrivateAttr(default=())
    _bound_findings: tuple[tuple[FindingCode, str, RelationshipKind | None], ...] = PrivateAttr(
        default=()
    )

    def __init__(self, **data: object) -> None:
        authority = data.pop("_builder_authority", None)
        record_identifiers = data.pop("_bound_record_identifiers", None)
        if authority is not _RESULT_BUILDER_AUTHORITY or type(record_identifiers) is not tuple:
            raise TraceValidationError(
                "Trace results are created only by the deterministic validator"
            )
        super().__init__(**data)
        self._builder_authority = authority
        self._bound_trace_identifier = self.trace_identifier
        self._bound_record_identifiers = record_identifiers
        self._bound_findings = tuple(
            (finding.code, finding.subject_identifier, finding.relationship)
            for finding in self.findings
        )
        if not trace_validation_result_is_consistent(self):
            raise TraceValidationError("The deterministic trace result is inconsistent")

    @field_validator("findings", mode="before")
    @classmethod
    def findings_must_be_exact_instances(cls, value: object) -> object:
        if type(value) is not tuple or any(type(item) is not TraceFinding for item in value):
            raise ValueError("trace result findings must be exact typed instances")
        return value


def trace_validation_result_is_consistent(value: object) -> bool:
    """Recheck result counts, finding order, and private source bindings."""
    if type(value) is not TraceValidationResult:
        return False
    findings = getattr(value, "findings", None)
    if type(findings) is not tuple or any(not _finding_is_consistent(item) for item in findings):
        return False
    errors = sum(item.severity is FindingSeverity.ERROR for item in findings)
    warnings = sum(item.severity is FindingSeverity.WARNING for item in findings)
    infos = sum(item.severity is FindingSeverity.INFO for item in findings)
    ordering = tuple(
        (
            _FINDING_ORDER_INDEX[item.code],
            _RELATIONSHIP_ORDER_INDEX[item.relationship] if item.relationship is not None else -1,
        )
        for item in findings
    )
    record_identifiers = getattr(value, "_bound_record_identifiers", None)
    finding_bindings = tuple(
        (finding.code, finding.subject_identifier, finding.relationship) for finding in findings
    )
    return (
        type(getattr(value, "trace_complete", None)) is bool
        and type(getattr(value, "error_count", None)) is int
        and type(getattr(value, "warning_count", None)) is int
        and type(getattr(value, "info_count", None)) is int
        and type(getattr(value, "record_count", None)) is int
        and value.error_count == errors
        and value.warning_count == warnings
        and value.info_count == infos
        and value.trace_complete is (errors == 0)
        and ordering == tuple(sorted(ordering))
        and getattr(value, "_builder_authority", None) is _RESULT_BUILDER_AUTHORITY
        and getattr(value, "_bound_trace_identifier", None) == value.trace_identifier
        and type(record_identifiers) is tuple
        and len(record_identifiers) == value.record_count
        and len(set(record_identifiers)) == len(record_identifiers)
        and getattr(value, "_bound_findings", None) == finding_bindings
    )


def _finding(
    code: FindingCode,
    subject_identifier: str,
    relationship: RelationshipKind | None,
) -> TraceFinding:
    return TraceFinding(
        code=code,
        subject_identifier=subject_identifier,
        relationship=relationship,
        _builder_authority=_FINDING_BUILDER_AUTHORITY,
    )


def _relation_findings(
    *,
    source_identifier: str,
    relationship: RelationshipKind,
    targets: tuple[str, ...],
    records_by_identifier: dict[str, object],
    requirements_by_identifier: dict[str, EmbeddedRequirement],
    allowed_record_types: tuple[type[object], ...],
    allow_requirements: bool = False,
) -> list[TraceFinding]:
    findings: list[TraceFinding] = []
    for target_identifier in targets:
        if target_identifier == source_identifier:
            findings.append(_finding(FindingCode.SELF_REFERENCE, source_identifier, relationship))
            continue
        target = records_by_identifier.get(target_identifier)
        if target is None:
            target = requirements_by_identifier.get(target_identifier)
        if target is None:
            findings.append(
                _finding(FindingCode.DANGLING_REFERENCE, source_identifier, relationship)
            )
        elif type(target) not in allowed_record_types and not (
            allow_requirements and type(target) is EmbeddedRequirement
        ):
            findings.append(
                _finding(FindingCode.WRONG_TARGET_TYPE, source_identifier, relationship)
            )
    return findings


def _semantic_findings(trace: TraceDocument) -> tuple[TraceFinding, ...]:
    records_by_identifier: dict[str, object] = {
        record.identifier: record for record in trace.records
    }
    requirements_by_identifier = {
        requirement.identifier: requirement
        for record in trace.records
        if type(record) is WorkPacket
        for requirement in record.requirements
    }
    findings: list[TraceFinding] = []

    for record in trace.records:
        if type(record) is WorkPacket:
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.ADVANCES_GOAL,
                    targets=record.advances_goal,
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(Goal,),
                )
            )
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.GOVERNED_BY,
                    targets=record.governed_by,
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(AuthoritySource,),
                )
            )
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.CONSTRAINED_BY,
                    targets=record.constrained_by,
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(Constraint,),
                )
            )
            if record.realization_status.value == "published" and not any(
                type(candidate) is Commit and record.identifier in candidate.publishes
                for candidate in trace.records
            ):
                findings.append(
                    _finding(
                        FindingCode.MISSING_REQUIRED_RELATIONSHIP,
                        record.identifier,
                        RelationshipKind.PUBLICATION_SUPPORT,
                    )
                )
            publication_gates = tuple(
                records_by_identifier.get(candidate.authorized_by_gate)
                for candidate in trace.records
                if type(candidate) is Commit and record.identifier in candidate.publishes
            )
            approved_by_gate = any(
                type(gate) is ApprovalGate and gate.approval_status is ApprovalStatus.APPROVED
                for gate in publication_gates
            )
            if (record.approval_status is ApprovalStatus.APPROVED and not approved_by_gate) or (
                record.approval_status is not ApprovalStatus.APPROVED and approved_by_gate
            ):
                findings.append(
                    _finding(
                        FindingCode.ILLEGAL_STATUS_COMBINATION,
                        record.identifier,
                        RelationshipKind.APPROVAL_EVIDENCE,
                    )
                )
            if (
                record.automated_verification_status is AutomatedVerificationStatus.AUTOMATED_PASSED
                and not any(
                    type(candidate) is VerificationResult
                    and candidate.result is VerificationOutcome.PASSED
                    and any(
                        target in requirements_by_identifier
                        or type(records_by_identifier.get(target)) is ImplementationArtifact
                        for target in candidate.verifies
                    )
                    for candidate in trace.records
                )
            ):
                findings.append(
                    _finding(
                        FindingCode.MISSING_REQUIRED_RELATIONSHIP,
                        record.identifier,
                        RelationshipKind.VERIFICATION_SUPPORT,
                    )
                )
        elif type(record) is AuthoritySource:
            if (
                not record.evidence
                or record.evidence_status is AuthorityEvidenceStatus.UNCONFIRMED_FROM_REPOSITORY
            ):
                findings.append(
                    _finding(
                        FindingCode.MISSING_AUTHORITY_EVIDENCE,
                        record.identifier,
                        RelationshipKind.AUTHORITY_EVIDENCE,
                    )
                )
        elif type(record) is Decision:
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.SELECTED_BY,
                    targets=(record.selected_by,),
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(AuthoritySource,),
                )
            )
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.IMPLEMENTED_BY,
                    targets=record.implemented_by,
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(ImplementationArtifact,),
                )
            )
        elif type(record) is ImplementationArtifact:
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.IMPLEMENTS,
                    targets=record.implements,
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(Decision,),
                    allow_requirements=True,
                )
            )
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.VERIFIED_BY,
                    targets=record.verified_by,
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(VerificationResult,),
                )
            )
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.PUBLISHED_IN,
                    targets=record.published_in,
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(Commit,),
                )
            )
        elif type(record) is VerificationResult:
            relation_findings = _relation_findings(
                source_identifier=record.identifier,
                relationship=RelationshipKind.VERIFIES,
                targets=record.verifies,
                records_by_identifier=records_by_identifier,
                requirements_by_identifier=requirements_by_identifier,
                allowed_record_types=(ImplementationArtifact,),
                allow_requirements=True,
            )
            findings.extend(relation_findings)
            if len(relation_findings) == len(record.verifies):
                findings.append(
                    _finding(
                        FindingCode.UNSUPPORTED_VERIFICATION_CLAIM,
                        record.identifier,
                        RelationshipKind.VERIFIES,
                    )
                )
        elif type(record) is ApprovalGate:
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.REQUIRED_AUTHORITY,
                    targets=(record.required_authority,),
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(AuthoritySource,),
                )
            )
            authority = records_by_identifier.get(record.required_authority)
            if (
                type(authority) is AuthoritySource
                and authority.authority_kind is not AuthorityKind.EXPLICIT_HUMAN_INSTRUCTION
            ):
                findings.append(
                    _finding(
                        FindingCode.UNSUPPORTED_AUTHORITY_CLAIM,
                        record.identifier,
                        RelationshipKind.REQUIRED_AUTHORITY,
                    )
                )
            if (
                record.approval_status is ApprovalStatus.UNKNOWN_FROM_REPOSITORY
                and record.approval_evidence_status
                is ApprovalEvidenceStatus.NOT_RECORDED_IN_REPOSITORY
            ):
                findings.append(
                    _finding(
                        FindingCode.MISSING_APPROVAL_EVIDENCE,
                        record.identifier,
                        RelationshipKind.APPROVAL_EVIDENCE,
                    )
                )
        elif type(record) is Commit:
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.PUBLISHES,
                    targets=record.publishes,
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(WorkPacket, ImplementationArtifact),
                )
            )
            gate = records_by_identifier.get(record.authorized_by_gate)
            if type(gate) is ApprovalGate and gate.approval_status in {
                ApprovalStatus.NOT_REQUIRED,
                ApprovalStatus.PENDING,
                ApprovalStatus.REJECTED,
                ApprovalStatus.REVOKED,
            }:
                findings.append(
                    _finding(
                        FindingCode.ILLEGAL_STATUS_COMBINATION,
                        record.identifier,
                        RelationshipKind.AUTHORIZED_BY_GATE,
                    )
                )
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.AUTHORIZED_BY_GATE,
                    targets=(record.authorized_by_gate,),
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(ApprovalGate,),
                )
            )
            findings.extend(
                (
                    _finding(
                        FindingCode.COMMIT_DOES_NOT_PROVE_AUTHORIZATION,
                        record.identifier,
                        RelationshipKind.AUTHORIZATION_CLAIM,
                    ),
                    _finding(
                        FindingCode.COMMIT_DOES_NOT_PROVE_CORRECTNESS,
                        record.identifier,
                        RelationshipKind.CORRECTNESS_CLAIM,
                    ),
                )
            )
        elif type(record) is NextAction:
            findings.extend(
                _relation_findings(
                    source_identifier=record.identifier,
                    relationship=RelationshipKind.ENABLED_BY,
                    targets=record.enabled_by,
                    records_by_identifier=records_by_identifier,
                    requirements_by_identifier=requirements_by_identifier,
                    allowed_record_types=(WorkPacket, VerificationResult, Commit),
                )
            )
            if record.blocked_by:
                findings.extend(
                    _relation_findings(
                        source_identifier=record.identifier,
                        relationship=RelationshipKind.BLOCKED_BY,
                        targets=record.blocked_by,
                        records_by_identifier=records_by_identifier,
                        requirements_by_identifier=requirements_by_identifier,
                        allowed_record_types=(),
                    )
                )

    subject = records_by_identifier[trace.subject_record_identifier]
    repository_assertion_subject = (
        subject
        if any(
            evidence.provenance is EvidenceProvenance.REPOSITORY_DOCUMENT
            for evidence in subject.evidence
        )
        else next(
            (
                record
                for record in trace.records
                if any(
                    evidence.provenance is EvidenceProvenance.REPOSITORY_DOCUMENT
                    for evidence in record.evidence
                )
            ),
            None,
        )
    )
    if repository_assertion_subject is not None:
        findings.append(
            _finding(
                FindingCode.REPOSITORY_ASSERTION_NOT_EXTERNAL_TRUTH,
                repository_assertion_subject.identifier,
                RelationshipKind.ASSERTION_SCOPE,
            )
        )
    record_order = {record.identifier: index for index, record in enumerate(trace.records)}
    return tuple(
        sorted(
            findings,
            key=lambda finding: (
                _FINDING_ORDER_INDEX[finding.code],
                record_order[finding.subject_identifier],
                _RELATIONSHIP_ORDER_INDEX[finding.relationship]
                if finding.relationship is not None
                else -1,
            ),
        )
    )


def validate_trace(trace: TraceDocument) -> TraceValidationResult:
    """Validate one exact contract-valid trace without resolving external state."""
    if not trace_document_is_consistent(trace):
        raise TraceValidationError("An exact validated trace document is required")
    findings = _semantic_findings(trace)
    errors = sum(item.severity is FindingSeverity.ERROR for item in findings)
    warnings = sum(item.severity is FindingSeverity.WARNING for item in findings)
    infos = sum(item.severity is FindingSeverity.INFO for item in findings)
    record_identifiers = tuple(record.identifier for record in trace.records)
    return TraceValidationResult(
        trace_identifier=trace.trace_identifier,
        subject_record_identifier=trace.subject_record_identifier,
        trace_complete=errors == 0,
        error_count=errors,
        warning_count=warnings,
        info_count=infos,
        findings=findings,
        record_count=len(trace.records),
        _builder_authority=_RESULT_BUILDER_AUTHORITY,
        _bound_record_identifiers=record_identifiers,
    )


def validate_r2_trace() -> TraceValidationResult:
    """Load and validate only the fixed repository-owned R2 trace."""
    return validate_trace(load_r2_trace())
