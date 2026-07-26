# O3 Synthetic Handoff Completeness Experiment

This is a public, repository-authored synthetic experiment. The packet, artifacts,
verification, approval, commit, and publication described below are fictional claims
created only to exercise the O2 trace contracts and validator. They do not assert that
the fictional work occurred, that its artifact exists, or that its zero Git object
identifier identifies a real commit.

## Synthetic completed packet

### Goal

Publish deterministic documentation metadata in a stable key-and-value format.

### Requirements

- Claim one documentation metadata artifact.
- Use only public or synthetic content.

### Constraints

- Use harmless fictional repository documentation or deterministic metadata.
- Perform no runtime, model, routing, retrieval, persistence, execution, or external
  inspection.
- Treat every statement in this packet as an experiment assertion rather than external
  truth.

### Decisions

The fictional packet claims that a stable key-and-value format was selected. The trace
represents that decision with a bounded decision record. It does not claim a real human
selected or approved the format.

### Claimed implementation artifacts

The packet claims that `docs/synthetic/packet-metadata.md` was created. That path is
intentionally only trace metadata; O3 does not create or inspect the fictional artifact.

### Claimed verification

The packet claims a deterministic pytest result verified the fictional artifact and the
synthetic-data requirement. The claim is part of the fixture. O3 does not run that
fictional test or prove artifact existence.

### Approval gate

Publication is represented as requiring an explicit human instruction. The trace
deliberately declares that both the authority evidence and approval evidence are absent
from the repository.

### Publication state

The packet claims a published state through a fictional all-zero Git object identifier.
The commit record publishes the packet but omits the artifact even though the artifact
points to that commit.

### Next action

The fictional handoff points to a proposed portable Council contract checkpoint and
also names a deliberately absent blocker. This experiment does not authorize that
checkpoint or R4B.

## Deliberately planted handoff defects

The trace is contract-valid TOML. Its five defects are semantic:

1. The required explicit-human authority has no repository evidence.
2. The publication gate has no first-class approval evidence.
3. The next action has a dangling `blocked_by` relationship.
4. The artifact's `verified_by` relationship targets an authority record rather than a
   verification result.
5. The artifact points to the fictional commit, but the commit does not reciprocally
   publish the artifact.

The existing validator detects the first four. Its current semantics validate the
artifact's `published_in` target type but do not require a reciprocal `publishes` edge,
so the fifth defect is manual-only. No new validator rule was added because O3 is a
comparison experiment and the missing reciprocal rule should not be introduced without
a separately justified contract decision.

## Manual review assertion

The manual findings are an immutable Python tuple authored in
`src/local_ai_guild/o3_experiment.py`. They are experiment expectations, not an
observation from an external reviewer and not proof of real-world facts. The comparison
key is only the finding code, subject identifier, and relationship; free-form messages
are excluded.

The manual assertion contains five findings:

- `missing_authority_evidence`
- `missing_approval_evidence`
- `dangling_reference`
- `wrong_target_type`
- `missing_required_relationship` for the non-reciprocal publication edge

## Official deterministic result

The unchanged O2 validator returns seven findings:

- Four error findings matching the first four planted defects.
- `commit_does_not_prove_authorization`.
- `commit_does_not_prove_correctness`.
- `repository_assertion_not_external_truth`.

The last three are informational scope boundaries rather than additional planted
structural defects.

## Official comparison result

`run_o3_handoff_experiment()` returns:

- Manual findings: 5
- Validator findings: 7
- Matched findings: 4
- Manual-only findings: 1
- Validator-only findings: 3

Combining manual and deterministic review improves this synthetic handoff check: the
validator consistently catches four structural defects and supplies three epistemic
caveats, while manual review catches the reciprocal publication gap outside the
validator's current semantics. The result does not manufacture complete agreement.

## Limits

The fixed loader reads only `docs/traces/o3-synthetic-handoff.toml` and accepts no
caller path. Parsing and validation are bounded and in memory after that single read.
The experiment does not resolve citations, inspect Git, inspect artifact paths, verify
human identity, authenticate approval, establish external truth, or prove general
ontology correctness. It performs no mutation or persistence and retains no raw TOML,
packet prose, paths, or parser errors in its comparison result.

No runtime, model, OpenClaw component, routing, retrieval, cloud service, persistence,
or tool execution was installed, configured, or used.
