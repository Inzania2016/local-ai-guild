"""Pydantic adapters and redaction-safe validation conversion for R1."""

from typing import Any

from pydantic import TypeAdapter, ValidationError

from local_ai_guild.contracts import RoutingDecision, ToolProposal, ValidationIssue

TOOL_PROPOSAL_ADAPTER: TypeAdapter[ToolProposal] = TypeAdapter(ToolProposal)
ROUTING_DECISION_ADAPTER: TypeAdapter[RoutingDecision] = TypeAdapter(RoutingDecision)

SAFE_LOCATION_PARTS = frozenset(
    {
        "arguments",
        "code",
        "evidence_references",
        "issues",
        "location",
        "max_results",
        "message",
        "outcome",
        "path",
        "project_status",
        "proposal",
        "query",
        "read_public_doc",
        "reason",
        "refused",
        "routed",
        "search_public_docs",
        "text",
        "tool",
    }
)


def validate_tool_proposal(value: object) -> ToolProposal:
    """Validate untrusted proposal data against the discriminated tool contracts."""
    return TOOL_PROPOSAL_ADAPTER.validate_python(value)


def tool_proposal_json_schema() -> dict[str, Any]:
    """Generate, but do not persist, the R1 proposal boundary JSON Schema."""
    return TOOL_PROPOSAL_ADAPTER.json_schema()


def routing_decision_json_schema() -> dict[str, Any]:
    """Generate, but do not persist, the R1 decision boundary JSON Schema."""
    return ROUTING_DECISION_ADAPTER.json_schema()


def validation_issues(error: ValidationError) -> tuple[ValidationIssue, ...]:
    """Convert Pydantic errors without copying rejected input into a refusal."""
    return tuple(
        ValidationIssue(
            location=tuple(_safe_location_part(part) for part in item["loc"]),
            code=item["type"],
            message=_safe_validation_message(item["type"]),
        )
        for item in error.errors(include_url=False, include_context=False, include_input=False)
    )


def _safe_location_part(part: object) -> str | int:
    """Keep schema-owned locations while redacting attacker-controlled field names."""
    if isinstance(part, int) and not isinstance(part, bool):
        return part
    if isinstance(part, str) and part in SAFE_LOCATION_PARTS:
        return part
    return "<redacted>"


def _safe_validation_message(code: str) -> str:
    """Return bounded messages that cannot interpolate rejected input."""
    match code:
        case "extra_forbidden":
            return "Extra fields are not permitted"
        case "int_type":
            return "Value must be an integer"
        case "string_type":
            return "Value must be a string"
        case "missing":
            return "Required field is missing"
        case "string_too_long":
            return "String exceeds the maximum length"
        case "string_too_short":
            return "String is below the minimum length"
        case "greater_than_equal":
            return "Value is below the minimum"
        case "less_than_equal":
            return "Value exceeds the maximum"
        case "literal_error" | "union_tag_invalid" | "union_tag_not_found":
            return "Value does not match an allowed discriminator"
        case _:
            return "Value failed boundary validation"
