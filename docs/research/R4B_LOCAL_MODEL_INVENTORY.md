# R4B Local Model Inventory

## Scope and safety boundary

Inventory date: 2026-07-28

This is a filesystem-and-manifest inventory only. No model runtime CLI, model API,
tensor parser, or runtime library was used. No model was loaded, invoked, downloaded,
imported, converted, quantized, or modified.

Public-safe aliases:

- `<OLLAMA_MODEL_ROOT>` means the configured local Ollama model directory.
- `<LM_STUDIO_MODEL_ROOT>` means the `downloadsFolder` read from LM Studio's local
  settings.

The aliases deliberately suppress the user profile. Modification timestamps are
low-trust operational metadata: they help distinguish local files but do not establish
provenance, installation time, or runtime availability.

## Process preflight

No Ollama, LM Studio, llama.cpp, OpenClaw, or clearly attributable Node process was
present before inspection.

## Ollama manifest inventory

All manifest SHA-256 values were calculated directly from local manifest bytes. All
present blob SHA-256 values were recalculated from local blob bytes and matched their
content-addressed filenames.

Every manifest has schema version 2 and uses config media type
`application/vnd.docker.container.image.v1+json`.

### `registry.ollama.ai/library/qwen2.5-coder:7b`

Classification: `identity_confirmed`

- Manifest:
  `<OLLAMA_MODEL_ROOT>/manifests/registry.ollama.ai/library/qwen2.5-coder/7b`
- Manifest SHA-256:
  `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`
- Local modification time: `2026-03-30T11:04:27.8127177Z`
- Schema version: 2
- Config:
  `sha256:d9bb33f2786931fea42f50936a2424818aa2f14500638af2f01861eb2c8fb446`,
  487 bytes, present and hash-verified
- Total referenced size: 4,683,087,561 bytes, about 4.36 GiB
- Completeness: every referenced blob exists and matches its digest

| Layer media type | Digest | Size | Sharing |
| --- | --- | ---: | --- |
| `application/vnd.ollama.image.model` | `sha256:60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463` | 4,683,074,048 | shared with the identical `latest` alias |
| `application/vnd.ollama.image.system` | `sha256:66b9ea09bd5b7099cbb4fc820f31b575c0366fa439b08245566692c6784e281e` | 68 | referenced by the 7B, `latest`, and incomplete 14B manifests |
| `application/vnd.ollama.image.template` | `sha256:1e65450c30670713aa47fe23e8b9662bdf4065e81cc8e3cbfaa98924fcc0d320` | 1,615 | referenced by the 7B, `latest`, and incomplete 14B manifests |
| `application/vnd.ollama.image.license` | `sha256:832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e` | 11,343 | referenced by the 7B, `latest`, and incomplete 14B manifests |

The local config declares:

- format: GGUF;
- family: `qwen2`;
- model type: `7.6B`;
- quantization/file type: `Q4_K_M`;
- packaged target architecture: `amd64`;
- packaged target OS: `linux`.

The manifest body is byte-identical by SHA-256 to the official public Ollama registry
response for `library/qwen2.5-coder:7b`. The model-layer digest beginning
`sha256:60e05f` is therefore confirmed in full, not inferred from the tag.

### `registry.ollama.ai/library/qwen2.5-coder:latest`

Classification: `identity_confirmed`, but ineligible as a route identifier

- Manifest:
  `<OLLAMA_MODEL_ROOT>/manifests/registry.ollama.ai/library/qwen2.5-coder/latest`
- Manifest SHA-256:
  `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`
- Local modification time: `2026-03-30T10:35:06.1719709Z`
- Config, layers, sizes, and completeness: identical to the 7B manifest

This alias currently identifies the same bytes as `7b`, but `latest` is floating and
must not appear in a qualified route.

### `registry.ollama.ai/library/qwen2.5-coder:14b`

Classification: `artifact_incomplete`

- Manifest:
  `<OLLAMA_MODEL_ROOT>/manifests/registry.ollama.ai/library/qwen2.5-coder/14b`
- Manifest SHA-256:
  `9ec8897f747e246e970bc5cfdda85d22f1123dc2e3d34978a010a75968716849`
- Local modification time: `2026-03-30T09:18:11.8584739Z`
- Config:
  `sha256:0578f229f23ad620e123654fd0b4708405e7af3629ec1aecf3f553f54e06bc40`,
  488 declared bytes, missing
- Model:
  `sha256:ac9bc7a69dab38da1c790838955f1293420b55ab555ef6b4615efa1c1507b1ed`,
  8,988,110,784 declared bytes, missing
- System, template, and Apache-2.0 license layers: present only because they are shared
  with the complete 7B artifact
- Total referenced size: 8,988,124,298 bytes

The missing config and model layer make architecture, quantization, immutable model
content, and runtime availability unresolved. This is not an installed candidate.

### `registry.ollama.ai/library/qwen3-coder:30b`

Classification: `artifact_incomplete`

- Manifest:
  `<OLLAMA_MODEL_ROOT>/manifests/registry.ollama.ai/library/qwen3-coder/30b`
- Manifest SHA-256:
  `06c1097efce0431c2045fe7b2e5108366e43bee1b4603a7aded8f21689e90bca`
- Local modification time: `2026-03-30T08:42:27.9616375Z`
- Config:
  `sha256:24a94682582c6045f4950846fc7711479dcecb478b86759f0306a2ef8484d318`,
  539 declared bytes, missing
- Model:
  `sha256:1194192cf2a187eb02722edcc3f77b11d21f537048ce04b67ccf8ba78863006a`,
  18,556,688,736 declared bytes, missing
- License:
  `sha256:d18a5cc71b84bc4af394a31116bd3932b42241de70c77d2b76d69a314ec8aa12`,
  11,338 declared bytes, missing
- Parameters:
  `sha256:69aa441ea44ff5e1e7b56cac4f471e71e8a5e2e3963c29684a9234d5d5e5f7aa`,
  148 declared bytes, missing
- Total referenced size: 18,556,700,761 bytes

No referenced blob exists. This is not an installed candidate.

## LM Studio inventory

LM Studio's settings name `<LM_STUDIO_MODEL_ROOT>` as its `downloadsFolder`. Bounded
inspection found one GGUF file and no adjacent model card, README, config, tokenizer,
license, or other provenance file.

### Qwen2.5-Coder 7B Instruct Q5_K_M

Classification: `identity_confirmed`

- Public-safe path:
  `<LM_STUDIO_MODEL_ROOT>/apto-as/Qwen2.5-Coder-7B-Instruct-Q5_K_M-GGUF/qwen2.5-coder-7b-instruct-q5_k_m.gguf`
- Filename: `qwen2.5-coder-7b-instruct-q5_k_m.gguf`
- Size: 5,444,831,744 bytes, about 5.07 GiB
- SHA-256:
  `b0f8a344452d5462193991fd7cf2bffdbee1a05fccfe98aa25a6ed91a56624a2`
- Local modification time: `2026-06-16T11:48:03.2763326Z`
- Filename/repository family: Qwen2.5-Coder-7B-Instruct
- Filename/repository quantization: `Q5_K_M`
- Repository/publisher visible from directory structure: `apto-as`

The calculated local SHA-256 exactly matches the Hugging Face LFS SHA-256 and size for
the same filename in
`apto-as/Qwen2.5-Coder-7B-Instruct-Q5_K_M-GGUF` at revision
`10ba8b9be9729feb1d3c476d014c861dbfc01177`. This confirms the exact converted
artifact without parsing or loading GGUF tensors.

The conversion repository identifies
`Qwen/Qwen2.5-Coder-7B-Instruct` as its base model but does not pin the exact base-model
revision used for conversion. Exact converted-artifact identity is confirmed; exact
conversion-source revision remains a provenance condition.

## Inventory conclusion

Two complete immutable local artifacts exist:

1. the official Ollama registry Q4_K_M artifact, identified by manifest and every blob
   digest; and
2. the LM Studio Q5_K_M GGUF, identified by a local SHA-256 that matches its exact
   Hugging Face LFS object.

They are two quantizations and packaging routes of the same Qwen2.5-Coder-7B-Instruct
model family. They do not provide model-family or training-distribution diversity.

The incomplete 14B and 30B manifests are excluded. Runtime loadability, acceleration,
throughput, latency, stability, context behavior, and model capability remain untested.
