# R4B Local Model Provenance and License Review

## Status and scope

Review date: 2026-07-28

This is a bounded technical provenance and license review for a public/synthetic
capability benchmark. It is not legal advice, legal approval, production approval,
commercial approval, model adoption, or authorization to load or invoke a model.

Evidence classes are kept distinct:

- **Official-source fact:** read from the original publisher or official distribution
  source.
- **Local artifact observation:** calculated or read directly from bounded local files.
- **Inference:** a reasoned link not encoded as a complete reproducible lineage.
- **Human or legal judgment:** requires a named authorized reviewer.

## Original publisher and upstream model

### Observed official-source facts

- Publisher: Qwen.
- Model family: Qwen2.5-Coder.
- Exact upstream model:
  [`Qwen/Qwen2.5-Coder-7B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct).
- Reviewed official revision:
  [`c03e6d358207e414f1eca0bb1891e29f1db0e242`](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct/tree/c03e6d358207e414f1eca0bb1891e29f1db0e242).
- Architecture: `Qwen2ForCausalLM`, model type `qwen2`.
- Parameter count: 7.61 billion according to the official model card.
- Official configuration: 28 layers, hidden size 3,584, 28 attention heads, 4
  key/value heads, and 32,768 `max_position_embeddings`.
- Official tokenizer configuration: 32,768 `model_max_length`.
- Intended context: the model card advertises up to 131,072 tokens only with the
  documented YaRN long-context adjustment; the shipped reviewed config remains 32,768.
- Intended capability descriptions: code generation, code reasoning, code fixing, code
  agents, and retained general competencies. These are publisher descriptions, not
  Local AI Guild benchmark results.
- License identifier: Apache-2.0.
- License source:
  [`LICENSE` at the reviewed revision](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct/blob/c03e6d358207e414f1eca0bb1891e29f1db0e242/LICENSE).
- The reviewed upstream repository exposes no separate acceptable-use or responsible-use
  policy file. Absence from this bounded repository inventory does not prove that no
  external law, policy, trademark rule, or organizational restriction applies.

### License obligations requiring human acceptance

Apache-2.0 generally requires preserving the license and applicable copyright,
attribution, patent, and notice material when redistributing covered work. Modified or
converted distributions may carry additional notice duties. The exact treatment of
model weights and conversions under organizational policy is a human or legal judgment.

No field-of-use restriction is visible in the Apache-2.0 text. That supports technical
eligibility for a public/synthetic benchmark but does not approve corporate,
commercial, government, client, contract, regulated, or production use.

## Ollama Q4_K_M artifact

### Local artifact observations

- Local manifest SHA-256:
  `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`.
- Local model-layer SHA-256:
  `60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463`.
- Local license-layer SHA-256:
  `832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e`.
- Local config identifies GGUF, family `qwen2`, type `7.6B`, and Q4_K_M.

### Official distribution evidence

- Official Ollama route:
  [`qwen2.5-coder:7b`](https://ollama.com/library/qwen2.5-coder:7b).
- Official registry manifest:
  [`registry.ollama.ai/v2/library/qwen2.5-coder/manifests/7b`](https://registry.ollama.ai/v2/library/qwen2.5-coder/manifests/7b).
- The official registry manifest body hashes to the exact local manifest SHA-256 and
  declares the exact local config and layer digests and sizes.
- The official Ollama page identifies Qwen2.5-Coder 7B, the 4.7 GB distribution, the
  same abbreviated manifest identity, and Apache License.
- The local 11,343-byte license layer is byte-for-byte identical by SHA-256 to Qwen's
  official Apache-2.0 license file at the reviewed upstream revision.

### Provenance classification

The local artifact is confidently linked to the exact official Ollama registry
distribution. The distribution is confidently linked by project identity, family,
parameter class, model card, and identical official license to
Qwen2.5-Coder-7B-Instruct.

The registry metadata does not state the exact Qwen source revision or reproducible
conversion recipe used to produce the Q4_K_M model layer. That is a provenance
limitation, not an immutable local-identity failure.

Technical classification: suitable for conditional qualification for a bounded
public/synthetic benchmark, subject to:

1. human or authorized legal acceptance of Apache-2.0 obligations and the official
   Ollama redistribution lineage;
2. retention of the exact manifest, model, config, and license digests;
3. rejection of the floating `latest` alias;
4. no claim that the quantized artifact is bit-reproducible from the reviewed upstream
   revision.

## LM Studio Q5_K_M artifact

### Local artifact observations

- Local file SHA-256:
  `b0f8a344452d5462193991fd7cf2bffdbee1a05fccfe98aa25a6ed91a56624a2`.
- Local file size: 5,444,831,744 bytes.
- Filename and repository structure identify Q5_K_M and
  Qwen2.5-Coder-7B-Instruct.
- No adjacent local card, license, tokenizer, or provenance file exists.

### Distribution evidence

- Conversion repository:
  [`apto-as/Qwen2.5-Coder-7B-Instruct-Q5_K_M-GGUF`](https://huggingface.co/apto-as/Qwen2.5-Coder-7B-Instruct-Q5_K_M-GGUF).
- Reviewed conversion revision:
  [`10ba8b9be9729feb1d3c476d014c861dbfc01177`](https://huggingface.co/apto-as/Qwen2.5-Coder-7B-Instruct-Q5_K_M-GGUF/tree/10ba8b9be9729feb1d3c476d014c861dbfc01177).
- The local SHA-256 and size exactly match the repository's LFS object for
  `qwen2.5-coder-7b-instruct-q5_k_m.gguf`.
- The conversion card declares Apache-2.0, names
  `Qwen/Qwen2.5-Coder-7B-Instruct` as the base model, and states that conversion used
  llama.cpp through the GGUF-my-repo service.

### Provenance classification

The exact converted file and conversion-repository revision are confirmed. The
conversion repository is community-authored rather than the original publisher and
does not pin the exact base-model revision used during conversion. Its base lineage is
therefore credible but not fully reproducible from the cited metadata alone.

Technical classification: not selected for the proposed route. It could receive a
separate conditional benchmark review, but it provides no model-family diversity over
the Ollama artifact and has a less direct distribution chain.

Human or legal conditions include:

1. accept the Apache-2.0 obligations for both the original work and conversion;
2. accept the community conversion provenance and missing pinned base revision;
3. preserve the original publisher and conversion attribution;
4. do not infer that quantization changes remove upstream obligations.

## Redistribution, conversion, and intended-use boundary

- Local use does not itself establish permission for later redistribution of the
  quantized files.
- Copying either artifact into a future WSL2 or container environment would be a
  separately authorized action and must preserve the approved digest and license
  evidence.
- Conversion and quantization do not establish a new intended-use approval.
- Only repository-owned public or synthetic benchmark data is eligible.
- No model in this review is qualified for production, unrestricted coding, sensitive
  data, corporate source, government data, client work, or general use.

## Review conclusion

No unknown or facially incompatible license was found for the bounded public/synthetic
benchmark. The Ollama artifact has the strongest route provenance because its complete
local manifest is byte-identical to the official registry manifest and its license
layer is byte-identical to the original publisher's Apache-2.0 license.

Classification: `accept_with_named_condition`

The named conditions require human or authorized legal acceptance. This review does not
grant that acceptance.
