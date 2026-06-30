# Workshop Todo List

## Act 1 — Respond to the RFP

- [x] Read the RFP together using `@docs/rfp/MC-2026-0417.md`
- [x] Summarize the RFP: required items, desired items, ambiguities
- [x] Read `docs/rfp/meridian-background.md` and `docs/rfp/vendor-handoff.md`
- [x] Draft 3–5 clarifying questions for procurement (per RFP §6, due April 28)
- [x] Write `proposal/executive-summary.md`
- [x] Write `proposal/technical-approach.md`
- [x] Write `proposal/timeline.md`
- [x] Write `proposal/pricing.md`
- [x] Build `proposal/capabilities-deck.html` (10–15 slides)
- [x] (Optional) Convert deck to `proposal/capabilities-deck.pptx`

### Quality Review — Korrekturen

- [x] **KRITISCH** Create `proposal/relevant-experience.md` — 3 anonymisierte Referenzprojekte
- [x] **KRITISCH** Add experience slide to deck — Slide 11 "Relevant Experience" (3 Projektkarten)
- [x] Reconcile Phase 1 duration — jetzt konsistent Wochen 1–2 in timeline.md + Deck
- [x] Add "What's not included" scope exclusions to `proposal/pricing.md`
- [x] Address EUR vs USD currency question in `proposal/pricing.md`
- [x] Strengthen CI integration in `proposal/technical-approach.md` — GitHub Actions workflow als konkretes Deliverable
- [x] Add client responsibilities / dependencies note to `proposal/timeline.md`
- [x] adesso logo in deck (wordmark, brand red #e3000f)
- [x] Team slide — 4 named profiles (Lars, Sophie, Daniel, Yuki)
- [x] Pricing slide — vollständige Aufschlüsselung per Deliverable
- [x] R4 section in technical-approach.md — Methodik + Deliverable-Detail
- [x] Team role assignments in technical-approach.md
- [x] Timeline — R3 Meilensteine geklärt (Week 5 IT gate, Week 8 final)
- [x] Timeline — Phase 3 fallback wenn D1–D3 abgelehnt
- [x] Relevant experience — 4. Projekt (Helix) + realistische Schwächen pro Projekt
- [x] (Optional) Add architecture diagram or Restocking wireframe to deck

## Act 2 — Deliver the engagement

- [x] Start the app with `/start` and verify it runs at localhost:3000
- [x] R4: Architecture review → generate `proposal/architecture.html`
- [x] R1: Audit and fix all Reports module defects (filters, i18n, API patterns)
  - [x] Audit complete — 6 defects found (see architecture.html#reports-audit)
  - [x] Fix: FilterBar ignored — Reports.vue doesn't use `useFilters`
  - [x] Fix: No i18n — hardcoded English, no `t()` calls
  - [x] Fix: 14 console.log() statements
  - [x] Fix: API endpoints return raw dicts instead of Pydantic models
  - [x] Fix: Options API → migrate to Composition API (`<script setup>`)
  - [x] Fix: Duplicate `formatNumber()` — use shared `currency.js` instead
- [x] R2: Build Restocking recommendations view (stock + demand + budget ceiling)
  - [x] Fix: `translateCategory` used hardcoded EN map — switched to `t('categories.*')` keys for proper Japanese translation

### Quality Review — R2 Restocking
- [x] QR pass — one i18n gap found and fixed (translateCategory now uses t() keys)

- [x] R3: Write automated browser tests using Playwright MCP for critical flows
  - [x] Write backend unit tests for restocking endpoint (`tests/backend/test_restocking.py`, 17 tests)
### Quality Review — Extended R1 Defect Sweep
- [x] Fix: `nav.companyName` = "Catalyst Components" → "Meridian Components" (en.js + ja.js)
- [x] Fix: "Reports" nav tab hardcoded English → `t('nav.reports')` (App.vue + locales)
- [x] Fix: `/api/tasks` endpoints missing on server — added CRUD routes (server/main.py)
- [x] Fix: Dead `createPurchaseOrder`/`getPurchaseOrderByBacklogItem` methods in api.js
- [x] Fix: `PurchaseOrderModal` referenced but never imported/exists in Dashboard.vue
- [x] Fix: PO status check used `item.purchase_order_id` but API returns `item.has_purchase_order`
- [x] Fix: `getCircleSegment` used multiplier 440 but SVG circumference is 408 (Dashboard.vue)
- [x] Fix: Spending quarter filter (`Q2-2025`) broke `split('-')[1]` → $0 KPIs (Spending.vue)
- [x] Fix: `console.log` + blocking `alert()` in transaction click handler (Spending.vue)
- [x] Fix: `getBarHeight` hardcoded max 25000 — bars overflow container (Spending.vue)
- [x] Fix: Demand trend cards showed `++4.5%` (double `+`) for increasing items (Demand.vue)
- [x] Fix: Backlog.vue entirely hardcoded English — added `useI18n` + locale keys (Backlog.vue)
- [x] Fix: Reports.vue error message hardcoded English → `t('reports.error.loadFailed')` (Reports.vue)
- [x] Fix: Missing comma after `reports` key in nav object (en.js + ja.js) — JS syntax error that crashed locale parse
- [x] Fix: `getBarHeight` hardcoded maxValue=25000 → dynamic `maxCostValue` computed from actual data (Spending.vue)

- [ ] Commit, push, and open a PR
- [ ] (Stretch) D1: UI modernization
- [ ] (Stretch) D2: Full i18n for remaining modules
- [ ] (Stretch) D3: Dark mode (prototype on a worktree branch)
