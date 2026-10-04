![Titan Business Operating System — modular Laravel business platform with shared domains, bounded AI execution, and verifiable module health](docs/images/titan-bos-banner.svg)

<div align="center">

# Titan Business Operating System

**A modular Laravel business operating system that combines shared operational domains with bounded multi-provider AI execution, module health verification, and field-oriented application surfaces.**

*Engineering focus: one shared domain core, inspectable AI tool execution, verifiable module boundaries, and configuration-driven service workflows.*

[![CI](https://github.com/Masterleeaus/Titan-Business-Operating-System/actions/workflows/ci.yml/badge.svg)](https://github.com/Masterleeaus/Titan-Business-Operating-System/actions/workflows/ci.yml)
![PHP](https://img.shields.io/badge/PHP-8.4-777BB4?logo=php&logoColor=white)
![Laravel](https://img.shields.io/badge/Laravel-12-FF2D20?logo=laravel&logoColor=white)
![Filament](https://img.shields.io/badge/Filament-4-FDAE4B)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[Architecture](docs/architecture.md) · [Evaluation](docs/evaluation.md) · [Documentation](docs/README.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md)

</div>

---

## Overview

Titan Business Operating System is a modular Laravel application for service-business operations.

Instead of splitting scheduling, finance, communications, field work, documents, administration, and AI assistance into unrelated applications, the repository brings them into one shared domain core with module-owned services, migrations, events, jobs, Filament resources, and PWA-oriented interfaces.

The codebase currently demonstrates four important engineering ideas:

- **bounded multi-provider AI execution** — OpenAI-compatible, Anthropic, and Gemini drivers normalise into one assistant/tool loop
- **module health verification** — installable modules expose post-install verification that can fail CI
- **shared operational domains** — finance, field operations, communications, documents, people, quality, and integrations live behind one Laravel application boundary
- **configuration-driven product surfaces** — interfaces and vertical behaviour are layered over shared domain code rather than requiring a full backend fork per vertical

> **Core principle:** business state should remain ordinary, inspectable application state even when AI is involved.

---

## Measured evidence

Evidence is placed before feature marketing deliberately.

| Evidence | Verified result | Reproduce / inspect |
| --- | --- | --- |
| LLM driver implementations | **3** first-party driver paths: OpenAI-compatible, Anthropic, Gemini | `plugins/filament-chatbot/src/Drivers/` |
| Bounded tool loop | Default maximum **5 tool-call iterations**; unresolved loops are persisted as failed runs | `RunProcessorService.php` |
| Tool execution evidence | Run records persist status, output, tool calls, tool results, model and token usage where returned | `RunProcessorService.php` |
| Module verification command | `titan:module:verify` verifies one or all discovered modules and exits non-zero on unhealthy state | `VerifyModuleCommand.php` |
| Module command regression coverage | **4 verify-specific command tests** plus install/status/upgrade command tests in the same suite | `tests/Feature/Modules/ModuleCommandsTest.php` |
| CI dependency/bootstrap state | Composer installation and Laravel package discovery completed in both jobs in CI run **#95** | GitHub Actions run 37176359112 |
| Current test-suite result | **13 passed / 724 failed** in CI run #95; failures are dominated by the existing duplicate `invoices` table migration state | GitHub Actions run 37176359112 |
| Fresh migration check | Currently **blocked before migration execution** by CI database environment configuration; module verification is consequently skipped | `.github/workflows/ci.yml`, run #95 |
| Repository-level AI benchmark | **Not established** | `docs/evaluation.md` |

### What those numbers mean

They establish that the repository contains real provider drivers, a bounded tool-execution mechanism, module verification logic, regression tests, and an active CI pipeline.

They do **not** establish:

- production readiness
- a passing full application test suite
- AI-quality superiority
- safe autonomous execution
- provider equivalence
- deployment-scale reliability

---

## What is new

### 1. Normalised multi-provider tool execution

The strongest AI engineering mechanism in this repository is not a chat UI. It is the reusable assistant execution boundary under `plugins/filament-chatbot/`.

The assistant layer can select an OpenAI-compatible, Anthropic, Gemini, or custom `LlmDriverContract` implementation. Provider-specific request and response shapes are normalised into the structure expected by one run processor.

```text
Assistant input + context
          │
          ▼
Assistant configuration
          │
          ▼
Provider driver selection
   ┌──────┼────────┐
   ▼      ▼        ▼
OpenAI  Anthropic Gemini
   └──────┼────────┘
          ▼
Normalised response
          │
          ├──── no tool call ───► persist completed run
          │
          ▼
Tool resolution + execution
          │
          ▼
Append tool result to context
          │
          └──── repeat, maximum 5 rounds
                         │
                         ▼
                 persist failure if unresolved
```

#### Why it matters

- **Provider separation** — application workflow code does not need provider-specific response handling.
- **Bounded execution** — tool loops cannot continue indefinitely.
- **Persistent evidence** — run state, calls, results, outputs, model identity and token usage can be stored.
- **Failure visibility** — exceptions and iteration exhaustion become explicit failed run state.
- **Extension point** — custom drivers may implement the same contract.

#### Implementation

```text
plugins/filament-chatbot/src/
├── Contracts/LlmDriverContract.php
├── Drivers/
│   ├── OpenAiDriver.php
│   ├── AnthropicDriver.php
│   └── GeminiDriver.php
└── Services/
    ├── AssistantService.php
    └── RunProcessorService.php
```

#### Current boundary

This is an implemented provider/tool abstraction. It is **not yet backed by a repository-level comparative evaluation** proving equivalent behaviour across all three providers.

---

### 2. Module health as an executable contract

The second distinctive mechanism is the repository's module lifecycle tooling.

`php artisan titan:module:verify` converts “this module is installed correctly” from a documentation claim into an executable check.

```text
Module discovered on disk
         │
         ▼
ModuleInstaller::verify()
         │
         ▼
registered health hooks
         │
    ┌────┴────┐
    ▼         ▼
 passed     failed
    │         │
    ▼         ▼
healthy    non-zero exit
              │
              ▼
             CI
```

The command supports one module or every discovered module and reports individual check results.

#### Evidence

Dedicated command tests verify:

- an existing module succeeds
- a nonexistent module fails
- `--all` succeeds when all discovered modules are healthy
- missing module / `--all` input fails

The repository setup script and CI migration job both call:

```bash
php artisan titan:module:verify --all
```

#### Current boundary

The verification step is implemented and tested in source, but the current CI fresh-migration job fails earlier in database bootstrap, so the CI run does not yet reach the all-module verification step.

---

## Verified capabilities

| Capability | Implemented | Test evidence present | Evaluation evidence |
| --- | :---: | :---: | :---: |
| Modular Laravel domain core | ✓ | ✓ | — |
| Filament administration surfaces | ✓ | ✓ / mixed | — |
| Multi-provider assistant drivers | ✓ | Partial | — |
| Bounded tool-call run processor | ✓ | Partial | — |
| Module install / status / verify / upgrade commands | ✓ | ✓ | — |
| PWA-oriented field surfaces | ✓ | Partial | — |
| InstantAds AI adapters | ✓ | Partial | — |
| EInvoice AI adapters | ✓ | Partial | — |
| Finance / purchasing / payroll modules | ✓ | Partial | — |
| Communications integrations | ✓ | Partial | — |
| Full-suite green CI | — | **No** | — |
| Repository-level AI benchmark | — | — | **No** |

**Implemented**, **tested**, and **evaluated** are deliberately treated as different states.

---

## Example: bounded assistant run

The repository's distinctive AI path is a persisted assistant run rather than a one-shot wrapper around an API.

Conceptually:

```php
$run = $assistantService->createRun($thread, $input);

$processor->process(
    run: $run,
    maxIterations: 5,
);
```

Possible terminal state:

```json
{
  "status": "completed",
  "model": "provider-model",
  "tool_calls": [],
  "tool_results": [],
  "input_tokens": null,
  "output_tokens": null
}
```

If the assistant continues requesting tools past the configured bound, the run is stored as failed with:

```text
Maximum tool-call iterations reached without a final response.
```

Primary implementation:

- `plugins/filament-chatbot/src/Services/RunProcessorService.php`
- `plugins/filament-chatbot/src/Services/AssistantService.php`

---

## Installation and quick start

### Requirements

- PHP **8.4**
- Composer
- Node.js + npm
- a Laravel-compatible database
- provider credentials only for the AI providers you intend to exercise

### Clone and install

```bash
git clone https://github.com/Masterleeaus/Titan-Business-Operating-System.git
cd Titan-Business-Operating-System

composer install
npm install
cp .env.example .env
php artisan key:generate
```

Configure the database, then:

```bash
php artisan migrate
php artisan titan:module:verify --all
npm run build
```

Run locally:

```bash
composer run dev
```

### Test

```bash
composer run test
npm run build
```

### One-command project setup

The Composer manifest also defines:

```bash
composer run setup
```

which performs dependency installation, environment bootstrap, migration, module verification, frontend installation, and frontend build.

**Current caveat:** the repository does not yet have a clean full CI run; see [Evaluation](docs/evaluation.md) and [Known limitations](#known-limitations).

---

## Reproducible evaluation

The project does not currently publish a repository-level AI benchmark.

That is the correct boundary until provider behaviour and tool execution are tested against a fixed scenario set.

### Current CI evidence

The most recent source-backed CI evidence reviewed during this README pass is workflow run **#95**:

- PHP setup: passed
- Composer install: passed
- package discovery / Filament upgrade: passed
- application key generation: passed
- test execution: reached
- tests: **13 passed / 724 failed**
- dominant test blocker: duplicate `invoices` table creation under SQLite
- fresh migration job: database bootstrap/configuration failure before migrations execute
- post-migration `titan:module:verify --all`: skipped because the prior step failed

The README therefore does **not** display a green-test claim.

### Evaluation work that should come next

#### Provider normalisation suite

Run identical labelled scenarios against:

- OpenAI-compatible driver
- Anthropic driver
- Gemini driver

Measure:

- final-response normalisation
- tool-call normalisation
- malformed provider response handling
- provider error propagation
- token-usage mapping
- multi-round tool execution consistency

#### Tool-loop safety suite

Measure:

- valid tool resolution
- nonexistent tool rejection
- unavailable function handling
- malformed arguments
- repeated tool calls
- iteration exhaustion
- thrown tool exceptions
- persistence of failed state

#### Module verifier suite

Measure:

- healthy module pass rate
- intentionally broken module detection
- missing provider detection
- migration requirement detection
- command exit-code correctness

Full methodology and evidence rules: [docs/evaluation.md](docs/evaluation.md).

---

## Known limitations

1. **The full test suite is currently red.** The latest reviewed CI run reports 13 passing and 724 failing tests, with the duplicate `invoices` migration state dominating failures.

2. **The fresh-migration CI job is not currently proving fresh migration health.** Its database configuration does not produce the intended MySQL credentials at runtime, so it fails before migration execution and skips the module-verification step.

3. **Provider parity is not evaluated.** Three drivers exist, but the repository does not yet publish a shared provider conformance benchmark.

4. **Tool execution is bounded, not a complete authority system.** A five-round iteration limit prevents runaway loops, but the repository should not infer that every tool is safe merely because it is callable.

5. **Tenancy is an architectural requirement, not a fully audited guarantee.** The repository contains multiple historical naming schemes and domain modules; cross-tenant isolation requires systematic regression coverage.

6. **Product naming is evolving.** This README presents canonical engineering boundaries rather than treating every historical surface name in design documents as a current commercial product claim.

7. **The repository contains inherited and third-party material.** Attribution and licensing must be preserved. The root MIT file currently carries upstream copyright text and should not be reinterpreted as proof that every repository component has identical provenance.

---

## Testing

Primary backend command:

```bash
composer run test
```

Module lifecycle regression example:

```text
tests/Feature/Modules/ModuleCommandsTest.php

✓ install existing module
✓ reject nonexistent module
✓ idempotent install
✓ forced reinstall
✓ status output
✓ installed-module status
✓ verify existing module
✓ reject nonexistent module verification
✓ verify --all
✓ reject missing verify arguments
✓ reject unavailable upgrade path
✓ reject nonexistent upgrade target
```

The CI workflow is designed around two separate proofs:

```text
Fresh Migration Check                  Test Suite
        │                                  │
composer install                       composer install
        │                                  │
MySQL bootstrap                        app bootstrap
        │                                  │
migrate:fresh                          Pest suite
        │
titan:module:verify --all
```

At present, neither branch completes successfully end to end.

---

## System behaviour

A typical AI-assisted operation moves through:

```text
Authenticated application surface
            │
            ▼
Assistant thread + persisted run
            │
            ▼
Assistant configuration
            │
            ▼
LLM connection / driver
            │
            ▼
Normalised model response
            │
      ┌─────┴─────┐
      │           │
      ▼           ▼
final output   tool calls
      │           │
      │           ▼
      │      configured tool
      │           │
      │           ▼
      │      tool result
      │           │
      └───────────┴────► next bounded iteration
            │
            ▼
completed / failed persisted state
```

This flow is deliberately more inspectable than a controller directly calling a provider and discarding intermediate state.

---

## Architecture

<p align="center">
  <img src="docs/images/titan-bos-architecture.svg" alt="Titan Business Operating System architecture: application surfaces connect to shared Laravel modules, bounded AI services, module verification, Filament interfaces, and PWA-oriented field surfaces." width="100%" />
</p>

```text
┌────────────────────────────────────────────────────────────┐
│                    APPLICATION SURFACES                    │
│ owner / operations / field / customer / admin / AI        │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                    SHARED DOMAIN CORE                      │
│ operations · finance · people · docs · comms · quality    │
└──────────────┬──────────────────────────┬──────────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────────┐   ┌─────────────────────────────┐
│ AI EXECUTION BOUNDARY    │   │ MODULE LIFECYCLE BOUNDARY  │
│ drivers · runs · tools   │   │ install · verify · upgrade │
└──────────────┬───────────┘   └──────────────┬──────────────┘
               │                              │
               └──────────────┬───────────────┘
                              ▼
┌────────────────────────────────────────────────────────────┐
│ FILAMENT · PWA · QUEUES · EVENTS · EXTERNAL INTEGRATIONS  │
└────────────────────────────────────────────────────────────┘
```

Detailed architecture: [docs/architecture.md](docs/architecture.md)

---

## Reliability engineering

Source-visible reliability mechanisms include:

- bounded AI tool-call iterations
- persisted failed/completed assistant-run state
- exception capture on assistant execution
- explicit module verification with non-zero failure exit
- idempotency tests for module installation
- separate fresh-migration and application-test CI jobs
- Laravel queues and domain jobs
- feature/unit tests distributed across core and modules

The present reliability weakness is not hidden: the repository's verification pipeline is active but currently red.

---

## Safety and authority

The tool loop provides an execution mechanism. It should not be interpreted as a complete authorization model.

A safer application path is:

```text
User intent
   ↓
Authenticated application context
   ↓
Assistant recommendation / tool request
   ↓
Tool availability
   ↓
Domain authorization + validation
   ↓
Business-state mutation
   ↓
Persisted result / audit evidence
```

The repository should continue moving permission checks toward the domain action being performed rather than relying on model behaviour to decide authority.

---

## Observability

Assistant runs can persist:

- run status
- input and output
- message context
- requested tool calls
- tool results
- provider model
- input-token count
- output-token count
- start and completion timestamps
- failure messages

Module verification emits per-hook pass/fail results and a process exit status suitable for CI.

A future improvement is a single trace identifier that joins assistant runs, tool actions, queues, domain events, and external integrations.

---

## Continuous integration

`.github/workflows/ci.yml` currently defines:

### Fresh Migration Check

- PHP 8.4
- MySQL 8
- Composer install
- environment setup
- `migrate:fresh`
- `titan:module:verify --all`

### Test Suite

- PHP 8.4
- SQLite support
- Composer install
- Laravel bootstrap
- Pest test suite

The pipeline structure is appropriate; the current blockers need repair before the badge should be interpreted as project readiness.

---

## Security

Security-sensitive areas include:

- tenant/company scoping
- assistant tool execution
- provider credentials
- webhooks and external integrations
- payments and invoices
- file/document access
- field/PWA sync
- role and permission enforcement

The previous root security file described a different project name and tenancy vocabulary. It has been realigned to this repository as part of this portfolio pass.

See [SECURITY.md](SECURITY.md).

---

## Project status

| Area | Status |
| --- | --- |
| Shared Laravel module architecture | 🟢 Implemented |
| Filament 4 integration | 🟢 Implemented |
| OpenAI-compatible driver | 🟢 Implemented |
| Anthropic driver | 🟢 Implemented |
| Gemini driver | 🟢 Implemented |
| Bounded tool loop | 🟢 Implemented |
| Module verifier | 🟢 Implemented + test source |
| Frontend build tooling | 🟢 Present |
| Full application test suite | 🔴 Red |
| Fresh migration CI proof | 🔴 Blocked |
| Cross-provider evaluation | ⚪ Not established |
| Production certification | ⚪ Not claimed |

---

## Why this exists

Operational AI systems become harder to reason about when model integration is scattered across controllers and each product surface owns its own version of business state.

Titan Business Operating System explores a different structure:

1. keep the core business domains in ordinary Laravel modules
2. let multiple interfaces operate over the same domain state
3. place provider-specific AI behaviour behind drivers
4. persist assistant runs and tool evidence
5. bound tool iteration
6. make module health executable through verification commands

The central contribution is therefore **not simply “Laravel with AI.”**

It is the combination of a **modular business operating system with a normalised, bounded AI execution layer and executable module-health contracts**.

---

## Repository structure

```text
Titan-Business-Operating-System/
├── app/
│   ├── Console/Commands/Modules/      # module lifecycle CLI
│   ├── Models/
│   ├── Services/
│   └── Modules/
├── Modules/                           # business/domain modules
├── plugins/
│   └── filament-chatbot/
│       └── src/
│           ├── Contracts/
│           ├── Drivers/
│           ├── Models/
│           └── Services/
├── resources/                         # views, frontend assets, knowledge material
├── routes/
├── database/
├── tests/
├── docs/
│   ├── architecture.md
│   ├── evaluation.md
│   └── README.md
├── .github/workflows/
│   └── ci.yml
├── README.md
├── SECURITY.md
├── CONTRIBUTING.md
├── LICENSE
├── composer.json
└── package.json
```

---

## Design decisions

### Why normalise providers?

The assistant run processor should reason about one response contract rather than branching throughout application code for every provider.

### Why bound tool iterations?

A tool-capable model can repeatedly request actions. A hard execution bound gives the software a deterministic failure condition.

### Why persist tool calls and tool results?

Because tool execution is application behaviour, not ephemeral model reasoning. It should be inspectable after the request ends.

### Why module verification?

A modular application needs more than “the files exist.” Modules should be able to assert their own post-install health and fail CI when unhealthy.

### Why a shared domain core?

Separate interfaces should not create separate versions of the customer, job, invoice, worker, or operational truth.

---

## Technology

| Area | Technology |
| --- | --- |
| Language | PHP 8.4 |
| Framework | Laravel 12 |
| Module system | nwidart/laravel-modules |
| Admin | Filament 4 |
| Frontend | Vue, Inertia, Vite, Tailwind |
| AI execution | Repository-local Filament chatbot plugin |
| Providers | OpenAI-compatible, Anthropic, Gemini |
| Auth | Laravel Fortify, Sanctum |
| Realtime | Laravel Reverb / Echo |
| Testing | Pest 4 |
| CI | GitHub Actions |
| Payments / comms / integrations | Multiple adapter packages; verify per module |

---

## Performance

No p50/p95/p99 latency, throughput, token-cost, or provider-cost benchmark is currently published.

Performance claims should be added only with:

- fixed scenario set
- runtime/provider versions
- environment description
- test date
- reproduction command
- raw results

---

## Model and provider support

| Provider path | Implemented | Cross-provider conformance evaluated | Notes |
| --- | :---: | :---: | --- |
| OpenAI-compatible | ✓ | — | OpenAI-style Chat Completions contract |
| Anthropic | ✓ | — | request/response translation into normalised contract |
| Gemini | ✓ | — | generateContent translation into normalised contract |
| Custom `LlmDriverContract` | supported by resolver | — | requires compatible implementation |

“Implemented” does not mean every provider/model combination has been verified.

---

## Roadmap

### Immediate

- [ ] repair duplicate `invoices` migration/test state
- [ ] repair fresh-migration CI database bootstrap
- [ ] get `migrate:fresh` to complete in CI
- [ ] run `titan:module:verify --all` successfully in CI
- [ ] reduce full-suite failures to zero or explicitly quarantined known cases

### Next

- [ ] add provider-conformance scenarios
- [ ] add tool-loop adversarial and malformed-input tests
- [ ] evaluate iteration-exhaustion and failure persistence
- [ ] add tenant-isolation regression cases around AI-triggered tools
- [ ] add trace IDs spanning assistant run → tool → domain action

### Later

- [ ] latency and provider-cost benchmark
- [ ] feature ablation for bounded versus unbounded execution
- [ ] deployment smoke tests
- [ ] provider capability matrix based on executed tests

Roadmap items are intentions, not current capabilities.

---

## Engineering principles

### Evidence over claims

Repository paths, tests, CI logs, and reproduction commands take priority over adjectives.

### Model capability is not authority

A model being able to request a tool does not mean it should be allowed to mutate every domain object.

### Probabilistic reasoning, deterministic boundaries

Provider output may be probabilistic; iteration limits, permissions, validation, module verification, and state transitions should not be.

### Failures remain visible

Failed runs, failed module health checks, and red CI are evidence. They should not be edited out of the portfolio story.

### Shared state beats duplicated surfaces

Different interfaces should converge on the same domain truth.

---

## Documentation

| Document | Purpose |
| --- | --- |
| [docs/README.md](docs/README.md) | Engineering documentation entry point |
| [docs/architecture.md](docs/architecture.md) | Canonical system boundaries |
| [docs/evaluation.md](docs/evaluation.md) | Evidence rules and evaluation plan |
| [SECURITY.md](SECURITY.md) | Security policy and current security boundaries |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution and verification expectations |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | Reproducibility pipeline |

---

## Contributing

Before submitting a change, aim to run:

```bash
composer install
composer run test
php artisan titan:module:verify --all
npm install
npm run build
```

If a repository-wide blocker prevents completion, document the exact command and error rather than describing the change as fully verified.

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Responsible use

This repository should not be interpreted as evidence that autonomous AI execution is safe for financial, employment, compliance, safety-critical, or other high-impact decisions.

Human approval, domain authorization, tenant isolation, credential protection, and deployment-specific controls may still be required.

---

## License and provenance

The root repository contains an MIT license file carrying upstream copyright text.

The codebase also includes third-party packages, plugins, historical product material, and repository-local work. Preserve upstream attribution and review component-specific licensing before redistribution.

See [LICENSE](LICENSE).

---

<div align="center">

### Titan Business Operating System

**Shared business state. Bounded AI execution. Verifiable modules.**

Built so the important engineering claims can be inspected and challenged.

</div>
