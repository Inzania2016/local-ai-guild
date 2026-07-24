"""Tests for non-executing deterministic R2 policy evaluation."""

import json

import pytest
from pydantic import ValidationError

from local_ai_guild.contracts import (
    ProjectStatusArguments,
    ProjectStatusProposal,
    SuccessfulRoutingDecision,
    ToolIdentifier,
)
from local_ai_guild.evidence import (
    R1_EVIDENCE_REGISTRY,
    EvidenceEnvelopeError,
    EvidenceKind,
    EvidenceProvenance,
    EvidenceReference,
    RoutingDecisionEnvelope,
    build_routing_decision_envelope,
)
from local_ai_guild.mock_router import route_user_input
from local_ai_guild.policy import (
    ALLOW_EVIDENCE_BY_TOOL,
    APPROVAL_EVIDENCE_BY_TOOL,
    APPROVAL_REQUIRED_ISSUE,
    DEFAULT_POLICY_PROFILE,
    NOT_ALLOWLISTED_ISSUE,
    POLICY_EVIDENCE_REGISTRY,
    ROUTING_REFUSED_ISSUE,
    PolicyDecision,
    PolicyEvaluationEnvelope,
    PolicyInputError,
    PolicyIssue,
    PolicyIssueCode,
    PolicyOutcome,
    PolicyProfile,
    build_policy_evaluation_envelope,
    evaluate_policy,
)


def test_policy_models_are_strict_frozen_and_forbid_extras() -> None:
    for model in (PolicyIssue, PolicyProfile, PolicyDecision, PolicyEvaluationEnvelope):
        assert model.model_config["strict"] is True
        assert model.model_config["extra"] == "forbid"
        assert model.model_config["frozen"] is True


def test_approval_required_tools_must_be_allowlisted() -> None:
    with pytest.raises(ValidationError):
        PolicyProfile(
            allowlisted_tools=frozenset(),
            approval_required_tools=frozenset({ToolIdentifier.READ_PUBLIC_DOC}),
        )


def test_policy_profile_frozen_sets_are_immutable() -> None:
    assert isinstance(DEFAULT_POLICY_PROFILE.allowlisted_tools, frozenset)
    assert isinstance(DEFAULT_POLICY_PROFILE.approval_required_tools, frozenset)
    with pytest.raises(AttributeError):
        DEFAULT_POLICY_PROFILE.allowlisted_tools.add(ToolIdentifier.PROJECT_STATUS)  # type: ignore[attr-defined]
    with pytest.raises(ValidationError):
        DEFAULT_POLICY_PROFILE.allowlisted_tools = frozenset()  # type: ignore[misc]


def test_policy_enums_do_not_coerce_strings() -> None:
    with pytest.raises(ValidationError):
        PolicyIssue(
            code="routing_was_refused",  # type: ignore[arg-type]
            message="Synthetic message",
        )
    with pytest.raises(ValidationError):
        PolicyDecision(
            outcome="allow",  # type: ignore[arg-type]
            evidence=(ALLOW_EVIDENCE_BY_TOOL[ToolIdentifier.PROJECT_STATUS],),
            tool=ToolIdentifier.PROJECT_STATUS,
        )


def test_policy_profile_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        PolicyProfile(
            allowlisted_tools=frozenset(ToolIdentifier),
            approval_required_tools=frozenset(),
            unexpected=True,  # type: ignore[call-arg]
        )


@pytest.mark.parametrize(
    "value",
    [
        [ToolIdentifier.PROJECT_STATUS],
        {ToolIdentifier.PROJECT_STATUS},
        frozenset({"project_status"}),
        frozenset({"unknown_tool"}),
        frozenset({True}),
        frozenset({1}),
        True,
        1,
        {},
        object(),
    ],
)
def test_policy_profile_rejects_collection_and_enum_coercion(value: object) -> None:
    with pytest.raises(ValidationError):
        PolicyProfile(
            allowlisted_tools=value,  # type: ignore[arg-type]
            approval_required_tools=frozenset(),
        )
    with pytest.raises(ValidationError):
        PolicyProfile(
            allowlisted_tools=frozenset(ToolIdentifier),
            approval_required_tools=value,  # type: ignore[arg-type]
        )


def test_empty_and_duplicate_policy_collections_are_unambiguous() -> None:
    empty = PolicyProfile(
        allowlisted_tools=frozenset(),
        approval_required_tools=frozenset(),
    )
    duplicate_source = [
        ToolIdentifier.PROJECT_STATUS,
        ToolIdentifier.PROJECT_STATUS,
    ]
    duplicate_free = PolicyProfile(
        allowlisted_tools=frozenset(duplicate_source),
        approval_required_tools=frozenset(),
    )

    assert not empty.allowlisted_tools
    assert not empty.approval_required_tools
    assert duplicate_free.allowlisted_tools == frozenset({ToolIdentifier.PROJECT_STATUS})


def test_default_profile_has_no_mutable_shared_collection() -> None:
    source = {ToolIdentifier.PROJECT_STATUS}
    profile = PolicyProfile(
        allowlisted_tools=frozenset(source),
        approval_required_tools=frozenset(),
    )
    source.add(ToolIdentifier.SEARCH_PUBLIC_DOCS)

    assert profile.allowlisted_tools == frozenset({ToolIdentifier.PROJECT_STATUS})
    assert DEFAULT_POLICY_PROFILE.allowlisted_tools == frozenset(ToolIdentifier)


def test_policy_evidence_registry_is_immutable() -> None:
    with pytest.raises(TypeError):
        POLICY_EVIDENCE_REGISTRY["policy:injected-v1"] = next(  # type: ignore[index]
            iter(POLICY_EVIDENCE_REGISTRY.values())
        )


def test_policy_registry_is_unique_consistent_and_disjoint_from_routing() -> None:
    assert len(POLICY_EVIDENCE_REGISTRY) == len(set(POLICY_EVIDENCE_REGISTRY))
    assert all(
        key == reference.identifier
        and reference.kind is EvidenceKind.POLICY_RULE
        and reference.provenance is EvidenceProvenance.SYNTHETIC
        for key, reference in POLICY_EVIDENCE_REGISTRY.items()
    )
    assert len({reference.identifier for reference in POLICY_EVIDENCE_REGISTRY.values()}) == len(
        POLICY_EVIDENCE_REGISTRY
    )
    assert set(POLICY_EVIDENCE_REGISTRY).isdisjoint(R1_EVIDENCE_REGISTRY)


def test_direct_policy_decision_rejects_caller_written_issue() -> None:
    caller_issue = PolicyIssue(
        code=PolicyIssueCode.ROUTING_WAS_REFUSED,
        message="PRIVATE_CALLER_MESSAGE",
    )
    with pytest.raises(ValidationError):
        PolicyDecision(
            outcome=PolicyOutcome.REFUSE,
            issues=(caller_issue,),
            evidence=(POLICY_EVIDENCE_REGISTRY["policy:refuse-routing-refusal-v1"],),
        )


def test_direct_policy_decision_rejects_equal_caller_written_constants() -> None:
    caller_issue = PolicyIssue(
        code=PolicyIssueCode.HUMAN_APPROVAL_REQUIRED,
        message="The routed tool requires human approval",
    )
    caller_evidence = EvidenceReference(
        identifier="policy:require-approval-read-public-doc-v1",
        kind=EvidenceKind.POLICY_RULE,
        provenance=EvidenceProvenance.SYNTHETIC,
    )

    with pytest.raises(ValidationError):
        PolicyDecision(
            outcome=PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
            issues=(caller_issue,),
            evidence=(caller_evidence,),
            tool=ToolIdentifier.READ_PUBLIC_DOC,
        )


def test_direct_policy_decision_rejects_non_synthetic_policy_evidence() -> None:
    public_reference = EvidenceReference(
        identifier="policy:allow-project-status-v1",
        kind=EvidenceKind.POLICY_RULE,
        provenance=EvidenceProvenance.PUBLIC,
    )
    with pytest.raises(ValidationError):
        PolicyDecision(
            outcome=PolicyOutcome.ALLOW,
            evidence=(public_reference,),
            tool=ToolIdentifier.PROJECT_STATUS,
        )


@pytest.mark.parametrize(
    "fields",
    [
        {
            "outcome": PolicyOutcome.ALLOW,
            "issues": (ROUTING_REFUSED_ISSUE,),
            "evidence": (ALLOW_EVIDENCE_BY_TOOL[ToolIdentifier.PROJECT_STATUS],),
            "tool": ToolIdentifier.PROJECT_STATUS,
        },
        {
            "outcome": PolicyOutcome.ALLOW,
            "issues": (),
            "evidence": (APPROVAL_EVIDENCE_BY_TOOL[ToolIdentifier.READ_PUBLIC_DOC],),
            "tool": ToolIdentifier.READ_PUBLIC_DOC,
        },
        {
            "outcome": PolicyOutcome.REFUSE,
            "issues": (NOT_ALLOWLISTED_ISSUE,),
            "evidence": (ALLOW_EVIDENCE_BY_TOOL[ToolIdentifier.PROJECT_STATUS],),
            "tool": ToolIdentifier.PROJECT_STATUS,
        },
        {
            "outcome": PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
            "issues": (APPROVAL_REQUIRED_ISSUE,),
            "evidence": (APPROVAL_EVIDENCE_BY_TOOL[ToolIdentifier.READ_PUBLIC_DOC],),
        },
        {
            "outcome": PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
            "issues": (NOT_ALLOWLISTED_ISSUE,),
            "evidence": (APPROVAL_EVIDENCE_BY_TOOL[ToolIdentifier.READ_PUBLIC_DOC],),
            "tool": ToolIdentifier.READ_PUBLIC_DOC,
        },
        {
            "outcome": PolicyOutcome.REFUSE,
            "issues": (ROUTING_REFUSED_ISSUE,),
            "evidence": (POLICY_EVIDENCE_REGISTRY["policy:refuse-routing-refusal-v1"],),
            "tool": ToolIdentifier.PROJECT_STATUS,
        },
        {
            "outcome": PolicyOutcome.ALLOW,
            "issues": (),
            "evidence": (),
            "tool": ToolIdentifier.PROJECT_STATUS,
        },
        {
            "outcome": PolicyOutcome.ALLOW,
            "issues": (),
            "evidence": (R1_EVIDENCE_REGISTRY["rule:project-status-v1"],),
            "tool": ToolIdentifier.PROJECT_STATUS,
        },
        {
            "outcome": PolicyOutcome.ALLOW,
            "issues": (),
            "evidence": (
                ALLOW_EVIDENCE_BY_TOOL[ToolIdentifier.PROJECT_STATUS],
                ALLOW_EVIDENCE_BY_TOOL[ToolIdentifier.PROJECT_STATUS],
            ),
            "tool": ToolIdentifier.PROJECT_STATUS,
        },
    ],
)
def test_direct_policy_decision_rejects_inconsistent_combinations(
    fields: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        PolicyDecision(**fields)  # type: ignore[arg-type]


def test_direct_policy_decision_rejects_raw_nested_dictionaries() -> None:
    with pytest.raises(ValidationError):
        PolicyDecision(
            outcome=PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
            issues=(APPROVAL_REQUIRED_ISSUE.model_dump(),),
            evidence=(APPROVAL_EVIDENCE_BY_TOOL[ToolIdentifier.READ_PUBLIC_DOC].model_dump(),),
            tool=ToolIdentifier.READ_PUBLIC_DOC,
        )


@pytest.mark.parametrize(
    ("command", "outcome", "tool"),
    [
        ("status", PolicyOutcome.ALLOW, ToolIdentifier.PROJECT_STATUS),
        ("search docs: public routing", PolicyOutcome.ALLOW, ToolIdentifier.SEARCH_PUBLIC_DOCS),
        (
            "read doc: README.md",
            PolicyOutcome.REQUIRE_HUMAN_APPROVAL,
            ToolIdentifier.READ_PUBLIC_DOC,
        ),
    ],
)
def test_default_policy_routed_outcomes(
    command: str, outcome: PolicyOutcome, tool: ToolIdentifier
) -> None:
    result = build_policy_evaluation_envelope(route_user_input(command))

    assert result.policy.outcome is outcome
    assert result.policy.tool is tool
    assert result.policy.evidence


def test_r1_refusal_becomes_policy_refusal() -> None:
    result = build_policy_evaluation_envelope(route_user_input("unknown public command"))

    assert result.policy.outcome is PolicyOutcome.REFUSE
    assert result.policy.tool is None
    assert result.policy.issues[0].code is PolicyIssueCode.ROUTING_WAS_REFUSED


def test_valid_profile_excluding_routed_tool_refuses_before_approval() -> None:
    profile = PolicyProfile(
        allowlisted_tools=frozenset({ToolIdentifier.PROJECT_STATUS}),
        approval_required_tools=frozenset(),
    )
    result = build_policy_evaluation_envelope(route_user_input("read doc: README.md"), profile)

    assert result.policy.outcome is PolicyOutcome.REFUSE
    assert result.policy.issues[0].code is PolicyIssueCode.TOOL_NOT_ALLOWLISTED
    assert result.policy.evidence[0].identifier == "policy:refuse-unallowlisted-tool-v1"


@pytest.mark.parametrize(
    "command",
    [
        "status",
        "search docs: public routing",
        "read doc: README.md",
    ],
)
def test_empty_allowlist_refuses_every_routed_tool(command: str) -> None:
    profile = PolicyProfile(
        allowlisted_tools=frozenset(),
        approval_required_tools=frozenset(),
    )
    result = build_policy_evaluation_envelope(route_user_input(command), profile)

    assert result.policy.outcome is PolicyOutcome.REFUSE
    assert result.policy.issues == (NOT_ALLOWLISTED_ISSUE,)


def test_allowlisted_non_approval_tool_is_allowed() -> None:
    profile = PolicyProfile(
        allowlisted_tools=frozenset({ToolIdentifier.SEARCH_PUBLIC_DOCS}),
        approval_required_tools=frozenset(),
    )
    result = build_policy_evaluation_envelope(
        route_user_input("search docs: synthetic query"),
        profile,
    )

    assert result.policy.outcome is PolicyOutcome.ALLOW
    assert not result.policy.issues


def test_routing_refusal_precedes_tool_policy() -> None:
    empty_profile = PolicyProfile(
        allowlisted_tools=frozenset(),
        approval_required_tools=frozenset(),
    )
    result = build_policy_evaluation_envelope(
        route_user_input("unknown public command"),
        empty_profile,
    )

    assert result.policy.outcome is PolicyOutcome.REFUSE
    assert result.policy.issues == (ROUTING_REFUSED_ISSUE,)


def test_every_policy_outcome_uses_typed_synthetic_policy_evidence() -> None:
    results = [
        build_policy_evaluation_envelope(route_user_input("status")),
        build_policy_evaluation_envelope(route_user_input("read doc: README.md")),
        build_policy_evaluation_envelope(route_user_input("unknown public command")),
    ]
    for result in results:
        assert result.policy.evidence
        assert all(
            reference.kind is EvidenceKind.POLICY_RULE
            and reference.provenance is EvidenceProvenance.SYNTHETIC
            and POLICY_EVIDENCE_REGISTRY[reference.identifier] is reference
            for reference in result.policy.evidence
        )


def test_user_input_cannot_influence_policy_issue_or_evidence() -> None:
    marker = "PRIVATE_POLICY_MARKER"
    result = build_policy_evaluation_envelope(route_user_input(marker))
    policy_json = result.policy.model_dump_json()

    assert marker not in policy_json


def test_marker_inputs_cannot_influence_bounded_policy_failures() -> None:
    marker = "PRIVATE_BOUNDARY_MARKER"

    class MarkerObject:
        def __repr__(self) -> str:
            return marker

    routing = build_routing_decision_envelope(route_user_input("status"))
    failures: list[Exception] = []
    for call in (
        lambda: build_policy_evaluation_envelope({marker: "attacker field"}),
        lambda: build_policy_evaluation_envelope(MarkerObject()),
        lambda: evaluate_policy(MarkerObject()),
        lambda: evaluate_policy(routing, MarkerObject()),  # type: ignore[arg-type]
    ):
        with pytest.raises((EvidenceEnvelopeError, PolicyInputError)) as captured:
            call()
        failures.append(captured.value)

    assert all(marker not in str(error) for error in failures)


def test_invalid_request_object_repr_is_absent_from_policy_output() -> None:
    marker = "PRIVATE_INVALID_REQUEST_REPR_MARKER"

    class InvalidRequest:
        def __repr__(self) -> str:
            return marker

    result = build_policy_evaluation_envelope(route_user_input(InvalidRequest()))
    assert marker not in result.model_dump_json()


def test_policy_rejects_raw_dictionary_and_standalone_proposal() -> None:
    with pytest.raises(PolicyInputError, match="validated routing decision envelope"):
        evaluate_policy({"decision": "not validated"})
    with pytest.raises(PolicyInputError, match="validated routing decision envelope"):
        evaluate_policy(ProjectStatusProposal(arguments=ProjectStatusArguments()))


def test_policy_rejects_arbitrary_objects_and_boundary_subclasses_without_echo() -> None:
    class MarkerObject:
        def __repr__(self) -> str:
            return "PRIVATE_POLICY_OBJECT_REPR_MARKER"

    class EnvelopeSubclass(RoutingDecisionEnvelope):
        pass

    class ProfileSubclass(PolicyProfile):
        pass

    routing = build_routing_decision_envelope(route_user_input("status"))
    with pytest.raises(ValidationError):
        EnvelopeSubclass(
            decision=routing.decision,
            evidence=routing.evidence,
        )
    profile_subclass = ProfileSubclass(
        allowlisted_tools=frozenset(ToolIdentifier),
        approval_required_tools=frozenset(),
    )

    for envelope, profile in (
        (MarkerObject(), DEFAULT_POLICY_PROFILE),
        (routing, MarkerObject()),
        (routing, profile_subclass),
    ):
        with pytest.raises(PolicyInputError) as captured:
            evaluate_policy(envelope, profile)  # type: ignore[arg-type]
        assert "PRIVATE_POLICY_OBJECT_REPR_MARKER" not in str(captured.value)


def test_combined_helper_rejects_raw_dictionary() -> None:
    with pytest.raises(EvidenceEnvelopeError, match="validated R1 routing decision"):
        build_policy_evaluation_envelope({"outcome": "routed"})


def test_combined_helper_rejects_decision_and_profile_subclasses() -> None:
    class DecisionSubclass(SuccessfulRoutingDecision):
        pass

    class ProfileSubclass(PolicyProfile):
        pass

    decision = route_user_input("status")
    decision_subclass = DecisionSubclass(
        proposal=decision.proposal,
        evidence_references=decision.evidence_references,
    )
    profile_subclass = ProfileSubclass(
        allowlisted_tools=frozenset(ToolIdentifier),
        approval_required_tools=frozenset(),
    )

    with pytest.raises(EvidenceEnvelopeError):
        build_policy_evaluation_envelope(decision_subclass)
    with pytest.raises(PolicyInputError):
        build_policy_evaluation_envelope(decision, profile_subclass)


def test_policy_result_has_no_execution_state() -> None:
    result = build_policy_evaluation_envelope(route_user_input("status"))
    serialized = result.policy.model_dump()

    assert "executed" not in serialized
    assert "execution" not in serialized


def test_combined_envelope_binds_exact_profile_and_policy_result() -> None:
    decision = route_user_input("read doc: README.md")
    routing = build_routing_decision_envelope(decision)
    approval_policy = evaluate_policy(routing, DEFAULT_POLICY_PROFILE)
    allow_profile = PolicyProfile(
        allowlisted_tools=frozenset(ToolIdentifier),
        approval_required_tools=frozenset(),
    )
    allow_policy = evaluate_policy(routing, allow_profile)

    approval_envelope = PolicyEvaluationEnvelope(
        routing=routing,
        profile=DEFAULT_POLICY_PROFILE,
        policy=approval_policy,
    )
    allow_envelope = PolicyEvaluationEnvelope(
        routing=routing,
        profile=allow_profile,
        policy=allow_policy,
    )

    assert approval_envelope.policy.outcome is PolicyOutcome.REQUIRE_HUMAN_APPROVAL
    assert allow_envelope.policy.outcome is PolicyOutcome.ALLOW
    with pytest.raises(ValidationError):
        PolicyEvaluationEnvelope(
            routing=routing,
            profile=allow_profile,
            policy=approval_policy,
        )


def test_combined_envelope_rejects_policy_for_a_different_tool() -> None:
    status_routing = build_routing_decision_envelope(route_user_input("status"))
    search_routing = build_routing_decision_envelope(
        route_user_input("search docs: synthetic query")
    )
    search_policy = evaluate_policy(search_routing)

    with pytest.raises(ValidationError):
        PolicyEvaluationEnvelope(
            routing=status_routing,
            profile=DEFAULT_POLICY_PROFILE,
            policy=search_policy,
        )


def test_combined_envelope_rejects_raw_nested_dictionaries() -> None:
    result = build_policy_evaluation_envelope(route_user_input("status"))

    with pytest.raises(ValidationError):
        PolicyEvaluationEnvelope(
            routing=result.routing.model_dump(),
            profile=result.profile,
            policy=result.policy,
        )
    with pytest.raises(ValidationError):
        PolicyEvaluationEnvelope(
            routing=result.routing,
            profile=result.profile.model_dump(),
            policy=result.policy,
        )
    with pytest.raises(ValidationError):
        PolicyEvaluationEnvelope(
            routing=result.routing,
            profile=result.profile,
            policy=result.policy.model_dump(),
        )


def test_combined_envelope_serialization_is_deterministic() -> None:
    first = build_policy_evaluation_envelope(route_user_input("status")).model_dump_json()
    second = build_policy_evaluation_envelope(route_user_input("status")).model_dump_json()

    assert first == second
    assert json.loads(first)["policy"]["outcome"] == "allow"
    assert json.loads(first)["profile"]["allowlisted_tools"] == [
        "project_status",
        "read_public_doc",
        "search_public_docs",
    ]


def test_new_envelope_json_schemas_can_be_generated() -> None:
    assert RoutingDecisionEnvelope.model_json_schema()["title"] == "RoutingDecisionEnvelope"
    assert PolicyEvaluationEnvelope.model_json_schema()["title"] == "PolicyEvaluationEnvelope"


def test_raw_command_is_not_stored_and_arguments_remain_only_in_nested_decision() -> None:
    raw_command = "search docs: PUBLIC_QUERY_MARKER"
    result = build_policy_evaluation_envelope(route_user_input(raw_command))
    serialized = result.model_dump_json()

    assert raw_command not in serialized
    assert serialized.count("PUBLIC_QUERY_MARKER") == 1
    assert "PUBLIC_QUERY_MARKER" not in result.policy.model_dump_json()


def test_policy_issue_does_not_contain_document_path() -> None:
    path = "docs/architecture/SYSTEM_CONTEXT.md"
    result = build_policy_evaluation_envelope(route_user_input(f"read doc: {path}"))

    assert path not in result.policy.model_dump_json()


def test_refusal_envelope_does_not_recover_rejected_input() -> None:
    marker = "PRIVATE_REJECTED_MARKER"
    result = build_policy_evaluation_envelope(route_user_input(f"read doc: {marker}.txt"))

    assert marker not in result.model_dump_json()
