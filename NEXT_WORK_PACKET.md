# Next Work Packet

## Human R4B authorization review

This is a human decision packet. It reviews the completed bounded experiment design and
either approves, rejects, or defers specifically named later installation and execution
actions.

It must not download, install, configure, start, or execute OpenClaw or another runtime;
create an environment, agent, session, credential, route, tool, model, or provider
connection; change WSL2, container, host, firewall, or network state; run the proof of
concept; select OpenClaw; or create the R4C runtime-selection ADR.

### Entry evidence

- `docs/experiments/R4B_ENTRY_GATE_REVIEW.md`
- `docs/experiments/R4B_AUTHORIZATION_PACKET.md`
- `docs/security/R4B_THREAT_MODEL.md`
- `docs/experiments/R4B_EXPERIMENT_RUNBOOK.md`
- `docs/experiments/R4B_TEARDOWN_AND_RESIDUE_PLAN.md`
- `docs/architecture/COUNCIL_RUNTIME_BOUNDARY.md`
- `docs/architecture/COUNCIL_RUNTIME_REQUIREMENTS.md`
- `docs/experiments/OPENCLAW_REFERENCE_RUNTIME_POC.md`
- the accepted minimum portable Council contracts and public synthetic proceeding

### Goal

Review every unchecked authorization item and determine whether the exact candidate,
dedicated-WSL2 design, data, credentials, models, routes, tools, budgets, events,
verification, comparison, stop, and teardown controls are sufficiently bounded for a
later experiment.

### Required review

- Reconfirm official OpenClaw `v2026.7.1`, immutable commit
  `2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4`, release integrity, and retrieval
  source.
- Review the MIT core license, incorporated-code notice, shipped dependency/component
  inventory, model/provider licenses and terms, and intended use. Do not infer approval
  from technical suitability.
- Accept or reject the dedicated experiment-only WSL2 design, externally enforced
  host/filesystem/network/credential/quota/budget/stop boundaries, and residual risk.
- Approve the exact public or synthetic bundle and its provenance, sanitization, and
  independent review.
- Prefer no credentials and no cloud route. If a cloud subtest is necessary, name the
  exact provider, model, endpoint class, dedicated credential scope, quota, privacy
  boundary, and USD 10 hard ceiling.
- Select exact model identifiers only after license, intended-use, privacy, capability,
  context, output, invocation, and cost review. `unselected` authorizes no invocation.
- Accept or reject the tool allowlist and denylist, depth-one worker boundary, hard
  budgets, event inventory, external corroboration, deterministic checks, equal
  dispatcher comparison, stop conditions, teardown, retained evidence, and residue
  standard.
- Name the human stop authority and distinguish installation approval from execution
  approval.

### Required result

Record exactly one:

- `approved_for_later_bounded_actions`: the external human record names the candidate,
  environment, models, routes, credentials, endpoints, tools, budgets, operators,
  stop authority, installation action, execution action, and validity period;
- `rejected`: installation and execution remain prohibited, with the reason preserved;
- `deferred`: authorization remains `not_authorized`, with the smallest unresolved
  prerequisite named.

An approval record authorizes only the exact later actions it names. The review itself
performs none of them, does not establish runtime capability or security, and does not
select OpenClaw for adoption.

### Recommended model

Use GPT-5.6 Sol High for the documentation and human-review support because the decision
combines supply-chain, licensing, threat, isolation, model/provider, evidence, budget,
and teardown judgments. Use xhigh only if the dependency-license or network-isolation
review presents a material ambiguity. The human, not the model, owns the decision.
