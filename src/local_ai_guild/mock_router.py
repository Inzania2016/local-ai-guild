"""Deterministic R1 routing with no tool execution or external I/O."""

from pydantic import ValidationError

from local_ai_guild.contracts import (
    ProjectStatusArguments,
    ProjectStatusProposal,
    ReadPublicDocArguments,
    ReadPublicDocProposal,
    RefusalReason,
    RefusedRoutingDecision,
    RoutingDecision,
    SearchPublicDocsArguments,
    SearchPublicDocsProposal,
    SuccessfulRoutingDecision,
    UserRequest,
)
from local_ai_guild.validation import validation_issues

STATUS_EVIDENCE = ("rule:project-status-v1",)
SEARCH_EVIDENCE = ("rule:search-public-docs-v1",)
READ_EVIDENCE = ("rule:read-public-doc-v1",)
UNKNOWN_EVIDENCE = ("rule:refuse-unknown-request-v1",)
INVALID_REQUEST_EVIDENCE = ("rule:refuse-invalid-request-v1",)
INVALID_ARGUMENTS_EVIDENCE = ("rule:refuse-invalid-arguments-v1",)

SEARCH_PREFIX = "search docs:"
READ_PREFIX = "read doc:"


def route_user_input(raw_input: object) -> RoutingDecision:
    """Validate untrusted input, then apply the documented deterministic rules."""
    try:
        request = UserRequest(text=raw_input)
    except ValidationError as error:
        return RefusedRoutingDecision(
            reason=RefusalReason.INVALID_REQUEST,
            issues=validation_issues(error),
            evidence_references=INVALID_REQUEST_EVIDENCE,
        )
    return route_request(request)


def route_request(request: UserRequest) -> RoutingDecision:
    """Route a validated request without reading, executing, or mutating anything."""
    command = request.text.strip()

    if command == "status":
        proposal = ProjectStatusProposal(arguments=ProjectStatusArguments())
        return SuccessfulRoutingDecision(proposal=proposal, evidence_references=STATUS_EVIDENCE)

    if command == SEARCH_PREFIX or command.startswith(f"{SEARCH_PREFIX} "):
        return _route_search(command[len(SEARCH_PREFIX) :].strip())

    if command == READ_PREFIX or command.startswith(f"{READ_PREFIX} "):
        return _route_read(command[len(READ_PREFIX) :].strip())

    return RefusedRoutingDecision(
        reason=RefusalReason.UNKNOWN_REQUEST,
        evidence_references=UNKNOWN_EVIDENCE,
    )


def _route_search(query: str) -> RoutingDecision:
    try:
        arguments = SearchPublicDocsArguments(query=query)
    except ValidationError as error:
        return _invalid_arguments(error)
    proposal = SearchPublicDocsProposal(arguments=arguments)
    return SuccessfulRoutingDecision(proposal=proposal, evidence_references=SEARCH_EVIDENCE)


def _route_read(path: str) -> RoutingDecision:
    try:
        arguments = ReadPublicDocArguments(path=path)
    except ValidationError as error:
        return _invalid_arguments(error)
    proposal = ReadPublicDocProposal(arguments=arguments)
    return SuccessfulRoutingDecision(proposal=proposal, evidence_references=READ_EVIDENCE)


def _invalid_arguments(error: ValidationError) -> RefusedRoutingDecision:
    return RefusedRoutingDecision(
        reason=RefusalReason.INVALID_ARGUMENTS,
        issues=validation_issues(error),
        evidence_references=INVALID_ARGUMENTS_EVIDENCE,
    )
