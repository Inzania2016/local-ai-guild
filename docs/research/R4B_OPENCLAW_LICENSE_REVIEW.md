# R4B OpenClaw License and Component Review

## Status and scope

This is a bounded static metadata review of the proposed OpenClaw candidate. It is not
legal advice or legal approval. It does not authorize download, installation,
configuration, execution, commercial use, corporate use, government use, contract use,
model use, or adoption.

Candidate:

```text
OpenClaw v2026.7.1
openclaw/openclaw commit 2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4
release date 2026-07-13
package openclaw@2026.7.1
```

No candidate package, archive, container image, or model was downloaded or installed
during this review.

## Source classification

### Observed official-source facts

- The official repository is
  [`openclaw/openclaw`](https://github.com/openclaw/openclaw).
- The official
  [`v2026.7.1` release](https://github.com/openclaw/openclaw/releases/tag/v2026.7.1)
  identifies release date 2026-07-13, package `openclaw@2026.7.1`, and immutable
  commit `2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4`.
- The official release records npm integrity
  `sha512-ge/Xss99CHAjPL/ikmH/UFoiOrjcxDB4sW3y9mhyCD+dYW3wzV7TKbAVdkrXFgAG2d2BjpJofP97zUZ+umxo8g==`
  and links official release evidence. The reviewed commit is GitHub-verified.
- The candidate
  [`package.json`](https://github.com/openclaw/openclaw/blob/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4/package.json)
  identifies version `2026.7.1`, license `MIT`, the `openclaw` CLI entry point,
  supported Node ranges, and installation lifecycle scripts.
- The candidate
  [`LICENSE`](https://github.com/openclaw/openclaw/blob/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4/LICENSE)
  is MIT and requires preservation of the copyright and permission notice.
- The candidate
  [`THIRD_PARTY_NOTICES.md`](https://github.com/openclaw/openclaw/blob/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4/THIRD_PARTY_NOTICES.md)
  records Pi/pi-mono incorporated or adapted code under MIT. It explicitly does not
  replace normal package-manager dependency metadata.
- The official
  [`SECURITY.md`](https://github.com/openclaw/openclaw/blob/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4/SECURITY.md)
  describes a trusted single-operator boundary, trusted plugins, host-first execution
  behavior when sandboxing is inactive, and a loopback-only web-interface
  recommendation.
- The official README describes npm, pnpm, and bun installation paths. The R4B design
  does not choose a floating install command and would require the exact package
  version and integrity before any later authorized installation.

### Repository design decisions

- Evaluate only `v2026.7.1`; reject `latest`, prereleases, unpinned source, and a
  different commit.
- Prefer the published npm artifact and its shrinkwrap as the reviewable candidate
  surface rather than an unbounded source-workspace installation.
- Pin Node.js `24.15.0` if installation is later authorized because it satisfies
  upstream's recommended Node 24 line. A different Node build requires a refreshed
  review.
- Do not use a container image unless the human review separately pins its immutable
  digest, base image, SBOM or equivalent inventory, license set, and provenance.

### Inferences

- The MIT core license contains no field-of-use restriction. That supports technical
  eligibility for a bounded experiment but does not establish suitability for
  commercial, corporate, government, client, or contract use.
- The lock metadata is sufficiently complete for a bounded exception-focused review,
  but static identifiers do not prove that source distributions, generated code,
  native binaries, optional paths, or notices fully satisfy every obligation.

### Unresolved human or legal judgments

- Whether the MIT core and incorporated-code notices are acceptable for the intended
  organization and experiment.
- Whether the MPL-2.0, dual-license, Zlib-combination, Unlicense, and BlueOak entries
  below require additional notice, source, election, policy, or legal treatment.
- Whether published native binaries, optional code paths, post-install behavior, and
  transitive source distributions match their lock metadata.
- Whether Node.js and any later selected container base comply with organizational
  software policy.
- Whether model, dataset, adapter, and provider licenses are independently acceptable.

## Package manager and lockfiles

| Surface | Observed fact | Review meaning |
| --- | --- | --- |
| Source workspace package manager | `pnpm@11.2.2` with a pinned package-manager integrity string in `package.json` | Source development uses pnpm. |
| Source workspace lock | [`pnpm-lock.yaml`](https://github.com/openclaw/openclaw/blob/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4/pnpm-lock.yaml), lockfile version `9.0` | Pins the wider monorepo graph but does not carry license fields. It is broader than the proposed published-package surface. |
| Published package lock | [`npm-shrinkwrap.json`](https://github.com/openclaw/openclaw/blob/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4/npm-shrinkwrap.json), lockfile version `3` | The bounded installation-resolution inventory for `openclaw@2026.7.1`. |
| Lifecycle scripts | Root package declares preinstall and postinstall scripts; the shrinkwrap marks the root and three dependencies as having install scripts | Later installation inspection must record every script and resulting file/process/network side effect. Static review does not execute them. |

## Dependency inventory

The candidate `package.json` declares:

- 56 direct runtime dependency entries;
- one optional dependency, `sqlite-vec@0.1.9`;
- no `bundledDependencies` field;
- 31 development dependencies, excluded from the proposed published-package runtime
  surface.

The shrinkwrap root resolves 55 external direct dependencies plus one optional
dependency. The apparent difference is the source-workspace dependency
`@openclaw/ai@workspace:*`, which is not a shrinkwrap root entry. Its official
[`packages/ai/package.json`](https://github.com/openclaw/openclaw/blob/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4/packages/ai/package.json)
identifies `@openclaw/ai@2026.7.1` as MIT and describes the provider-adapter package
included in the release.

The published shrinkwrap contains 308 package records including the root. Every record
has a visible license field:

| License identifier | Package records | Static classification |
| --- | ---: | --- |
| MIT | 219 | routine permissive; preserve applicable notices |
| ISC | 26 | routine permissive |
| BSD-3-Clause | 18 | permissive with notice/non-endorsement conditions |
| Apache-2.0 | 15 | permissive with notice, license, and patent terms |
| BSD-2-Clause | 11 | routine permissive |
| BlueOak-1.0.0 | 8 | permissive but less common; policy/legal awareness required |
| `MIT OR Apache` | 6 | permissive election must be documented consistently |
| `(MIT AND Zlib)` | 1 | both permissive obligations apply |
| `(MIT OR GPL-3.0-or-later)` | 1 | select and document the MIT path for this experiment |
| 0BSD | 1 | permissive |
| MPL-2.0 | 1 | file-level copyleft obligations require manual review |
| Unlicense | 1 | uncommon public-domain-style text; organizational policy review required |

No shrinkwrap license field is missing. No AGPL, LGPL, CDDL, EPL, SSPL, BUSL,
source-available, proprietary, `SEE LICENSE`, or unknown identifier is visible in this
bounded metadata surface.

## Exceptions and manual review

| Package | Version | Visible license | Why manual review remains |
| --- | --- | --- | --- |
| `web-push` | `3.6.7` | MPL-2.0 | Confirm file-level source/notice obligations for the exact shipped use and whether the feature is enabled in the bounded runtime. |
| `jszip` | `3.10.1` | `(MIT OR GPL-3.0-or-later)` | Select the MIT branch explicitly and preserve its notice; do not imply GPL is the chosen basis. |
| `pako` | `1.0.11` | `(MIT AND Zlib)` | Confirm both license texts/notices are retained as required. |
| `fast-sha256` | `1.3.0` | Unlicense | Confirm organizational policy accepts the uncommon license and provenance. |
| Eight BlueOak packages | pinned by shrinkwrap | BlueOak-1.0.0 | Confirm the organization accepts the less-common permissive license identifier. |
| `@openclaw/ai` | `2026.7.1` source-workspace package | MIT | It is declared as `workspace:*` in root metadata rather than represented as a shrinkwrap root; installed-file inspection must confirm the published artifact contains the expected pinned internal code. |

These exceptions do not establish a prohibited license, but Codex cannot make the legal
acceptance decision.

## Node.js runtime

OpenClaw supports Node `>=22.22.3 <23`, `>=24.15.0 <25`, or `>=25.9.0` and recommends
Node 24 for new installations. The proposed exact runtime is Node.js `24.15.0`.

The official
[`nodejs/node v24.15.0 LICENSE`](https://github.com/nodejs/node/blob/v24.15.0/LICENSE)
begins with MIT terms and includes third-party component notices and licenses. A later
installation must pin the official Node distribution and verify its archive signature or
digest, full license bundle, and provenance. This review does not approve Node.js for an
organization.

## Container-image considerations

No container image is selected in this packet. A tag such as `latest` is ineligible.
Before a later container-backed installation, the human review must either:

1. approve a specific image by registry, immutable digest, source revision, base-image
   digest, architecture, SBOM or equivalent component inventory, signature/provenance,
   and license bundle; or
2. explicitly authorize the dedicated-WSL2 experiment without a container image and
   accept the revised process/resource boundary.

The core MIT license does not automatically approve a container base, OS packages,
native libraries, Node distribution, or generated image contents.

## Incorporated code and native/runtime surface

The official third-party notice covers adapted Pi/pi-mono code and
`@earendil-works/pi-tui` under MIT. The dependency graph also includes native or
platform-sensitive surfaces such as `@lydell/node-pty`, `sqlite-vec`,
`tree-sitter-bash`, media/parser packages, `playwright-core`, and install scripts.
License metadata does not establish security, runtime necessity, sandboxing, or the
absence of additional native notices.

The R4B tool policy disables browser, unrestricted shell, messaging, marketplace,
personal-account, and broad network surfaces. Installed-file and effective-feature
inspection must verify that disabled components cannot silently broaden the experiment
boundary.

## Static-review limitations

This review:

- read official metadata and text files only;
- did not retrieve the npm artifact, source archive, container image, or SBOM;
- did not recalculate release, package, or dependency digests;
- did not inspect every dependency's source tree or distributed license file;
- did not execute installation or lifecycle scripts;
- did not validate vulnerability status, export controls, patents beyond license text,
  trademark terms, privacy terms, provider terms, or jurisdiction-specific obligations;
- did not approve any model, dataset, adapter, provider, or intended use.

## Codex license recommendation

Classification: `accept_with_named_condition`

The static metadata does not reveal a clearly incompatible license for the bounded
public/synthetic experiment, and the dependency closure is sufficiently enumerated for
human review. Installation should remain deferred until a human or authorized legal
reviewer accepts the named exceptions, the exact Node distribution, the no-container or
pinned-container choice, and installed-artifact provenance. This conclusion is
technical review evidence, not legal approval.
