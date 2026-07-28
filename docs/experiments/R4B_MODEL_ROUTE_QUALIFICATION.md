# R4B Model Route Qualification

## Result and authority boundary

Qualification result: `conditionally_qualified_for_benchmark`

Authorization status: `not_authorized`

Human decision: `pending`

This result qualifies one immutable local route for a later bounded capability
benchmark. It does not authorize loading or invoking the model, starting a runtime,
creating an environment, installing or executing OpenClaw, or adopting any runtime or
model. No human authorization item is checked.

## Entry evidence

- `docs/research/R4B_LOCAL_MODEL_INVENTORY.md`
- `docs/research/R4B_LOCAL_MODEL_LICENSE_REVIEW.md`
- `docs/experiments/R4B_HUMAN_AUTHORIZATION_REVIEW.md`
- `docs/experiments/R4B_AUTHORIZATION_PACKET.md`
- `docs/architecture/COUNCIL_RUNTIME_BOUNDARY.md`
- `docs/architecture/COUNCIL_RUNTIME_REQUIREMENTS.md`
- accepted portable Council contracts, fixture, validator, and tests

## Machine context

The packet uses the human-declared profile:

```text
Windows 11 Home
Intel Core i7-9700F, 8 cores / 8 threads
32 GB system memory
AMD Radeon RX 6700 XT
12 GB GPU memory
Ollama and LM Studio installed
```

This is declared context, not a performance measurement. No acceleration backend,
driver behavior, memory allocation, model load, or inference was tested.

## Candidate disposition

| Candidate | Identity | Provenance/license | Static fit | Disposition |
| --- | --- | --- | --- | --- |
| Ollama `qwen2.5-coder:7b` Q4_K_M | exact local manifest and every blob hash confirmed; manifest matches official registry | official Ollama distribution linked to official Qwen model and byte-identical Apache-2.0 license; exact conversion source revision absent | `plausible_with_reduced_context` | selected only for the conditional benchmark route |
| Ollama `qwen2.5-coder:latest` | exact bytes currently equal 7B | same | same | rejected as a floating identifier |
| Ollama `qwen2.5-coder:14b` | missing config and model blobs | unresolved artifact | incomplete | `artifact_incomplete`; excluded |
| Ollama `qwen3-coder:30b` | every referenced blob missing | unresolved artifact and license | incomplete and declared weights exceed GPU memory | `artifact_incomplete`; excluded |
| LM Studio Qwen2.5-Coder-7B-Instruct Q5_K_M | local hash exactly matches Hugging Face LFS object at conversion revision `10ba8b9be9729feb1d3c476d014c861dbfc01177` | Apache-2.0 card and official Qwen base link; exact base revision used for conversion absent | `plausible_with_reduced_context` | exact alternate artifact, not selected |

## Static hardware-fit assessment

### Architecture basis

The reviewed official Qwen config declares 28 layers, hidden size 3,584, 28 attention
heads, and 4 key/value heads. Head dimension is therefore 128.

For risk estimation only, an unquantized FP16 key/value cache would require roughly:

```text
28 layers × 4 KV heads × 128 dimensions × 2 for K and V × 2 bytes
= 114,688 bytes per token
```

This is about:

- 0.875 GiB for one 8,192-token active context;
- 2.56 GiB for one 24,000-token active context;
- 3.5 GiB for one 32,768-token active context.

Actual runtimes may use different cache types, padding, batching, allocation, and
offload. The estimate is a conservative planning aid, not measured memory use.

### Ollama Q4_K_M

- Artifact/weight-file floor: 4,683,074,048 bytes, about 4.36 GiB.
- CPU-only feasibility: plausible within declared 32 GB system memory at reduced
  context, but throughput and latency are unknown.
- GPU offload: capacity appears plausible for one reduced active context within 12 GB
  VRAM, but full offload, AMD acceleration, Vulkan/ROCm support, and stability are
  unverified.
- System-memory pressure: plausible for the bounded benchmark; multiple retained
  contexts and runtime buffers can materially increase use.
- VRAM pressure: one 8,192-token estimated FP16 KV cache plus weight bytes is about
  5.24 GiB before runtime and compute buffers. Four resident contexts would add about
  3.5 GiB total KV cache. At the previous 24,000-token proposal, four resident caches
  alone would be about 10.25 GiB and would not fit with the weights in 12 GB VRAM.
- Upstream default-config context: 32,768 tokens.
- Upstream advertised extended context: 131,072 only with a YaRN configuration change,
  which is outside this packet.
- Proposed R4B context ceiling: 8,192 total tokens per invocation.
- Proposed output ceiling: 2,048 tokens within that total context.
- Classification: `plausible_with_reduced_context`.

### LM Studio Q5_K_M

- Artifact/weight-file floor: 5,444,831,744 bytes, about 5.07 GiB.
- CPU-only feasibility: plausible within declared 32 GB system memory at reduced
  context; unmeasured.
- GPU offload: capacity appears plausible for one reduced context, but LM Studio backend
  selection, AMD support, offload fraction, and stability are unverified.
- VRAM pressure: higher than the Q4_K_M route by about 0.71 GiB before runtime buffers.
- Proposed context and output ceilings if separately evaluated: 8,192 and 2,048.
- Classification: `plausible_with_reduced_context`.

Artifact fit does not establish acceptable latency, tokens per second, acceleration,
context reliability, instruction following, quality, or stability.

## Council-role capability requirements

The later benchmark must test, rather than assume:

- structured packet comprehension;
- strict schema and format following;
- evidence-linked claims;
- independently frozen positions;
- cross-review without premature disclosure;
- preservation of material dissent;
- adversarial boundary analysis;
- provenance and evidence auditing;
- repeated-run consistency;
- memory and runtime viability at the frozen limits.

Static artifact inspection establishes none of these capabilities.

## Single-model independence assessment

One exact model may support a runtime-mechanics benchmark if external controls provide
procedural independence:

- separate role sessions and workspaces;
- identical independent packet delivery;
- no cross-session memory;
- both member positions frozen before peer disclosure;
- identical route and limits for the OpenClaw and custom-dispatcher paths;
- external event and artifact verification.

This is **procedural independence only**. It is not model diversity.

Using one model for all four roles creates correlated-failure risk:

- shared blind spots and training biases;
- shared schema or formatting failures;
- shared hallucination and unsupported-citation tendencies;
- shared evidence-selection bias;
- reduced adversarial independence;
- reduced value from an auditor that may repeat the same reasoning failure.

The later benchmark may evaluate runtime mechanics under that limitation. It must not
claim independent model judgment, ensemble diversity, or broad Council robustness.

## Heterogeneous-route assessment

A heterogeneous route is not presently justified.

The LM Studio and Ollama artifacts use different quantizations and distribution
packages, but both identify Qwen2.5-Coder-7B-Instruct as the underlying family. Different
quantization is not evidence of a different training distribution or independent blind
spots. The LM Studio conversion also has a longer community provenance chain.

Using the second artifact would add route and runtime variables without adding
meaningful model diversity. It could also confound the required OpenClaw versus
custom-dispatcher comparison. Both later runtime paths must therefore use the same exact
single-model route.

## Exact conditional route plan

```text
Route plan: r4b-local-qwen25-coder-7b-q4km-v1
Artifact: ollama-registry/qwen2.5-coder:7b
Manifest digest: sha256:dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364
Model-layer digest: sha256:60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463
Config digest: sha256:d9bb33f2786931fea42f50936a2424818aa2f14500638af2f01861eb2c8fb446
License digest: sha256:832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e
Upstream identity: Qwen/Qwen2.5-Coder-7B-Instruct
Distribution: official Ollama qwen2.5-coder:7b manifest
Runtime: Ollama
Quantization: Q4_K_M
Roles: Council member A; Council member B; security adversary; evidence auditor
Runtime paths: OpenClaw candidate path and equivalent custom-dispatcher path
Allowed data: approved repository-owned public or synthetic bundle only
Context ceiling: 8,192 total tokens per invocation
Output ceiling: 2,048 tokens within the context ceiling
Invocation ceiling: 10 planned per path; 12 hard maximum per path
Sampling: unresolved until benchmark thresholds are defined
Cloud: disabled
Credentials: none
Capability status: untested
```

The route is local-only. The deterministic dispatcher and verifier use no model.

### Fail-closed conditions

The route fails qualification if:

- any manifest, model, config, template, system, or license digest differs;
- any referenced blob is absent;
- `latest` or another floating tag is substituted;
- the runtime resolves a different model identity;
- the route is unavailable without download, import, conversion, or configuration
  change;
- input plus reserved output exceeds 8,192 tokens;
- more than the approved invocation allocation is requested;
- a cloud route, provider connection, or credential appears;
- the OpenClaw and custom-dispatcher paths differ;
- unapproved data enters the packet;
- human license acceptance or benchmark authorization is absent.

### Named conditions

1. A human or authorized legal reviewer must accept the Apache-2.0 and official Ollama
   redistribution posture.
2. A human must accept the reduced 8,192/2,048 per-invocation limits as an explicit
   amendment to the earlier 24,000/4,000 proposal.
3. The benchmark must freeze the exact route and verify every digest before runtime
   start.
4. The benchmark must not rely on GPU acceleration; CPU fallback and actual
   memory/runtime viability remain test outcomes.
5. The benchmark must label the single-model correlated-failure limitation.
6. Separate human authorization is required before starting Ollama or invoking the
   model.

## Qualification rationale

The local artifact has immutable identity, complete hash-verified content, exact
official Ollama registry correspondence, an authoritative Qwen lineage, an exact
Apache-2.0 license match, and plausible static fit at a reduced context. No runtime
action is needed to resolve its identity.

The result is conditional because legal acceptance, the reduced context amendment,
actual runtime availability, hardware behavior, and every role capability remain
unverified.

## Benchmark-readiness boundary

The smallest next packet is **R4B local-model capability benchmark**. It must first
design one minimal public/synthetic case set and predeclare acceptance thresholds for
format compliance, evidence citation, frozen positions, cross-review, dissent,
adversarial analysis, evidence audit, repeatability, memory, and runtime viability.

That packet must obtain separate human authorization before it starts Ollama or invokes
the model. It must not install or execute OpenClaw, authorize R4B runtime installation,
or treat benchmark success as production qualification.
