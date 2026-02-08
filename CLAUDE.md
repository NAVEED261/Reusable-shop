# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

---

# Men's Boutique E-Commerce Platform - Implementation Plan

**Project**: Transform learnflow-app into a complete men's boutique e-commerce platform
**Status**: Ready for autonomous execution
**Timeline**: 7 days
**Reusability**: 70-80% of existing codebase

## Execution Mode: FULLY AUTONOMOUS

- ✅ Execute all phases without asking for confirmation
- ✅ Use browser automation for GitHub, Vercel, image selection
- ✅ Deploy to production automatically
- ✅ Run E2E tests autonomously
- ✅ Create comprehensive documentation

## Implementation Phases

### Phase 1: Product Images & Database (Day 1)

**Objective**: Acquire 40 men's clothing images and update database

**Tasks**:
1. Use `browser-use` skill to autonomously download images from royalty-free sources:
   - Unsplash, Pexels, Pixabay
   - 10 Fancy Suits, 10 Shalwar Qameez, 10 Cotton Suits, 10 Designer Brands
   - Save to: `/public/images/{category}/{category}-{01-10}.jpg`
   - Optimize: 800x1200px, <200KB, WebP format

2. Update database content:
   - Edit `database/seeds/sample_products.sql`
   - Change product names/descriptions for men's clothing
   - Run migration: `psql $DATABASE_URL < database/seeds/sample_products.sql`

**Critical Files**:
- `learnflow-app/app/frontend/public/images/` (add images)
- `learnflow-app/database/seeds/sample_products.sql` (update)

**Validation**: All 40 images load, products display correctly

---

### Phase 2: RAG System Implementation (Day 2-3)

**Objective**: Implement Qdrant vector database for intelligent product recommendations

**Tasks**:
1. Set up Qdrant vector database
   - Add to Docker Compose
   - Create collection with OpenAI embeddings (1536 dimensions)
   - Build `chat-service/app/rag_client.py` wrapper

2. Generate product embeddings
   - Create `scripts/generate_embeddings.py`
   - Use OpenAI `text-embedding-ada-002`
   - Store embeddings in Qdrant for all 40 products

3. Enhance chat service with RAG
   - Modify `chat-service/app/routes.py`
   - Add semantic search before responses
   - Inject product context into system prompt

**Skills**: `building-rag-systems`
**Agent**: `prod-microservices-operator`

**Validation**: Chat query "formal wedding suit" returns relevant products with context

---

### Phase 3: WhatsApp Integration (Day 3)

**Objective**: Add WhatsApp Click-to-Chat feature

**Tasks**:
1. Create WhatsApp button component
   - New: `components/WhatsAppButton.tsx`
   - Pre-fill message with product name + URL
   - Format: `https://wa.me/{number}?text={message}`

2. Integrate into product pages
   - Modify: `app/products/[id]/page.tsx`
   - Add env variable: `NEXT_PUBLIC_WHATSAPP_NUMBER`

**Skills**: `building-nextjs-apps`
**Agent**: `frontend-ui-architect`

**Validation**: WhatsApp button opens with pre-filled product message

---

### Phase 4: Stripe Payment Integration (Day 4-5)

#### 4.1 Backend (Day 4)

**Tasks**:
1. Add Stripe to order service
   - Install `stripe==7.8.0`
   - New: `order-service/app/stripe_client.py`
   - Implement `create_payment_intent()` for PKR currency

2. Create webhook handler
   - Add `/api/webhooks/stripe` endpoint
   - Verify webhook signature
   - Update order status on payment success

3. Update checkout endpoint to return `client_secret`

**Skills**: `building-fastapi-apps`
**Agent**: `prod-microservices-operator`

#### 4.2 Frontend (Day 5)

**Tasks**:
1. Install Stripe Elements
   - `npm install @stripe/stripe-js @stripe/react-stripe-js`

2. Create checkout form
   - New: `components/StripeCheckoutForm.tsx`
   - Use `PaymentElement` component

3. Integrate in cart page
   - Modify: `app/cart/page.tsx`
   - Call checkout API, get `clientSecret`

**Skills**: `building-nextjs-apps`
**Agent**: `frontend-ui-architect`

**Validation**: Test card (4242 4242 4242 4242) processes successfully

---

### Phase 5: End-to-End Testing (Day 6)

**Objective**: Comprehensive test suite validation

**Tasks**:
1. Frontend E2E tests (Playwright)
   - Complete checkout flow
   - Product browsing and search
   - Cart management

2. Backend API tests (pytest)
   - Stripe payment intent creation
   - Webhook handling
   - RAG semantic search

3. Integration tests
   - Service-to-service communication
   - Database transactions

**Skills**: `autonomous-e2e-testing`
**Agent**: `autonomous-e2e-testing`

**Validation**: 95%+ test pass rate, 70%+ backend coverage, 60%+ frontend

---

### Phase 6: Production Deployment (Day 7)

#### 6.1 Frontend to Vercel

**Tasks**:
1. Verify local build succeeds
2. Deploy with Vercel CLI: `vercel --prod`
3. Configure environment variables:
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
   - `NEXT_PUBLIC_WHATSAPP_NUMBER`

#### 6.2 Backend Deployment

**Options**:
- **Railway.app** (recommended for simplicity)
- **Render.com**
- **Kubernetes** (production-grade)

**Tasks**:
1. Deploy each FastAPI service
2. Set environment variables
3. Verify database connectivity
4. Test Stripe webhooks

**Skills**: `deploying-cloud-k8s`, `containerizing-applications`
**Agent**: `prod-microservices-operator`

#### 6.3 Database & Qdrant

**Tasks**:
1. Create production PostgreSQL (Neon/Supabase)
2. Run migrations
3. Seed product data
4. Generate production embeddings

**Validation**: All services healthy, payments work, RAG responses correct

---

## Critical Files to Modify

### Must Modify:
1. `learnflow-app/database/seeds/sample_products.sql` - Products for men's clothing
2. `learnflow-app/app/backend/chat-service/app/routes.py` - RAG integration
3. `learnflow-app/app/backend/order-service/app/routes.py` - Stripe checkout + webhook
4. `learnflow-app/app/frontend/app/products/[id]/page.tsx` - WhatsApp button
5. `learnflow-app/app/frontend/app/cart/page.tsx` - Stripe checkout form

### Must Create:
1. `learnflow-app/app/backend/chat-service/app/rag_client.py` - Qdrant wrapper
2. `learnflow-app/app/backend/order-service/app/stripe_client.py` - Stripe integration
3. `learnflow-app/app/frontend/components/WhatsAppButton.tsx` - WhatsApp component
4. `learnflow-app/app/frontend/components/StripeCheckoutForm.tsx` - Payment form
5. `learnflow-app/scripts/generate_embeddings.py` - Embedding generation
6. `learnflow-app/docker-compose.yml` - Add Qdrant service
7. E2E test files for all critical flows

---

## Skill & Agent Mapping

| Phase | Task | Skill | Agent |
|-------|------|-------|-------|
| 1 | Image acquisition | `browser-use` | Main |
| 2 | RAG system | `building-rag-systems` | `prod-microservices-operator` |
| 3 | WhatsApp | `building-nextjs-apps` | `frontend-ui-architect` |
| 4.1 | Stripe backend | `building-fastapi-apps` | `prod-microservices-operator` |
| 4.2 | Stripe frontend | `building-nextjs-apps` | `frontend-ui-architect` |
| 5 | E2E testing | `autonomous-e2e-testing` | `autonomous-e2e-testing` |
| 6 | Deployment | `deploying-cloud-k8s` | `prod-microservices-operator` |

---

## Verification Checklist

- [ ] Phase 1: All 40 images load, products show men's clothing
- [ ] Phase 2: Chat returns context-aware product recommendations
- [ ] Phase 3: WhatsApp button works on all product pages
- [ ] Phase 4: Test payment succeeds, order status updates
- [ ] Phase 5: 95%+ tests pass, no critical failures
- [ ] Phase 6: Production site live, all features work

**Final Validation**:
- [ ] Browse → Cart → Checkout → Pay → Order confirmed
- [ ] Chat provides relevant recommendations
- [ ] WhatsApp integration works
- [ ] Images load correctly
- [ ] Page load <2.5s, API <200ms
- [ ] Error rate <1%, uptime 99.9%

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Image licensing | Use only Unsplash/Pexels/Pixabay |
| Stripe webhooks | Implement retry logic, monitor logs |
| RAG performance | Optimize embeddings, cache results |
| Deployment issues | Blue-green deployment, rollback plan |

---

## Timeline

| Day | Phase | Hours |
|-----|-------|-------|
| 1 | Images + DB | 4-5h |
| 2 | Qdrant setup | 4-5h |
| 3 | RAG + WhatsApp | 4-5h |
| 4 | Stripe backend | 4-5h |
| 5 | Stripe frontend | 3-4h |
| 6 | E2E testing | 8h |
| 7 | Deployment | 6-8h |

**Total**: 7 days (33-41 hours)

---

## Success Metrics

- **Technical**: 99.9% uptime, <200ms API response, <1% error rate
- **Quality**: 70%+ test coverage, zero critical vulnerabilities
- **Performance**: <2.5s page load, <500ms RAG search
- **Business**: >95% payment success rate, >3 messages per chat session

---

## Deployment URLs

**Frontend**: https://vercel.com/naveeds-projects-04d1df6d
**GitHub**: https://github.com/NAVEED261/Reusable-shop
**Backend**: TBD (Railway/Render/K8s)
