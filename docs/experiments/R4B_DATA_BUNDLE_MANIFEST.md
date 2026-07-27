# R4B Proposed Data-Bundle Manifest

## Status and boundary

Bundle approval: `pending`

Authorization status: `not_authorized`

This is the exact proposed source inventory for a later R4B pre-run bundle. It does not
stage, copy, freeze, approve, or authorize use of any file. Final SHA-256 digests must be
generated only after the human-approved source revisions are frozen during the later
pre-run phase.

Only repository-owned public or synthetic material is eligible. The bundle excludes
corporate, proprietary, government, military, client, contract, work-derived, personal,
health, financial, email, message, browser, home-directory, local-secret, production,
credential, private-network, and unclear-provenance material.

## Bundle roles

- `member_a` and `member_b`: independent Council-member roles.
- `security_adversary`: bounded threat and control review.
- `evidence_auditor`: provenance, completeness, and claim review.
- `dispatcher`: OpenClaw adapter or custom-dispatcher path under identical policy.
- `external_verifier`: deterministic process outside runtime authority.
- `human_operator`: approval and unconditional stop authority.

## Proposed manifest

`TBD_PRE_RUN_SHA256` is a required later value, not a wildcard. Any source change after
digest generation invalidates the bundle and requires regeneration plus human review.

| File path | Semantic purpose | Classification | Provenance | Expected SHA-256 | Sanitization status | Approval status | Allowed roles | Teardown disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `docs/experiments/R4B_DATA_BUNDLE_MANIFEST.md` | Authoritative allowlist for bundle construction | public | repository-authored R4B control document | `TBD_PRE_RUN_SHA256` | current public-boundary review complete; final scan pending | pending | all roles; dispatcher; verifier; human | retain repository original and approved durable copy; destroy runtime copies |
| `docs/experiments/R4B_AUTHORIZATION_PACKET.md` | Decision question, scope, alternatives, roles, policies, budgets, events, and stop boundary | public | repository-authored authorization design | `TBD_PRE_RUN_SHA256` | current public-boundary review complete; final scan pending | pending | all roles; dispatcher; verifier; human | retain approved durable copy; destroy runtime copies |
| `docs/security/R4B_THREAT_MODEL.md` | Experiment-specific assets, trust boundaries, threats, controls, evidence, and residual risk | public | repository-authored security design | `TBD_PRE_RUN_SHA256` | current public-boundary review complete; final scan pending | pending | security adversary; evidence auditor; members after independent-position freeze; verifier; human | retain approved durable copy; destroy runtime copies |
| `docs/experiments/R4B_EXPERIMENT_RUNBOOK.md` | Proposed phases, required events, deterministic checks, and comparison dimensions | public | repository-authored experiment design | `TBD_PRE_RUN_SHA256` | current public-boundary review complete; final scan pending | pending | dispatcher; security adversary; evidence auditor; verifier; human; members receive only phase-relevant extracts | retain approved durable copy; destroy runtime copies |
| `docs/experiments/R4B_TEARDOWN_AND_RESIDUE_PLAN.md` | Required removal, retained evidence, residue inspection, and failure handling | public | repository-authored teardown design | `TBD_PRE_RUN_SHA256` | current public-boundary review complete; final scan pending | pending | security adversary; evidence auditor; verifier; human | retain approved durable copy; destroy runtime copies |
| `docs/architecture/COUNCIL_RUNTIME_BOUNDARY.md` | Portable Council/runtime ownership and adapter-operation boundary | public | accepted repository architecture | `TBD_PRE_RUN_SHA256` | existing public repository content; final scan pending | pending | all roles; dispatcher; verifier; human | retain approved durable copy; destroy runtime copies |
| `docs/architecture/COUNCIL_RUNTIME_REQUIREMENTS.md` | Objective runtime requirements and six adoption gates | public | accepted repository architecture | `TBD_PRE_RUN_SHA256` | existing public repository content; final scan pending | pending | all roles; dispatcher; verifier; human | retain approved durable copy; destroy runtime copies |
| `docs/experiments/OPENCLAW_REFERENCE_RUNTIME_POC.md` | Candidate mapping, minimum flow, comparison question, and decision boundary | public | repository-authored R4A experiment design | `TBD_PRE_RUN_SHA256` | existing public repository content; final scan pending | pending | all roles; dispatcher; verifier; human | retain approved durable copy; destroy runtime copies |
| `docs/research/R4B_OPENCLAW_LICENSE_REVIEW.md` | Bounded candidate, dependency, Node, and container-license evidence | public | repository-authored review of cited official sources | `TBD_PRE_RUN_SHA256` | current citation and public-boundary scan complete; final pre-run scan pending | pending; legal acceptance separate | evidence auditor; security adversary; human; members after independent-position freeze | retain approved durable copy; destroy runtime copies |
| `src/local_ai_guild/council_contracts.py` | Accepted portable Council schemas | public source | published Local AI Guild implementation | `TBD_PRE_RUN_SHA256` | existing public repository source; final scan pending | pending for experiment bundle | dispatcher; external verifier; evidence auditor; human | retain repository source and approved durable copy; destroy runtime copies |
| `src/local_ai_guild/council_fixture.py` | Existing public synthetic proceeding and role/packet examples | synthetic | repository-authored fixed fixture | `TBD_PRE_RUN_SHA256` | synthetic and public; final scan pending | pending for experiment bundle | dispatcher; external verifier; evidence auditor; human; members receive only approved packet/evidence extracts | retain repository source and approved durable copy; destroy runtime copies |
| `src/local_ai_guild/council_validation.py` | Existing deterministic portable-contract validator | public source | published Local AI Guild implementation | `TBD_PRE_RUN_SHA256` | existing public repository source; final scan pending | pending for experiment bundle | external verifier; evidence auditor; human | retain repository source and approved durable copy; destroy runtime copies |
| `tests/test_council_contracts.py` | Deterministic accepted-contract test evidence and negative cases | public source and synthetic tests | published Local AI Guild tests | `TBD_PRE_RUN_SHA256` | existing public repository tests; final scan pending | pending for experiment bundle | external verifier; evidence auditor; security adversary; human | retain repository source and approved durable copy; destroy runtime copies |

## Derived structured packet

The later pre-run process must create one strict `CouncilWorkPacket` from the exact
decision question and limits in `R4B_AUTHORIZATION_PACKET.md`. It must:

- use new Council-owned identifiers rather than runtime IDs;
- contain no new factual evidence, host details, free-form credentials, or paths;
- preserve the same question, alternatives, exclusions, budgets, evidence requirements,
  and human approval separation;
- validate against the accepted contract before delivery;
- receive its own final SHA-256 digest and manifest row before execution.

That derived packet does not yet exist and is not implicitly approved by this manifest.
Its generation is a later pre-run action after human authorization.

## Role-disclosure boundary

- Both Council members receive identical packet and approved public/synthetic evidence.
- Neither member receives peer work, threat-model conclusions, license conclusions, or
  auditor conclusions before both independent positions are externally frozen.
- The security adversary receives only sanitized effective-control evidence and approved
  artifacts; no host inventory, secret, or credential value enters the model context.
- The evidence auditor receives bounded source locators and sanitized exports, not raw
  runtime logs or host details.
- The runtime receives no human-decision authority, credential value, private source, or
  repository write access.

## Pre-run approval and digest procedure

Before any later execution, the data owner and independent reviewer must:

1. resolve every file to the exact human-approved Local AI Guild commit;
2. confirm each path is tracked, public, and unchanged from that commit;
3. run credential, private-address, user-path, internal-endpoint, and sensitive-data
   scans;
4. review provenance and every scan exception manually;
5. generate SHA-256 digests and replace every `TBD_PRE_RUN_SHA256`;
6. add and validate the derived structured packet;
7. record data-owner approval, independent sanitization review, and bundle approval
   outside the runtime;
8. construct a read-only bundle and verify its digest after staging.

Any unexpected file, unresolved scan hit, path outside this table, digest mismatch,
unclear provenance, or sensitive material stops bundle construction.

## Retention and destruction

Repository originals remain public repository content. Approved Council artifacts,
sanitized bounded event export, deterministic verification, routing/cost report,
security and evidence reviews, teardown evidence, and the human decision may be retained
only under the teardown plan.

All role copies, writable workspaces, model inputs/outputs not promoted to approved
Council artifacts, raw logs, temporary exports, caches, session state, memory, derived
runtime configuration, and staging areas must be destroyed. Post-run inspection must
reconcile retained files against the approved durable-evidence allowlist.
