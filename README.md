![Titan Business Operating System — modular Laravel business platform with shared domains and configurable overlays](docs/images/titan-bos-banner.svg)

# Titan Business Operating System

> A modular Laravel operating system for cleaning and adjacent service businesses: one shared domain core for owner, dispatch, field, customer, finance, communications, documents, and AI-assisted workflows.

Titan Business Operating System is the application source for a service-operations platform built as a modular monolith. It brings operational workflows, configurable vertical experiences, Filament administration, PWA-oriented field surfaces, and bounded AI features into one codebase so a business can extend its operating model without forking the core.

<p align="center">
  <img src="docs/images/titan-bos-architecture.svg" alt="Titan Business Operating System flow from user surfaces through shared Laravel modules and vertical overlays to Filament, PWA, tests, and configuration." width="100%" />
</p>

## Why this project exists

Service businesses often stitch scheduling, customer communication, field execution, invoicing, document generation, and marketing across disconnected tools. Titan BOS addresses that fragmentation with:

- a shared Laravel domain core instead of separate vertical applications
- purpose-built surfaces for owners, dispatchers, field operators, customers, and single-operator businesses
- configuration-driven vertical overlays for industry terminology, checklists, approvals, and artefacts
- AI assistance where the repository has concrete provider adapters, tool execution, or feature-level fallbacks

The result is an engineering platform for teams that need domain-specific workflows while keeping business rules, tenant boundaries, and integrations in one maintainable backend.

## Product and engineering highlights

| Capability | What the repository implements |
|---|---|
| Modular application core | Domain modules under Modules/ containing services, migrations, events, jobs, manifests, and Filament integrations |
| Admin and operations UI | Filament 4 resources and panels for operational, financial, people, communication, and integration domains |
| Field and customer surfaces | TitanPWA, TitanGo, and related PWA/node contracts for offline-aware work, sync, push, and recovery flows |
| AI assistant foundation | Provider drivers for OpenAI-compatible, Anthropic, and Gemini APIs, plus a bounded run processor with tool calls |
| Feature-level AI | InstantAds copy/image adapters with fallbacks and EInvoice invoice-oriented AI adapters |
| Documents and finance | TitanDocs, TitanVault, EInvoice, accounting, payroll, purchasing, and supply-chain modules |
| Communications | TitanHello, TitanTalk, TitanReach, webhooks, Twilio/Vonage/Telegram/OneSignal integration surfaces |
| Vertical extensibility | Shared workflows with configuration overlays rather than copied module forks |

## Architecture at a glance

~~~
Titan Business Operating System
├── Shared Laravel application core
│   ├── Domain modules under Modules/
│   ├── tenant-scoped workflows and migrations
│   ├── services, events, jobs, queues, and manifests
│   └── Filament 4 admin resources and panels
├── Product surfaces
│   ├── Titan Pro       owner and director command centre
│   ├── Ground Zero     dispatch and operations control
│   ├── Titan Go        field operator / cleaner PWA
│   ├── Zero Fuss       customer self-service PWA
│   ├── Titan Zero      chat and AI-oriented surface
│   ├── ZeroPay         invoicing and cashflow surface
│   ├── Titan Studio    marketing and lead workflows
│   ├── Titan Solo      single-operator mode
│   └── Titan Hello     communications and receptionist workflows
├── AI implementation surfaces
│   ├── plugins/filament-chatbot/
│   ├── Modules/InstantAds/
│   └── Modules/EInvoice/AI/
└── Documentation and design system
    ├── docs/04-AI/ and docs/architecture/
    ├── docs/05-Node/PWA/
    └── vertical overlay and module blueprints
~~~

The important architectural choice is the shared core: panels, PWAs, and integrations read and write the same domain modules. Vertical behaviour is expressed through configuration and overlay rules rather than a code fork for every industry.

## AI engineering that is in the code

This repository has a concrete AI foundation as well as broader AI architecture documentation.

### Reusable chatbot driver and tool loop

The filament-chatbot plugin normalises OpenAI-compatible, Anthropic, and Gemini provider calls behind driver contracts. RunProcessorService persists assistant runs and processes tool calls for up to five iterations before failing closed. This gives the application a reusable execution boundary for chat-driven workflows instead of scattering provider-specific calls through controllers.

### Bounded feature adapters

- Modules/InstantAds/Services/AdCopyService.php generates marketing copy through a bounded provider integration and supports fallback behaviour when provider configuration is absent.
- Modules/InstantAds/Services/AIChatImageService.php handles image ingestion and chat embedding by attaching already-generated images to a TitanZero signal.
- Modules/EInvoice/AI/ contains invoice-oriented AI code for financial document workflows.
- AI knowledge packs and vertical documentation provide the context layer for future domain-specific assistance.

### Honest gateway boundary

The current tree contains a reusable chatbot driver/tool loop and direct feature adapters. A single TitanZero::query() gateway is described in the architecture docs but is not yet an implemented invariant across every AI surface. That distinction makes the current code easier to evaluate and gives future consolidation a clear target.

## Domain map

The current module grouping makes the product surface easy to navigate:

- Operations: BookingModule, ManagedPremises, CleanQuality, TitanGo, TitanPWA
- Financial: Accountings, EInvoice, Payroll, Purchase, SupplyChain
- People: Recruit, Performance, Biometric, Letter
- Communications: TitanHello, TitanReach, TitanTalk, Webhooks
- AI and platform: TitanZero, TitanCore, Aitools
- Documents: TitanDocs, TitanVault
- Client-facing: Complaint, Clients, Asset
- Integrations: TitanIntegrations, QRCode

Tenant-facing queries are designed to be scoped to company_id; this is an architectural requirement, not a claim that every current query has been independently audited. Queues, provider adapters, and module manifests keep integration concerns close to the domain that owns them.

## Product surfaces and vertical overlays

The platform is designed around nine named surfaces over the shared backend:

| Surface | Primary audience | Product role |
|---|---|---|
| Titan Pro | Owner / director | Configure the business and review operations |
| Ground Zero | Dispatcher / operations team | Coordinate jobs, people, and live work |
| Titan Go | Field operator | Complete work from a mobile-oriented surface |
| Zero Fuss | Customer | Self-service and customer-facing workflows |
| Titan Zero | User and operator | Chat-oriented AI interaction surface |
| ZeroPay | Finance team | Invoicing, payments, and cashflow workflows |
| Titan Studio | Marketing team | Content, campaigns, and lead workflows |
| Titan Solo | Single operator | Simplified owner-operator experience |
| Titan Hello | Customer communications | Receptionist and omni-channel workflows |

Vertical overlays cover cleaning, property, specialist, and mobile-service contexts. They are intended to inject terminology, lifecycle rules, compliance gates, checklists, artefacts, and AI knowledge packs without duplicating the backend.

## Technology

| Layer | Technology |
|---|---|
| Framework | Laravel 12, PHP 8.4 |
| Module system | nwidart/laravel-modules 10.x |
| Admin panels | Filament 4 |
| AI | Chatbot provider drivers, tool-call processing, InstantAds, EInvoice AI |
| Real-time | Pusher and Laravel Echo |
| Communications | Twilio, Vonage, Telegram, OneSignal |
| Payments | Stripe, Square, PayID, PayPal, Razorpay, Mollie, BPAY |
| Documents | DomPDF and TitanDocs |
| Storage | AWS S3 or local Flysystem |
| Queues | Laravel database or Redis queues |
| Auth | Laravel Fortify and Sanctum |
| Search | Meilisearch / Scout-compatible |

## Evidence and current state

The Filament 4 chatbot resources were repaired in [PR #93](https://github.com/Masterleeaus/Titan-Business-Operating-System/pull/93). That change aligns the four Resource form contracts, AssistantRunResource infolist, resource page namespaces, and stale asset registrations with the current plugin tree.

[PR CI run #93](https://github.com/Masterleeaus/Titan-Business-Operating-System/actions/runs/37176197106) passed Composer installation and package discovery. The same run reached the application test phase but remains red on repository-wide issues: the test job reported 724 failures / 13 passes from the existing SQLite invoices duplicate-table setup, and fresh migration failed at MySQL authentication. The README does not treat that run as a passing full-suite result.

## Quickstart

Clone the repository and install the PHP and frontend dependencies:

~~~
composer install
npm install
~~~

Create a local environment and application key:

~~~
cp .env.example .env
php artisan key:generate
~~~

Run the application setup:

~~~
php artisan migrate
php artisan db:seed
npm run dev
php artisan queue:work
~~~

Useful validation commands:

~~~
php artisan test
npm run build
~~~

These commands require a configured PHP, database, Node.js, and provider environment. AI provider calls additionally require the relevant credentials and configuration.

## Code map

~~~
app/                    Core Laravel application
Modules/                Domain modules and their resources
plugins/filament-chatbot/Reusable chatbot drivers and run processor
docs/                   Architecture, product, AI, and node/PWA guidance
resources/              Blade views, assets, and AI knowledge packs
config/                 Platform and vertical configuration
database/               Migrations and seeders
routes/                 Web, API, public, settings, and SuperAdmin routes
tests/                  Feature and unit tests
~~~

Start with docs/README.md for repository guidance, then use the module map and docs/04-AI/ or docs/05-Node/PWA/ for the relevant implementation surface.

## Current boundaries

The repository combines implemented application code with active product development and architecture work. Several named surfaces and the central TitanZero gateway are still evolving, and the full application suite currently has the CI blockers described above. Provider-specific behaviour is bounded by its adapter and configuration; the repository does not claim universal model support, production readiness, benchmark performance, or a completed single-gateway AI runtime.

## Contributing

1. Read docs/README.md before code or architecture changes.
2. Check docs/Titan_Blueprints/34-PLATFORM-AND-MODULE-CHECKLIST-MASTER.md before marking work complete.
3. Scope tenant queries to company_id.
4. Extend shared modules and configuration overlays instead of forking vertical implementations.
5. Treat the chatbot driver/tool loop as the reusable AI surface while consolidating direct adapters toward the documented gateway architecture.
