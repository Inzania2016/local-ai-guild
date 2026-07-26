"""Fixed TOML loaders for repository-owned evidence traces."""

import tomllib
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from pydantic import ValidationError

from local_ai_guild.trace_contracts import (
    ApprovalEvidenceStatus,
    ApprovalGate,
    ApprovalGateKind,
    ApprovalStatus,
    ArtifactKind,
    AuthorityEvidenceStatus,
    AuthorityKind,
    AuthoritySource,
    AutomatedVerificationStatus,
    Commit,
    Constraint,
    ConstraintKind,
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
    RealizationStatus,
    TraceDocument,
    TraceRecord,
    VerificationComponent,
    VerificationMethod,
    VerificationOutcome,
    VerificationResult,
    WorkPacket,
)

_R2_TRACE_PATH: Final = Path(__file__).resolve().parents[2] / "docs" / "traces" / "r2-closeout.toml"
_O3_TRACE_PATH: Final = (
    Path(__file__).resolve().parents[2] / "docs" / "traces" / "o3-synthetic-handoff.toml"
)


class TraceLoadErrorCode(StrEnum):
    """Bounded fixed-loader error categories."""

    MISSING = "fixed_trace_missing"
    UNREADABLE = "fixed_trace_unreadable"
    INVALID_TOML = "invalid_toml"
    INVALID_CONTRACT = "invalid_trace_contract"


_TRACE_LOAD_MESSAGES: Final = MappingProxyType(
    {
        TraceLoadErrorCode.MISSING: "The fixed R2 trace file is missing",
        TraceLoadErrorCode.UNREADABLE: "The fixed R2 trace file is unreadable",
        TraceLoadErrorCode.INVALID_TOML: "The fixed R2 trace contains invalid TOML",
        TraceLoadErrorCode.INVALID_CONTRACT: "The fixed R2 trace contract is invalid",
    }
)


class TraceLoadError(ValueError):
    """A bounded failure that never includes source text or machine paths."""

    def __init__(self, code: TraceLoadErrorCode) -> None:
        self.code = code
        super().__init__(_TRACE_LOAD_MESSAGES[code])


def _mapping(value: object, expected_keys: set[str]) -> dict[str, object]:
    if type(value) is not dict or set(value) != expected_keys:
        raise ValueError
    return value


def _mapping_with_optional(
    value: object, required_keys: set[str], optional_keys: set[str]
) -> dict[str, object]:
    if type(value) is not dict:
        raise ValueError
    keys = set(value)
    if not required_keys <= keys or not keys <= required_keys | optional_keys:
        raise ValueError
    return value


def _string(value: object) -> str:
    if type(value) is not str:
        raise ValueError
    return value


def _boolean(value: object) -> bool:
    if type(value) is not bool:
        raise ValueError
    return value


def _integer(value: object) -> int:
    if type(value) is not int:
        raise ValueError
    return value


def _enum(enum_type: type[StrEnum], value: object) -> StrEnum:
    return enum_type(_string(value))


def _strings(value: object) -> tuple[str, ...]:
    if type(value) is not list or any(type(item) is not str for item in value):
        raise ValueError
    return tuple(value)


def _enum_tuple(enum_type: type[StrEnum], value: object) -> tuple[StrEnum, ...]:
    if type(value) is not list:
        raise ValueError
    return tuple(_enum(enum_type, item) for item in value)


def _evidence(value: object) -> EvidenceLocator:
    data = _mapping(
        value,
        {"kind", "locator", "scope", "epistemic_status", "provenance"},
    )
    return EvidenceLocator(
        kind=_enum(EvidenceKind, data["kind"]),
        locator=_string(data["locator"]),
        scope=_string(data["scope"]),
        epistemic_status=_enum(EpistemicStatus, data["epistemic_status"]),
        provenance=_enum(EvidenceProvenance, data["provenance"]),
    )


def _evidence_tuple(value: object) -> tuple[EvidenceLocator, ...]:
    if type(value) is not list:
        raise ValueError
    return tuple(_evidence(item) for item in value)


def _requirement(value: object) -> EmbeddedRequirement:
    data = _mapping(value, {"identifier", "statement", "required", "evidence"})
    return EmbeddedRequirement(
        identifier=_string(data["identifier"]),
        statement=_string(data["statement"]),
        required=_boolean(data["required"]),
        evidence=_evidence_tuple(data["evidence"]),
    )


def _requirements(value: object) -> tuple[EmbeddedRequirement, ...]:
    if type(value) is not list:
        raise ValueError
    return tuple(_requirement(item) for item in value)


def _common(data: dict[str, object]) -> dict[str, object]:
    return {
        "identifier": _string(data["identifier"]),
        "title": _string(data["title"]),
        "evidence": _evidence_tuple(data["evidence"]),
    }


def _goal(value: object) -> Goal:
    data = _mapping_with_optional(
        value,
        {"record_type", "identifier", "title", "evidence"},
        {"description"},
    )
    values = _common(data)
    if "description" in data:
        values["description"] = _string(data["description"])
    return Goal(record_type=_string(data["record_type"]), **values)


def _work_packet(value: object) -> WorkPacket:
    data = _mapping(
        value,
        {
            "record_type",
            "identifier",
            "title",
            "requirements",
            "governed_by",
            "constrained_by",
            "advances_goal",
            "realization_status",
            "automated_verification_status",
            "human_verification_status",
            "approval_status",
            "approval_evidence_status",
            "evidence",
        },
    )
    return WorkPacket(
        record_type=_string(data["record_type"]),
        requirements=_requirements(data["requirements"]),
        governed_by=_strings(data["governed_by"]),
        constrained_by=_strings(data["constrained_by"]),
        advances_goal=_strings(data["advances_goal"]),
        realization_status=_enum(RealizationStatus, data["realization_status"]),
        automated_verification_status=_enum(
            AutomatedVerificationStatus, data["automated_verification_status"]
        ),
        human_verification_status=_enum(HumanVerificationStatus, data["human_verification_status"]),
        approval_status=_enum(ApprovalStatus, data["approval_status"]),
        approval_evidence_status=_enum(ApprovalEvidenceStatus, data["approval_evidence_status"]),
        **_common(data),
    )


def _authority_source(value: object) -> AuthoritySource:
    data = _mapping(
        value,
        {
            "record_type",
            "identifier",
            "title",
            "authority_kind",
            "scope",
            "precedence",
            "evidence_status",
            "evidence",
        },
    )
    return AuthoritySource(
        record_type=_string(data["record_type"]),
        authority_kind=_enum(AuthorityKind, data["authority_kind"]),
        scope=_string(data["scope"]),
        precedence=_integer(data["precedence"]),
        evidence_status=_enum(AuthorityEvidenceStatus, data["evidence_status"]),
        **_common(data),
    )


def _constraint(value: object) -> Constraint:
    data = _mapping(
        value,
        {"record_type", "identifier", "title", "constraint_kind", "evidence"},
    )
    return Constraint(
        record_type=_string(data["record_type"]),
        constraint_kind=_enum(ConstraintKind, data["constraint_kind"]),
        **_common(data),
    )


def _decision(value: object) -> Decision:
    data = _mapping(
        value,
        {
            "record_type",
            "identifier",
            "title",
            "selected_by",
            "implemented_by",
            "evidence",
        },
    )
    return Decision(
        record_type=_string(data["record_type"]),
        selected_by=_string(data["selected_by"]),
        implemented_by=_strings(data["implemented_by"]),
        **_common(data),
    )


def _artifact(value: object) -> ImplementationArtifact:
    data = _mapping(
        value,
        {
            "record_type",
            "identifier",
            "title",
            "artifact_kind",
            "repository_path",
            "implements",
            "verified_by",
            "published_in",
            "evidence",
        },
    )
    return ImplementationArtifact(
        record_type=_string(data["record_type"]),
        artifact_kind=_enum(ArtifactKind, data["artifact_kind"]),
        repository_path=_string(data["repository_path"]),
        implements=_strings(data["implements"]),
        verified_by=_strings(data["verified_by"]),
        published_in=_strings(data["published_in"]),
        **_common(data),
    )


def _verification(value: object) -> VerificationResult:
    data = _mapping(
        value,
        {
            "record_type",
            "identifier",
            "title",
            "method",
            "result",
            "verifies",
            "automated_verification_status",
            "human_verification_status",
            "limitations",
            "component_checks",
            "evidence",
        },
    )
    return VerificationResult(
        record_type=_string(data["record_type"]),
        method=_enum(VerificationMethod, data["method"]),
        result=_enum(VerificationOutcome, data["result"]),
        verifies=_strings(data["verifies"]),
        automated_verification_status=_enum(
            AutomatedVerificationStatus, data["automated_verification_status"]
        ),
        human_verification_status=_enum(HumanVerificationStatus, data["human_verification_status"]),
        limitations=_strings(data["limitations"]),
        component_checks=_enum_tuple(VerificationComponent, data["component_checks"]),
        **_common(data),
    )


def _approval_gate(value: object) -> ApprovalGate:
    data = _mapping(
        value,
        {
            "record_type",
            "identifier",
            "title",
            "gate_kind",
            "required_authority",
            "approval_status",
            "approval_evidence_status",
            "evidence",
        },
    )
    return ApprovalGate(
        record_type=_string(data["record_type"]),
        gate_kind=_enum(ApprovalGateKind, data["gate_kind"]),
        required_authority=_string(data["required_authority"]),
        approval_status=_enum(ApprovalStatus, data["approval_status"]),
        approval_evidence_status=_enum(ApprovalEvidenceStatus, data["approval_evidence_status"]),
        **_common(data),
    )


def _commit(value: object) -> Commit:
    data = _mapping(
        value,
        {
            "record_type",
            "identifier",
            "title",
            "sha",
            "publishes",
            "authorized_by_gate",
            "realization_status",
            "evidence",
        },
    )
    return Commit(
        record_type=_string(data["record_type"]),
        sha=_string(data["sha"]),
        publishes=_strings(data["publishes"]),
        authorized_by_gate=_string(data["authorized_by_gate"]),
        realization_status=_enum(RealizationStatus, data["realization_status"]),
        **_common(data),
    )


def _next_action(value: object) -> NextAction:
    data = _mapping(
        value,
        {
            "record_type",
            "identifier",
            "title",
            "enabled_by",
            "blocked_by",
            "evidence",
        },
    )
    return NextAction(
        record_type=_string(data["record_type"]),
        enabled_by=_strings(data["enabled_by"]),
        blocked_by=_strings(data["blocked_by"]),
        **_common(data),
    )


_RECORD_LOADERS: Final = MappingProxyType(
    {
        "goal": _goal,
        "work_packet": _work_packet,
        "authority_source": _authority_source,
        "constraint": _constraint,
        "decision": _decision,
        "implementation_artifact": _artifact,
        "verification_result": _verification,
        "approval_gate": _approval_gate,
        "commit": _commit,
        "next_action": _next_action,
    }
)


def _record(value: object) -> TraceRecord:
    if type(value) is not dict or type(value.get("record_type")) is not str:
        raise ValueError
    loader = _RECORD_LOADERS.get(value["record_type"])
    if loader is None:
        raise ValueError
    return loader(value)


def _trace_document(value: object) -> TraceDocument:
    data = _mapping(
        value,
        {"schema_version", "trace_identifier", "subject_record_identifier", "records"},
    )
    records = data["records"]
    if type(records) is not list:
        raise ValueError
    return TraceDocument(
        schema_version=_string(data["schema_version"]),
        trace_identifier=_string(data["trace_identifier"]),
        subject_record_identifier=_string(data["subject_record_identifier"]),
        records=tuple(_record(record) for record in records),
    )


def _load_fixed_trace(trace_path: Path) -> TraceDocument:
    try:
        with trace_path.open("rb") as source:
            parsed = tomllib.load(source)
    except FileNotFoundError:
        raise TraceLoadError(TraceLoadErrorCode.MISSING) from None
    except PermissionError:
        raise TraceLoadError(TraceLoadErrorCode.UNREADABLE) from None
    except tomllib.TOMLDecodeError:
        raise TraceLoadError(TraceLoadErrorCode.INVALID_TOML) from None
    except UnicodeDecodeError:
        raise TraceLoadError(TraceLoadErrorCode.INVALID_TOML) from None
    except OSError:
        raise TraceLoadError(TraceLoadErrorCode.UNREADABLE) from None

    try:
        return _trace_document(parsed)
    except (KeyError, TypeError, ValueError, ValidationError):
        raise TraceLoadError(TraceLoadErrorCode.INVALID_CONTRACT) from None


def load_r2_trace() -> TraceDocument:
    """Load only the fixed repository-owned R2 trace through the TOML boundary."""
    return _load_fixed_trace(_R2_TRACE_PATH)


def load_o3_trace() -> TraceDocument:
    """Load only the fixed repository-owned synthetic O3 trace."""
    return _load_fixed_trace(_O3_TRACE_PATH)
