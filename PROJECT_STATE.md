# Project State

Last updated: 2026-07-21

## Confirmed current facts

- R0 established the repository control plane and minimal Python skeleton.
- The repository path is `C:\dev\source\Repos\local-ai-guild`.
- Python is pinned to 3.12 for project work.
- The package exposes only a harmless `status` command.
- Example configuration files contain no live provider or model connection details.
- No AI SDK, web framework, vector database, runtime-specific dependency, MCP implementation, HTTP API, dispatcher, retrieval implementation, cloud integration, training pipeline, or Docker configuration is present.
- The repository-local environment uses Python 3.12.6 with Ruff 0.15.22 and pytest 8.4.2.
- R0 repository verification, Ruff, pytest, and CLI status checks pass as recorded in `VERIFICATION.md`.
- The authority documents establish an explicit public-repository data boundary: public or synthetic fixtures are the default, and work-derived material requires sanitization, explicit repository approval, and independent pre-commit review.
- Model, dataset, and adapter licenses require review before adoption; R0 selects no project license and approves no candidate license.

## Planned, not implemented

- `E:\AI` will hold active models, runtimes, caches, and active workspace assets.
- `D:\AI` will hold archives, datasets, experiments, benchmark history, and backups.
- Candidate components and model hypotheses are described in `VISION.md` and architecture documents.

## Not validated

- No local or cloud model candidate has been evaluated.
- LM Studio, Ollama, OpenCode, llama.cpp, and cloud agents have not been configured or invoked by R0.
- The planned storage layout has not been provisioned or validated by R0.
- No project, model, dataset, or adapter license has been selected or approved.

## Current stage gate

R0 is complete at the repository level. This does not validate any model or runtime. The next permitted implementation scope is R1 in `NEXT_WORK_PACKET.md`.
