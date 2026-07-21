"""Behavior tests for the deterministic, non-executing R1 mock router."""

import pytest

from local_ai_guild.contracts import (
    ReadPublicDocProposal,
    RefusalReason,
    RefusedRoutingDecision,
    SearchPublicDocsProposal,
    SuccessfulRoutingDecision,
    ToolIdentifier,
)
from local_ai_guild.mock_router import route_user_input


def assert_success(decision: object) -> SuccessfulRoutingDecision:
    assert isinstance(decision, SuccessfulRoutingDecision)
    assert decision.evidence_references
    assert all(reference.startswith("rule:") for reference in decision.evidence_references)
    return decision


def assert_refusal(decision: object, reason: RefusalReason) -> RefusedRoutingDecision:
    assert isinstance(decision, RefusedRoutingDecision)
    assert decision.reason is reason
    assert decision.evidence_references
    return decision


def test_status_routes_to_project_status() -> None:
    decision = assert_success(route_user_input("  status  "))

    assert decision.proposal.tool is ToolIdentifier.PROJECT_STATUS
    assert decision.proposal.arguments.model_dump() == {}


def test_valid_documentation_search_routes() -> None:
    decision = assert_success(route_user_input("search docs: deterministic routing"))

    assert isinstance(decision.proposal, SearchPublicDocsProposal)
    assert decision.proposal.arguments.query == "deterministic routing"
    assert decision.proposal.arguments.max_results == 5


def test_valid_public_markdown_path_routes() -> None:
    decision = assert_success(route_user_input("read doc: docs/architecture/SYSTEM_CONTEXT.md"))

    assert isinstance(decision.proposal, ReadPublicDocProposal)
    assert decision.proposal.arguments.path == "docs/architecture/SYSTEM_CONTEXT.md"


def test_unknown_command_is_refused() -> None:
    assert_refusal(route_user_input("please infer what I mean"), RefusalReason.UNKNOWN_REQUEST)


@pytest.mark.parametrize("command", ["search docs:routing", "read doc:README.md"])
def test_command_prefix_requires_documented_space(command: str) -> None:
    assert_refusal(route_user_input(command), RefusalReason.UNKNOWN_REQUEST)


@pytest.mark.parametrize(
    "command",
    [
        "search docs:",
        f"search docs: {'x' * 201}",
        "read doc: C:/private/notes.md",
        "read doc: \\\\server\\share\\notes.md",
        "read doc: docs/../notes.md",
        "read doc: docs\\notes.md",
        "read doc: docs/notes.txt",
        "read doc:",
        "read doc:    ",
    ],
)
def test_recognized_command_with_invalid_arguments_is_typed_refusal(command: str) -> None:
    decision = assert_refusal(route_user_input(command), RefusalReason.INVALID_ARGUMENTS)

    assert decision.issues
    assert all(issue.code and issue.message for issue in decision.issues)


def test_non_string_input_is_typed_refusal_not_exception() -> None:
    decision = assert_refusal(route_user_input(5), RefusalReason.INVALID_REQUEST)

    assert decision.issues


def test_invalid_request_refusal_does_not_serialize_rejected_input() -> None:
    marker = "SECRET_REQUEST_MARKER"
    decision = assert_refusal(
        route_user_input({"unexpected": marker}), RefusalReason.INVALID_REQUEST
    )

    assert marker not in decision.model_dump_json()


def test_user_input_cannot_become_an_evidence_reference() -> None:
    attacker_rule = "rule:attacker-controlled-v999"
    decision = assert_refusal(route_user_input(attacker_rule), RefusalReason.UNKNOWN_REQUEST)

    assert attacker_rule not in decision.evidence_references


@pytest.mark.parametrize(
    "command",
    [
        "Status",
        "SEARCH DOCS: routing",
        "Read doc: README.md",
        "find documentation about routing",
    ],
)
def test_router_is_case_sensitive_and_has_no_fuzzy_matching(command: str) -> None:
    assert_refusal(route_user_input(command), RefusalReason.UNKNOWN_REQUEST)
