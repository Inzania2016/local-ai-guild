"""One public synthetic in-memory proceeding for portable Council contracts."""

from typing import Final

from local_ai_guild.council_contracts import (
    ApprovalRequest,
    CouncilEvidence,
    CouncilPermission,
    CouncilProceeding,
    CouncilWorkPacket,
    CrossReview,
    DecisionOutcome,
    DecisionRecord,
    DissentStatement,
    EpistemicClassification,
    EvidenceKind,
    EvidenceProvenance,
    FreshnessPolicy,
    FrozenPosition,
    KnowledgeClass,
    KnowledgePromotionRequest,
    PositionDisposition,
    PositionIntegrityStatus,
    ReviewAssessment,
    RoleContract,
    RoleKind,
    RuntimeEvent,
    RuntimeEventKind,
    RuntimeEventOutcome,
    VerificationMethod,
    VerificationOutcome,
    VerificationRecord,
)

HUMAN_ROLE: Final = RoleContract(
    identifier="role:human-chair-v1",
    title="Human Council chair",
    role_kind=RoleKind.HUMAN_AUTHORITY,
    purpose="Make the bounded human decision requested by the Council",
    obligations=("Review evidence and material dissent before deciding",),
    permissions=(CouncilPermission.READ_PACKET, CouncilPermission.READ_EVIDENCE),
    prohibited_behaviors=("Do not delegate human approval to a model or runtime",),
    independent=False,
    may_approve=True,
)

ANALYST_A_ROLE: Final = RoleContract(
    identifier="role:independent-analyst-a-v1",
    title="Independent analyst A",
    role_kind=RoleKind.COUNCIL_MEMBER,
    purpose="Produce one independent position and review disclosed frozen material",
    obligations=("Submit an independent position before peer disclosure",),
    permissions=(
        CouncilPermission.READ_PACKET,
        CouncilPermission.READ_EVIDENCE,
        CouncilPermission.SUBMIT_POSITION,
        CouncilPermission.REVIEW_POSITION,
    ),
    prohibited_behaviors=("Do not alter another role or frozen position",),
    independent=True,
    may_approve=False,
)

ANALYST_B_ROLE: Final = RoleContract(
    identifier="role:independent-analyst-b-v1",
    title="Independent analyst B",
    role_kind=RoleKind.COUNCIL_MEMBER,
    purpose="Produce one independent position and challenge disclosed frozen material",
    obligations=("Preserve disagreements supported by the synthetic record",),
    permissions=(
        CouncilPermission.READ_PACKET,
        CouncilPermission.READ_EVIDENCE,
        CouncilPermission.SUBMIT_POSITION,
        CouncilPermission.REVIEW_POSITION,
    ),
    prohibited_behaviors=("Do not claim approval or mutate Council authority",),
    independent=True,
    may_approve=False,
)

VERIFIER_ROLE: Final = RoleContract(
    identifier="role:deterministic-verifier-v1",
    title="Deterministic verifier",
    role_kind=RoleKind.DETERMINISTIC_VERIFIER,
    purpose="Record bounded deterministic checks without claiming approval",
    obligations=("State limitations separately from the verification outcome",),
    permissions=(
        CouncilPermission.READ_PACKET,
        CouncilPermission.READ_EVIDENCE,
        CouncilPermission.SUBMIT_VERIFICATION,
    ),
    prohibited_behaviors=("Do not represent verification as human approval",),
    independent=True,
    may_approve=False,
)

SYNTHETIC_PACKET: Final = CouncilWorkPacket(
    identifier="work_packet:portable-contract-review-v1",
    title="Synthetic portable contract review",
    question="Should the synthetic metadata format be accepted with one modification",
    scope="Public synthetic metadata and portable Council contract behavior only",
    constraints=(
        "Use no runtime-native identity or authority",
        "Preserve one material dissent",
    ),
    required_outputs=(
        "Two independently frozen positions",
        "One cross-review and one human decision request",
    ),
    evidence_standard="Repository-authored synthetic assertions plus deterministic checks",
    participant_role_ids=(
        HUMAN_ROLE.identifier,
        ANALYST_A_ROLE.identifier,
        ANALYST_B_ROLE.identifier,
        VERIFIER_ROLE.identifier,
    ),
)

POSITION_A: Final = FrozenPosition(
    identifier="position:metadata-accept-v1",
    work_packet_id=SYNTHETIC_PACKET.identifier,
    author_role_id=ANALYST_A_ROLE.identifier,
    content_digest=f"sha256:{'a' * 64}",
    disposition=PositionDisposition.APPROVE,
    summary="Accept the format because its fields remain deterministic and portable",
    produced_independently=True,
    integrity_status=PositionIntegrityStatus.FROZEN,
)

POSITION_B: Final = FrozenPosition(
    identifier="position:metadata-modify-v1",
    work_packet_id=SYNTHETIC_PACKET.identifier,
    author_role_id=ANALYST_B_ROLE.identifier,
    content_digest=f"sha256:{'b' * 64}",
    disposition=PositionDisposition.MODIFY,
    summary="Require explicit canonical relationship direction before acceptance",
    produced_independently=True,
    integrity_status=PositionIntegrityStatus.FROZEN,
)

PACKET_EVIDENCE: Final = CouncilEvidence(
    identifier="evidence:synthetic-packet-v1",
    kind=EvidenceKind.SOURCE,
    locator="synthetic:portable-contract-packet-v1",
    claim="The repository-authored fixture defines one harmless synthetic proceeding",
    provenance=EvidenceProvenance.SYNTHETIC_ASSERTION,
    epistemic_classification=EpistemicClassification.RETRIEVED_FACT,
)

POSITION_EVIDENCE: Final = CouncilEvidence(
    identifier="evidence:canonical-direction-v1",
    kind=EvidenceKind.POSITION_SUPPORT,
    locator="synthetic:canonical-relationship-review-v1",
    claim="A single stored relationship direction avoids reciprocal-edge drift",
    provenance=EvidenceProvenance.SYNTHETIC_ASSERTION,
    epistemic_classification=EpistemicClassification.INFERENCE,
)

VERIFICATION_EVIDENCE: Final = CouncilEvidence(
    identifier="evidence:deterministic-contract-check-v1",
    kind=EvidenceKind.VERIFICATION_OUTPUT,
    locator="synthetic:deterministic-contract-check-v1",
    claim="The synthetic contracts passed the declared deterministic checks",
    provenance=EvidenceProvenance.DETERMINISTIC_TOOL,
    epistemic_classification=EpistemicClassification.OBSERVED_FACT,
)

CROSS_REVIEW: Final = CrossReview(
    identifier="review:analyst-b-reviews-a-v1",
    frozen_position_id=POSITION_A.identifier,
    reviewer_role_id=ANALYST_B_ROLE.identifier,
    assessment=ReviewAssessment.MIXED,
    evidence_ids=(POSITION_EVIDENCE.identifier,),
    findings=(
        "The position is portable but should state canonical relationship direction",
        "The frozen digest permits review of the submitted version",
    ),
)

DETERMINISTIC_VERIFICATION: Final = VerificationRecord(
    identifier="verification:portable-contracts-v1",
    work_packet_id=SYNTHETIC_PACKET.identifier,
    subject_ids=(POSITION_A.identifier, POSITION_B.identifier, CROSS_REVIEW.identifier),
    verifier_role_id=VERIFIER_ROLE.identifier,
    method=VerificationMethod.DETERMINISTIC_CHECK,
    outcome=VerificationOutcome.PASSED,
    evidence_ids=(VERIFICATION_EVIDENCE.identifier,),
    limitations=(
        "Verification establishes contract consistency only",
        "Verification does not establish human approval or external truth",
    ),
)

HUMAN_APPROVAL_REQUEST: Final = ApprovalRequest(
    identifier="approval_request:portable-contract-decision-v1",
    work_packet_id=SYNTHETIC_PACKET.identifier,
    required_human_role_id=HUMAN_ROLE.identifier,
    question="Approve, modify, defer, or reject the synthetic metadata direction",
    alternatives=("Approve", "Modify", "Defer", "Reject"),
    evidence_ids=(
        PACKET_EVIDENCE.identifier,
        DETERMINISTIC_VERIFICATION.identifier,
    ),
)

HUMAN_DECISION: Final = DecisionRecord(
    identifier="decision:portable-contract-direction-v1",
    work_packet_id=SYNTHETIC_PACKET.identifier,
    approval_request_id=HUMAN_APPROVAL_REQUEST.identifier,
    decided_by_role_id=HUMAN_ROLE.identifier,
    outcome=DecisionOutcome.MODIFIED,
    rationale="Accept the synthetic format with canonical one-direction relationships",
    evidence_ids=(
        DETERMINISTIC_VERIFICATION.identifier,
        CROSS_REVIEW.identifier,
    ),
    dissent=(
        DissentStatement(
            role_id=ANALYST_B_ROLE.identifier,
            frozen_position_id=POSITION_B.identifier,
            summary="Retain the request for explicit relationship-direction documentation",
        ),
    ),
)

KNOWLEDGE_PROMOTION: Final = KnowledgePromotionRequest(
    identifier="promotion_request:canonical-direction-v1",
    work_packet_id=SYNTHETIC_PACKET.identifier,
    candidate_digest=f"sha256:{'c' * 64}",
    target_class=KnowledgeClass.AUTHORITATIVE_KNOWLEDGE,
    evidence_ids=(DETERMINISTIC_VERIFICATION.identifier,),
    review_ids=(CROSS_REVIEW.identifier,),
    approval_request_id=HUMAN_APPROVAL_REQUEST.identifier,
    rationale="Propose canonical relationship direction for separate governed promotion",
    freshness_policy=FreshnessPolicy.CURRENT_UNTIL_SUPERSEDED,
)

RUNTIME_EVENTS: Final = (
    RuntimeEvent(
        identifier="runtime_event:packet-delivered-v1",
        correlation_id=SYNTHETIC_PACKET.identifier,
        event_kind=RuntimeEventKind.SESSION_STARTED,
        outcome=RuntimeEventOutcome.OBSERVED,
        detail_code="packet_delivery_observed",
    ),
    RuntimeEvent(
        identifier="runtime_event:position-exported-v1",
        correlation_id=POSITION_A.identifier,
        event_kind=RuntimeEventKind.POSITION_EXPORTED,
        outcome=RuntimeEventOutcome.SUCCEEDED,
        detail_code="frozen_position_exported",
    ),
    RuntimeEvent(
        identifier="runtime_event:session-ended-v1",
        correlation_id=HUMAN_APPROVAL_REQUEST.identifier,
        event_kind=RuntimeEventKind.SESSION_TERMINATED,
        outcome=RuntimeEventOutcome.OBSERVED,
        detail_code="bounded_session_ended",
    ),
)

SYNTHETIC_COUNCIL_PROCEEDING: Final = CouncilProceeding(
    identifier="proceeding:portable-contract-checkpoint-v1",
    work_packet=SYNTHETIC_PACKET,
    roles=(HUMAN_ROLE, ANALYST_A_ROLE, ANALYST_B_ROLE, VERIFIER_ROLE),
    positions=(POSITION_A, POSITION_B),
    reviews=(CROSS_REVIEW,),
    evidence=(PACKET_EVIDENCE, POSITION_EVIDENCE, VERIFICATION_EVIDENCE),
    verifications=(DETERMINISTIC_VERIFICATION,),
    approval_requests=(HUMAN_APPROVAL_REQUEST,),
    decisions=(HUMAN_DECISION,),
    knowledge_promotions=(KNOWLEDGE_PROMOTION,),
    runtime_events=RUNTIME_EVENTS,
)


def synthetic_council_proceeding() -> CouncilProceeding:
    """Return the immutable repository-owned public synthetic proceeding."""
    return SYNTHETIC_COUNCIL_PROCEEDING
