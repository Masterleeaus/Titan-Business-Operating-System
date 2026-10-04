# Contributing to Titan Business Operating System

## Principle

A contribution is not complete merely because the source compiles or the feature appears in the UI.

Changes should preserve the repository's shared-domain architecture and make verification clearer.

## Before coding

Identify the boundary being changed:

- domain module
- Filament/admin interface
- PWA/field interface
- AI provider driver
- assistant/tool execution
- module lifecycle tooling
- finance/payments
- communications/integration
- tenancy/authorization
- migration/infrastructure

## Local setup

```bash
composer install
npm install
cp .env.example .env
php artisan key:generate
```

Configure a local database before running migrations.

## Verification

Aim to run:

```bash
php artisan migrate
php artisan titan:module:verify --all
composer run test
npm run build
```

The repository currently has known test and CI blockers. If they prevent full verification:

- report the exact command that failed
- include the failure reason
- distinguish targeted verification from full-suite verification
- do not mark unrun tests as passing

## AI changes

Changes to provider drivers or the assistant tool loop should cover, where relevant:

- normal completion
- provider error
- malformed provider response
- tool-call translation
- unknown tool
- unavailable function
- malformed arguments
- thrown tool exception
- iteration exhaustion
- failed-state persistence
- token-usage mapping

## Module changes

Module changes should preserve:

- installability
- idempotent installation where expected
- module health verification
- tenant/company scoping
- migrations
- tests
- resource/route registration

If a module owns a post-install invariant, prefer adding it to module verification rather than documenting it only in prose.

## High-risk changes

Changes involving authorization, tenant boundaries, payment state, payroll, credentials, webhooks, files, AI-triggered mutations, or external side effects should include negative tests and replay/idempotency cases where applicable.

## Evidence language

Use these labels consistently:

- **Implemented**
- **Tested**
- **Evaluated**
- **Experimental**
- **Planned**

Do not use them as synonyms.

## Documentation

Update the same pull request when a change affects:

- public capability claims
- architecture
- evaluation status
- security posture
- known limitations
- installation or reproduction commands

Start with `docs/README.md`.
