# Titan Business Operating System — Architecture

## Scope

This document describes the source-backed architecture of the current repository. It does not promote every historical product name or design document to a current runtime claim.

## 1. Shared domain core

The application is a Laravel modular monolith.

Canonical business functionality is primarily expressed through:

- `Modules/`
- `app/`
- module migrations
- services
- events
- jobs
- Filament resources
- routes
- tests

The architectural objective is for multiple interfaces to operate over one domain model rather than maintaining separate backend implementations per surface.

## 2. AI execution boundary

The clearest reusable AI boundary is:

```text
plugins/filament-chatbot/src/
├── Contracts/LlmDriverContract.php
├── Drivers/
│   ├── OpenAiDriver.php
│   ├── AnthropicDriver.php
│   └── GeminiDriver.php
├── Models/
└── Services/
    ├── AssistantService.php
    └── RunProcessorService.php
```

### Provider normalisation

`AssistantService::resolveDriver()` selects a provider implementation from connection configuration.

The Anthropic and Gemini drivers translate provider-specific request/response formats into the normalised structure consumed by `RunProcessorService`.

### Bounded tool execution

`RunProcessorService::process()`:

1. persists processing state
2. builds assistant context
3. calls the selected provider
4. resolves and executes configured tools
5. adds tool results back to model context
6. repeats up to a default five iterations
7. persists success or explicit failure

This is an execution boundary, not a complete authorization boundary.

## 3. Module lifecycle boundary

The repository contains module lifecycle commands for installation, status, verification, and upgrades.

`titan:module:verify` can target one module or all discovered modules.

Verification returns a process failure code if any module is unhealthy, making module health usable by CI.

## 4. Interface boundary

The repository includes Filament administration and PWA-oriented/field interfaces.

Interfaces should remain presentation and interaction surfaces over the shared domain core.

Historical surface naming in older documents may differ from current commercial naming. Engineering documentation should therefore prefer capability boundaries over marketing labels unless the runtime and commercial model are intentionally aligned.

## 5. System map

```text
Users / operators / field clients
            │
            ▼
Application interfaces
Filament · web · PWA-oriented surfaces
            │
            ▼
Shared Laravel domain modules
operations · finance · people · comms · docs · quality
            │
       ┌────┴─────────────┐
       ▼                  ▼
AI execution          module lifecycle
drivers/runs/tools    install/verify/upgrade
       │                  │
       └────────┬─────────┘
                ▼
queues · events · persistence · integrations
```

## 6. Important invariants

The desired architecture requires:

- tenant/company boundaries to be enforced in domain code
- tools to respect ordinary application authorization
- provider credentials to remain server-side
- AI output not to bypass validation
- module verification to fail closed on unhealthy modules
- business state to remain inspectable without relying on model context
- external integrations to remain adapter/boundary concerns

## 7. Current verification boundary

The architecture is implemented unevenly across a large codebase.

Current CI proves that dependency installation reaches the application test stage, but the full suite and fresh-migration job are red. See `docs/evaluation.md`.

The repository therefore makes architecture claims from source evidence and keeps production-readiness claims separate.
