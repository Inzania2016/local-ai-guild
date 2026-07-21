"""Boundary tests for strict R1 proposal and decision contracts."""

import json

import pytest
from pydantic import ValidationError

from local_ai_guild.contracts import (
    BoundaryModel,
    ProjectStatusArguments,
    ProjectStatusProposal,
    ReadPublicDocArguments,
    RefusalReason,
    RefusedRoutingDecision,
    SearchPublicDocsArguments,
    SuccessfulRoutingDecision,
)
from local_ai_guild.validation import (
    tool_proposal_json_schema,
    validate_tool_proposal,
    validation_issues,
)


def test_boundary_models_inherit_strict_forbid_and_frozen_configuration() -> None:
    for model in BoundaryModel.__subclasses__():
        assert model.model_config["strict"] is True
        assert model.model_config["extra"] == "forbid"
        assert model.model_config["frozen"] is True


def test_fixed_contract_serialization_is_deterministic() -> None:
    decision = SuccessfulRoutingDecision(
        proposal=ProjectStatusProposal(arguments=ProjectStatusArguments()),
        evidence_references=("rule:project-status-v1",),
    )

    serialized = decision.model_dump_json()
    assert serialized == (
        '{"outcome":"routed","proposal":{"tool":"project_status","arguments":{}},'
        '"evidence_references":["rule:project-status-v1"]}'
    )
    assert json.loads(serialized) == {
        "outcome": "routed",
        "proposal": {"tool": "project_status", "arguments": {}},
        "evidence_references": ["rule:project-status-v1"],
    }


def test_proposal_json_schema_can_be_generated() -> None:
    schema = tool_proposal_json_schema()

    assert schema["discriminator"]["propertyName"] == "tool"
    assert "oneOf" in schema


@pytest.mark.parametrize("max_results", [0, 11])
def test_search_result_bounds_are_strict(max_results: int) -> None:
    with pytest.raises(ValidationError):
        SearchPublicDocsArguments(query="routing", max_results=max_results)


@pytest.mark.parametrize("max_results", ["5", 5.0, True, False])
def test_search_result_count_rejects_coercion(max_results: object) -> None:
    with pytest.raises(ValidationError):
        SearchPublicDocsArguments(query="routing", max_results=max_results)  # type: ignore[arg-type]


def test_search_query_rejects_non_string_coercion() -> None:
    with pytest.raises(ValidationError):
        SearchPublicDocsArguments(query=5)  # type: ignore[arg-type]


def test_public_document_path_rejects_non_string_coercion() -> None:
    with pytest.raises(ValidationError):
        ReadPublicDocArguments(path=5)  # type: ignore[arg-type]


def test_unknown_tool_identifier_is_rejected() -> None:
    with pytest.raises(ValidationError):
        validate_tool_proposal({"tool": "unknown", "arguments": {}})


def test_extra_proposal_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        validate_tool_proposal(
            {"tool": "project_status", "arguments": {}, "unexpected": "not allowed"}
        )


def test_tool_and_argument_shape_must_match() -> None:
    with pytest.raises(ValidationError):
        validate_tool_proposal({"tool": "project_status", "arguments": {"query": "wrong contract"}})


@pytest.mark.parametrize(
    ("tool", "arguments"),
    [
        ("project_status", {"path": "README.md"}),
        ("search_public_docs", {"path": "README.md"}),
        ("read_public_doc", {"query": "routing"}),
    ],
)
def test_each_discriminator_rejects_another_tools_arguments(
    tool: str, arguments: dict[str, str]
) -> None:
    with pytest.raises(ValidationError):
        validate_tool_proposal({"tool": tool, "arguments": arguments})


@pytest.mark.parametrize("tool", ["search_public_docs", "read_public_doc"])
def test_empty_arguments_are_rejected_except_for_project_status(tool: str) -> None:
    with pytest.raises(ValidationError):
        validate_tool_proposal({"tool": tool, "arguments": {}})

    proposal = validate_tool_proposal({"tool": "project_status", "arguments": {}})
    assert isinstance(proposal, ProjectStatusProposal)


def test_extra_nested_argument_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        validate_tool_proposal(
            {
                "tool": "search_public_docs",
                "arguments": {"query": "routing", "unexpected": "not allowed"},
            }
        )


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (r"C:\file.md", None),
        ("C:file.md", None),
        ("C:/file.md", None),
        (r"\\server\share\file.md", None),
        ("//server/share/file.md", None),
        (r"..\file.md", None),
        ("folder/../file.md", None),
        (r"folder\file.md", None),
        ("/file.md", None),
        ("./file.md", "./file.md"),
        ("folder/file.MD", "folder/file.MD"),
        ("folder/file.md ", "folder/file.md"),
        ("   ", None),
        ("folder/", None),
        ("folder/file.md/", None),
        ("folder/file.md.txt", None),
    ],
)
def test_public_document_path_edge_cases(path: str, expected: str | None) -> None:
    if expected is None:
        with pytest.raises(ValidationError):
            ReadPublicDocArguments(path=path)
        return

    assert ReadPublicDocArguments(path=path).path == expected


@pytest.mark.parametrize(
    "payload",
    [
        {"tool": "SECRET_TOOL_MARKER", "arguments": {}},
        {
            "tool": "project_status",
            "arguments": {},
            "SECRET_FIELD_MARKER": "SECRET_VALUE_MARKER",
        },
        {
            "tool": "search_public_docs",
            "arguments": {"query": "public", "SECRET_FIELD_MARKER": "SECRET_VALUE_MARKER"},
        },
    ],
)
def test_validation_issue_conversion_redacts_rejected_proposal_data(
    payload: dict[str, object],
) -> None:
    with pytest.raises(ValidationError) as captured:
        validate_tool_proposal(payload)

    refusal = RefusedRoutingDecision(
        reason=RefusalReason.INVALID_ARGUMENTS,
        issues=validation_issues(captured.value),
        evidence_references=("rule:refuse-invalid-arguments-v1",),
    )
    serialized = refusal.model_dump_json()

    assert "SECRET_TOOL_MARKER" not in serialized
    assert "SECRET_FIELD_MARKER" not in serialized
    assert "SECRET_VALUE_MARKER" not in serialized
    assert "input" not in serialized.lower()
