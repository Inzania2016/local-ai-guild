# Local AI Guild

Local AI Guild is a local-first orchestration project for routing bounded work among deterministic tools, local models, and explicitly approved cloud adapters. The repository is the durable control plane: policies, typed contracts, implementation code, tests, evaluation definitions, and traceable evidence live here. Model weights, runtime caches, and generated traces do not.

## Current status

The project is at **R0: repository control plane and minimal skeleton**. No model runtime, provider, dispatcher, retrieval system, cloud integration, or training pipeline is implemented or claimed to have been tested.

The only executable application behavior is a harmless status command. Bootstrap and use the repository-local interpreter:

```powershell
.\scripts\bootstrap.ps1
.\.venv\Scripts\python.exe -m local_ai_guild status
.\scripts\verify-repository.ps1
```

## Design principles

- Deterministic scripts establish facts; model output is treated as a proposal.
- Models may request narrow, approved tools but never receive unrestricted shell access.
- Important claims must link to evidence.
- Cloud delegation is explicit, policy-controlled, and never automatic.
- The system must provide value before custom model training exists.
- Delivery proceeds through small, independently verifiable work packets.

## Planned storage layout

- Repository: `C:\dev\source\Repos\local-ai-guild`
- Active models, runtimes, caches, and active workspace assets: `E:\AI`
- Archives, datasets, experiments, benchmark history, and backups: `D:\AI`

These locations are documented plans, not evidence that the directories or runtimes have been configured.

## Repository map

- `config/`: tracked examples; real local configuration is ignored
- `docs/architecture/`: planned system boundaries and flows
- `docs/decisions/`: future architecture decision records
- `docs/experiments/`: experiment designs and results
- `docs/verification/`: durable verification procedures
- `src/local_ai_guild/`: Python package
- `tests/`: deterministic automated tests
- `evals/`: future evaluation definitions
- `artifacts/`: ignored generated evidence, traces, and benchmark results

Read [PROJECT_STATE.md](PROJECT_STATE.md) for confirmed current facts, [ROADMAP.md](ROADMAP.md) for staged plans, and [NEXT_WORK_PACKET.md](NEXT_WORK_PACKET.md) for the single proposed next packet.

## Security

This is a public repository. Use public or synthetic fixtures by default. Never add non-public work material, production data, credentials, internal network details, unsanitized work-derived prompts or traces, or personal information that is not intentionally public. Work-derived material requires sanitization, explicit repository approval, and independent review before commit. Model, dataset, and adapter licenses require review before adoption. See [SECURITY.md](SECURITY.md).

## Development

Python 3.12 is pinned in `.python-version`. Development dependencies are Ruff and pytest only. The bootstrap script creates `.venv` inside the repository and installs the declared project dependencies; it does not install system software or change machine-wide settings.

No commits or pushes are performed by repository scripts.
