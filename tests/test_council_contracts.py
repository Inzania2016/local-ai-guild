"""Focused tests for the minimum portable Council-contract checkpoint."""

import inspect
import subprocess
import sys
from types import MappingProxyType

import pytest
from pydantic import ValidationError

import local_ai_guild.council_contracts as council_contracts
import local_ai_guild.council_validation as council_validation
from local_ai_guild.contracts import BoundaryModel
from local_ai_guild.council_contracts import (
    ApprovalRequest,
    CouncilEvidence,
    CouncilProceeding,
    CouncilWorkPacket,
    CrossReview,
    DecisionRecord,
    DissentStatement,
    FrozenPosition,
    KnowledgePromotionRequest,
    PositionIntegrityStatus,
    RoleContract,
    RuntimeEvent,
    VerificationRecord,
    council_proceeding_is_consistent,
)
from local_ai_guild.council_fixture import synthetic_council_proceeding
from local_ai_guild.council_validation import (
    COUNCIL_ISSUE_MESSAGES,
    COUNCIL_ISSUE_ORDER,
    CouncilIssueCode,
    CouncilValidationError,
    CouncilValidationIssue,
    CouncilValidationResult,
    council_validation_result_is_consistent,
    validate_council_proceeding,
)

_CONTRACT_TYPES = (
    RoleContract,
    CouncilWorkPacket,
    FrozenPosition,
    CrossReview,
    CouncilEvidence,
    VerificationRecord,
    ApprovalRequest,
    DecisionRecord,
    KnowledgePromotionRequest,
    RuntimeEvent,
)


def _fields(model: BoundaryModel, **changes: object) -> dict[str, object]:
    values = {name: getattr(model, name) for name in type(model).model_fields}
    values.update(changes)
    return values


def _replace(
    proceeding: CouncilProceeding,
    original: BoundaryModel,
    replacement: BoundaryModel,
) -> CouncilProceeding:
    collection_names = (
        "roles",
        "positions",
        "reviews",
        "evidence",
        "verifications",
        "approval_requests",
        "decisions",
        "knowledge_promotions",
        "runtime_events",
    )
    for name in collection_names:
        collection = getattr(proceeding, name)
        if original in collection:
            changed = tuple(replacement if item is original else item for item in collection)
            return CouncilProceeding(**_fields(proceeding, **{name: changed}))
    raise AssertionError("record was not found")


def _codes(proceeding: CouncilProceeding) -> tuple[CouncilIssueCode, ...]:
    return tuple(issue.code for issue in validate_council_proceeding(proceeding).issues)


def test_all_requested_contracts_are_strict_frozen_and_extra_forbid() -> None:
    proceeding = synthetic_council_proceeding()
    instances = (
        proceeding.roles[0],
        proceeding.work_packet,
        proceeding.positions[0],
        proceeding.reviews[0],
        proceeding.evidence[0],
        proceeding.verifications[0],
        proceeding.approval_requests[0],
        proceeding.decisions[0],
        proceeding.knowledge_promotions[0],
        proceeding.runtime_events[0],
    )
    assert tuple(type(instance) for instance in instances) == _CONTRACT_TYPES
    for instance in instances:
        assert instance.model_config["strict"] is True
        assert instance.model_config["frozen"] is True
        assert instance.model_config["extra"] == "forbid"
        with pytest.raises(ValidationError):
            type(instance)(**_fields(instance), unexpected_field="rejected")
        with pytest.raises(ValidationError):
            instance.identifier = "role:changed-v1"


@pytest.mark.parametrize(
    "instance",
    (
        synthetic_council_proceeding().roles[0],
        synthetic_council_proceeding().work_packet,
        synthetic_council_proceeding().positions[0],
        synthetic_council_proceeding().reviews[0],
        synthetic_council_proceeding().evidence[0],
        synthetic_council_proceeding().verifications[0],
        synthetic_council_proceeding().approval_requests[0],
        synthetic_council_proceeding().decisions[0],
        synthetic_council_proceeding().knowledge_promotions[0],
        synthetic_council_proceeding().runtime_events[0],
    ),
)
def test_each_contract_rejects_the_wrong_identifier_namespace(
    instance: BoundaryModel,
) -> None:
    with pytest.raises(ValidationError):
        type(instance)(**_fields(instance, identifier="wrong:synthetic-record-v1"))


def test_relationship_identifiers_reject_non_durable_forms() -> None:
    position = synthetic_council_proceeding().positions[0]
    for invalid in (
        "session-123",
        "openclaw:agent",
        "https://example.com/object",
        "role:no-version",
        "C:\\workspace\\record",
    ):
        with pytest.raises(ValidationError):
            FrozenPosition(**_fields(position, author_role_id=invalid))


def test_contract_fields_are_runtime_neutral() -> None:
    forbidden_names = {
        "runtime_agent_id",
        "session_id",
        "model_name",
        "workspace_path",
        "provider_configuration",
        "openclaw_object",
    }
    all_fields = {
        field_name for contract_type in _CONTRACT_TYPES for field_name in contract_type.model_fields
    }
    assert forbidden_names.isdisjoint(all_fields)
    source = inspect.getsource(council_contracts).lower()
    assert "openclaw" not in source
    assert "session_id" not in source
    assert "model_name" not in source
    assert "workspace_path" not in source
    assert "provider_configuration" not in source


def test_frozen_position_requires_digest_and_preserves_integrity_state() -> None:
    position = synthetic_council_proceeding().positions[0]
    assert position.content_digest.startswith("sha256:")
    assert len(position.content_digest) == 71
    assert position.integrity_status is PositionIntegrityStatus.FROZEN
    with pytest.raises(ValidationError):
        FrozenPosition(**_fields(position, content_digest="sha256:not-a-digest"))


def test_synthetic_proceeding_covers_the_required_flow_and_is_valid() -> None:
    proceeding = synthetic_council_proceeding()
    assert type(proceeding) is CouncilProceeding
    assert council_proceeding_is_consistent(proceeding)
    assert len(proceeding.positions) == 2
    assert all(position.produced_independently for position in proceeding.positions)
    assert all(
        position.integrity_status is PositionIntegrityStatus.FROZEN
        for position in proceeding.positions
    )
    assert len(proceeding.reviews) == 1
    assert len(proceeding.verifications) == 1
    assert len(proceeding.approval_requests) == 1
    assert len(proceeding.decisions) == 1
    assert len(proceeding.decisions[0].dissent) == 1
    assert len(proceeding.knowledge_promotions) == 1
    assert len(proceeding.runtime_events) == 3
    result = validate_council_proceeding(proceeding)
    assert result.valid is True
    assert result.issue_count == 0
    assert result.contract_count == 19


def test_relationships_have_one_canonical_stored_direction() -> None:
    assert "review_ids" not in FrozenPosition.model_fields
    assert "reviewed_by" not in FrozenPosition.model_fields
    assert "position_ids" not in RoleContract.model_fields
    assert "published_by" not in CouncilWorkPacket.model_fields
    assert "promotion_ids" not in ApprovalRequest.model_fields
    assert "runtime_event_ids" not in CouncilWorkPacket.model_fields
    assert "frozen_position_id" in CrossReview.model_fields
    assert "correlation_id" in RuntimeEvent.model_fields


def test_duplicate_identifiers_are_reported() -> None:
    proceeding = synthetic_council_proceeding()
    changed = CouncilProceeding(
        **_fields(proceeding, roles=(*proceeding.roles, proceeding.roles[0]))
    )
    assert CouncilIssueCode.DUPLICATE_IDENTIFIER in _codes(changed)


def test_missing_and_wrong_type_references_are_distinguished() -> None:
    proceeding = synthetic_council_proceeding()
    position = proceeding.positions[0]
    missing = FrozenPosition(**_fields(position, author_role_id="role:synthetic-missing-v1"))
    wrong_type = FrozenPosition(
        **_fields(position, author_role_id=proceeding.work_packet.identifier)
    )
    assert CouncilIssueCode.MISSING_REFERENCE in _codes(_replace(proceeding, position, missing))
    assert CouncilIssueCode.WRONG_REFERENCE_TYPE in _codes(
        _replace(proceeding, position, wrong_type)
    )


def test_review_of_unconfirmed_position_and_self_review_are_reported() -> None:
    proceeding = synthetic_council_proceeding()
    position = proceeding.positions[0]
    review = proceeding.reviews[0]
    unconfirmed = FrozenPosition(
        **_fields(position, integrity_status=PositionIntegrityStatus.UNCONFIRMED)
    )
    self_review = CrossReview(**_fields(review, reviewer_role_id=position.author_role_id))
    assert CouncilIssueCode.POSITION_NOT_FROZEN in _codes(
        _replace(proceeding, position, unconfirmed)
    )
    assert CouncilIssueCode.SELF_REVIEW in _codes(_replace(proceeding, review, self_review))


def test_decision_requires_approval_request_and_human_authority() -> None:
    proceeding = synthetic_council_proceeding()
    decision = proceeding.decisions[0]
    approval = proceeding.approval_requests[0]
    no_request = DecisionRecord(**_fields(decision, approval_request_id=None))
    non_human = ApprovalRequest(
        **_fields(approval, required_human_role_id=proceeding.roles[1].identifier)
    )
    assert CouncilIssueCode.MISSING_APPROVAL_REQUEST in _codes(
        _replace(proceeding, decision, no_request)
    )
    assert CouncilIssueCode.APPROVAL_NON_HUMAN in _codes(_replace(proceeding, approval, non_human))


def test_verification_cannot_be_used_as_approval() -> None:
    proceeding = synthetic_council_proceeding()
    decision = proceeding.decisions[0]
    verification = proceeding.verifications[0]
    changed = DecisionRecord(**_fields(decision, approval_request_id=verification.identifier))
    codes = _codes(_replace(proceeding, decision, changed))
    assert CouncilIssueCode.WRONG_REFERENCE_TYPE in codes
    assert CouncilIssueCode.VERIFICATION_AS_APPROVAL in codes
    assert all("approval" not in name for name in VerificationRecord.model_fields)


def test_decision_preserves_dissent_and_all_four_outcomes_are_bounded() -> None:
    decision = synthetic_council_proceeding().decisions[0]
    assert len(decision.dissent) == 1
    assert decision.dissent[0].frozen_position_id.endswith("-v1")
    schema = DecisionRecord.model_json_schema()
    serialized_schema = str(schema)
    for outcome in ("approved", "modified", "deferred", "rejected"):
        assert outcome in serialized_schema


def test_promotion_requires_valid_evidence_review_and_human_gate() -> None:
    proceeding = synthetic_council_proceeding()
    promotion = proceeding.knowledge_promotions[0]
    changed = KnowledgePromotionRequest(
        **_fields(
            promotion,
            evidence_ids=(),
            review_ids=(),
            approval_request_id=None,
        )
    )
    codes = _codes(_replace(proceeding, promotion, changed))
    assert CouncilIssueCode.MISSING_PROMOTION_EVIDENCE in codes
    assert CouncilIssueCode.MISSING_PROMOTION_REVIEW in codes
    assert CouncilIssueCode.MISSING_APPROVAL_REQUEST in codes
    assert changed.request_state == "proposed"


def test_runtime_event_unknown_correlation_and_authority_leak_are_reported() -> None:
    proceeding = synthetic_council_proceeding()
    event = proceeding.runtime_events[0]
    approval = proceeding.approval_requests[0]
    unknown = RuntimeEvent(**_fields(event, correlation_id="work_packet:synthetic-missing-v1"))
    leaked = ApprovalRequest(**_fields(approval, required_human_role_id=event.identifier))
    assert CouncilIssueCode.UNKNOWN_RUNTIME_CORRELATION in _codes(
        _replace(proceeding, event, unknown)
    )
    leak_codes = _codes(_replace(proceeding, approval, leaked))
    assert CouncilIssueCode.WRONG_REFERENCE_TYPE in leak_codes
    assert CouncilIssueCode.RUNTIME_AUTHORITY_LEAK in leak_codes
    assert set(RuntimeEvent.model_fields) == {
        "identifier",
        "correlation_id",
        "event_kind",
        "outcome",
        "detail_code",
    }


def test_multiple_issues_use_registry_owned_deterministic_order() -> None:
    proceeding = synthetic_council_proceeding()
    position = FrozenPosition(
        **_fields(
            proceeding.positions[0],
            author_role_id="role:synthetic-missing-v1",
            integrity_status=PositionIntegrityStatus.UNCONFIRMED,
        )
    )
    decision = DecisionRecord(**_fields(proceeding.decisions[0], approval_request_id=None))
    promotion = KnowledgePromotionRequest(
        **_fields(
            proceeding.knowledge_promotions[0],
            evidence_ids=(),
            review_ids=(),
            approval_request_id=None,
        )
    )
    event = RuntimeEvent(
        **_fields(
            proceeding.runtime_events[0],
            correlation_id="work_packet:synthetic-missing-v1",
        )
    )
    changed = CouncilProceeding(
        **_fields(
            proceeding,
            roles=(*proceeding.roles, proceeding.roles[0]),
            positions=(position, proceeding.positions[1]),
            decisions=(decision,),
            knowledge_promotions=(promotion,),
            runtime_events=(event, *proceeding.runtime_events[1:]),
        )
    )
    result = validate_council_proceeding(changed)
    indexes = tuple(COUNCIL_ISSUE_ORDER.index(issue.code) for issue in result.issues)
    assert indexes == tuple(sorted(indexes))
    assert type(COUNCIL_ISSUE_MESSAGES) is MappingProxyType
    assert set(COUNCIL_ISSUE_MESSAGES) == set(CouncilIssueCode)
    assert all(issue.message is COUNCIL_ISSUE_MESSAGES[issue.code] for issue in result.issues)


def test_validator_rejects_raw_subclassed_and_corrupted_proceedings() -> None:
    proceeding = synthetic_council_proceeding()
    with pytest.raises(CouncilValidationError):
        validate_council_proceeding({"identifier": "proceeding:raw-v1"})  # type: ignore[arg-type]

    class ProceedingSubclass(CouncilProceeding):
        pass

    subclass = ProceedingSubclass(**_fields(proceeding))
    corrupted = proceeding.model_copy(update={"roles": tuple(reversed(proceeding.roles))})
    constructed = CouncilProceeding.model_construct(**_fields(proceeding))
    raw_dissent = DissentStatement.model_construct(
        role_id="PRIVATE-MARKER",
        frozen_position_id="PRIVATE-MARKER",
        summary="PRIVATE-MARKER",
    )
    corrupted_decision = proceeding.decisions[0].model_copy(update={"dissent": (raw_dissent,)})
    corrupted_nested = _replace(proceeding, proceeding.decisions[0], corrupted_decision)
    for probe in (subclass, corrupted, constructed, corrupted_nested):
        with pytest.raises(CouncilValidationError):
            validate_council_proceeding(probe)


def test_result_direct_construction_and_corruption_are_rejected() -> None:
    proceeding = synthetic_council_proceeding()
    invalid_position = FrozenPosition(
        **_fields(
            proceeding.positions[0],
            author_role_id="role:synthetic-missing-v1",
        )
    )
    missing_approval = DecisionRecord(**_fields(proceeding.decisions[0], approval_request_id=None))
    changed = _replace(proceeding, proceeding.positions[0], invalid_position)
    changed = _replace(changed, changed.decisions[0], missing_approval)
    result = validate_council_proceeding(changed)
    assert len(result.issues) > 1
    with pytest.raises(CouncilValidationError):
        CouncilValidationResult(**_fields(result))
    probes = (
        result.model_copy(update={"proceeding_identifier": "proceeding:relabeled-v1"}),
        result.model_copy(update={"issues": ()}),
        result.model_copy(update={"issue_count": 0}),
        result.model_copy(update={"valid": True}),
        result.model_copy(update={"issues": tuple(reversed(result.issues))}),
        CouncilValidationResult.model_construct(**_fields(result)),
    )
    assert all(not council_validation_result_is_consistent(probe) for probe in probes)


def test_caller_created_issue_lookalike_cannot_forge_result() -> None:
    proceeding = synthetic_council_proceeding()
    invalid_position = FrozenPosition(
        **_fields(
            proceeding.positions[0],
            author_role_id="role:synthetic-missing-v1",
        )
    )
    result = validate_council_proceeding(
        _replace(proceeding, proceeding.positions[0], invalid_position)
    )
    issue = result.issues[0]
    lookalike = CouncilValidationIssue.model_construct(
        code=issue.code,
        subject_identifier=issue.subject_identifier,
        relationship=issue.relationship,
    )
    forged = result.model_copy(update={"issues": (lookalike, *result.issues[1:])})
    assert not council_validation_result_is_consistent(forged)


def test_same_process_serialization_is_deterministic() -> None:
    outputs = tuple(
        validate_council_proceeding(synthetic_council_proceeding()).model_dump_json()
        for _ in range(3)
    )
    assert len(set(outputs)) == 1
    assert "session_id" not in outputs[0]
    assert "model_name" not in outputs[0]
    assert "workspace_path" not in outputs[0]


def test_separate_process_serialization_is_deterministic() -> None:
    command = (
        "from local_ai_guild.council_fixture import synthetic_council_proceeding;"
        "from local_ai_guild.council_validation import validate_council_proceeding;"
        "print(validate_council_proceeding(synthetic_council_proceeding()).model_dump_json())"
    )
    outputs = tuple(
        subprocess.run(
            [sys.executable, "-c", command],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        for _ in range(2)
    )
    assert len(set(outputs)) == 1
    assert "0x" not in outputs[0]


def test_no_runtime_adapter_execution_loader_or_persistence_surface() -> None:
    sources = "\n".join(
        (
            inspect.getsource(council_contracts),
            inspect.getsource(council_validation),
        )
    ).lower()
    for forbidden in (
        "import subprocess",
        "import requests",
        "import httpx",
        "import socket",
        "import tomllib",
        "from pathlib",
        ".open(",
        "write_text(",
        "import sqlite",
        "runtime adapter",
        "openclaw",
    ):
        assert forbidden not in sources
