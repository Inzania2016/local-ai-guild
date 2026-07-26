"""Focused tests for the bounded synthetic O3 handoff experiment."""

import inspect
import io
import subprocess
import sys
from types import MappingProxyType

import pytest
from pydantic import ValidationError

import local_ai_guild.o3_experiment as o3_experiment
import local_ai_guild.trace_loading as trace_loading
import local_ai_guild.trace_validation as trace_validation
from local_ai_guild.o3_experiment import (
    O3_MANUAL_REVIEW,
    HandoffComparisonResult,
    HandoffExperimentError,
    HandoffFinding,
    handoff_comparison_result_is_consistent,
    run_o3_handoff_experiment,
)
from local_ai_guild.trace_contracts import TraceDocument, trace_document_is_consistent
from local_ai_guild.trace_loading import TraceLoadError, load_o3_trace, load_r2_trace
from local_ai_guild.trace_validation import (
    FINDING_MESSAGES,
    FindingCode,
    RelationshipKind,
    validate_trace,
)


def _fields(model: object, **changes: object) -> dict[str, object]:
    values = {name: getattr(model, name) for name in type(model).model_fields}
    values.update(changes)
    return values


def _keys(findings: object) -> tuple[tuple[FindingCode, str, RelationshipKind | None], ...]:
    assert type(findings) is tuple
    return tuple(
        (finding.code, finding.subject_identifier, finding.relationship) for finding in findings
    )


class _BinaryPath:
    def __init__(self, content: bytes) -> None:
        self._content = content

    def open(self, mode: str) -> io.BytesIO:
        return io.BytesIO(self._content)


def test_fixed_o3_loader_accepts_no_arguments_and_does_not_add_generic_loader() -> None:
    assert tuple(inspect.signature(load_o3_trace).parameters) == ()
    with pytest.raises(TypeError):
        load_o3_trace("PRIVATE-MARKER")  # type: ignore[call-arg]
    assert not hasattr(trace_loading, "load_trace")


def test_o3_trace_is_exact_contract_valid_and_o2_loader_is_unchanged() -> None:
    o3_trace = load_o3_trace()
    r2_trace = load_r2_trace()
    assert type(o3_trace) is TraceDocument
    assert trace_document_is_consistent(o3_trace)
    assert o3_trace.trace_identifier == "trace:o3-synthetic-handoff-v1"
    assert o3_trace.subject_record_identifier == "work_packet:synthetic-metadata-v1"
    assert len(o3_trace.records) == 10
    assert r2_trace.trace_identifier == "trace:r2-closeout-v1"


def test_planted_defects_are_semantic_findings_not_parser_failures() -> None:
    result = validate_trace(load_o3_trace())
    error_keys = {
        (finding.code, finding.subject_identifier, finding.relationship)
        for finding in result.findings
        if finding.severity.value == "error"
    }
    assert result.error_count == 4
    assert error_keys == {
        (
            FindingCode.MISSING_AUTHORITY_EVIDENCE,
            "authority:synthetic-packet-owner-v1",
            RelationshipKind.AUTHORITY_EVIDENCE,
        ),
        (
            FindingCode.MISSING_APPROVAL_EVIDENCE,
            "approval_gate:synthetic-publication-v1",
            RelationshipKind.APPROVAL_EVIDENCE,
        ),
        (
            FindingCode.DANGLING_REFERENCE,
            "next_action:council-contract-checkpoint-v1",
            RelationshipKind.BLOCKED_BY,
        ),
        (
            FindingCode.WRONG_TARGET_TYPE,
            "artifact:synthetic-metadata-doc-v1",
            RelationshipKind.VERIFIED_BY,
        ),
    }


def test_manual_review_is_immutable_bounded_and_repository_authored() -> None:
    assert type(O3_MANUAL_REVIEW) is tuple
    assert len(O3_MANUAL_REVIEW) == 5
    assert all(type(finding) is HandoffFinding for finding in O3_MANUAL_REVIEW)
    assert all(finding.code in FindingCode for finding in O3_MANUAL_REVIEW)
    assert all(finding.relationship in RelationshipKind for finding in O3_MANUAL_REVIEW)
    with pytest.raises(ValidationError):
        O3_MANUAL_REVIEW[0].subject_identifier = "artifact:changed-v1"
    with pytest.raises(HandoffExperimentError):
        HandoffFinding(
            code=FindingCode.DANGLING_REFERENCE,
            subject_identifier="artifact:caller-created-v1",
            relationship=RelationshipKind.VERIFIED_BY,
        )


def test_comparison_preserves_matched_manual_only_and_validator_only_findings() -> None:
    result = run_o3_handoff_experiment()
    assert result.manual_finding_count == 5
    assert result.validator_finding_count == 7
    assert len(result.matched_findings) == 4
    assert _keys(result.manual_only_findings) == (
        (
            FindingCode.MISSING_REQUIRED_RELATIONSHIP,
            "artifact:synthetic-metadata-doc-v1",
            RelationshipKind.PUBLISHED_IN,
        ),
    )
    assert _keys(result.validator_only_findings) == (
        (
            FindingCode.COMMIT_DOES_NOT_PROVE_AUTHORIZATION,
            "commit:synthetic-publication-v1",
            RelationshipKind.AUTHORIZATION_CLAIM,
        ),
        (
            FindingCode.COMMIT_DOES_NOT_PROVE_CORRECTNESS,
            "commit:synthetic-publication-v1",
            RelationshipKind.CORRECTNESS_CLAIM,
        ),
        (
            FindingCode.REPOSITORY_ASSERTION_NOT_EXTERNAL_TRUTH,
            "work_packet:synthetic-metadata-v1",
            RelationshipKind.ASSERTION_SCOPE,
        ),
    )


def test_comparison_order_is_deterministic_and_does_not_use_messages() -> None:
    result = run_o3_handoff_experiment()
    for collection in (
        result.matched_findings,
        result.manual_only_findings,
        result.validator_only_findings,
    ):
        keys = _keys(collection)
        assert keys == tuple(
            sorted(
                keys,
                key=lambda key: (
                    key[0].value,
                    key[1],
                    key[2].value if key[2] is not None else "",
                ),
            )
        )
    serialized = result.model_dump_json()
    assert all(message not in serialized for message in FINDING_MESSAGES.values())


def test_validator_behavior_is_not_hardcoded_to_o3_trace_identifier() -> None:
    trace = load_o3_trace()
    differently_identified = TraceDocument(
        **_fields(trace, trace_identifier="trace:different-synthetic-handoff-v1")
    )
    original = validate_trace(trace)
    changed = validate_trace(differently_identified)
    assert changed.trace_identifier == "trace:different-synthetic-handoff-v1"
    assert _keys(changed.findings) == _keys(original.findings)
    validator_source = inspect.getsource(trace_validation)
    assert "o3-synthetic-handoff" not in validator_source
    assert "synthetic-metadata" not in validator_source


def test_result_direct_construction_is_rejected() -> None:
    result = run_o3_handoff_experiment()
    with pytest.raises(HandoffExperimentError):
        HandoffComparisonResult(**_fields(result))


def test_result_corruption_relabeling_removal_counts_and_order_are_rejected() -> None:
    result = run_o3_handoff_experiment()
    probes = (
        result.model_copy(update={"trace_identifier": "trace:relabeled-v1"}),
        result.model_copy(update={"subject_record_identifier": "work_packet:relabeled-v1"}),
        result.model_copy(update={"matched_findings": result.matched_findings[:-1]}),
        result.model_copy(update={"manual_finding_count": 999}),
        result.model_copy(update={"validator_finding_count": 999}),
        result.model_copy(update={"matched_findings": tuple(reversed(result.matched_findings))}),
        HandoffComparisonResult.model_construct(**_fields(result)),
    )
    assert all(not handoff_comparison_result_is_consistent(probe) for probe in probes)


def test_caller_created_finding_lookalike_cannot_forge_a_result() -> None:
    result = run_o3_handoff_experiment()
    original = result.matched_findings[0]
    lookalike = HandoffFinding.model_construct(
        code=original.code,
        subject_identifier=original.subject_identifier,
        relationship=original.relationship,
    )
    forged = result.model_copy(
        update={"matched_findings": (lookalike, *result.matched_findings[1:])}
    )
    assert not handoff_comparison_result_is_consistent(forged)


def test_reassigned_public_manual_review_cannot_change_official_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = run_o3_handoff_experiment().model_dump_json()
    lookalike = HandoffFinding.model_construct(
        code=FindingCode.SELF_REFERENCE,
        subject_identifier="artifact:caller-created-v1",
        relationship=RelationshipKind.IMPLEMENTS,
    )
    monkeypatch.setattr(o3_experiment, "O3_MANUAL_REVIEW", (lookalike,))
    assert run_o3_handoff_experiment().model_dump_json() == original


def test_same_process_serialization_is_deterministic_and_bounded() -> None:
    outputs = tuple(run_o3_handoff_experiment().model_dump_json() for _ in range(3))
    assert len(set(outputs)) == 1
    for forbidden in (
        "repository_path",
        "docs/traces",
        "parser",
        "TOML",
        "PRIVATE",
        "timestamp",
        "hostname",
    ):
        assert forbidden not in outputs[0]


def test_two_separate_process_serializations_are_identical() -> None:
    command = (
        "from local_ai_guild.o3_experiment import run_o3_handoff_experiment;"
        "print(run_o3_handoff_experiment().model_dump_json())"
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


@pytest.mark.parametrize(
    "content",
    (
        b'PRIVATE_MARKER = "PRIVATE-VALUE"\ninvalid = [',
        b"""
schema_version = "0.1"
trace_identifier = "trace:private-marker-v1"
subject_record_identifier = "work_packet:private-marker-v1"
PRIVATE_MARKER = "PRIVATE-VALUE"
records = []
""",
    ),
)
def test_o3_loader_rejects_markers_without_retaining_source(
    monkeypatch: pytest.MonkeyPatch,
    content: bytes,
) -> None:
    monkeypatch.setattr(trace_loading, "_O3_TRACE_PATH", _BinaryPath(content))
    with pytest.raises(TraceLoadError) as captured:
        load_o3_trace()
    assert "PRIVATE" not in str(captured.value)
    assert "MARKER" not in str(captured.value)


def test_comparison_contract_uses_strict_frozen_extra_forbid_models() -> None:
    result = run_o3_handoff_experiment()
    assert result.model_config["strict"] is True
    assert result.model_config["frozen"] is True
    assert result.model_config["extra"] == "forbid"
    assert type(FINDING_MESSAGES) is MappingProxyType
