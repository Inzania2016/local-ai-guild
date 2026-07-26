"""Bounded comparison for the synthetic O3 handoff experiment."""

from enum import StrEnum
from typing import Final

from pydantic import PrivateAttr, StrictInt, field_validator

from local_ai_guild.contracts import BoundaryModel
from local_ai_guild.trace_contracts import DurableIdentifier, TraceIdentifier
from local_ai_guild.trace_loading import load_o3_trace
from local_ai_guild.trace_validation import (
    FindingCode,
    RelationshipKind,
    TraceFinding,
    validate_trace,
)


class HandoffExperimentError(TypeError):
    """Bounded rejection of forged or corrupted O3 experiment output."""


class _BuilderAuthority(StrEnum):
    FINDING = "finding"
    RESULT = "result"


_FINDING_BUILDER_AUTHORITY: Final = _BuilderAuthority.FINDING
_RESULT_BUILDER_AUTHORITY: Final = _BuilderAuthority.RESULT


class HandoffFinding(BoundaryModel):
    """One bounded comparison key without a free-form finding message."""

    code: FindingCode
    subject_identifier: DurableIdentifier
    relationship: RelationshipKind | None
    _builder_authority: _BuilderAuthority | None = PrivateAttr(default=None)
    _bound_key: tuple[FindingCode, str, RelationshipKind | None] | None = PrivateAttr(default=None)

    def __init__(self, **data: object) -> None:
        authority = data.pop("_builder_authority", None)
        if authority is not _FINDING_BUILDER_AUTHORITY:
            raise HandoffExperimentError(
                "Handoff findings are created only by the O3 experiment evaluator"
            )
        super().__init__(**data)
        self._builder_authority = authority
        self._bound_key = (self.code, self.subject_identifier, self.relationship)


type FindingKey = tuple[FindingCode, str, RelationshipKind | None]


def _finding(key: FindingKey) -> HandoffFinding:
    return HandoffFinding(
        code=key[0],
        subject_identifier=key[1],
        relationship=key[2],
        _builder_authority=_FINDING_BUILDER_AUTHORITY,
    )


_MANUAL_O3_KEYS: Final[tuple[FindingKey, ...]] = (
    (
        FindingCode.DANGLING_REFERENCE,
        "next_action:council-contract-checkpoint-v1",
        RelationshipKind.BLOCKED_BY,
    ),
    (
        FindingCode.MISSING_APPROVAL_EVIDENCE,
        "approval_gate:synthetic-publication-v1",
        RelationshipKind.APPROVAL_EVIDENCE,
    ),
    (
        FindingCode.MISSING_AUTHORITY_EVIDENCE,
        "authority:synthetic-packet-owner-v1",
        RelationshipKind.AUTHORITY_EVIDENCE,
    ),
    (
        FindingCode.MISSING_REQUIRED_RELATIONSHIP,
        "artifact:synthetic-metadata-doc-v1",
        RelationshipKind.PUBLISHED_IN,
    ),
    (
        FindingCode.WRONG_TARGET_TYPE,
        "artifact:synthetic-metadata-doc-v1",
        RelationshipKind.VERIFIED_BY,
    ),
)

# This immutable tuple is a repository-authored experiment assertion, not external truth.
O3_MANUAL_REVIEW: Final = tuple(_finding(key) for key in _MANUAL_O3_KEYS)


def _key(value: HandoffFinding | TraceFinding) -> FindingKey:
    return (value.code, value.subject_identifier, value.relationship)


def _key_order(key: FindingKey) -> tuple[str, str, str]:
    relationship = key[2].value if key[2] is not None else ""
    return (key[0].value, key[1], relationship)


def _finding_is_consistent(value: object) -> bool:
    return (
        type(value) is HandoffFinding
        and type(getattr(value, "code", None)) is FindingCode
        and type(getattr(value, "subject_identifier", None)) is str
        and (
            getattr(value, "relationship", None) is None
            or type(value.relationship) is RelationshipKind
        )
        and getattr(value, "_builder_authority", None) is _FINDING_BUILDER_AUTHORITY
        and getattr(value, "_bound_key", None) == _key(value)
    )


class HandoffComparisonResult(BoundaryModel):
    """Evaluator-built partition of manual and deterministic O3 findings."""

    trace_identifier: TraceIdentifier
    subject_record_identifier: DurableIdentifier
    manual_finding_count: StrictInt
    validator_finding_count: StrictInt
    matched_findings: tuple[HandoffFinding, ...]
    manual_only_findings: tuple[HandoffFinding, ...]
    validator_only_findings: tuple[HandoffFinding, ...]
    _builder_authority: _BuilderAuthority | None = PrivateAttr(default=None)
    _bound_trace_identifier: str | None = PrivateAttr(default=None)
    _bound_subject_identifier: str | None = PrivateAttr(default=None)
    _bound_partitions: tuple[tuple[FindingKey, ...], ...] = PrivateAttr(default=())

    def __init__(self, **data: object) -> None:
        authority = data.pop("_builder_authority", None)
        if authority is not _RESULT_BUILDER_AUTHORITY:
            raise HandoffExperimentError(
                "Handoff comparison results are created only by the O3 experiment evaluator"
            )
        super().__init__(**data)
        self._builder_authority = authority
        self._bound_trace_identifier = self.trace_identifier
        self._bound_subject_identifier = self.subject_record_identifier
        self._bound_partitions = _partitions(self)
        if not handoff_comparison_result_is_consistent(self):
            raise HandoffExperimentError("The O3 handoff comparison result is inconsistent")

    @field_validator(
        "matched_findings",
        "manual_only_findings",
        "validator_only_findings",
        mode="before",
    )
    @classmethod
    def findings_must_be_exact_instances(cls, value: object) -> object:
        if type(value) is not tuple or any(type(item) is not HandoffFinding for item in value):
            raise ValueError("comparison findings must be exact typed instances")
        return value


def _partitions(value: HandoffComparisonResult) -> tuple[tuple[FindingKey, ...], ...]:
    return tuple(
        tuple(_key(finding) for finding in findings)
        for findings in (
            value.matched_findings,
            value.manual_only_findings,
            value.validator_only_findings,
        )
    )


def handoff_comparison_result_is_consistent(value: object) -> bool:
    """Recheck counts, ordering, partitions, and private evaluator bindings."""
    if type(value) is not HandoffComparisonResult:
        return False
    collections = (
        getattr(value, "matched_findings", None),
        getattr(value, "manual_only_findings", None),
        getattr(value, "validator_only_findings", None),
    )
    if any(
        type(collection) is not tuple
        or any(not _finding_is_consistent(finding) for finding in collection)
        for collection in collections
    ):
        return False
    partitions = tuple(tuple(_key(finding) for finding in collection) for collection in collections)
    flattened = tuple(key for partition in partitions for key in partition)
    matched, manual_only, validator_only = (set(partition) for partition in partitions)
    return (
        type(getattr(value, "manual_finding_count", None)) is int
        and type(getattr(value, "validator_finding_count", None)) is int
        and value.manual_finding_count == len(matched | manual_only)
        and value.validator_finding_count == len(matched | validator_only)
        and not (matched & manual_only or matched & validator_only or manual_only & validator_only)
        and len(flattened) == len(set(flattened))
        and all(tuple(sorted(partition, key=_key_order)) == partition for partition in partitions)
        and getattr(value, "_builder_authority", None) is _RESULT_BUILDER_AUTHORITY
        and getattr(value, "_bound_trace_identifier", None) == value.trace_identifier
        and getattr(value, "_bound_subject_identifier", None) == value.subject_record_identifier
        and getattr(value, "_bound_partitions", None) == partitions
    )


def run_o3_handoff_experiment() -> HandoffComparisonResult:
    """Compare the fixed manual assertion with deterministic O2 trace findings."""
    trace = load_o3_trace()
    validation = validate_trace(trace)
    manual_keys = set(_MANUAL_O3_KEYS)
    validator_keys = {_key(finding) for finding in validation.findings}

    def build(keys: set[FindingKey]) -> tuple[HandoffFinding, ...]:
        return tuple(_finding(key) for key in sorted(keys, key=_key_order))

    return HandoffComparisonResult(
        trace_identifier=trace.trace_identifier,
        subject_record_identifier=trace.subject_record_identifier,
        manual_finding_count=len(manual_keys),
        validator_finding_count=len(validator_keys),
        matched_findings=build(manual_keys & validator_keys),
        manual_only_findings=build(manual_keys - validator_keys),
        validator_only_findings=build(validator_keys - manual_keys),
        _builder_authority=_RESULT_BUILDER_AUTHORITY,
    )
