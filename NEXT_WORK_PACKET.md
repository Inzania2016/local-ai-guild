# Next Work Packet

## R4B local-model capability benchmark

This is a documentation-first benchmark-design packet for the conditionally qualified
route `r4b-local-qwen25-coder-7b-q4km-v1`.

It must freeze the route and predeclare a minimal public/synthetic benchmark and
acceptance thresholds before any inference. It does not authorize OpenClaw
installation, OpenClaw execution, model adoption, or production use.

### Authorization boundary

The packet must not start Ollama, load or invoke the model, or execute benchmark
inference unless a separate explicit human record authorizes those exact actions after
the benchmark design is complete.

Without that later action-specific authorization, the packet stops after documentation,
fixture, threshold, and deterministic-verifier preparation.

It must never:

- download, pull, import, convert, quantize, train, or modify a model;
- substitute `latest` or another artifact;
- use cloud routing or credentials;
- use private, work-derived, personal, client, government, production, or unclear-
  provenance data;
- create WSL2, VM, container, firewall, network, provider, or OpenClaw state;
- install or execute OpenClaw;
- authorize broader R4B installation or execution;
- select or adopt OpenClaw or the model;
- change authorization from `not_authorized`, change the human decision from
  `pending`, or check a human authorization item.

### Frozen route

```text
Route plan: r4b-local-qwen25-coder-7b-q4km-v1
Artifact: ollama-registry/qwen2.5-coder:7b
Manifest digest: sha256:dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364
Model-layer digest: sha256:60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463
Config digest: sha256:d9bb33f2786931fea42f50936a2424818aa2f14500638af2f01861eb2c8fb446
License digest: sha256:832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e
Context ceiling: 8,192 total tokens
Output ceiling: 2,048 tokens
Cloud: disabled
Credentials: none
```

Any digest or route mismatch fails closed.

### Required benchmark design

Use a minimal repository-owned public/synthetic case set. Define measurable thresholds
before inference for:

- instruction and packet comprehension;
- strict schema/format compliance;
- evidence citation and unsupported-claim rejection;
- independently frozen positions;
- cross-review without premature disclosure;
- preservation of material dissent;
- security-adversary boundary analysis;
- evidence and provenance auditing;
- repeated-run consistency;
- memory, process, context, and wall-clock viability.

Define deterministic scoring and redaction-safe results before any model output exists.
Do not make thresholds easier after observing results.

### Role and comparison boundary

Use the same exact route for:

- Council member A;
- Council member B;
- security adversary;
- evidence auditor;
- the later OpenClaw candidate path; and
- the equivalent custom-dispatcher path.

Externally enforce separate sessions, frozen positions, no cross-session memory, and
identical packet delivery. Record that this is procedural independence only and not
model diversity.

### Required decision before inference

A named human must separately record:

- exact runtime-start and inference actions;
- operator and stop authority;
- accepted model/license and reduced-context conditions;
- approved public/synthetic fixtures and digests;
- invocation allocation and wall-clock limits;
- process, memory, route, credential, and no-cloud controls;
- teardown and retained-evidence requirements;
- validity period.

Repository publication is not that authorization.

### Required result

The design packet must record one of:

- `ready_for_separate_benchmark_authorization`;
- `deferred` with the smallest unresolved design or control gap; or
- `rejected` with rationale.

If separately authorized inference later occurs, capability results must remain distinct
from runtime-mechanics, OpenClaw-adoption, production, and general-use claims.

### Recommended model

Use GPT-5.6 Sol High for benchmark design, threshold definition, evidence schemas, and
security review. Use xhigh only if the deterministic scoring or route-symmetry design
contains a material unresolved contradiction. No AI runtime is required to design the
packet.
