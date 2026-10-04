# Titan Business Operating System — Documentation

This directory contains both current engineering documentation and historical/product design material.

For portfolio and implementation work, start with the evidence-backed documents below.

## Start here

| Document | Purpose |
| --- | --- |
| [../README.md](../README.md) | Repository overview, evidence, quickstart and current status |
| [architecture.md](architecture.md) | Canonical high-level engineering boundaries |
| [evaluation.md](evaluation.md) | Verification state and evaluation methodology |
| [../SECURITY.md](../SECURITY.md) | Security reporting and current security boundaries |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | Development and verification expectations |

## Domain documentation

The repository also contains detailed material for:

- PWA / node operation
- signals and module blueprints
- AI architecture
- platform/module design
- interface/navigation design
- testing and deployment

Those documents vary in maturity. Some describe target architecture rather than completed runtime behaviour.

When documentation and source disagree, use this order of evidence:

1. current canonical runtime source
2. executable tests and CI
3. current architecture/evaluation docs
4. active implementation documents
5. historical blueprints / plans

Do not upgrade a planned capability to “implemented” solely because a design document exists.
