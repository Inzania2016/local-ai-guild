# Next Work Packet

## Proposed bounded R4B authorization-and-experiment-design packet

This is a proposed documentation and review packet. It requires explicit human approval
before work begins. It does not authorize runtime installation or execution.

### Goal

Turn the accepted portable Council contracts and completed R4B entry-gate review into one
fully bounded, independently reviewable experiment specification. The packet must close
or explicitly reject every prerequisite before asking a human whether a later OpenClaw
POC may be installed and executed.

### Entry evidence

- `docs/experiments/R4B_ENTRY_GATE_REVIEW.md`
- `docs/architecture/COUNCIL_RUNTIME_BOUNDARY.md`
- `docs/architecture/COUNCIL_RUNTIME_REQUIREMENTS.md`
- `docs/architecture/SECURITY_BOUNDARIES.md`
- `docs/experiments/OPENCLAW_REFERENCE_RUNTIME_POC.md`
- the accepted minimum portable Council contracts and synthetic proceeding

### In scope

- Finalize an experiment-specific threat model and residual-risk statement.
- Select and document one WSL2 or VM isolation design.
- Define independent host, network, filesystem, credential, approval, and audit controls.
- Define teardown, retained-artifact, residue-inspection, and failure procedures.
- Identify one precise eligible OpenClaw version through authorized current research.
- Complete a version-specific license and intended-use review without approving adoption.
- Freeze the public or synthetic input bundle and provenance review.
- Decide whether credentials are avoidable; otherwise specify dedicated revocable test
  credentials requiring human authorization.
- Define the exact model list and deny-by-default local/cloud routing policy.
- Define the exact tool allowlist and denylist.
- Fix subagent depth at one and specify depth-two denial.
- Set message, token, time, worker, and cost budgets.
- Freeze the required runtime-event inventory, schema, ordering, omissions, and redaction.
- Specify deterministic verification and independent observation procedures.
- Name the human stop authority and every immediate stop condition.
- Define the smaller custom-dispatcher comparison baseline and value criteria.
- Produce a final explicit approval request for later installation and execution.

### Out of scope

- Installing, downloading, configuring, or executing OpenClaw or another runtime.
- Configuring or invoking a model, provider, tool, credential, worker, or cloud route.
- Implementing an adapter, dispatcher, event ingester, or verification script.
- Running capability, security, routing, cost, teardown, or comparison tests.
- Selecting or adopting OpenClaw.
- Creating a runtime-selection ADR.
- Changing the accepted portable Council contracts.

### Required result

The packet must end with one of:

- a complete bounded experiment specification ready for a separate explicit human
  installation-and-execution authorization;
- a list of specific unresolved blockers and the smallest follow-up review;
- rejection of the candidate experiment because risk, license, isolation, or teardown
  requirements cannot be met.

Completing the design does not itself permit installation or execution.

### Recommended model

Use GPT-5.6 Sol High because the packet combines threat modeling, isolation, licensing,
runtime-version review, security controls, evidence design, and authorization boundaries.
Medium is sufficient only after version, license, isolation, and teardown decisions are
already fixed and independently reviewed.
