# Publication Index

## Purpose and authority

This is the authoritative detailed publication ledger for Local AI Guild. Root authority
documents should retain only the current facts needed for their purpose and link here
for full commit history.

A Git commit proves repository identity and content, not human authorization,
correctness, external truth, license approval, or runtime adoption. Reconciliation
commits update durable descriptions after publication; they are not substitutes for the
implementation or documentation checkpoint they describe.

## Reference namespaces

- `local-ai-guild/<sha>` identifies a commit in this repository.
- `openclaw/openclaw/<sha>` identifies an external upstream OpenClaw commit.
- A release tag is always paired with its project namespace.
- `historical` means the reference describes the state at that checkpoint.
- `current` means the reference defines the current published or executable state.
- `external` means the reference is not in Local AI Guild history.

## Local AI Guild publication ledger

| Stage or packet | Semantic role | Implementation or publication commit | Reconciliation commit | Current status | Authority document | Reference use | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Repository seed | Initial repository record before R0 | `local-ai-guild/eb42193de7dc7e6f85082f310095a52d15e78f62` | none | superseded by R0 | `VERIFICATION.md` | historical | Not the R0 control-plane checkpoint. |
| R0 | Repository control plane and minimal Python skeleton | `local-ai-guild/14f90483279b2739ea41739bdabae882666f48de` | none | published | `PROJECT_STATE.md` | historical | Establishes authority, security, verification, scripts, package skeleton, and public-repository boundary. |
| R1 | Typed tool contracts and deterministic mock router | `local-ai-guild/02f247da9821188493de7befcb54e8ecbaddd207` | `local-ai-guild/6c44970351fa2a59d78b51c8d2a441af381582ef` | published with path-contract correction | `PROJECT_STATE.md` | historical | The correction rejects colon-containing and URI-like public-document paths; it is a focused implementation fix, not a documentation-only reconciliation. |
| R2 | Typed evidence envelopes and deterministic policy checks | `local-ai-guild/903aa815a6e0176e682b4726ee8114627bd98940` | none | published | `DECISIONS.md` | historical | R2 policy outcomes remain non-executing metadata. |
| R3 | Hardened deterministic evaluation harness | `local-ai-guild/3f20d28390086619b8268e35855d4789b4a75304` | `local-ai-guild/3285d4410111f512068b33d9581ba97bc7690bd2` | published | `PROJECT_STATE.md` | historical | Reconciliation updates project state after R3 publication. |
| O2 | Hardened R2 evidence-trace validation pilot | `local-ai-guild/a79d8103ea7d2a13ac808ccf046efdf55b767d2b` | none | published | `PROJECT_STATE.md` | historical | The fixed trace is contract-valid and intentionally incomplete for publication-approval evidence. |
| R4A documentation | Portable Council/runtime boundary and OpenClaw evaluation design | `local-ai-guild/7e42066a882532f861038d7381a3c3727d2982ca` | `local-ai-guild/c68632b27802924b94e135f61ed153a4dd6c4485` | published; documentation only | `docs/architecture/COUNCIL_RUNTIME_BOUNDARY.md` | historical | The reconciliation records that R4A documentation was completed ahead of O3 without advancing runtime execution. |
| O3 | Public synthetic handoff-completeness experiment | `local-ai-guild/a307d1274a88a64ed6dd9a334f4f757f6d67ed80` | `local-ai-guild/a3e6facaf77153486236ebea5b4a383d216e7bcf` | published | `docs/experiments/O3_SYNTHETIC_HANDOFF.md` | historical | Reconciliation updates README and project state after O3 publication. |
| Minimum portable Council contracts | Strict portable Council contracts, fixture, validator, and tests | `local-ai-guild/6fe01f7dd0d756a757bea8213803f0e23c42bfab` | `local-ai-guild/be922ae6a047dec21be78c8815181611f67bd41e`; `local-ai-guild/9d0e2a225f4b9c41ac4f41a8ae125c4e9ad98e11` | published and accepted as current executable checkpoint | `docs/architecture/COUNCIL_RUNTIME_BOUNDARY.md` | current executable | The two reconciliation commits correct and finalize the published-state description; neither replaces the executable checkpoint. |
| R4B entry-gate review | Documentation-only six-gate review | `local-ai-guild/f49d6f26c712c451efc496b1f35f389422651c2e` | none | published; recommendation permits only proposing a bounded packet | `docs/experiments/R4B_ENTRY_GATE_REVIEW.md` | historical | Does not authorize installation, execution, selection, or adoption. |
| Bounded R4B authorization package | Authorization question, threat model, runbook, events, controls, and teardown design | `local-ai-guild/2984cecbf52bdf356d84c559bb49db13dc8bab9c` | `local-ai-guild/3cd6a30234e21ce9632cbc32943de810c8235bae` | published; `not_authorized` | `docs/experiments/R4B_AUTHORIZATION_PACKET.md` | historical | This commit contains the bounded authorization package, not merely the entry-gate review. |
| R4B publication-reference corrections | Correct the authorization-package publication description | `local-ai-guild/79ca62e3d779f5713b5cf4f0ed898be1c9d88110` | `local-ai-guild/c779ea815490ec14b9f6357729b46087235c03ba` | published | `PROJECT_STATE.md` | current reconciliation | These are documentation corrections, not R4B implementation or authorization checkpoints. |
| Current published baseline | Latest published Local AI Guild commit | `local-ai-guild/c779ea815490ec14b9f6357729b46087235c03ba` | none | current published baseline | `PROJECT_STATE.md` | current | Subject: `docs: finish R4B reference corrections`. No later packet identity is inferred before publication. |
| Current executable checkpoint | Latest accepted executable behavior | `local-ai-guild/6fe01f7dd0d756a757bea8213803f0e23c42bfab` | see Council-contract reconciliations above | current | `PROJECT_STATE.md` | current executable | The CLI remains at `Portable Council contracts checkpoint`; later R4B work is documentation only. |

## External candidate ledger

| External project | Release | External immutable commit | Release date | Status in Local AI Guild | Authority document | Reference use | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OpenClaw | `openclaw/openclaw/v2026.7.1` | `openclaw/openclaw/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4` | 2026-07-13 | candidate only; not selected, approved, adopted, installed, configured, or executed | `docs/experiments/R4B_AUTHORIZATION_PACKET.md` | external | This SHA is not a Local AI Guild commit. It identifies the proposed upstream candidate evaluated by documentation review. |

## Current publication invariants

- Current published Local AI Guild baseline:
  `c779ea815490ec14b9f6357729b46087235c03ba`.
- Current executable checkpoint:
  `6fe01f7dd0d756a757bea8213803f0e23c42bfab`.
- Bounded R4B authorization-package publication:
  `2984cecbf52bdf356d84c559bb49db13dc8bab9c`.
- R4B authorization status: `not_authorized`.
- Human R4B decision: `pending`.
- OpenClaw remains an external candidate; no R4B runtime experiment has executed.

## Reconciliation rule

After a future packet is committed and pushed, a publication reconciliation must:

1. record the exact new Local AI Guild commit and semantic role in this ledger;
2. update the current published baseline only after the remote publication is verified;
3. keep the implementation or documentation checkpoint distinct from any follow-up
   reconciliation commit;
4. update concise current-state summaries that name the previous baseline;
5. preserve historical verification references exactly as evidence of their original
   runs.

No future commit identity is predicted in advance.
