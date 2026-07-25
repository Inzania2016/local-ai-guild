"""Versioned public and synthetic R3 evaluation cases."""

from typing import Final

from local_ai_guild.contracts import RefusalReason, ToolIdentifier
from local_ai_guild.evaluation import (
    EvaluationCase,
    ExpectedEvaluationResult,
    RoutingOutcome,
)
from local_ai_guild.policy import (
    DEFAULT_POLICY_PROFILE,
    PolicyIssueCode,
    PolicyOutcome,
    PolicyProfile,
)

EMPTY_POLICY_PROFILE: Final = PolicyProfile(
    allowlisted_tools=frozenset(),
    approval_required_tools=frozenset(),
)
READ_WITHOUT_APPROVAL_PROFILE: Final = PolicyProfile(
    allowlisted_tools=frozenset({ToolIdentifier.READ_PUBLIC_DOC}),
    approval_required_tools=frozenset(),
)
READ_EXCLUDED_PROFILE: Final = PolicyProfile(
    allowlisted_tools=frozenset(
        {
            ToolIdentifier.PROJECT_STATUS,
            ToolIdentifier.SEARCH_PUBLIC_DOCS,
        }
    ),
    approval_required_tools=frozenset(),
)


R3_EVALUATION_CASES: Final[tuple[EvaluationCase, ...]] = (
    EvaluationCase(
        identifier="eval:status-allowed-v1",
        description="Status routes to the harmless project-status proposal and is allowed",
        input="status",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.ROUTED,
            routed_tool=ToolIdentifier.PROJECT_STATUS,
            routing_evidence_identifiers=("rule:project-status-v1",),
            policy_outcome=PolicyOutcome.ALLOW,
            policy_evidence_identifiers=("policy:allow-project-status-v1",),
        ),
    ),
    EvaluationCase(
        identifier="eval:search-allowed-v1",
        description="A synthetic public-document query routes to search and is allowed",
        input="search docs: synthetic public routing",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.ROUTED,
            routed_tool=ToolIdentifier.SEARCH_PUBLIC_DOCS,
            routing_evidence_identifiers=("rule:search-public-docs-v1",),
            policy_outcome=PolicyOutcome.ALLOW,
            policy_evidence_identifiers=("policy:allow-search-public-docs-v1",),
        ),
    ),
    EvaluationCase(
        identifier="eval:read-requires-approval-v1",
        description="A public Markdown path routes to read and requires human approval",
        input="read doc: README.md",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.ROUTED,
            routed_tool=ToolIdentifier.READ_PUBLIC_DOC,
            routing_evidence_identifiers=("rule:read-public-doc-v1",),
            policy_outcome=PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
            policy_issue_codes=(PolicyIssueCode.HUMAN_APPROVAL_REQUIRED,),
            policy_evidence_identifiers=("policy:require-approval-read-public-doc-v1",),
        ),
    ),
    EvaluationCase(
        identifier="eval:unknown-command-refused-v1",
        description="An unknown synthetic command is refused by routing and policy",
        input="unknown synthetic command",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.REFUSED,
            routing_reason=RefusalReason.UNKNOWN_REQUEST,
            routing_evidence_identifiers=("rule:refuse-unknown-request-v1",),
            policy_outcome=PolicyOutcome.REFUSE,
            policy_issue_codes=(PolicyIssueCode.ROUTING_WAS_REFUSED,),
            policy_evidence_identifiers=("policy:refuse-routing-refusal-v1",),
        ),
    ),
    EvaluationCase(
        identifier="eval:invalid-search-refused-v1",
        description="An empty documentation search is refused with invalid arguments",
        input="search docs:",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.REFUSED,
            routing_reason=RefusalReason.INVALID_ARGUMENTS,
            routing_evidence_identifiers=("rule:refuse-invalid-arguments-v1",),
            policy_outcome=PolicyOutcome.REFUSE,
            policy_issue_codes=(PolicyIssueCode.ROUTING_WAS_REFUSED,),
            policy_evidence_identifiers=("policy:refuse-routing-refusal-v1",),
        ),
    ),
    EvaluationCase(
        identifier="eval:invalid-document-path-refused-v1",
        description="A synthetic non-Markdown path is refused with invalid arguments",
        input="read doc: docs/public-example.txt",
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.REFUSED,
            routing_reason=RefusalReason.INVALID_ARGUMENTS,
            routing_evidence_identifiers=("rule:refuse-invalid-arguments-v1",),
            policy_outcome=PolicyOutcome.REFUSE,
            policy_issue_codes=(PolicyIssueCode.ROUTING_WAS_REFUSED,),
            policy_evidence_identifiers=("policy:refuse-routing-refusal-v1",),
        ),
    ),
    EvaluationCase(
        identifier="eval:non-string-request-refused-v1",
        description="A bounded synthetic integer is refused as an invalid request",
        input=7,
        policy_profile=DEFAULT_POLICY_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.REFUSED,
            routing_reason=RefusalReason.INVALID_REQUEST,
            routing_evidence_identifiers=("rule:refuse-invalid-request-v1",),
            policy_outcome=PolicyOutcome.REFUSE,
            policy_issue_codes=(PolicyIssueCode.ROUTING_WAS_REFUSED,),
            policy_evidence_identifiers=("policy:refuse-routing-refusal-v1",),
        ),
    ),
    EvaluationCase(
        identifier="eval:empty-allowlist-denies-status-v1",
        description="An empty allowlist refuses the routed project-status proposal",
        input="status",
        policy_profile=EMPTY_POLICY_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.ROUTED,
            routed_tool=ToolIdentifier.PROJECT_STATUS,
            routing_evidence_identifiers=("rule:project-status-v1",),
            policy_outcome=PolicyOutcome.REFUSE,
            policy_issue_codes=(PolicyIssueCode.TOOL_NOT_ALLOWLISTED,),
            policy_evidence_identifiers=("policy:refuse-unallowlisted-tool-v1",),
        ),
    ),
    EvaluationCase(
        identifier="eval:custom-profile-allows-read-v1",
        description="A custom profile allows the routed public Markdown read",
        input="read doc: README.md",
        policy_profile=READ_WITHOUT_APPROVAL_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.ROUTED,
            routed_tool=ToolIdentifier.READ_PUBLIC_DOC,
            routing_evidence_identifiers=("rule:read-public-doc-v1",),
            policy_outcome=PolicyOutcome.ALLOW,
            policy_evidence_identifiers=("policy:allow-read-public-doc-v1",),
        ),
    ),
    EvaluationCase(
        identifier="eval:custom-profile-denies-read-v1",
        description="A custom profile excludes and refuses the routed Markdown read",
        input="read doc: README.md",
        policy_profile=READ_EXCLUDED_PROFILE,
        expected=ExpectedEvaluationResult(
            routing_outcome=RoutingOutcome.ROUTED,
            routed_tool=ToolIdentifier.READ_PUBLIC_DOC,
            routing_evidence_identifiers=("rule:read-public-doc-v1",),
            policy_outcome=PolicyOutcome.REFUSE,
            policy_issue_codes=(PolicyIssueCode.TOOL_NOT_ALLOWLISTED,),
            policy_evidence_identifiers=("policy:refuse-unallowlisted-tool-v1",),
        ),
    ),
)

if len({case.identifier for case in R3_EVALUATION_CASES}) != len(R3_EVALUATION_CASES):
    raise RuntimeError("R3 evaluation case identifiers must be unique")
