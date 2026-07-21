# System Context

This document describes planned architecture, not implemented behavior.

Local AI Guild sits between a human-approved task and bounded execution facilities. It may eventually receive task text, retrieve relevant local evidence, ask candidate models for proposals, validate proposals against policy and typed tool contracts, execute allowlisted tools, and produce an evidence-backed result.

External systems may include local model runtimes, local storage under `E:\AI` and `D:\AI`, and explicitly approved cloud model APIs. None is connected in R0.

Humans retain authority over cloud escalation, mutating operations, commits, pushes, credentials, runtime installation, and changes to security policy.
