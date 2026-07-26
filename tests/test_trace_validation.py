"""Focused semantic, corruption, and deterministic-finding tests for O2."""

import subprocess
import sys
from types import MappingProxyType

import pytest

import local_ai_guild.trace_validation as trace_validation
from local_ai_guild.contracts import BoundaryModel
from local_ai_guild.trace_contracts import (
    ApprovalEvidenceStatus,
    ApprovalGate,
    ApprovalStatus,
    AuthorityEvidenceStatus,
    AuthorityKind,
    AuthoritySource,
    Commit,
    Constraint,
    Decision,
    EpistemicStatus,
    EvidenceKind,
    EvidenceLocator,
    EvidenceProvenance,
    Goal,
    ImplementationArtifact,
    NextAction,
    TraceDocument,
    VerificationResult,
    WorkPacket,
)
from local_ai_guild.trace_loading import load_r2_trace
from local_ai_guild.trace_validation import (
    FINDING_MESSAGES,
    FINDING_ORDER,
    FINDING_SEVERITIES,
    FindingCode,
    RelationshipKind,
    TraceFinding,
    TraceValidationError,
    TraceValidationResult,
    trace_validation_result_is_consistent,
    validate_r2_trace,
    validate_trace,
)


def _fields(model: BoundaryModel, **changes: object) -> dict[str, object]:
    values = {name: getattr(model, name) for name in type(model).model_fields}
    values.update(changes)
    return values


def _replace_record(trace: TraceDocument, replacement: BoundaryModel) -> TraceDocument:
    records = tuple(
        replacement if record.identifier == replacement.identifier else record
        for record in trace.records
    )
    return TraceDocument(**_fields(trace, records=records))


def _record(trace: TraceDocument, record_type: type[BoundaryModel]) -> BoundaryModel:
    return next(record for record in trace.records if type(record) is record_type)


def _codes(result: TraceValidationResult) -> tuple[FindingCode, ...]:
    return tuple(finding.code for finding in result.findings)


def _mapped_references(
    references: tuple[str, ...], identifier_map: dict[str, str]
) -> tuple[str, ...]:
    return tuple(identifier_map.get(reference, reference) for reference in references)


def _synthetic_publication_trace(*, approved: bool) -> TraceDocument:
    trace = load_r2_trace()
    identifier_map = {
        "work_packet:r2-v1": "work_packet:synthetic-publication-v1",
        "approval_gate:r2-publication-v1": "approval_gate:synthetic-publication-v1",
        "commit:r2-publication-v1": "commit:synthetic-publication-v1",
    }
    approval_evidence = EvidenceLocator(
        kind=EvidenceKind.HUMAN_APPROVAL_RECORD,
        locator="APPROVALS.md:1-2",
        scope="Synthetic human publication approval",
        epistemic_status=EpistemicStatus.RETRIEVED_FACT,
        provenance=EvidenceProvenance.HUMAN_RECORD,
    )
    synthetic_sha = "a" * 40
    commit_evidence = EvidenceLocator(
        kind=EvidenceKind.GIT_COMMIT,
        locator=f"git:{synthetic_sha}",
        scope="Synthetic publication identity",
        epistemic_status=EpistemicStatus.OBSERVED_FACT,
        provenance=EvidenceProvenance.GIT_HISTORY,
    )
    records: list[BoundaryModel] = []
    for record in trace.records:
        if type(record) is WorkPacket:
            records.append(
                WorkPacket(
                    **_fields(
                        record,
                        identifier=identifier_map[record.identifier],
                        approval_status=(
                            ApprovalStatus.APPROVED
                            if approved
                            else ApprovalStatus.UNKNOWN_FROM_REPOSITORY
                        ),
                        approval_evidence_status=(
                            ApprovalEvidenceStatus.RECORDED
                            if approved
                            else ApprovalEvidenceStatus.NOT_RECORDED_IN_REPOSITORY
                        ),
                        evidence=(
                            (*record.evidence, approval_evidence) if approved else record.evidence
                        ),
                    )
                )
            )
        elif type(record) is ImplementationArtifact:
            records.append(
                ImplementationArtifact(
                    **_fields(
                        record,
                        implements=_mapped_references(record.implements, identifier_map),
                        verified_by=_mapped_references(record.verified_by, identifier_map),
                        published_in=_mapped_references(record.published_in, identifier_map),
                    )
                )
            )
        elif type(record) is ApprovalGate:
            records.append(
                ApprovalGate(
                    **_fields(
                        record,
                        identifier=identifier_map[record.identifier],
                        approval_status=(
                            ApprovalStatus.APPROVED
                            if approved
                            else ApprovalStatus.UNKNOWN_FROM_REPOSITORY
                        ),
                        approval_evidence_status=(
                            ApprovalEvidenceStatus.RECORDED
                            if approved
                            else ApprovalEvidenceStatus.NOT_RECORDED_IN_REPOSITORY
                        ),
                        evidence=(approval_evidence,) if approved else (),
                    )
                )
            )
        elif type(record) is Commit:
            records.append(
                Commit(
                    **_fields(
                        record,
                        identifier=identifier_map[record.identifier],
                        sha=synthetic_sha,
                        publishes=_mapped_references(record.publishes, identifier_map),
                        authorized_by_gate=identifier_map[record.authorized_by_gate],
                        evidence=(commit_evidence,),
                    )
                )
            )
        elif type(record) is NextAction:
            records.append(
                NextAction(
                    **_fields(
                        record,
                        enabled_by=_mapped_references(record.enabled_by, identifier_map),
                    )
                )
            )
        else:
            records.append(record)
    return TraceDocument(
        schema_version="0.1",
        trace_identifier=(
            "trace:synthetic-complete-v1" if approved else "trace:synthetic-incomplete-v1"
        ),
        subject_record_identifier=identifier_map[trace.subject_record_identifier],
        records=tuple(records),
    )


def test_official_r2_trace_inventory_uses_exactly_ten_record_types() -> None:
    record_types = {type(record) for record in load_r2_trace().records}
    assert record_types == {
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
    }


def test_official_r2_trace_has_expected_bounded_findings_in_order() -> None:
    result = validate_r2_trace()
    assert result.trace_complete is False
    assert result.error_count == 1
    assert result.warning_count == 0
    assert result.info_count == 3
    assert result.record_count == 30
    assert _codes(result) == (
        FindingCode.MISSING_APPROVAL_EVIDENCE,
        FindingCode.COMMIT_DOES_NOT_PROVE_AUTHORIZATION,
        FindingCode.COMMIT_DOES_NOT_PROVE_CORRECTNESS,
        FindingCode.REPOSITORY_ASSERTION_NOT_EXTERNAL_TRUTH,
    )


def test_official_approval_finding_does_not_claim_rejection_or_nonoccurrence() -> None:
    finding = validate_r2_trace().findings[0]
    message = finding.message.lower()
    assert finding.code is FindingCode.MISSING_APPROVAL_EVIDENCE
    assert finding.subject_identifier == "approval_gate:r2-publication-v1"
    assert "failed" not in message
    assert "rejected" not in message
    assert "did not occur" not in message
    assert "not authorized" not in message


def test_findings_are_derived_for_differently_identified_incomplete_trace() -> None:
    trace = _synthetic_publication_trace(approved=False)
    result = validate_trace(trace)
    assert result.trace_complete is False
    approval = next(
        finding
        for finding in result.findings
        if finding.code is FindingCode.MISSING_APPROVAL_EVIDENCE
    )
    assert approval.subject_identifier == "approval_gate:synthetic-publication-v1"
    assert all("r2-publication" not in finding.subject_identifier for finding in result.findings)


def test_complete_synthetic_trace_is_trace_complete_without_approval_error() -> None:
    trace = _synthetic_publication_trace(approved=True)
    result = validate_trace(trace)
    assert result.trace_complete is True
    assert result.error_count == 0
    assert _codes(result) == (
        FindingCode.COMMIT_DOES_NOT_PROVE_AUTHORIZATION,
        FindingCode.COMMIT_DOES_NOT_PROVE_CORRECTNESS,
        FindingCode.REPOSITORY_ASSERTION_NOT_EXTERNAL_TRUTH,
    )
    assert result.findings[0].subject_identifier == "commit:synthetic-publication-v1"
    assert result.findings[-1].subject_identifier == "work_packet:synthetic-publication-v1"


def test_trace_without_commit_has_no_commit_specific_information() -> None:
    trace = _synthetic_publication_trace(approved=False)
    without_commit = TraceDocument(
        **_fields(
            trace,
            records=tuple(record for record in trace.records if type(record) is not Commit),
        )
    )
    result = validate_trace(without_commit)
    assert FindingCode.COMMIT_DOES_NOT_PROVE_AUTHORIZATION not in _codes(result)
    assert FindingCode.COMMIT_DOES_NOT_PROVE_CORRECTNESS not in _codes(result)


def test_repository_assertion_limitation_follows_evidence_semantics_and_subject() -> None:
    result = validate_trace(_synthetic_publication_trace(approved=True))
    assertion = next(
        finding
        for finding in result.findings
        if finding.code is FindingCode.REPOSITORY_ASSERTION_NOT_EXTERNAL_TRUTH
    )
    assert assertion.subject_identifier == "work_packet:synthetic-publication-v1"


def test_approval_status_cannot_be_forged_independently_of_packet_status() -> None:
    trace = _synthetic_publication_trace(approved=False)
    gate = _record(trace, ApprovalGate)
    approval_evidence = EvidenceLocator(
        kind=EvidenceKind.HUMAN_APPROVAL_RECORD,
        locator="APPROVALS.md:1-2",
        scope="Synthetic human publication approval",
        epistemic_status=EpistemicStatus.RETRIEVED_FACT,
        provenance=EvidenceProvenance.HUMAN_RECORD,
    )
    approved_gate = ApprovalGate(
        **_fields(
            gate,
            approval_status=ApprovalStatus.APPROVED,
            approval_evidence_status=ApprovalEvidenceStatus.RECORDED,
            evidence=(approval_evidence,),
        )
    )
    result = validate_trace(_replace_record(trace, approved_gate))
    assert FindingCode.ILLEGAL_STATUS_COMBINATION in _codes(result)


def test_unconfirmed_authority_cannot_satisfy_approved_gate() -> None:
    trace = _synthetic_publication_trace(approved=True)
    authority = next(
        record
        for record in trace.records
        if type(record) is AuthoritySource and record.identifier == "authority:project-owner-v1"
    )
    unconfirmed = AuthoritySource(
        **_fields(
            authority,
            evidence=(),
            evidence_status=AuthorityEvidenceStatus.UNCONFIRMED_FROM_REPOSITORY,
        )
    )
    result = validate_trace(_replace_record(trace, unconfirmed))
    assert FindingCode.MISSING_AUTHORITY_EVIDENCE in _codes(result)
    assert result.trace_complete is False


def test_non_human_authority_kind_cannot_satisfy_approval_gate() -> None:
    trace = _synthetic_publication_trace(approved=True)
    authority = next(
        record
        for record in trace.records
        if type(record) is AuthoritySource and record.identifier == "authority:project-owner-v1"
    )
    security_policy = AuthoritySource(
        **_fields(authority, authority_kind=AuthorityKind.SECURITY_POLICY)
    )
    result = validate_trace(_replace_record(trace, security_policy))
    assert FindingCode.UNSUPPORTED_AUTHORITY_CLAIM in _codes(result)
    assert result.trace_complete is False


def test_commit_cannot_serve_as_human_approval_evidence() -> None:
    with pytest.raises(ValueError):
        EvidenceLocator(
            kind=EvidenceKind.HUMAN_APPROVAL_RECORD,
            locator="git:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            scope="Synthetic invalid approval evidence",
            epistemic_status=EpistemicStatus.OBSERVED_FACT,
            provenance=EvidenceProvenance.HUMAN_RECORD,
        )


def test_publication_commit_cannot_be_authorized_by_rejected_gate() -> None:
    trace = _synthetic_publication_trace(approved=True)
    gate = _record(trace, ApprovalGate)
    packet = _record(trace, WorkPacket)
    rejected_gate = ApprovalGate(**_fields(gate, approval_status=ApprovalStatus.REJECTED))
    rejected_packet = WorkPacket(**_fields(packet, approval_status=ApprovalStatus.REJECTED))
    trace = _replace_record(_replace_record(trace, rejected_gate), rejected_packet)
    result = validate_trace(trace)
    assert FindingCode.ILLEGAL_STATUS_COMBINATION in _codes(result)
    assert result.trace_complete is False


def test_not_required_publication_gate_cannot_authorize_a_commit() -> None:
    trace = _synthetic_publication_trace(approved=True)
    gate = _record(trace, ApprovalGate)
    packet = _record(trace, WorkPacket)
    bypass_gate = ApprovalGate(
        **_fields(
            gate,
            approval_status=ApprovalStatus.NOT_REQUIRED,
            approval_evidence_status=ApprovalEvidenceStatus.NOT_REQUIRED,
            evidence=(),
        )
    )
    bypass_packet = WorkPacket(
        **_fields(
            packet,
            approval_status=ApprovalStatus.NOT_REQUIRED,
            approval_evidence_status=ApprovalEvidenceStatus.NOT_REQUIRED,
            evidence=tuple(
                evidence
                for evidence in packet.evidence
                if evidence.kind is not EvidenceKind.HUMAN_APPROVAL_RECORD
            ),
        )
    )
    result = validate_trace(_replace_record(_replace_record(trace, bypass_gate), bypass_packet))
    assert FindingCode.ILLEGAL_STATUS_COMBINATION in _codes(result)
    assert result.trace_complete is False


def test_all_official_relationships_except_approval_gap_are_complete() -> None:
    relationship_errors = {
        FindingCode.DANGLING_REFERENCE,
        FindingCode.WRONG_TARGET_TYPE,
        FindingCode.MISSING_REQUIRED_RELATIONSHIP,
        FindingCode.UNSUPPORTED_VERIFICATION_CLAIM,
        FindingCode.UNSUPPORTED_AUTHORITY_CLAIM,
        FindingCode.SELF_REFERENCE,
        FindingCode.MISSING_AUTHORITY_EVIDENCE,
    }
    assert not relationship_errors.intersection(_codes(validate_r2_trace()))


def test_dangling_authority_reference_is_reported_without_echoing_target() -> None:
    trace = load_r2_trace()
    packet = _record(trace, WorkPacket)
    changed = WorkPacket(**_fields(packet, governed_by=("authority:private-marker-v1",)))
    result = validate_trace(_replace_record(trace, changed))
    finding = next(item for item in result.findings if item.code is FindingCode.DANGLING_REFERENCE)
    assert finding.subject_identifier == packet.identifier
    assert finding.relationship is RelationshipKind.GOVERNED_BY
    assert "private-marker" not in finding.model_dump_json()


@pytest.mark.parametrize(
    ("record_type", "field_name", "target", "relationship"),
    (
        (WorkPacket, "advances_goal", ("authority:r2-work-packet-v1",), "advances_goal"),
        (WorkPacket, "governed_by", ("goal:evidence-before-execution-v1",), "governed_by"),
        (WorkPacket, "constrained_by", ("goal:evidence-before-execution-v1",), "constrained_by"),
        (Decision, "selected_by", "goal:evidence-before-execution-v1", "selected_by"),
        (Decision, "implemented_by", ("goal:evidence-before-execution-v1",), "implemented_by"),
        (
            ImplementationArtifact,
            "implements",
            ("goal:evidence-before-execution-v1",),
            "implements",
        ),
        (
            ImplementationArtifact,
            "verified_by",
            ("goal:evidence-before-execution-v1",),
            "verified_by",
        ),
        (
            ImplementationArtifact,
            "published_in",
            ("goal:evidence-before-execution-v1",),
            "published_in",
        ),
        (VerificationResult, "verifies", ("goal:evidence-before-execution-v1",), "verifies"),
        (
            ApprovalGate,
            "required_authority",
            "goal:evidence-before-execution-v1",
            "required_authority",
        ),
        (Commit, "publishes", ("goal:evidence-before-execution-v1",), "publishes"),
        (
            Commit,
            "authorized_by_gate",
            "goal:evidence-before-execution-v1",
            "authorized_by_gate",
        ),
        (NextAction, "enabled_by", ("goal:evidence-before-execution-v1",), "enabled_by"),
    ),
)
def test_wrong_relationship_target_types_are_reported(
    record_type: type[BoundaryModel],
    field_name: str,
    target: object,
    relationship: str,
) -> None:
    trace = load_r2_trace()
    record = _record(trace, record_type)
    changed = record_type(**_fields(record, **{field_name: target}))
    result = validate_trace(_replace_record(trace, changed))
    assert any(
        finding.code is FindingCode.WRONG_TARGET_TYPE
        and finding.subject_identifier == record.identifier
        and finding.relationship.value == relationship
        for finding in result.findings
    )


@pytest.mark.parametrize(
    ("record_type", "field_name", "relationship", "scalar"),
    (
        (WorkPacket, "advances_goal", RelationshipKind.ADVANCES_GOAL, False),
        (WorkPacket, "governed_by", RelationshipKind.GOVERNED_BY, False),
        (WorkPacket, "constrained_by", RelationshipKind.CONSTRAINED_BY, False),
        (Decision, "selected_by", RelationshipKind.SELECTED_BY, True),
        (Decision, "implemented_by", RelationshipKind.IMPLEMENTED_BY, False),
        (ImplementationArtifact, "implements", RelationshipKind.IMPLEMENTS, False),
        (ImplementationArtifact, "verified_by", RelationshipKind.VERIFIED_BY, False),
        (ImplementationArtifact, "published_in", RelationshipKind.PUBLISHED_IN, False),
        (VerificationResult, "verifies", RelationshipKind.VERIFIES, False),
        (ApprovalGate, "required_authority", RelationshipKind.REQUIRED_AUTHORITY, True),
        (Commit, "publishes", RelationshipKind.PUBLISHES, False),
        (Commit, "authorized_by_gate", RelationshipKind.AUTHORIZED_BY_GATE, True),
        (NextAction, "enabled_by", RelationshipKind.ENABLED_BY, False),
    ),
)
def test_every_supported_relationship_reports_a_missing_target(
    record_type: type[BoundaryModel],
    field_name: str,
    relationship: RelationshipKind,
    scalar: bool,
) -> None:
    trace = load_r2_trace()
    record = _record(trace, record_type)
    missing = "authority:synthetic-missing-v1"
    target = missing if scalar else (missing,)
    changed = record_type(**_fields(record, **{field_name: target}))
    result = validate_trace(_replace_record(trace, changed))
    assert any(
        finding.code is FindingCode.DANGLING_REFERENCE
        and finding.subject_identifier == record.identifier
        and finding.relationship is relationship
        for finding in result.findings
    )


@pytest.mark.parametrize(
    ("record_type", "field_name", "relationship", "scalar"),
    (
        (WorkPacket, "advances_goal", RelationshipKind.ADVANCES_GOAL, False),
        (WorkPacket, "governed_by", RelationshipKind.GOVERNED_BY, False),
        (WorkPacket, "constrained_by", RelationshipKind.CONSTRAINED_BY, False),
        (Decision, "selected_by", RelationshipKind.SELECTED_BY, True),
        (Decision, "implemented_by", RelationshipKind.IMPLEMENTED_BY, False),
        (ImplementationArtifact, "implements", RelationshipKind.IMPLEMENTS, False),
        (ImplementationArtifact, "verified_by", RelationshipKind.VERIFIED_BY, False),
        (ImplementationArtifact, "published_in", RelationshipKind.PUBLISHED_IN, False),
        (VerificationResult, "verifies", RelationshipKind.VERIFIES, False),
        (ApprovalGate, "required_authority", RelationshipKind.REQUIRED_AUTHORITY, True),
        (Commit, "publishes", RelationshipKind.PUBLISHES, False),
        (Commit, "authorized_by_gate", RelationshipKind.AUTHORIZED_BY_GATE, True),
        (NextAction, "enabled_by", RelationshipKind.ENABLED_BY, False),
    ),
)
def test_every_supported_relationship_reports_self_reference(
    record_type: type[BoundaryModel],
    field_name: str,
    relationship: RelationshipKind,
    scalar: bool,
) -> None:
    trace = load_r2_trace()
    record = _record(trace, record_type)
    target = record.identifier if scalar else (record.identifier,)
    changed = record_type(**_fields(record, **{field_name: target}))
    result = validate_trace(_replace_record(trace, changed))
    assert any(
        finding.code is FindingCode.SELF_REFERENCE
        and finding.subject_identifier == record.identifier
        and finding.relationship is relationship
        for finding in result.findings
    )


def test_valid_reciprocal_decision_artifact_links_are_not_cycles() -> None:
    result = validate_trace(_synthetic_publication_trace(approved=True))
    assert result.trace_complete is True
    assert FindingCode.SELF_REFERENCE not in _codes(result)
    assert FindingCode.WRONG_TARGET_TYPE not in _codes(result)


def test_embedded_requirement_in_wrong_relationship_field_is_wrong_target_type() -> None:
    trace = load_r2_trace()
    packet = _record(trace, WorkPacket)
    requirement_identifier = packet.requirements[0].identifier
    changed = WorkPacket(**_fields(packet, governed_by=(requirement_identifier,)))
    result = validate_trace(_replace_record(trace, changed))
    assert any(
        finding.code is FindingCode.WRONG_TARGET_TYPE
        and finding.relationship is RelationshipKind.GOVERNED_BY
        for finding in result.findings
    )


def test_published_packet_without_commit_support_is_reported() -> None:
    trace = load_r2_trace()
    records = tuple(record for record in trace.records if type(record) is not Commit)
    changed = TraceDocument(**_fields(trace, records=records))
    result = validate_trace(changed)
    assert any(
        finding.code is FindingCode.MISSING_REQUIRED_RELATIONSHIP
        and finding.relationship is RelationshipKind.PUBLICATION_SUPPORT
        for finding in result.findings
    )


def test_automated_pass_without_verification_support_is_reported() -> None:
    trace = load_r2_trace()
    records = tuple(record for record in trace.records if type(record) is not VerificationResult)
    changed = TraceDocument(**_fields(trace, records=records))
    result = validate_trace(changed)
    assert any(
        finding.code is FindingCode.MISSING_REQUIRED_RELATIONSHIP
        and finding.relationship is RelationshipKind.VERIFICATION_SUPPORT
        for finding in result.findings
    )


def test_verification_with_only_dangling_targets_is_unsupported() -> None:
    trace = load_r2_trace()
    verification = _record(trace, VerificationResult)
    changed = VerificationResult(**_fields(verification, verifies=("artifact:private-marker-v1",)))
    result = validate_trace(_replace_record(trace, changed))
    assert FindingCode.DANGLING_REFERENCE in _codes(result)
    assert FindingCode.UNSUPPORTED_VERIFICATION_CLAIM in _codes(result)


def test_validator_rejects_raw_dictionary_and_subclass() -> None:
    with pytest.raises(TraceValidationError) as raw_error:
        validate_trace({"PRIVATE_MARKER": "PRIVATE_VALUE"})  # type: ignore[arg-type]
    assert "PRIVATE" not in str(raw_error.value)

    class TraceSubclass(TraceDocument):
        pass

    trace = load_r2_trace()
    subclass = TraceSubclass(**_fields(trace))
    with pytest.raises(TraceValidationError):
        validate_trace(subclass)


def test_validator_rejects_model_construct_and_unchecked_copy_corruption() -> None:
    trace = load_r2_trace()
    constructed = TraceDocument.model_construct(
        schema_version="0.1",
        trace_identifier=trace.trace_identifier,
        subject_record_identifier=trace.subject_record_identifier,
        records=trace.records,
    )
    missing_fields = TraceDocument.model_construct(records=trace.records)
    relabeled = trace.model_copy(update={"trace_identifier": "trace:relabeled-v1"})
    duplicated = trace.model_copy(update={"records": (*trace.records, trace.records[0])})
    for corrupted in (constructed, missing_fields, relabeled, duplicated):
        with pytest.raises(TraceValidationError):
            validate_trace(corrupted)


def test_validator_rejects_raw_nested_dictionary_corruption() -> None:
    trace = load_r2_trace()
    goal = trace.records[0]
    raw_goal = goal.model_copy(update={"evidence": ({"PRIVATE": "MARKER"},)})
    corrupted = trace.model_copy(update={"records": (raw_goal, *trace.records[1:])})
    with pytest.raises(TraceValidationError) as captured:
        validate_trace(corrupted)
    assert "PRIVATE" not in str(captured.value)
    assert "MARKER" not in str(captured.value)


def test_finding_registry_is_complete_immutable_and_explicitly_ordered() -> None:
    assert type(FINDING_MESSAGES) is MappingProxyType
    assert type(FINDING_SEVERITIES) is MappingProxyType
    assert set(FINDING_MESSAGES) == set(FindingCode)
    assert set(FINDING_SEVERITIES) == set(FindingCode)
    assert len(FINDING_ORDER) == len(set(FINDING_ORDER)) == len(FindingCode)
    with pytest.raises(TypeError):
        FINDING_MESSAGES[FindingCode.DANGLING_REFERENCE] = "changed"  # type: ignore[index]


def test_finding_registry_builder_rejects_duplicates_and_incomplete_definitions() -> None:
    definitions = trace_validation._FINDING_DEFINITIONS
    with pytest.raises(RuntimeError):
        trace_validation._build_finding_registry((*definitions, definitions[0]))
    with pytest.raises(RuntimeError):
        trace_validation._build_finding_registry(definitions[:-1])


def test_finding_message_and_severity_are_registry_owned() -> None:
    for finding in validate_r2_trace().findings:
        assert finding.message is FINDING_MESSAGES[finding.code]
        assert finding.severity is FINDING_SEVERITIES[finding.code]
    with pytest.raises(TraceValidationError):
        TraceFinding(
            code=FindingCode.DANGLING_REFERENCE,
            subject_identifier="goal:synthetic-v1",
            relationship=RelationshipKind.ADVANCES_GOAL,
            message="PRIVATE MARKER",
        )


def test_validation_result_direct_construction_is_rejected() -> None:
    result = validate_r2_trace()
    with pytest.raises(TraceValidationError):
        TraceValidationResult(**_fields(result, trace_complete=True, findings=()))


def test_validation_result_corruption_is_detected() -> None:
    result = validate_r2_trace()
    probes = (
        result.model_copy(update={"trace_identifier": "trace:relabeled-v1"}),
        result.model_copy(update={"findings": ()}),
        result.model_copy(update={"findings": tuple(reversed(result.findings))}),
        result.model_copy(update={"error_count": 0}),
        result.model_copy(update={"trace_complete": True}),
        TraceValidationResult.model_construct(**_fields(result)),
    )
    assert all(not trace_validation_result_is_consistent(probe) for probe in probes)


def test_caller_created_finding_lookalike_cannot_forge_green_result() -> None:
    result = validate_r2_trace()
    lookalike = TraceFinding.model_construct(
        code=FindingCode.MISSING_APPROVAL_EVIDENCE,
        subject_identifier="approval_gate:r2-publication-v1",
        relationship=RelationshipKind.APPROVAL_EVIDENCE,
    )
    forged = result.model_copy(
        update={
            "findings": (lookalike,),
            "error_count": 0,
            "info_count": 0,
            "trace_complete": True,
        }
    )
    assert not trace_validation_result_is_consistent(forged)


def test_result_contains_no_raw_toml_or_run_metadata() -> None:
    serialized = validate_r2_trace().model_dump_json()
    for forbidden in (
        "schema_version",
        "component_checks",
        "repository_path",
        "timestamp",
        "duration",
        "hostname",
        "run_id",
        "PRIVATE",
    ):
        assert forbidden not in serialized
    assert '"severity":"warning"' not in serialized


def test_complete_and_incomplete_results_are_deterministic_in_process() -> None:
    complete = _synthetic_publication_trace(approved=True)
    incomplete = _synthetic_publication_trace(approved=False)
    complete_results = tuple(validate_trace(complete).model_dump_json() for _ in range(3))
    incomplete_results = tuple(validate_trace(incomplete).model_dump_json() for _ in range(3))
    assert len(set(complete_results)) == 1
    assert len(set(incomplete_results)) == 1


def test_malformed_semantic_result_is_deterministic_in_process() -> None:
    trace = _synthetic_publication_trace(approved=False)
    packet = _record(trace, WorkPacket)
    malformed = _replace_record(
        trace,
        WorkPacket(**_fields(packet, governed_by=("authority:synthetic-missing-v1",))),
    )
    first = validate_trace(malformed).model_dump_json()
    second = validate_trace(malformed).model_dump_json()
    assert first == second
    assert FindingCode.DANGLING_REFERENCE.value in first
    assert "synthetic-missing" not in first


@pytest.mark.parametrize("approved", (False, True))
def test_complete_and_incomplete_results_are_deterministic_across_four_processes(
    approved: bool,
) -> None:
    command = (
        "import runpy;"
        "from local_ai_guild.trace_validation import validate_trace;"
        "helper=runpy.run_path('tests/test_trace_validation.py')"
        "['_synthetic_publication_trace'];"
        f"print(validate_trace(helper(approved={approved!r})).model_dump_json())"
    )
    outputs = tuple(
        subprocess.run(
            [sys.executable, "-c", command],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        for _ in range(4)
    )
    assert len(set(outputs)) == 1
    assert "0x" not in outputs[0]
