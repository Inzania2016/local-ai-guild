"""Focused fixed-loader and redaction tests for O2."""

import inspect
import io
import subprocess
import sys
from pathlib import Path

import pytest

import local_ai_guild.trace_loading as trace_loading
from local_ai_guild.trace_contracts import TraceDocument
from local_ai_guild.trace_loading import (
    TraceLoadError,
    TraceLoadErrorCode,
    load_r2_trace,
)
from local_ai_guild.trace_validation import validate_r2_trace

_OFFICIAL_TRACE_PATH = Path(__file__).resolve().parents[1] / "docs" / "traces" / "r2-closeout.toml"


def _official_trace_bytes() -> bytes:
    return _OFFICIAL_TRACE_PATH.read_bytes()


def _replace_once(source: bytes, original: bytes, replacement: bytes) -> bytes:
    assert source.count(original) == 1
    return source.replace(original, replacement, 1)


def _assert_invalid_contract(
    monkeypatch: pytest.MonkeyPatch,
    content: bytes,
) -> None:
    monkeypatch.setattr(trace_loading, "_R2_TRACE_PATH", _BinaryPath(content))
    with pytest.raises(TraceLoadError) as captured:
        load_r2_trace()
    assert captured.value.code is TraceLoadErrorCode.INVALID_CONTRACT
    serialized_error = str(captured.value)
    assert "PRIVATE" not in serialized_error
    assert "MARKER" not in serialized_error


def test_fixed_loader_has_no_caller_path_parameter() -> None:
    assert tuple(inspect.signature(load_r2_trace).parameters) == ()
    with pytest.raises(TypeError):
        load_r2_trace("MARKER")  # type: ignore[call-arg]


def test_fixed_loader_returns_one_exact_trace_with_stable_order() -> None:
    first = load_r2_trace()
    second = load_r2_trace()
    assert type(first) is TraceDocument
    assert tuple(record.identifier for record in first.records) == tuple(
        record.identifier for record in second.records
    )
    assert len(first.records) == 30
    assert len({record.identifier for record in first.records}) == 30


def test_loader_uses_standard_library_tomllib() -> None:
    source = inspect.getsource(trace_loading)
    assert "import tomllib" in source
    assert "yaml" not in source.lower()


class _MissingPath:
    def open(self, mode: str) -> object:
        raise FileNotFoundError("PRIVATE-MARKER")


class _BinaryPath:
    def __init__(self, content: bytes) -> None:
        self._content = content

    def open(self, mode: str) -> io.BytesIO:
        return io.BytesIO(self._content)


def test_missing_fixed_trace_error_is_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(trace_loading, "_R2_TRACE_PATH", _MissingPath())
    with pytest.raises(TraceLoadError) as captured:
        load_r2_trace()
    assert captured.value.code is TraceLoadErrorCode.MISSING
    assert "PRIVATE-MARKER" not in str(captured.value)


class _UnreadablePath:
    def open(self, mode: str) -> object:
        raise PermissionError("PRIVATE-MARKER")


def test_unreadable_fixed_trace_error_is_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(trace_loading, "_R2_TRACE_PATH", _UnreadablePath())
    with pytest.raises(TraceLoadError) as captured:
        load_r2_trace()
    assert captured.value.code is TraceLoadErrorCode.UNREADABLE
    assert "PRIVATE-MARKER" not in str(captured.value)


def test_invalid_toml_error_does_not_leak_source(monkeypatch: pytest.MonkeyPatch) -> None:
    invalid = _BinaryPath(b'PRIVATE_KEY = "PRIVATE-MARKER"\ninvalid = [')
    monkeypatch.setattr(trace_loading, "_R2_TRACE_PATH", invalid)
    with pytest.raises(TraceLoadError) as captured:
        load_r2_trace()
    assert captured.value.code is TraceLoadErrorCode.INVALID_TOML
    assert "PRIVATE" not in str(captured.value)
    assert "[" not in str(captured.value)


def test_invalid_contract_error_does_not_leak_keys_or_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    invalid = _BinaryPath(
        "\n".join(
            (
                'schema_version = "0.1"',
                'trace_identifier = "trace:private-marker-v1"',
                'subject_record_identifier = "work_packet:r2-v1"',
                'PRIVATE_MARKER = "PRIVATE-MARKER"',
                "records = []",
            )
        ).encode()
    )
    monkeypatch.setattr(trace_loading, "_R2_TRACE_PATH", invalid)
    with pytest.raises(TraceLoadError) as captured:
        load_r2_trace()
    assert captured.value.code is TraceLoadErrorCode.INVALID_CONTRACT
    assert "PRIVATE" not in str(captured.value)
    assert "trace_identifier" not in str(captured.value)


@pytest.mark.parametrize(
    ("original", "replacement"),
    (
        (
            b'schema_version = "0.1"',
            b"schema_version = 2026-07-26T12:30:00Z",
        ),
        (b'schema_version = "0.1"', b"schema_version = 2026-07-26"),
        (b'schema_version = "0.1"', b"schema_version = 12:30:00"),
        (
            b'scope = "R2 typed evidence and deterministic policy implementation"\nprecedence = 1',
            b'scope = "R2 typed evidence and deterministic policy implementation"\n'
            b"precedence = 1.5",
        ),
        (
            b'scope = "R2 typed evidence and deterministic policy implementation"\nprecedence = 1',
            b'scope = "R2 typed evidence and deterministic policy implementation"\n'
            b"precedence = true",
        ),
        (
            b'scope = "R2 typed evidence and deterministic policy implementation"\nprecedence = 1',
            b'scope = "R2 typed evidence and deterministic policy implementation"\n'
            b"precedence = 999999999999999999999999999999999999",
        ),
        (
            b"blocked_by = []",
            b'blocked_by = ["constraint:no-execution-r2-v1", 1]',
        ),
        (
            b'record_type = "goal"',
            b'record_type = "goal"\nPRIVATE_FIELD = "PRIVATE-MARKER"',
        ),
        (b'record_type = "goal"', b'record_type = "PRIVATE-MARKER"'),
        (
            b'title = "Typed evidence and policy before any future execution boundary"',
            b'title = "PRIVATE-MARKER\\u0001"',
        ),
    ),
    ids=(
        "datetime",
        "date",
        "time",
        "float",
        "boolean-in-integer",
        "very-large-integer",
        "mixed-array",
        "unknown-field",
        "wrong-discriminator",
        "unicode-control",
    ),
)
def test_parseable_toml_values_outside_the_contract_are_rejected(
    monkeypatch: pytest.MonkeyPatch,
    original: bytes,
    replacement: bytes,
) -> None:
    content = _replace_once(_official_trace_bytes(), original, replacement)
    _assert_invalid_contract(monkeypatch, content)


def test_nested_unexpected_table_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    content = _official_trace_bytes() + b'\n[PRIVATE_TABLE]\nvalue = "PRIVATE-MARKER"\n'
    _assert_invalid_contract(monkeypatch, content)


def test_duplicate_semantic_record_from_array_of_tables_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    duplicate_goal = (
        b"\n[[records]]\n"
        b'record_type = "goal"\n'
        b'identifier = "goal:evidence-before-execution-v1"\n'
        b'title = "PRIVATE-MARKER"\n'
        b"evidence = [\n"
        b'  { kind = "repository_source", locator = "README.md:1-2", scope = "Duplicate", '
        b'epistemic_status = "retrieved_fact", provenance = "repository_document" },\n'
        b"]\n"
    )
    _assert_invalid_contract(monkeypatch, _official_trace_bytes() + duplicate_goal)


def test_empty_required_array_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    content = b"""
schema_version = "0.1"
trace_identifier = "trace:synthetic-empty-v1"
subject_record_identifier = "work_packet:synthetic-empty-v1"
records = []
"""
    _assert_invalid_contract(monkeypatch, content)


def test_repeated_in_process_result_serialization_is_identical() -> None:
    first = validate_r2_trace().model_dump_json()
    second = validate_r2_trace().model_dump_json()
    assert first == second


def test_separate_process_result_serialization_is_identical() -> None:
    command = (
        "from local_ai_guild.trace_validation import validate_r2_trace;"
        "print(validate_r2_trace().model_dump_json())"
    )
    first = subprocess.run(
        [sys.executable, "-c", command],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    second = subprocess.run(
        [sys.executable, "-c", command],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert first == second
    assert "0x" not in first
    assert "PRIVATE" not in first
