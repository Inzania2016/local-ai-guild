"""Focused strict-boundary tests for O2 trace contracts."""

import pytest
from pydantic import ValidationError

from local_ai_guild.contracts import BoundaryModel
from local_ai_guild.trace_contracts import (
    ApprovalEvidenceStatus,
    ApprovalGate,
    ApprovalStatus,
    AuthorityEvidenceStatus,
    AuthoritySource,
    AutomatedVerificationStatus,
    Commit,
    Constraint,
    Decision,
    EmbeddedRequirement,
    EpistemicStatus,
    EvidenceKind,
    EvidenceLocator,
    EvidenceProvenance,
    Goal,
    HumanVerificationStatus,
    ImplementationArtifact,
    NextAction,
    TraceDocument,
    VerificationOutcome,
    VerificationResult,
    WorkPacket,
    trace_document_is_consistent,
)
from local_ai_guild.trace_loading import load_r2_trace


def _fields(model: BoundaryModel, **changes: object) -> dict[str, object]:
    values = {name: getattr(model, name) for name in type(model).model_fields}
    values.update(changes)
    return values


def _record(record_type: type[BoundaryModel]) -> BoundaryModel:
    return next(record for record in load_r2_trace().records if type(record) is record_type)


def _repository_evidence(locator: str = "README.md:3-25") -> EvidenceLocator:
    return EvidenceLocator(
        kind=EvidenceKind.REPOSITORY_SOURCE,
        locator=locator,
        scope="Synthetic repository citation",
        epistemic_status=EpistemicStatus.RETRIEVED_FACT,
        provenance=EvidenceProvenance.REPOSITORY_DOCUMENT,
    )


@pytest.mark.parametrize(
    "model_type",
    (
        EvidenceLocator,
        EmbeddedRequirement,
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
        TraceDocument,
    ),
)
def test_trace_boundaries_inherit_strict_frozen_extra_forbid(
    model_type: type[BoundaryModel],
) -> None:
    assert model_type.model_config["strict"] is True
    assert model_type.model_config["frozen"] is True
    assert model_type.model_config["extra"] == "forbid"


def test_trace_document_and_nested_models_reject_mutation() -> None:
    trace = load_r2_trace()
    with pytest.raises(ValidationError):
        trace.trace_identifier = "trace:changed-v1"  # type: ignore[misc]
    with pytest.raises(ValidationError):
        trace.records[0].title = "Changed"  # type: ignore[misc]


def test_trace_document_rejects_extra_fields_and_raw_records() -> None:
    trace = load_r2_trace()
    with pytest.raises(ValidationError):
        TraceDocument(**_fields(trace), unexpected=True)
    with pytest.raises(ValidationError):
        TraceDocument(**_fields(trace, records=(trace.records[0].model_dump(),)))


def test_trace_document_rejects_subclassed_record() -> None:
    class GoalSubclass(Goal):
        pass

    goal = _record(Goal)
    subclass = GoalSubclass(**_fields(goal))
    trace = load_r2_trace()
    with pytest.raises(ValidationError):
        TraceDocument(**_fields(trace, records=(subclass, *trace.records[1:])))


def test_boolean_is_not_accepted_as_authority_precedence() -> None:
    authority = _record(AuthoritySource)
    with pytest.raises(ValidationError):
        AuthoritySource(**_fields(authority, precedence=True))


@pytest.mark.parametrize(
    ("value", "namespace"),
    (
        ("goal:test-v1", "goal"),
        ("work_packet:test-v1", "work_packet"),
        ("authority:test-v1", "authority"),
        ("constraint:test-v1", "constraint"),
        ("decision:test-v1", "decision"),
        ("artifact:test-v1", "artifact"),
        ("verification:test-v1", "verification"),
        ("approval_gate:test-v1", "approval_gate"),
        ("commit:test-v1", "commit"),
        ("next_action:test-v1", "next_action"),
        ("requirement:test-v1", "requirement"),
        ("trace:test-v1", "trace"),
    ),
)
def test_official_identifier_namespaces_are_present(value: str, namespace: str) -> None:
    assert value.partition(":")[0] == namespace


@pytest.mark.parametrize(
    "identifier",
    (
        "authority:wrong-v1",
        "goal:two:colons-v1",
        "Goal:uppercase-v1",
        "goal:space here-v1",
        "goal:\nmarker-v1",
        "https://example.com-v1",
        "goal:path/value-v1",
        "C:drive-v1",
        "goal:missing-version",
        "goal:zero-v0",
        f"goal:{'a' * 125}-v1",
    ),
)
def test_goal_rejects_invalid_or_wrong_namespace_identifiers(identifier: str) -> None:
    goal = _record(Goal)
    with pytest.raises(ValidationError):
        Goal(**_fields(goal, identifier=identifier))


@pytest.mark.parametrize(
    "locator",
    (
        "README.md:3-25",
        "docs/architecture/EXECUTION_FLOW.md:1-40",
        "NEXT_WORK_PACKET.md@6c44970:5-17",
    ),
)
def test_repository_evidence_locator_accepts_bounded_line_references(locator: str) -> None:
    assert _repository_evidence(locator).locator == locator


def test_git_evidence_locator_accepts_exact_sha() -> None:
    sha = "903aa815a6e0176e682b4726ee8114627bd98940"
    evidence = EvidenceLocator(
        kind=EvidenceKind.GIT_COMMIT,
        locator=f"git:{sha}",
        scope="Synthetic Git identity",
        epistemic_status=EpistemicStatus.OBSERVED_FACT,
        provenance=EvidenceProvenance.GIT_HISTORY,
    )
    assert evidence.locator == f"git:{sha}"


@pytest.mark.parametrize(
    "locator",
    (
        "../README.md:1-2",
        "/README.md:1-2",
        "C:/README.md:1-2",
        "\\\\server\\share\\README.md:1-2",
        "docs\\README.md:1-2",
        "https://example.com/readme.md:1-2",
        "README.md@@6c44970:1-2",
        "README.md@:1-2",
        "README.md@not-hex:1-2",
        "README.md:25-3",
        "README.md:0-3",
        "README.md:1-0",
        "README.md:1",
        "README.md:1-2:3-4",
        " README.md:1-2",
        "README.md:1-2 ",
        "README.md:\n1-2",
        f"{'a' * 201}:1-2",
    ),
)
def test_repository_evidence_locator_rejects_unsafe_forms(locator: str) -> None:
    with pytest.raises(ValidationError):
        _repository_evidence(locator)


def test_git_locator_metadata_must_agree() -> None:
    with pytest.raises(ValidationError):
        EvidenceLocator(
            kind=EvidenceKind.GIT_COMMIT,
            locator="git:903aa815a6e0176e682b4726ee8114627bd98940",
            scope="Synthetic Git identity",
            epistemic_status=EpistemicStatus.RETRIEVED_FACT,
            provenance=EvidenceProvenance.REPOSITORY_DOCUMENT,
        )


def test_approved_status_requires_recorded_human_approval_evidence() -> None:
    packet = _record(WorkPacket)
    with pytest.raises(ValidationError):
        WorkPacket(
            **_fields(
                packet,
                approval_status=ApprovalStatus.APPROVED,
                approval_evidence_status=ApprovalEvidenceStatus.NOT_RECORDED_IN_REPOSITORY,
            )
        )


def test_unknown_repository_status_rejects_recorded_evidence_state() -> None:
    packet = _record(WorkPacket)
    with pytest.raises(ValidationError):
        WorkPacket(
            **_fields(
                packet,
                approval_status=ApprovalStatus.UNKNOWN_FROM_REPOSITORY,
                approval_evidence_status=ApprovalEvidenceStatus.RECORDED,
            )
        )


def test_not_required_status_rejects_recorded_evidence_state() -> None:
    packet = _record(WorkPacket)
    with pytest.raises(ValidationError):
        WorkPacket(
            **_fields(
                packet,
                approval_status=ApprovalStatus.NOT_REQUIRED,
                approval_evidence_status=ApprovalEvidenceStatus.RECORDED,
            )
        )


def test_automated_verification_cannot_claim_human_pass() -> None:
    verification = _record(VerificationResult)
    with pytest.raises(ValidationError):
        VerificationResult(
            **_fields(
                verification,
                human_verification_status=HumanVerificationStatus.HUMAN_PASSED,
            )
        )


def test_passed_result_rejects_failed_automated_status() -> None:
    verification = _record(VerificationResult)
    with pytest.raises(ValidationError):
        VerificationResult(
            **_fields(
                verification,
                result=VerificationOutcome.PASSED,
                automated_verification_status=AutomatedVerificationStatus.AUTOMATED_FAILED,
            )
        )


def test_commit_rejects_malformed_sha() -> None:
    commit = _record(Commit)
    with pytest.raises(ValidationError):
        Commit(**_fields(commit, sha="903aa81"))


def test_confirmed_authority_requires_evidence() -> None:
    authority = _record(AuthoritySource)
    with pytest.raises(ValidationError):
        AuthoritySource(
            **_fields(
                authority,
                evidence=(),
            )
        )


def test_any_semantically_unconfirmed_authority_may_omit_evidence() -> None:
    authority = _record(AuthoritySource)
    unconfirmed = AuthoritySource(
        **_fields(
            authority,
            identifier="authority:synthetic-unconfirmed-v1",
            evidence=(),
            evidence_status=AuthorityEvidenceStatus.UNCONFIRMED_FROM_REPOSITORY,
        )
    )
    assert unconfirmed.evidence == ()


def test_unconfirmed_authority_rejects_claimed_confirming_evidence() -> None:
    authority = _record(AuthoritySource)
    with pytest.raises(ValidationError):
        AuthoritySource(
            **_fields(
                authority,
                evidence_status=AuthorityEvidenceStatus.UNCONFIRMED_FROM_REPOSITORY,
            )
        )


@pytest.mark.parametrize(
    ("record_type", "field_name"),
    (
        (WorkPacket, "governed_by"),
        (WorkPacket, "constrained_by"),
        (WorkPacket, "advances_goal"),
        (Decision, "implemented_by"),
        (ImplementationArtifact, "implements"),
        (ImplementationArtifact, "verified_by"),
        (ImplementationArtifact, "published_in"),
        (VerificationResult, "verifies"),
        (Commit, "publishes"),
        (NextAction, "enabled_by"),
    ),
)
def test_relationship_fields_reject_duplicate_targets(
    record_type: type[BoundaryModel], field_name: str
) -> None:
    record = _record(record_type)
    targets = getattr(record, field_name)
    with pytest.raises(ValidationError):
        record_type(**_fields(record, **{field_name: (targets[0], targets[0])}))


def test_next_action_blocked_by_rejects_duplicate_targets() -> None:
    next_action = _record(NextAction)
    with pytest.raises(ValidationError):
        NextAction(
            **_fields(
                next_action,
                blocked_by=(
                    "constraint:synthetic-block-v1",
                    "constraint:synthetic-block-v1",
                ),
            )
        )


def test_embedded_requirement_ids_are_globally_unique_across_work_packets() -> None:
    trace = load_r2_trace()
    packet = _record(WorkPacket)
    second_packet = WorkPacket(**_fields(packet, identifier="work_packet:synthetic-second-v1"))
    with pytest.raises(ValidationError):
        TraceDocument(**_fields(trace, records=(*trace.records, second_packet)))


def test_embedded_and_top_level_identifiers_share_one_logical_space() -> None:
    trace = load_r2_trace()
    packet = _record(WorkPacket)
    requirement_identifier = packet.requirements[0].identifier
    goal = _record(Goal)
    collided_goal = Goal.model_construct(**_fields(goal, identifier=requirement_identifier))
    records = tuple(
        collided_goal if record.identifier == goal.identifier else record
        for record in trace.records
    )
    with pytest.raises(ValidationError):
        TraceDocument(**_fields(trace, records=records))


@pytest.mark.parametrize(
    ("kind", "provenance", "epistemic_status"),
    (
        (
            EvidenceKind.DETERMINISTIC_RESULT,
            EvidenceProvenance.DETERMINISTIC_TOOL,
            EpistemicStatus.HYPOTHESIS,
        ),
        (
            EvidenceKind.REPOSITORY_SOURCE,
            EvidenceProvenance.REPOSITORY_DOCUMENT,
            EpistemicStatus.OBSERVED_FACT,
        ),
        (
            EvidenceKind.HUMAN_APPROVAL_RECORD,
            EvidenceProvenance.GIT_HISTORY,
            EpistemicStatus.RETRIEVED_FACT,
        ),
        (
            EvidenceKind.REPOSITORY_SOURCE,
            EvidenceProvenance.HUMAN_RECORD,
            EpistemicStatus.RETRIEVED_FACT,
        ),
    ),
)
def test_evidence_rejects_impossible_provenance_and_epistemic_combinations(
    kind: EvidenceKind,
    provenance: EvidenceProvenance,
    epistemic_status: EpistemicStatus,
) -> None:
    with pytest.raises(ValidationError):
        EvidenceLocator(
            kind=kind,
            locator="VERIFICATION.md:1-2",
            scope="Synthetic invalid evidence metadata",
            epistemic_status=epistemic_status,
            provenance=provenance,
        )


def test_human_verification_pass_requires_human_verification_record() -> None:
    packet = _record(WorkPacket)
    with pytest.raises(ValidationError):
        WorkPacket(
            **_fields(
                packet,
                human_verification_status=HumanVerificationStatus.HUMAN_PASSED,
            )
        )
    human_verification = EvidenceLocator(
        kind=EvidenceKind.VERIFICATION_RECORD,
        locator="VERIFICATION.md:1-2",
        scope="Synthetic human verification record",
        epistemic_status=EpistemicStatus.RETRIEVED_FACT,
        provenance=EvidenceProvenance.HUMAN_RECORD,
    )
    verified_packet = WorkPacket(
        **_fields(
            packet,
            human_verification_status=HumanVerificationStatus.HUMAN_PASSED,
            evidence=(*packet.evidence, human_verification),
        )
    )
    assert verified_packet.human_verification_status is HumanVerificationStatus.HUMAN_PASSED


def test_trace_document_rejects_duplicate_record_identifiers() -> None:
    trace = load_r2_trace()
    with pytest.raises(ValidationError):
        TraceDocument(**_fields(trace, records=(*trace.records, trace.records[0])))


def test_trace_document_private_binding_detects_relabel_and_reorder_corruption() -> None:
    trace = load_r2_trace()
    relabeled = trace.model_copy(update={"trace_identifier": "trace:relabeled-v1"})
    reordered = trace.model_copy(update={"records": tuple(reversed(trace.records))})
    assert not trace_document_is_consistent(relabeled)
    assert not trace_document_is_consistent(reordered)


def test_trace_document_detects_corrupted_nested_evidence() -> None:
    trace = load_r2_trace()
    goal = trace.records[0]
    evidence = goal.evidence[0].model_copy(update={"locator": "../MARKER:1-2"})
    corrupted_goal = goal.model_copy(update={"evidence": (evidence,)})
    corrupted_trace = trace.model_copy(update={"records": (corrupted_goal, *trace.records[1:])})
    assert not trace_document_is_consistent(corrupted_trace)


def test_trace_document_is_not_a_mapping_and_retains_no_raw_toml() -> None:
    trace = load_r2_trace()
    assert not isinstance(trace, dict)
    assert isinstance(trace.model_extra, type(None))
    assert "toml" not in trace.model_dump_json().lower()
