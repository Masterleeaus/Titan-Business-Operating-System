# Titan Business Operating System — Evaluation

## Evidence policy

This repository uses five different evidence labels:

- **Implemented** — canonical source is present and wired.
- **Tested** — relevant tests have executed successfully.
- **Evaluated** — a reproducible scenario set, metric, result, and comparison exist.
- **Experimental** — implementation exists but verification is incomplete.
- **Planned** — no implementation claim is made.

These labels are not interchangeable.

## Remediation after the reviewed run

The MySQL workflow configuration described below was repaired on `main`: CI now removes both commented and active DB settings from `.env` and appends one canonical testing database block. This is a configuration fix, not passing migration evidence. The duplicate `invoices` table ownership/collision remains unresolved and needs an explicit schema decision.

## Current CI evidence

Reviewed workflow: `CI`, run #95 / GitHub Actions run `37176359112`.

### Test Suite job

Reached:

- checkout
- PHP 8.4 setup
- Composer dependency installation
- environment copy
- application key generation
- Pest execution

Result:

```text
Tests: 724 failed, 13 passed (27 assertions)
Duration: 55.32s
```

The repeated failure shown in the job log is:

```text
SQLSTATE[HY000]: General error: 1 table "invoices" already exists
Connection: sqlite
Database: :memory:
```

This means the 724 failures should not be interpreted as 724 independent feature defects. A shared migration/bootstrap defect can cascade across a large test suite.

### Fresh Migration Check job

Reached:

- MySQL service startup
- PHP setup
- Composer install
- environment copy
- database configuration script
- application key generation

It then failed before migration execution with Laravel attempting:

```text
Database: laravel
user: root
using password: NO
```

The checked-in `.env.example` comments out the database name/user/password lines while the CI script only replaces uncommented lines matching `^DB_...`. The intended values therefore do not become active for those commented variables.

The job consequently does not yet establish whether `migrate:fresh` or post-migration module verification succeeds.

## Current evidence table

| Area | State |
| --- | --- |
| Composer install in CI | Verified in run #95 |
| Laravel package discovery | Verified in run #95 |
| Pest starts | Verified |
| Full Pest suite | Red |
| Fresh MySQL migration | Not reached successfully |
| `titan:module:verify --all` in CI | Skipped because migration job failed first |
| Multi-provider driver source | Implemented |
| Provider conformance benchmark | Not established |
| Tool-loop evaluation | Not established |
| Production certification | Not claimed |

## Evaluation 1 — provider conformance

### Claim

Provider-specific drivers should expose equivalent normalised behaviour to the run processor for supported operations.

### Providers

- OpenAI-compatible
- Anthropic
- Gemini

### Scenario classes

- simple text completion
- system instruction
- conversation history
- one tool call
- multiple tool calls
- tool result continuation
- empty response
- malformed response
- provider error
- token usage present
- token usage absent

### Metrics

- response-normalisation pass rate
- tool-call normalisation pass rate
- error propagation correctness
- usage-field mapping correctness

### Required reproduction

A future result should include:

- fixed scenario data
- provider/model versions
- seed where applicable
- repository commit
- raw outputs or redacted fixtures
- one command to run the suite

## Evaluation 2 — bounded tool execution

### Claim

The assistant loop should complete valid tool workflows while failing visibly and deterministically when it cannot resolve them within the configured bound.

### Cases

- valid tool
- unknown tool namespace
- missing function
- malformed arguments
- thrown tool exception
- repeated tool call
- no final answer after maximum iterations
- normal completion before maximum iterations

### Metrics

- valid completion rate
- invalid tool rejection rate
- correct failed-state persistence
- iteration-limit enforcement
- tool evidence persistence

### Ablation

Compare:

1. bounded tool loop
2. the same loop with the iteration limit disabled in a controlled test harness

The purpose is not to prove the bounded system is “smarter”; it is to show that the boundary prevents non-terminating tool-call behaviour.

## Evaluation 3 — module health verification

### Claim

The verifier should detect intentionally broken module health conditions and return a failing process status.

### Cases

- healthy module
- nonexistent module
- missing expected provider
- failed custom health hook
- broken migration requirement
- all modules healthy
- one unhealthy module among many

### Metrics

- true unhealthy detection rate
- false unhealthy rate
- exit-code correctness

## What current evidence establishes

It establishes that:

- the provider abstractions are implemented
- tool iterations are bounded in source
- assistant run state is persisted
- module verification is implemented
- dedicated module command tests exist
- CI actively executes dependency/bootstrap/test stages

## What it does not establish

It does not prove:

- provider parity
- production reliability
- tenant isolation across every module
- safe autonomous execution
- low latency
- low cost
- a green deployment path

## Priority before publishing AI benchmark numbers

1. repair the duplicate invoice migration state
2. repair the MySQL CI bootstrap
3. get fresh migrations green
4. get `titan:module:verify --all` to execute in CI
5. reduce or classify the remaining test failures
6. then add the provider and tool-loop benchmark suites
