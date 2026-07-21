"""Strict contracts at Local AI Guild's untrusted routing boundary."""

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator


class BoundaryModel(BaseModel):
    """Base configuration for immutable, strict boundary contracts."""

    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)


class UserRequest(BoundaryModel):
    """Untrusted user text before deterministic routing."""

    text: StrictStr


class ToolIdentifier(StrEnum):
    """R1-only mock tool identifiers."""

    PROJECT_STATUS = "project_status"
    SEARCH_PUBLIC_DOCS = "search_public_docs"
    READ_PUBLIC_DOC = "read_public_doc"


class ProjectStatusArguments(BoundaryModel):
    """The project status mock tool accepts no arguments."""


class SearchPublicDocsArguments(BoundaryModel):
    """Arguments for a future search over public or synthetic documentation."""

    query: StrictStr = Field(min_length=1, max_length=200)
    max_results: StrictInt = Field(default=5, ge=1, le=10)

    @field_validator("query")
    @classmethod
    def query_must_not_be_blank(cls, value: str) -> str:
        """Normalize surrounding whitespace and reject blank queries."""
        normalized = value.strip()
        if not normalized:
            raise ValueError("query must not be empty or whitespace-only")
        return normalized


class ReadPublicDocArguments(BoundaryModel):
    """Arguments for a future repository-relative public Markdown read."""

    path: StrictStr

    @field_validator("path")
    @classmethod
    def path_must_be_safe_public_markdown(cls, value: str) -> str:
        """Validate a repository-relative POSIX-style Markdown path without I/O."""
        normalized = value.strip()
        if not normalized:
            raise ValueError("path must not be empty or whitespace-only")
        if "\\" in normalized:
            raise ValueError("path must use forward slashes, not backslashes")
        if normalized.startswith("/"):
            raise ValueError("path must be repository-relative")
        if len(normalized) >= 2 and normalized[0].isalpha() and normalized[1] == ":":
            raise ValueError("path must not be drive-qualified")

        segments = normalized.split("/")
        if ".." in segments:
            raise ValueError("path traversal is not allowed")
        if not normalized.lower().endswith(".md"):
            raise ValueError("path must have a .md extension")
        return normalized


class ProjectStatusProposal(BoundaryModel):
    """Validated proposal for the project status mock tool."""

    tool: Literal[ToolIdentifier.PROJECT_STATUS] = ToolIdentifier.PROJECT_STATUS
    arguments: ProjectStatusArguments


class SearchPublicDocsProposal(BoundaryModel):
    """Validated proposal for the public documentation search mock tool."""

    tool: Literal[ToolIdentifier.SEARCH_PUBLIC_DOCS] = ToolIdentifier.SEARCH_PUBLIC_DOCS
    arguments: SearchPublicDocsArguments


class ReadPublicDocProposal(BoundaryModel):
    """Validated proposal for the public Markdown read mock tool."""

    tool: Literal[ToolIdentifier.READ_PUBLIC_DOC] = ToolIdentifier.READ_PUBLIC_DOC
    arguments: ReadPublicDocArguments


type ToolProposal = Annotated[
    ProjectStatusProposal | SearchPublicDocsProposal | ReadPublicDocProposal,
    Field(discriminator="tool"),
]


class ValidationIssue(BoundaryModel):
    """Redaction-safe description of one boundary validation failure."""

    location: tuple[StrictStr | StrictInt, ...]
    code: StrictStr
    message: StrictStr


class RefusalReason(StrEnum):
    """Deterministic R1 refusal categories."""

    INVALID_REQUEST = "invalid_request"
    UNKNOWN_REQUEST = "unknown_request"
    INVALID_ARGUMENTS = "invalid_arguments"


type EvidenceReferences = Annotated[tuple[StrictStr, ...], Field(min_length=1)]


class SuccessfulRoutingDecision(BoundaryModel):
    """A validated proposal selected by a deterministic routing rule."""

    outcome: Literal["routed"] = "routed"
    proposal: ToolProposal
    evidence_references: EvidenceReferences

    @field_validator("evidence_references")
    @classmethod
    def evidence_references_must_not_be_blank(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        """Require each evidence reference to be stable and non-blank."""
        if any(not reference.strip() for reference in value):
            raise ValueError("evidence references must not be blank")
        return value


class RefusedRoutingDecision(BoundaryModel):
    """A typed refusal produced without executing any tool."""

    outcome: Literal["refused"] = "refused"
    reason: RefusalReason
    issues: tuple[ValidationIssue, ...] = ()
    evidence_references: EvidenceReferences

    @field_validator("evidence_references")
    @classmethod
    def evidence_references_must_not_be_blank(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        """Require each evidence reference to be stable and non-blank."""
        if any(not reference.strip() for reference in value):
            raise ValueError("evidence references must not be blank")
        return value


type RoutingDecision = Annotated[
    SuccessfulRoutingDecision | RefusedRoutingDecision,
    Field(discriminator="outcome"),
]
