# Security Policy

## Scope

Titan Business Operating System contains business-operation, customer, workforce, financial, communication, document, integration, and AI-assisted workflows.

Security-sensitive boundaries include:

- authentication and authorization
- tenant/company data isolation
- AI tool execution
- provider credentials
- invoices, payments, payroll and finance
- customer and service-location data
- documents and file uploads
- webhooks and third-party integrations
- PWA / field-device synchronization
- queues and background jobs

## Supported code

The actively maintained target is the repository's current default branch, `main`.

No claim is made that every historical branch or retained module receives security backports.

## Reporting a vulnerability

Do **not** publish exploitable details, real credentials, customer information, or destructive proof-of-concept material in a public issue.

Preferred path:

1. use GitHub Private Vulnerability Reporting / Security Advisories for this repository when available
2. otherwise contact the repository owner privately through the account's published contact channel
3. include the affected component, impact, reproduction conditions, and a minimal non-destructive proof

## Security expectations

### Tenant isolation

The current architecture uses tenant/company scoping as a design requirement.

Because the repository contains a large set of modules and historical naming conventions, this README does **not** claim that every query has been independently audited for isolation.

Changes that read or mutate tenant-owned state should include cross-tenant negative tests.

### AI tool execution

A model requesting a tool is not authorization to perform the action.

Tool implementations should enforce ordinary application controls:

```text
authenticated actor
      ↓
tenant/company context
      ↓
capability / permission
      ↓
validated domain action
      ↓
state mutation
```

The bounded tool loop limits execution rounds but should not be treated as a security boundary by itself.

### Provider credentials

Provider API keys must remain server-side and must not be written to logs, committed to the repository, or returned to clients.

### External integrations

Webhook and callback endpoints should verify signatures or equivalent authenticity controls where the upstream service supports them.

### Financial state

Invoice, payment, refund, payroll, and settlement changes should receive stricter authorization, audit, replay/idempotency, and regression coverage than ordinary read-only features.

## Secrets

Never commit:

- API keys
- OAuth client secrets
- webhook signing secrets
- production database credentials
- customer exports
- private certificates
- real session tokens
- payment credentials

Use environment variables or deployment secret storage.

## Current verification boundary

The repository's CI pipeline is currently red. The current test and fresh-migration blockers are documented in `docs/evaluation.md`.

Do not describe a security-sensitive change as fully verified when the relevant regression tests did not run successfully.

## Responsible disclosure

Good-faith research should minimize access to data that is not owned by the researcher, avoid service disruption, and allow reasonable time for remediation before public disclosure.
