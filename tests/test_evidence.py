"""Tests for typed R2 evidence references and routing envelopes."""

import inspect

import pytest
from pydantic import ValidationError

from local_ai_guild.contracts import (
    ProjectStatusArguments,
    ProjectStatusProposal,
    RefusalReason,
    RefusedRoutingDecision,
    SuccessfulRoutingDecision,
    ValidationIssue,
)
from local_ai_guild.evidence import (
    R1_EVIDENCE_REGISTRY,
    EvidenceEnvelopeError,
    EvidenceKind,
    EvidenceProvenance,
    EvidenceReference,
    RoutingDecisionEnvelope,
    _synthetic_evidence_registry,
    build_routing_decision_envelope,
)
from local_ai_guild.mock_router import route_user_input


def synthetic_reference(
    identifier: str = "rule:public-example-v1",
    kind: EvidenceKind = EvidenceKind.ROUTING_RULE,
    provenance: EvidenceProvenance = EvidenceProvenance.SYNTHETIC,
) -> EvidenceReference:
    return EvidenceReference(
        identifier=identifier,
        kind=kind,
        provenance=provenance,
    )


def test_evidence_models_are_strict_frozen_and_forbid_extras() -> None:
    for model in (EvidenceReference, RoutingDecisionEnvelope):
        assert model.model_config["strict"] is True
        assert model.model_config["extra"] == "forbid"
        assert model.model_config["frozen"] is True

    with pytest.raises(ValidationError):
        EvidenceReference(
            identifier="rule:public-example-v1",
            kind=EvidenceKind.ROUTING_RULE,
            provenance=EvidenceProvenance.SYNTHETIC,
            unexpected="forbidden",  # type: ignore[call-arg]
        )


@pytest.mark.parametrize(
    ("identifier", "kind"),
    [
        ("rule:project-status-v1", EvidenceKind.ROUTING_RULE),
        ("policy:allow-project-status-v1", EvidenceKind.POLICY_RULE),
        ("policy:require-approval-read-public-doc-v1", EvidenceKind.POLICY_RULE),
    ],
)
def test_valid_evidence_identifiers(identifier: str, kind: EvidenceKind) -> None:
    assert synthetic_reference(identifier, kind).identifier == identifier


def test_public_provenance_metadata_is_supported() -> None:
    reference = EvidenceReference(
        identifier="rule:public-example-v1",
        kind=EvidenceKind.ROUTING_RULE,
        provenance=EvidenceProvenance.PUBLIC,
    )
    assert reference.provenance is EvidenceProvenance.PUBLIC


def test_evidence_enums_do_not_coerce_strings_or_unknown_values() -> None:
    with pytest.raises(ValidationError):
        EvidenceReference(
            identifier="rule:public-example-v1",
            kind="routing_rule",  # type: ignore[arg-type]
            provenance=EvidenceProvenance.SYNTHETIC,
        )
    with pytest.raises(ValidationError):
        EvidenceReference(
            identifier="rule:public-example-v1",
            kind=EvidenceKind.ROUTING_RULE,
            provenance="synthetic",  # type: ignore[arg-type]
        )
    with pytest.raises(ValidationError):
        EvidenceReference(
            identifier="rule:public-example-v1",
            kind="unknown_kind",  # type: ignore[arg-type]
            provenance=EvidenceProvenance.SYNTHETIC,
        )


def test_evidence_namespace_must_match_kind() -> None:
    with pytest.raises(ValidationError):
        synthetic_reference("policy:allow-project-status-v1", EvidenceKind.ROUTING_RULE)
    with pytest.raises(ValidationError):
        synthetic_reference("rule:project-status-v1", EvidenceKind.POLICY_RULE)


@pytest.mark.parametrize(
    "identifier",
    [
        "",
        "ab",
        f"rule:{'a' * 124}",
        " rule:project-status-v1",
        "rule:project-status-v1 ",
        "Rule:project-status-v1",
        "rule:Project-status-v1",
        "rule:with whitespace",
        "rule:with\tcontrol",
        "rule:with\nnewline",
        "1rule:project-status-v1",
        "rule:/absolute",
        r"rule:path\segment",
        r"C:\readme.md",
        "C:readme.md",
        "c:readme.md",
        "https://example.com/evidence",
        "https:example.com",
        "http:example.com",
        "file:readme.md",
        "docs/evidence.md",
        ":missing-namespace",
        "rule:",
        "rule:multiple:colons",
        "this is arbitrary user prose",
    ],
)
def test_invalid_evidence_identifiers(identifier: str) -> None:
    with pytest.raises(ValidationError):
        synthetic_reference(identifier)


def test_routing_envelope_evidence_cannot_be_empty() -> None:
    decision = route_user_input("status")
    with pytest.raises(ValidationError):
        RoutingDecisionEnvelope(decision=decision, evidence=())


def test_registry_resolves_every_r1_identifier() -> None:
    identifiers = {
        "rule:project-status-v1",
        "rule:search-public-docs-v1",
        "rule:read-public-doc-v1",
        "rule:refuse-unknown-request-v1",
        "rule:refuse-invalid-request-v1",
        "rule:refuse-invalid-arguments-v1",
    }
    assert set(R1_EVIDENCE_REGISTRY) == identifiers
    assert all(
        reference.kind is EvidenceKind.ROUTING_RULE
        and reference.provenance is EvidenceProvenance.SYNTHETIC
        for reference in R1_EVIDENCE_REGISTRY.values()
    )


def test_registry_keys_identifiers_and_inputs_are_unique() -> None:
    assert len(R1_EVIDENCE_REGISTRY) == len(set(R1_EVIDENCE_REGISTRY))
    assert all(key == reference.identifier for key, reference in R1_EVIDENCE_REGISTRY.items())
    assert len({reference.identifier for reference in R1_EVIDENCE_REGISTRY.values()}) == len(
        R1_EVIDENCE_REGISTRY
    )
    with pytest.raises(RuntimeError, match="must be unique"):
        _synthetic_evidence_registry(
            ("rule:duplicate-v1", "rule:duplicate-v1"),
            EvidenceKind.ROUTING_RULE,
        )


def test_r1_evidence_registry_is_immutable() -> None:
    with pytest.raises(TypeError):
        R1_EVIDENCE_REGISTRY["rule:injected-v1"] = synthetic_reference()  # type: ignore[index]
    with pytest.raises(ValidationError):
        R1_EVIDENCE_REGISTRY["rule:project-status-v1"].identifier = (  # type: ignore[misc]
            "rule:injected-v1"
        )


def test_unknown_routing_evidence_fails_closed_without_echo() -> None:
    marker = "rule:unknown-sensitive-marker-v1"
    decision = SuccessfulRoutingDecision(
        proposal=ProjectStatusProposal(arguments=ProjectStatusArguments()),
        evidence_references=(marker,),
    )

    with pytest.raises(EvidenceEnvelopeError) as captured:
        build_routing_decision_envelope(decision)

    assert marker not in str(captured.value)


def test_duplicate_routing_evidence_is_rejected() -> None:
    identifier = "rule:project-status-v1"
    decision = SuccessfulRoutingDecision(
        proposal=ProjectStatusProposal(arguments=ProjectStatusArguments()),
        evidence_references=(identifier, identifier),
    )
    with pytest.raises(EvidenceEnvelopeError, match="inconsistent"):
        build_routing_decision_envelope(decision)


def test_envelope_builder_does_not_accept_caller_supplied_evidence() -> None:
    assert tuple(inspect.signature(build_routing_decision_envelope).parameters) == ("decision",)


def test_envelope_builder_rejects_raw_dictionary() -> None:
    with pytest.raises(EvidenceEnvelopeError, match="validated R1 routing decision"):
        build_routing_decision_envelope({"outcome": "routed"})


def test_envelope_builder_rejects_arbitrary_object_proposal_and_subclass() -> None:
    class MarkerObject:
        def __repr__(self) -> str:
            return "PRIVATE_OBJECT_REPR_MARKER"

    class DecisionSubclass(SuccessfulRoutingDecision):
        pass

    subclass = DecisionSubclass(
        proposal=ProjectStatusProposal(arguments=ProjectStatusArguments()),
        evidence_references=("rule:project-status-v1",),
    )
    for value in (
        MarkerObject(),
        ProjectStatusProposal(arguments=ProjectStatusArguments()),
        subclass,
    ):
        with pytest.raises(EvidenceEnvelopeError) as captured:
            build_routing_decision_envelope(value)
        assert "PRIVATE_OBJECT_REPR_MARKER" not in str(captured.value)


@pytest.mark.parametrize(
    "command",
    [
        "status",
        "search docs: public routing",
        "read doc: README.md",
        "unknown public command",
        "search docs:",
        5,
    ],
)
def test_every_r1_success_and_refusal_can_be_wrapped(command: object) -> None:
    decision = route_user_input(command)
    envelope = build_routing_decision_envelope(decision)

    assert envelope.decision is decision
    assert tuple(reference.identifier for reference in envelope.evidence) == (
        decision.evidence_references
    )


def test_direct_envelope_rejects_inconsistent_evidence() -> None:
    decision = route_user_input("status")
    with pytest.raises(ValidationError):
        RoutingDecisionEnvelope(
            decision=decision,
            evidence=(synthetic_reference("rule:search-public-docs-v1"),),
        )


def test_direct_envelope_rejects_raw_nested_data_and_caller_created_evidence() -> None:
    decision = route_user_input("status")
    registered = R1_EVIDENCE_REGISTRY["rule:project-status-v1"]
    caller_created = synthetic_reference("rule:project-status-v1")

    with pytest.raises(ValidationError):
        RoutingDecisionEnvelope(
            decision=decision.model_dump(),
            evidence=(registered,),
        )
    with pytest.raises(ValidationError):
        RoutingDecisionEnvelope(
            decision=decision,
            evidence=(registered.model_dump(),),
        )
    with pytest.raises(ValidationError):
        RoutingDecisionEnvelope(
            decision=decision,
            evidence=(caller_created,),
        )


@pytest.mark.parametrize(
    "decision",
    [
        SuccessfulRoutingDecision(
            proposal=ProjectStatusProposal(arguments=ProjectStatusArguments()),
            evidence_references=("rule:refuse-unknown-request-v1",),
        ),
        RefusedRoutingDecision(
            reason=RefusalReason.UNKNOWN_REQUEST,
            evidence_references=("rule:project-status-v1",),
        ),
    ],
)
def test_success_and_refusal_evidence_cannot_be_crossed(
    decision: SuccessfulRoutingDecision | RefusedRoutingDecision,
) -> None:
    reference = R1_EVIDENCE_REGISTRY[decision.evidence_references[0]]
    with pytest.raises(ValidationError):
        RoutingDecisionEnvelope(decision=decision, evidence=(reference,))
    with pytest.raises(EvidenceEnvelopeError):
        build_routing_decision_envelope(decision)


def test_forged_refusal_issue_cannot_smuggle_caller_content() -> None:
    marker = "PRIVATE_REFUSAL_ISSUE_MARKER"
    decision = RefusedRoutingDecision(
        reason=RefusalReason.INVALID_REQUEST,
        issues=(ValidationIssue(location=("text",), code="string_type", message=marker),),
        evidence_references=("rule:refuse-invalid-request-v1",),
    )

    with pytest.raises(EvidenceEnvelopeError) as captured:
        build_routing_decision_envelope(decision)

    assert marker not in str(captured.value)


def test_refused_decision_does_not_recover_input() -> None:
    marker = "PRIVATE_REQUEST_MARKER"
    decision = route_user_input(marker)
    assert isinstance(decision, RefusedRoutingDecision)

    serialized = build_routing_decision_envelope(decision).model_dump_json()
    assert marker not in serialized
