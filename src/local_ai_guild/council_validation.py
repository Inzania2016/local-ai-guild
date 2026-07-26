"""Deterministic cross-contract validation for one portable Council proceeding."""

from enum import StrEnum
from types import MappingProxyType
from typing import Final

from pydantic import PrivateAttr, StrictBool, StrictInt, computed_field, field_validator

from local_ai_guild.contracts import BoundaryModel
from local_ai_guild.council_contracts import (
    ApprovalRequest,
    CouncilEvidence,
    CouncilIdentifier,
    CouncilProceeding,
    CouncilWorkPacket,
    CrossReview,
    DecisionRecord,
    FrozenPosition,
    KnowledgeClass,
    KnowledgePromotionRequest,
    PositionIntegrityStatus,
    RoleContract,
    RoleKind,
    RuntimeEvent,
    VerificationRecord,
    council_proceeding_is_consistent,
)


class CouncilValidationError(TypeError):
    """Bounded rejection of a raw, subclassed, or corrupted proceeding."""


class CouncilIssueCode(StrEnum):
    """Essential portable proceeding failures."""

    DUPLICATE_IDENTIFIER = "duplicate_identifier"
    MISSING_REFERENCE = "missing_reference"
    WRONG_REFERENCE_TYPE = "wrong_reference_type"
    POSITION_NOT_FROZEN = "position_not_frozen"
    SELF_REVIEW = "self_review"
    MISSING_APPROVAL_REQUEST = "missing_approval_request"
    APPROVAL_NON_HUMAN = "approval_non_human"
    VERIFICATION_AS_APPROVAL = "verification_as_approval"
    APPROVAL_SCOPE_MISMATCH = "approval_scope_mismatch"
    MISSING_PROMOTION_EVIDENCE = "missing_promotion_evidence"
    MISSING_PROMOTION_REVIEW = "missing_promotion_review"
    UNKNOWN_RUNTIME_CORRELATION = "unknown_runtime_correlation"
    RUNTIME_AUTHORITY_LEAK = "runtime_authority_leak"


class CouncilRelationship(StrEnum):
    """Schema-owned relationship names used by bounded issues."""

    IDENTIFIER = "identifier"
    PARTICIPANT_ROLE = "participant_role"
    POSITION_WORK_PACKET = "position_work_packet"
    POSITION_AUTHOR = "position_author"
    REVIEW_POSITION = "review_position"
    REVIEWER_ROLE = "reviewer_role"
    REVIEW_EVIDENCE = "review_evidence"
    VERIFICATION_WORK_PACKET = "verification_work_packet"
    VERIFICATION_SUBJECT = "verification_subject"
    VERIFIER_ROLE = "verifier_role"
    VERIFICATION_EVIDENCE = "verification_evidence"
    APPROVAL_WORK_PACKET = "approval_work_packet"
    REQUIRED_HUMAN_AUTHORITY = "required_human_authority"
    APPROVAL_EVIDENCE = "approval_evidence"
    DECISION_WORK_PACKET = "decision_work_packet"
    DECISION_APPROVAL_REQUEST = "decision_approval_request"
    DECISION_AUTHORITY = "decision_authority"
    DECISION_EVIDENCE = "decision_evidence"
    DISSENT_ROLE = "dissent_role"
    DISSENT_POSITION = "dissent_position"
    PROMOTION_WORK_PACKET = "promotion_work_packet"
    PROMOTION_EVIDENCE = "promotion_evidence"
    PROMOTION_REVIEW = "promotion_review"
    PROMOTION_APPROVAL_REQUEST = "promotion_approval_request"
    RUNTIME_CORRELATION = "runtime_correlation"


class _BuilderAuthority(StrEnum):
    ISSUE = "issue"
    RESULT = "result"


_ISSUE_DEFINITIONS: Final = (
    (
        CouncilIssueCode.DUPLICATE_IDENTIFIER,
        "A Council identifier is declared more than once",
    ),
    (
        CouncilIssueCode.MISSING_REFERENCE,
        "A required Council relationship target is absent",
    ),
    (
        CouncilIssueCode.WRONG_REFERENCE_TYPE,
        "A Council relationship target has the wrong contract type",
    ),
    (
        CouncilIssueCode.POSITION_NOT_FROZEN,
        "A review targets a position whose frozen integrity is unconfirmed",
    ),
    (
        CouncilIssueCode.SELF_REVIEW,
        "A position author cannot perform its cross-review",
    ),
    (
        CouncilIssueCode.MISSING_APPROVAL_REQUEST,
        "A decision or authoritative promotion lacks its approval request",
    ),
    (
        CouncilIssueCode.APPROVAL_NON_HUMAN,
        "Approval authority is attributed to a non-human role",
    ),
    (
        CouncilIssueCode.VERIFICATION_AS_APPROVAL,
        "A verification record is being treated as approval",
    ),
    (
        CouncilIssueCode.APPROVAL_SCOPE_MISMATCH,
        "An approval request belongs to a different work packet",
    ),
    (
        CouncilIssueCode.MISSING_PROMOTION_EVIDENCE,
        "A knowledge-promotion request lacks valid Council evidence",
    ),
    (
        CouncilIssueCode.MISSING_PROMOTION_REVIEW,
        "A knowledge-promotion request lacks a valid cross-review",
    ),
    (
        CouncilIssueCode.UNKNOWN_RUNTIME_CORRELATION,
        "A runtime event refers to an unknown Council object",
    ),
    (
        CouncilIssueCode.RUNTIME_AUTHORITY_LEAK,
        "Runtime telemetry is being used as Council authority",
    ),
)


def _build_issue_registry(definitions: object) -> MappingProxyType[CouncilIssueCode, str]:
    if type(definitions) is not tuple or any(
        type(item) is not tuple
        or len(item) != 2
        or type(item[0]) is not CouncilIssueCode
        or type(item[1]) is not str
        or not 1 <= len(item[1]) <= 96
        for item in definitions
    ):
        raise RuntimeError("Council issue definitions are invalid")
    codes = tuple(item[0] for item in definitions)
    if len(set(codes)) != len(codes) or set(codes) != set(CouncilIssueCode):
        raise RuntimeError("Council issue definitions must be unique and complete")
    return MappingProxyType(dict(definitions))


COUNCIL_ISSUE_MESSAGES: Final = _build_issue_registry(_ISSUE_DEFINITIONS)
COUNCIL_ISSUE_ORDER: Final = tuple(code for code, _ in _ISSUE_DEFINITIONS)
_ISSUE_ORDER_INDEX: Final = MappingProxyType(
    {code: index for index, code in enumerate(COUNCIL_ISSUE_ORDER)}
)
_RELATIONSHIP_ORDER: Final = tuple(CouncilRelationship)
_RELATIONSHIP_ORDER_INDEX: Final = MappingProxyType(
    {relationship: index for index, relationship in enumerate(_RELATIONSHIP_ORDER)}
)
_ISSUE_BUILDER_AUTHORITY: Final = _BuilderAuthority.ISSUE
_RESULT_BUILDER_AUTHORITY: Final = _BuilderAuthority.RESULT


class CouncilValidationIssue(BoundaryModel):
    """One evaluator-built issue with a registry-owned message."""

    code: CouncilIssueCode
    subject_identifier: CouncilIdentifier
    relationship: CouncilRelationship
    _builder_authority: _BuilderAuthority | None = PrivateAttr(default=None)
    _bound_key: tuple[CouncilIssueCode, str, CouncilRelationship] | None = PrivateAttr(default=None)

    def __init__(self, **data: object) -> None:
        authority = data.pop("_builder_authority", None)
        if authority is not _ISSUE_BUILDER_AUTHORITY:
            raise CouncilValidationError(
                "Council issues are created only by the deterministic validator"
            )
        super().__init__(**data)
        self._builder_authority = authority
        self._bound_key = (self.code, self.subject_identifier, self.relationship)

    @computed_field(return_type=str)
    @property
    def message(self) -> str:
        """Derive the only permitted message from the immutable registry."""
        return COUNCIL_ISSUE_MESSAGES[self.code]


type IssueKey = tuple[CouncilIssueCode, str, CouncilRelationship]


def _issue(
    code: CouncilIssueCode,
    subject_identifier: str,
    relationship: CouncilRelationship,
) -> CouncilValidationIssue:
    return CouncilValidationIssue(
        code=code,
        subject_identifier=subject_identifier,
        relationship=relationship,
        _builder_authority=_ISSUE_BUILDER_AUTHORITY,
    )


def _issue_is_consistent(value: object) -> bool:
    return (
        type(value) is CouncilValidationIssue
        and type(getattr(value, "code", None)) is CouncilIssueCode
        and type(getattr(value, "subject_identifier", None)) is str
        and type(getattr(value, "relationship", None)) is CouncilRelationship
        and getattr(value, "_builder_authority", None) is _ISSUE_BUILDER_AUTHORITY
        and getattr(value, "_bound_key", None)
        == (value.code, value.subject_identifier, value.relationship)
        and value.message is COUNCIL_ISSUE_MESSAGES[value.code]
    )


class CouncilValidationResult(BoundaryModel):
    """Evaluator-built deterministic result for one exact proceeding."""

    proceeding_identifier: CouncilIdentifier
    valid: StrictBool
    issue_count: StrictInt
    contract_count: StrictInt
    issues: tuple[CouncilValidationIssue, ...]
    _builder_authority: _BuilderAuthority | None = PrivateAttr(default=None)
    _bound_proceeding_identifier: str | None = PrivateAttr(default=None)
    _bound_contract_identifiers: tuple[str, ...] = PrivateAttr(default=())
    _bound_issue_keys: tuple[IssueKey, ...] = PrivateAttr(default=())

    def __init__(self, **data: object) -> None:
        authority = data.pop("_builder_authority", None)
        contract_identifiers = data.pop("_bound_contract_identifiers", None)
        if authority is not _RESULT_BUILDER_AUTHORITY or type(contract_identifiers) is not tuple:
            raise CouncilValidationError(
                "Council results are created only by the deterministic validator"
            )
        super().__init__(**data)
        self._builder_authority = authority
        self._bound_proceeding_identifier = self.proceeding_identifier
        self._bound_contract_identifiers = contract_identifiers
        self._bound_issue_keys = tuple(
            (issue.code, issue.subject_identifier, issue.relationship) for issue in self.issues
        )
        if not council_validation_result_is_consistent(self):
            raise CouncilValidationError("The Council validation result is inconsistent")

    @field_validator("issues", mode="before")
    @classmethod
    def issues_must_be_exact_instances(cls, value: object) -> object:
        if type(value) is not tuple or any(
            type(item) is not CouncilValidationIssue for item in value
        ):
            raise ValueError("Council result issues must be exact typed instances")
        return value


def council_validation_result_is_consistent(value: object) -> bool:
    """Recheck result counts, ordering, and private source bindings."""
    if type(value) is not CouncilValidationResult:
        return False
    issues = getattr(value, "issues", None)
    if type(issues) is not tuple or any(not _issue_is_consistent(issue) for issue in issues):
        return False
    keys = tuple((issue.code, issue.subject_identifier, issue.relationship) for issue in issues)
    ordering = tuple(
        (_ISSUE_ORDER_INDEX[issue.code], _RELATIONSHIP_ORDER_INDEX[issue.relationship])
        for issue in issues
    )
    identifiers = getattr(value, "_bound_contract_identifiers", None)
    return (
        type(getattr(value, "valid", None)) is bool
        and type(getattr(value, "issue_count", None)) is int
        and type(getattr(value, "contract_count", None)) is int
        and value.valid is (len(issues) == 0)
        and value.issue_count == len(issues)
        and type(identifiers) is tuple
        and value.contract_count == len(identifiers)
        and ordering == tuple(sorted(ordering))
        and getattr(value, "_builder_authority", None) is _RESULT_BUILDER_AUTHORITY
        and getattr(value, "_bound_proceeding_identifier", None) == value.proceeding_identifier
        and getattr(value, "_bound_issue_keys", None) == keys
    )


def _records(proceeding: CouncilProceeding) -> tuple[BoundaryModel, ...]:
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


def _reference_issue(
    *,
    source_identifier: str,
    target_identifier: str,
    relationship: CouncilRelationship,
    records_by_identifier: dict[str, BoundaryModel],
    allowed_types: tuple[type[BoundaryModel], ...],
) -> tuple[CouncilValidationIssue | None, BoundaryModel | None]:
    target = records_by_identifier.get(target_identifier)
    if target is None:
        return (
            _issue(CouncilIssueCode.MISSING_REFERENCE, source_identifier, relationship),
            None,
        )
    if type(target) not in allowed_types:
        return (
            _issue(CouncilIssueCode.WRONG_REFERENCE_TYPE, source_identifier, relationship),
            target,
        )
    return None, target


def _append_reference_issue(
    issues: list[CouncilValidationIssue],
    *,
    source_identifier: str,
    target_identifier: str,
    relationship: CouncilRelationship,
    records_by_identifier: dict[str, BoundaryModel],
    allowed_types: tuple[type[BoundaryModel], ...],
) -> BoundaryModel | None:
    issue, target = _reference_issue(
        source_identifier=source_identifier,
        target_identifier=target_identifier,
        relationship=relationship,
        records_by_identifier=records_by_identifier,
        allowed_types=allowed_types,
    )
    if issue is not None:
        issues.append(issue)
    return target


def _semantic_issues(proceeding: CouncilProceeding) -> tuple[CouncilValidationIssue, ...]:
    records = _records(proceeding)
    records_by_identifier: dict[str, BoundaryModel] = {}
    issues: list[CouncilValidationIssue] = []
    seen: set[str] = {proceeding.identifier}
    duplicate_identifiers: set[str] = set()
    for record in records:
        if record.identifier in seen:
            duplicate_identifiers.add(record.identifier)
        else:
            seen.add(record.identifier)
            records_by_identifier[record.identifier] = record
    for identifier in sorted(duplicate_identifiers):
        issues.append(
            _issue(
                CouncilIssueCode.DUPLICATE_IDENTIFIER,
                identifier,
                CouncilRelationship.IDENTIFIER,
            )
        )

    packet = proceeding.work_packet
    for role_id in packet.participant_role_ids:
        _append_reference_issue(
            issues,
            source_identifier=packet.identifier,
            target_identifier=role_id,
            relationship=CouncilRelationship.PARTICIPANT_ROLE,
            records_by_identifier=records_by_identifier,
            allowed_types=(RoleContract,),
        )

    for position in proceeding.positions:
        _append_reference_issue(
            issues,
            source_identifier=position.identifier,
            target_identifier=position.work_packet_id,
            relationship=CouncilRelationship.POSITION_WORK_PACKET,
            records_by_identifier=records_by_identifier,
            allowed_types=(CouncilWorkPacket,),
        )
        _append_reference_issue(
            issues,
            source_identifier=position.identifier,
            target_identifier=position.author_role_id,
            relationship=CouncilRelationship.POSITION_AUTHOR,
            records_by_identifier=records_by_identifier,
            allowed_types=(RoleContract,),
        )

    for review in proceeding.reviews:
        reviewed_position = _append_reference_issue(
            issues,
            source_identifier=review.identifier,
            target_identifier=review.frozen_position_id,
            relationship=CouncilRelationship.REVIEW_POSITION,
            records_by_identifier=records_by_identifier,
            allowed_types=(FrozenPosition,),
        )
        _append_reference_issue(
            issues,
            source_identifier=review.identifier,
            target_identifier=review.reviewer_role_id,
            relationship=CouncilRelationship.REVIEWER_ROLE,
            records_by_identifier=records_by_identifier,
            allowed_types=(RoleContract,),
        )
        for evidence_id in review.evidence_ids:
            _append_reference_issue(
                issues,
                source_identifier=review.identifier,
                target_identifier=evidence_id,
                relationship=CouncilRelationship.REVIEW_EVIDENCE,
                records_by_identifier=records_by_identifier,
                allowed_types=(CouncilEvidence,),
            )
        if type(reviewed_position) is FrozenPosition:
            if reviewed_position.integrity_status is not PositionIntegrityStatus.FROZEN:
                issues.append(
                    _issue(
                        CouncilIssueCode.POSITION_NOT_FROZEN,
                        review.identifier,
                        CouncilRelationship.REVIEW_POSITION,
                    )
                )
            if reviewed_position.author_role_id == review.reviewer_role_id:
                issues.append(
                    _issue(
                        CouncilIssueCode.SELF_REVIEW,
                        review.identifier,
                        CouncilRelationship.REVIEWER_ROLE,
                    )
                )

    for verification in proceeding.verifications:
        _append_reference_issue(
            issues,
            source_identifier=verification.identifier,
            target_identifier=verification.work_packet_id,
            relationship=CouncilRelationship.VERIFICATION_WORK_PACKET,
            records_by_identifier=records_by_identifier,
            allowed_types=(CouncilWorkPacket,),
        )
        for subject_id in verification.subject_ids:
            _append_reference_issue(
                issues,
                source_identifier=verification.identifier,
                target_identifier=subject_id,
                relationship=CouncilRelationship.VERIFICATION_SUBJECT,
                records_by_identifier=records_by_identifier,
                allowed_types=(FrozenPosition, CrossReview, CouncilEvidence),
            )
        _append_reference_issue(
            issues,
            source_identifier=verification.identifier,
            target_identifier=verification.verifier_role_id,
            relationship=CouncilRelationship.VERIFIER_ROLE,
            records_by_identifier=records_by_identifier,
            allowed_types=(RoleContract,),
        )
        for evidence_id in verification.evidence_ids:
            _append_reference_issue(
                issues,
                source_identifier=verification.identifier,
                target_identifier=evidence_id,
                relationship=CouncilRelationship.VERIFICATION_EVIDENCE,
                records_by_identifier=records_by_identifier,
                allowed_types=(CouncilEvidence,),
            )

    for approval in proceeding.approval_requests:
        _append_reference_issue(
            issues,
            source_identifier=approval.identifier,
            target_identifier=approval.work_packet_id,
            relationship=CouncilRelationship.APPROVAL_WORK_PACKET,
            records_by_identifier=records_by_identifier,
            allowed_types=(CouncilWorkPacket,),
        )
        authority = _append_reference_issue(
            issues,
            source_identifier=approval.identifier,
            target_identifier=approval.required_human_role_id,
            relationship=CouncilRelationship.REQUIRED_HUMAN_AUTHORITY,
            records_by_identifier=records_by_identifier,
            allowed_types=(RoleContract,),
        )
        if type(authority) is RoleContract and (
            authority.role_kind is not RoleKind.HUMAN_AUTHORITY or not authority.may_approve
        ):
            issues.append(
                _issue(
                    CouncilIssueCode.APPROVAL_NON_HUMAN,
                    approval.identifier,
                    CouncilRelationship.REQUIRED_HUMAN_AUTHORITY,
                )
            )
        if type(authority) is RuntimeEvent:
            issues.append(
                _issue(
                    CouncilIssueCode.RUNTIME_AUTHORITY_LEAK,
                    approval.identifier,
                    CouncilRelationship.REQUIRED_HUMAN_AUTHORITY,
                )
            )
        for evidence_id in approval.evidence_ids:
            _append_reference_issue(
                issues,
                source_identifier=approval.identifier,
                target_identifier=evidence_id,
                relationship=CouncilRelationship.APPROVAL_EVIDENCE,
                records_by_identifier=records_by_identifier,
                allowed_types=(CouncilEvidence, VerificationRecord),
            )

    for decision in proceeding.decisions:
        _append_reference_issue(
            issues,
            source_identifier=decision.identifier,
            target_identifier=decision.work_packet_id,
            relationship=CouncilRelationship.DECISION_WORK_PACKET,
            records_by_identifier=records_by_identifier,
            allowed_types=(CouncilWorkPacket,),
        )
        approval: BoundaryModel | None = None
        if decision.approval_request_id is None:
            issues.append(
                _issue(
                    CouncilIssueCode.MISSING_APPROVAL_REQUEST,
                    decision.identifier,
                    CouncilRelationship.DECISION_APPROVAL_REQUEST,
                )
            )
        else:
            approval = _append_reference_issue(
                issues,
                source_identifier=decision.identifier,
                target_identifier=decision.approval_request_id,
                relationship=CouncilRelationship.DECISION_APPROVAL_REQUEST,
                records_by_identifier=records_by_identifier,
                allowed_types=(ApprovalRequest,),
            )
            if approval is None:
                issues.append(
                    _issue(
                        CouncilIssueCode.MISSING_APPROVAL_REQUEST,
                        decision.identifier,
                        CouncilRelationship.DECISION_APPROVAL_REQUEST,
                    )
                )
            elif type(approval) is VerificationRecord:
                issues.append(
                    _issue(
                        CouncilIssueCode.VERIFICATION_AS_APPROVAL,
                        decision.identifier,
                        CouncilRelationship.DECISION_APPROVAL_REQUEST,
                    )
                )
            elif type(approval) is ApprovalRequest and (
                approval.work_packet_id != decision.work_packet_id
            ):
                issues.append(
                    _issue(
                        CouncilIssueCode.APPROVAL_SCOPE_MISMATCH,
                        decision.identifier,
                        CouncilRelationship.DECISION_APPROVAL_REQUEST,
                    )
                )
        authority = _append_reference_issue(
            issues,
            source_identifier=decision.identifier,
            target_identifier=decision.decided_by_role_id,
            relationship=CouncilRelationship.DECISION_AUTHORITY,
            records_by_identifier=records_by_identifier,
            allowed_types=(RoleContract,),
        )
        if type(authority) is RoleContract and (
            authority.role_kind is not RoleKind.HUMAN_AUTHORITY or not authority.may_approve
        ):
            issues.append(
                _issue(
                    CouncilIssueCode.APPROVAL_NON_HUMAN,
                    decision.identifier,
                    CouncilRelationship.DECISION_AUTHORITY,
                )
            )
        if type(authority) is RuntimeEvent:
            issues.append(
                _issue(
                    CouncilIssueCode.RUNTIME_AUTHORITY_LEAK,
                    decision.identifier,
                    CouncilRelationship.DECISION_AUTHORITY,
                )
            )
        for evidence_id in decision.evidence_ids:
            _append_reference_issue(
                issues,
                source_identifier=decision.identifier,
                target_identifier=evidence_id,
                relationship=CouncilRelationship.DECISION_EVIDENCE,
                records_by_identifier=records_by_identifier,
                allowed_types=(CouncilEvidence, VerificationRecord, CrossReview),
            )
        for dissent in decision.dissent:
            _append_reference_issue(
                issues,
                source_identifier=decision.identifier,
                target_identifier=dissent.role_id,
                relationship=CouncilRelationship.DISSENT_ROLE,
                records_by_identifier=records_by_identifier,
                allowed_types=(RoleContract,),
            )
            _append_reference_issue(
                issues,
                source_identifier=decision.identifier,
                target_identifier=dissent.frozen_position_id,
                relationship=CouncilRelationship.DISSENT_POSITION,
                records_by_identifier=records_by_identifier,
                allowed_types=(FrozenPosition,),
            )

    for promotion in proceeding.knowledge_promotions:
        _append_reference_issue(
            issues,
            source_identifier=promotion.identifier,
            target_identifier=promotion.work_packet_id,
            relationship=CouncilRelationship.PROMOTION_WORK_PACKET,
            records_by_identifier=records_by_identifier,
            allowed_types=(CouncilWorkPacket,),
        )
        valid_evidence = 0
        for evidence_id in promotion.evidence_ids:
            target = _append_reference_issue(
                issues,
                source_identifier=promotion.identifier,
                target_identifier=evidence_id,
                relationship=CouncilRelationship.PROMOTION_EVIDENCE,
                records_by_identifier=records_by_identifier,
                allowed_types=(CouncilEvidence, VerificationRecord),
            )
            valid_evidence += type(target) in {CouncilEvidence, VerificationRecord}
        if valid_evidence == 0:
            issues.append(
                _issue(
                    CouncilIssueCode.MISSING_PROMOTION_EVIDENCE,
                    promotion.identifier,
                    CouncilRelationship.PROMOTION_EVIDENCE,
                )
            )
        valid_reviews = 0
        for review_id in promotion.review_ids:
            target = _append_reference_issue(
                issues,
                source_identifier=promotion.identifier,
                target_identifier=review_id,
                relationship=CouncilRelationship.PROMOTION_REVIEW,
                records_by_identifier=records_by_identifier,
                allowed_types=(CrossReview,),
            )
            valid_reviews += type(target) is CrossReview
        if valid_reviews == 0:
            issues.append(
                _issue(
                    CouncilIssueCode.MISSING_PROMOTION_REVIEW,
                    promotion.identifier,
                    CouncilRelationship.PROMOTION_REVIEW,
                )
            )
        approval_required = promotion.target_class in {
            KnowledgeClass.AUTHORITATIVE_KNOWLEDGE,
            KnowledgeClass.APPROVED_DECISION,
        }
        if approval_required and promotion.approval_request_id is None:
            issues.append(
                _issue(
                    CouncilIssueCode.MISSING_APPROVAL_REQUEST,
                    promotion.identifier,
                    CouncilRelationship.PROMOTION_APPROVAL_REQUEST,
                )
            )
        elif promotion.approval_request_id is not None:
            target = _append_reference_issue(
                issues,
                source_identifier=promotion.identifier,
                target_identifier=promotion.approval_request_id,
                relationship=CouncilRelationship.PROMOTION_APPROVAL_REQUEST,
                records_by_identifier=records_by_identifier,
                allowed_types=(ApprovalRequest,),
            )
            if approval_required and type(target) is not ApprovalRequest:
                issues.append(
                    _issue(
                        CouncilIssueCode.MISSING_APPROVAL_REQUEST,
                        promotion.identifier,
                        CouncilRelationship.PROMOTION_APPROVAL_REQUEST,
                    )
                )

    valid_runtime_targets = (
        CouncilWorkPacket,
        RoleContract,
        FrozenPosition,
        CrossReview,
        CouncilEvidence,
        VerificationRecord,
        ApprovalRequest,
        DecisionRecord,
        KnowledgePromotionRequest,
    )
    for event in proceeding.runtime_events:
        target = records_by_identifier.get(event.correlation_id)
        if target is None or type(target) not in valid_runtime_targets:
            issues.append(
                _issue(
                    CouncilIssueCode.UNKNOWN_RUNTIME_CORRELATION,
                    event.identifier,
                    CouncilRelationship.RUNTIME_CORRELATION,
                )
            )

    record_order = {
        identifier: index
        for index, identifier in enumerate(
            (proceeding.identifier, *(record.identifier for record in records))
        )
    }
    return tuple(
        sorted(
            issues,
            key=lambda issue: (
                _ISSUE_ORDER_INDEX[issue.code],
                record_order.get(issue.subject_identifier, len(record_order)),
                issue.subject_identifier,
                _RELATIONSHIP_ORDER_INDEX[issue.relationship],
            ),
        )
    )


def validate_council_proceeding(proceeding: CouncilProceeding) -> CouncilValidationResult:
    """Validate one exact in-memory proceeding without mutation or external resolution."""
    if not council_proceeding_is_consistent(proceeding):
        raise CouncilValidationError("An exact validated Council proceeding is required")
    issues = _semantic_issues(proceeding)
    identifiers = (
        proceeding.identifier,
        *(record.identifier for record in _records(proceeding)),
    )
    return CouncilValidationResult(
        proceeding_identifier=proceeding.identifier,
        valid=not issues,
        issue_count=len(issues),
        contract_count=len(identifiers),
        issues=issues,
        _builder_authority=_RESULT_BUILDER_AUTHORITY,
        _bound_contract_identifiers=identifiers,
    )
