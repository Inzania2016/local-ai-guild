# R4B Teardown and Residue Plan

## Status

Authorization status: `not_authorized`

This is a proposed closeout specification. It does not authorize creating or removing a
WSL2 distribution, container, credential, rule, file, process,
runtime, cache, or other state. The later human authorization must name the environment,
destructive targets, retained evidence, operators, and deletion authority before any
teardown action.

Incomplete teardown is an experiment failure. It blocks R4C even when the Council flow,
runtime, and comparison otherwise appear successful.

## Objectives

Teardown must:

1. stop all experiment computation and access;
2. revoke every experiment credential and route;
3. remove or invalidate all runtime, role, session, workspace, memory, cache,
   configuration, temporary, mount, listener, and network state;
4. preserve only explicitly approved, sanitized, runtime-independent evidence;
5. inspect the Windows host, isolation environment, external services, repository, and
   ignored files against the pre-run baseline;
6. record every disposition and unresolved residue without relying only on runtime logs.

## Preconditions

Before teardown, the named operator must have:

- the exact authorization and stop record;
- the pre-run host and environment baseline;
- the WSL2 distribution, runtime, component, credential, endpoint, mount, workspace, cache,
  process, listener, and generated-file manifests;
- the approved durable-evidence allowlist and digests;
- externally validated copies of evidence that must survive;
- exact independently resolved teardown targets;
- a safe quarantine path for ambiguous state;
- the credential custodian and infrastructure operator available;
- a rule that unknown, broad, or unresolved targets are not deleted until a human
  resolves them.

If required evidence cannot be exported and validated safely, stop and classify the run
as failed. Do not retain the runtime merely to conceal an evidence-portability failure.

## Removal or invalidation inventory

| Item | Required disposition | Evidence |
| --- | --- | --- |
| Runtime processes | Terminate and prove absent | Pre/post process inventory and termination events |
| Containers | Stop and remove experiment containers, writable layers, volumes, and experiment-only networks | Engine inventory, object identities, pre/post comparison |
| WSL2 distribution | Remove after evidence export unless the human explicitly authorizes bounded quarantine or retention | Exact distribution identity, destruction or retention authorization, host inventory |
| Runtime installation | Remove with the environment or prove no installed files remain outside it | Installed-file/package manifest reconciliation |
| Runtime workspaces | Destroy all role and shared staging workspaces except approved exported evidence | Workspace manifest and filesystem scan |
| Agent state | Destroy role, worker, identity, queue, and task state | Runtime/state inventory plus filesystem inspection |
| Sessions | Terminate and remove session/transcript state not on the evidence allowlist | Session inventory and absence result |
| Runtime memory | Remove local/global memory indexes, stores, embeddings, summaries, and caches | Memory-store inventory and filesystem/database inspection |
| Experiment model caches | Remove model weights, adapters, tokenizer files, compiled kernels, and provider caches created for R4B | Pre/post cache inventory and storage reconciliation |
| Temporary files | Remove experiment temp, spool, lock, socket, PID, download, extraction, and crash files | Temp-root inventory and scan |
| Dedicated credentials | Revoke, rotate, or delete immediately | Provider/secret-store record and failed-use confirmation where safe |
| Tokens and provider keys | Invalidate all access and refresh material; remove local copies | Provider-side audit and secret scan |
| Network rules | Remove experiment-only allowlists, routes, proxies, port mappings, and DNS exceptions | Pre/post effective network-policy comparison |
| Network listeners | Terminate and prove no experiment listener remains | Independent listener inventory |
| Mounted directories | Unmount and remove experiment mount declarations or mappings | Pre/post mount inventory |
| Export staging areas | Move approved evidence to durable storage, then destroy staging and rejects | Digest reconciliation and staging absence |
| Operational logs | Preserve only approved sanitized event export; remove logs with secrets, host details, raw prompts, or unapproved content | Log manifest, redaction review, content scan |
| Generated runtime configuration | Remove secrets, route config, agent config, permissions, skills, startup, provider, and gateway files | Configuration manifest and filesystem scan |
| Services and startup entries | Disable/remove any experiment service, task, daemon, startup entry, or auto-restart state | Service/task/startup pre/post inventory |
| Custom-dispatcher state | Remove with the same standard as candidate runtime state | Component, file, process, session, and workspace reconciliation |

Deletion inside the wrong boundary is not acceptable evidence. Target identity must be
resolved independently before destructive action. Ambiguous or unexpectedly broad
targets are quarantined and escalated to the human instead of guessed.

## Approved durable evidence

Only these reviewed artifacts may survive:

- portable Council work packet, roles, evidence references, frozen positions,
  cross-reviews, approval request, dissent-preserving synthesis, human decision, and
  durable decision record;
- sanitized bounded runtime-event export with its schema, declared omissions, and
  external corroboration references;
- deterministic verification results and input digests;
- model routing, usage, budget, and cost report without credentials;
- security-adversary and evidence-auditor reports;
- OpenClaw/custom-dispatcher comparison record;
- candidate provenance and license-review record;
- teardown, residue, and credential-revocation evidence;
- final sanitized R4C input package.

Every retained artifact must:

- appear on the preapproved allowlist;
- use a Council-owned or otherwise durable open format;
- validate without OpenClaw or the custom dispatcher;
- have a stable digest and classification;
- contain no credential, personal data, work-derived data, private address, host
  identifier, internal endpoint, raw secret-bearing log, or unapproved operational
  detail;
- have an owner, retention purpose, access boundary, and deletion or review date.

Runtime-native databases, opaque session exports, memory stores, caches, raw logs, and
configuration are not durable evidence.

## Teardown sequence

1. Record the stop or normal-closeout reason; emit `teardown_started`.
2. Disable all new session, worker, model, provider, tool, and network activity at the
   independent gates.
3. Terminate sessions, workers, runtime processes, services, and listeners.
4. Revoke dedicated credentials and verify provider-side invalidation.
5. Export, validate, sanitize, digest, and copy only the approved durable evidence.
6. Remove experiment containers, volumes, networks, runtime and dispatcher state,
   workspaces, memory, caches, temporary files, configuration, logs, mounts, startup
   state, and network exceptions.
7. Remove the dedicated WSL2 distribution unless exact retention is separately
   authorized; retained environments must be stopped, disconnected, access-controlled,
   and classified as incomplete teardown until destroyed.
8. Emit `teardown_completed` only after every manifest item has a disposition.
9. Conduct the independent residue inspection below.
10. Emit `residue_inspection_completed` only after the signed report exists.
11. Re-run secret, sensitive-data, private-address, host-detail, and Git-state scans over
    retained evidence and the repository.
12. Classify closeout truthfully. Any unexplained residue yields `failed_teardown`.

No remediation outside the authorized teardown plan is implied. A newly discovered
target, privilege need, provider action, or network change requires human direction.

## Residue inspection

| Surface | Required inspection | Pass condition |
| --- | --- | --- |
| Windows host | Processes, services, tasks, startup state, files, directories, mounts, environment, credential stores, listeners, routes, firewall/proxy changes | Matches pre-run baseline except approved durable evidence |
| Dedicated WSL2 distribution | Existence, running state, storage, exports, shared paths, integrations | Removed, or explicitly quarantined under a separate retention authorization and reported as unresolved for teardown |
| Containers | Containers, images created solely for R4B, volumes, networks, build/cache layers, port mappings | No experiment object or listener remains |
| Filesystem | Runtime files, workspaces, session state, memory, caches, temp, downloads, configs, logs, staging, symlinks, mounts | Only allowlisted durable evidence remains |
| Credential stores | Environment, files, secret stores, provider account, shell history, logs, process metadata | No active or recoverable experiment credential remains |
| Environment variables | Windows, WSL2/VM, container, service, and process launch environments | No experiment secret, route, path, model, or provider value remains |
| Process list | Host and isolation-environment processes, workers, daemons, orphaned children | No experiment process remains |
| Network listeners | Host, WSL2/VM, container, proxy, and forwarded ports | No experiment listener or port mapping remains |
| Firewall and routing | Rules, proxies, DNS, routes, endpoint allowlists, VPN/tunnel state | Effective policy matches pre-run baseline |
| Git repository | Tracked, staged, untracked, ignored, worktree, hooks, config, remotes | No runtime mutation, secret, evidence leak, or unexpected local change |
| Ignored local files | Local config, traces, evidence, benchmark output, caches, model files, secrets | No experiment residue outside approved durable storage |
| Provider records | Active credentials, sessions, usage, routes, quotas, charges, retained uploads | Credential revoked; usage/cost reconciled; retention limits documented |
| Durable evidence | Digests, schemas, readability, classification, access, retention | Valid and readable without either runtime; no sensitive content |

The reviewer must compare against the Phase 2 baseline and record both expected and
unexpected differences. “Not observed” is not equivalent to “proven absent” where the
surface cannot be inspected; the limitation must remain an unresolved failure or
explicit residual risk for the human.

## Credential closeout

For each credential, record:

- opaque credential record ID, provider, purpose, owner, scope, quota, issue and expiry
  times;
- which boundary received it and which roles were denied it;
- provider-side revocation or deletion result;
- local secret-store, environment, process, file, log, event, artifact, and cache scan;
- any provider retention or audit record that cannot be deleted;
- confirmation that no production or personal credential was used.

Do not record the credential value, prefix, fingerprint that weakens secrecy, or secret-
bearing error. A credential that cannot be revoked or whose exposure cannot be bounded
causes `failed_teardown`.

## Evidence and repository scan

Before closeout, scan all retained evidence and repository-visible changes for:

- credential-like values, keys, tokens, certificates, passwords, and private keys;
- personal, corporate, government, client, contract, production, or work-derived data;
- Windows user paths, home paths, hostnames, private addresses, internal endpoints,
  connection details, listener addresses, and provider account identifiers;
- raw prompts, traces, logs, crash dumps, databases, configuration, runtime state,
  benchmark inputs, or evidence bundles outside the approved sanitized schema;
- runtime installation/configuration commands or adoption claims accidentally added to
  durable project authority.

Hits must be resolved by exclusion, approved bounded sanitization plus independent
review, or experiment failure. Secret values are never copied into a finding.

## Failure and quarantine

Teardown is incomplete when any item:

- has no disposition or cannot be inspected;
- persists without explicit retention authorization;
- cannot be revoked, terminated, unmounted, disconnected, deleted, or safely
  quarantined;
- contains sensitive or unclear-provenance data;
- differs from baseline without explanation;
- is required to read the supposedly portable Council evidence;
- depends on runtime self-report as the only evidence.

On incomplete teardown:

1. stop all remaining authorized activity;
2. revoke network and credentials where already authorized and safe;
3. preserve only the minimum sanitized evidence needed to explain the failure;
4. isolate or quarantine the exact unresolved environment without broadening access;
5. record `failed_teardown`;
6. notify the named human;
7. do not resume, adopt, begin R4C, or infer permission to remediate.

## Closeout record

The final record must state:

- experiment path and immutable candidate identity;
- start, stop, termination, teardown, and inspection outcomes;
- every removed, invalidated, retained, quarantined, or unresolved item;
- credential and provider disposition;
- network and host baseline comparison;
- repository and ignored-file state;
- retained-evidence manifest and digests;
- scan results and limitations;
- final state: `teardown_complete` or `failed_teardown`;
- reviewer and human acknowledgement.

Only `teardown_complete`, combined with all other required R4B evidence, can make the
experiment eligible for a later R4C review. It never selects or adopts OpenClaw.
