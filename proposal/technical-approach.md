# Technical Approach — Meridian Components Inventory Dashboard
**RFP MC-2026-0417 | adesso Response**

---

## Technical Approach

Our approach is rooted in understanding what the previous vendor left before writing a single line of code. We begin each deliverable with a read-and-map phase — examining existing Vue components, FastAPI endpoints, and data files — so that every fix and every new feature builds on an accurate picture of the current system rather than assumptions. The stack (Vue 3 + Vite frontend, Python FastAPI backend, JSON-backed data layer) is well-understood by our team, and the architecture is small enough that a thorough orientation takes hours, not days.

---

### R1 — Reports Module Remediation

Before touching code, we conduct a structured audit of the Reports page. This means reading every Vue component in the Reports module, tracing each filter through to its corresponding FastAPI endpoint, and documenting where the wiring breaks — missing query parameters, mismatched response shapes, untranslated strings, and any patterns that diverge from the rest of the application. We will document every defect we find — we expect to substantially exceed eight — and address them in priority order.

Our fix strategy follows the audit findings. For filter behavior, we wire the missing query parameters end-to-end: the Vue component emits the correct params, the API accepts and applies them, and the response reflects the filtered result. For i18n gaps, we add the missing translation keys to the existing i18n configuration (the project already has an i18n setup in place) and ensure every user-facing string in the Reports view is covered. For API pattern inconsistencies, we align the Reports endpoints with the conventions used elsewhere in the FastAPI layer — consistent field naming, consistent error shapes, consistent pagination where applicable. Each defect gets a corresponding entry in our issue log so Meridian's IT team has a clear before/after record.

---

### R2 — Restocking Recommendations

The Restocking view is a net-new feature added as a first-class page in the Vue application, consistent in structure and navigation with the existing views. The operator experience is straightforward: select a warehouse, enter a budget ceiling, and see a ranked list of recommended purchase orders.

On the backend, we add a single new FastAPI endpoint — `/api/restocking` — that accepts warehouse and budget parameters. The endpoint reads current inventory levels and demand forecast data, then applies a prioritisation algorithm: items are ranked by reorder urgency (a function of current stock relative to reorder threshold and lead time) weighted by unit cost. The allocation engine then walks down the ranked list, building a purchase order set that stays within the operator-supplied budget ceiling. The response returns each recommended line item with quantity, unit cost, subtotal, and the rationale score so operators can see why an item was prioritised. The algorithm includes a minimum-data threshold: SKUs with fewer than 30 days of demand history (likely for recently added Tokyo warehouse items) fall back to supplier reorder-point defaults rather than forecast-driven recommendations, preventing false confidence on sparse data.

On the frontend, the new Vue view consumes this endpoint and renders the recommendations in a clear table. The budget ceiling input is reactive — changing it re-queries the API and updates the list without a page reload. The view is built using the Composition API, consistent with the modern parts of the existing codebase.

---

### R3 — Automated Browser Testing

We use Playwright for end-to-end test coverage. We use Playwright as our standard end-to-end testing tool. It requires no additional tooling decisions from Meridian's IT team and integrates cleanly with any standard CI pipeline.

Coverage targets the four flows IT has confirmed as critical: inventory browse with warehouse filter applied, the orders view including status filter, the Reports module (all filter interactions and data display — this directly validates the R1 remediation), and the new Restocking flow (budget input, recommendation output). Tests run headless and produce clear pass/fail output suitable for a CI pipeline. We will document how to run the suite locally. As part of the R3 deliverable, adesso will deliver a ready-to-run CI configuration file (GitHub Actions workflow by default; adaptable to GitLab CI, Jenkins, or Azure DevOps at no additional cost). The test suite will run headless, produce a clear pass/fail report, and be executable with a single command — no adesso involvement required for ongoing test runs.

The intent is not just coverage for its own sake but a regression net: once the Reports defects are fixed, the tests confirm they stay fixed.

---

### R4 — Architecture Documentation

We deliver a current-state architecture overview as a self-contained HTML page with an embedded interactive diagram, a written component inventory table, and a dedicated section flagging technical debt for Meridian IT. Delivered end of Week 2, shared with IT before any code changes begin — so the team is aligned on the baseline before remediation work starts.

**Methodology.** The review is conducted by reading the codebase directly, verifying the previous vendor's handoff notes against the actual code, and documenting what we find rather than what we were told. The review covers four areas:

- **Data flow.** We trace the full path from source to screen: JSON files in `server/data/` → `mock_data.py` → FastAPI endpoint handlers → Pydantic response models → `api.js` in the Vue client → component computed properties and template bindings. Each hop is documented with the field names and shapes that cross it, so Meridian IT can follow data from a raw JSON record to a rendered cell without guessing.

- **Component inventory.** We catalogue every view and component in the frontend, noting which use the Composition API and which still use the Options API. Components that have not yet been migrated are flagged — they are not bugs, but they are friction for future maintainers, and Meridian should know where they are. The inventory is delivered as a table: component name, file path, API style, notes.

- **Filter system.** We document how the four dashboard filters (Time Period, Warehouse, Category, Order Status) are wired end-to-end: how each filter state is held in the Vue component, how it is serialised into query parameters, how the FastAPI endpoint receives and applies it, and where the current implementation deviates from a consistent pattern. This directly informs the R1 remediation plan.

- **Known gaps and technical debt.** We document findings that are not broken but are debt: inconsistent naming conventions, endpoints that do not follow the rest of the API's patterns, missing validation, areas where the test surface is thin. These are presented to IT as a prioritised list, not a complaint — the goal is an honest baseline.

The documentation is written for Meridian's IT team, not for developers — it prioritises clarity over technical depth, and includes a plain-language summary of each layer alongside the visual. This gives IT a durable reference for onboarding future vendors or internal staff, which directly addresses the pain Meridian experienced when the previous vendor departed with minimal handoff.

---

### D1–D3 — Desired Deliverables

**D1 — UI Modernisation.** We refine the existing interface using the design tokens already present in the codebase. This is a polish pass, not a rebrand: improved spacing, consistent component states, accessible colour contrast, and responsive behaviour for the tablet-sized screens common on warehouse floors. Meridian's procurement response (Q2) confirmed this scope explicitly — clean, accessible, and consistently styled is the target. If Meridian later decides to pursue a full visual identity change or custom design system, that would be scoped separately as a change order.

**D2 — Full Internationalisation.** The existing i18n setup covers the primary views; we extend it to all remaining views and components. Given the Tokyo warehouse's varying English proficiency (opened 2023, noted in background materials), we treat Japanese as the primary second language, with the translation file structure ready to accommodate additional locales if Meridian expands further.

**D3 — Dark Mode.** We implement dark mode via CSS custom properties, giving operators a toggle that persists across sessions. Warehouse floor stations frequently operate in low-light environments, and a well-implemented dark mode reduces eye strain and screen glare without any change to the underlying component logic.

---

### Delivery Team Assignments

| Deliverable | Owner | Support |
|---|---|---|
| R4 Architecture documentation | Daniel Kovač (backend) + Sophie Berger (frontend) | Lars Meijering (review) |
| R1 Reports remediation | Sophie Berger | Daniel Kovač (API fixes) |
| R2 Restocking recommendations | Daniel Kovač (API) + Sophie Berger (UI) | Yuki Tanabe (test coverage) |
| R3 Automated testing | Yuki Tanabe | Sophie Berger (test scenario design) |
| D1 UI modernization | Sophie Berger | — |
| D2 Internationalization | Sophie Berger + Yuki Tanabe | — |
| D3 Dark mode | Sophie Berger | — |

---

### Assumptions

Several gaps in the RFP required us to make reasonable assumptions, which we flag here for client confirmation. On budget, we have scoped this engagement at a fixed fee of €37,500 for required deliverables, with a not-to-exceed cap of €52,500 if all optional items are included (detailed in the Pricing section), but have not received a stated range from procurement — if Meridian's ceiling differs materially, we are open to a phased scope conversation. On "current standards" for D1, we have assumed clean, accessible, mobile-friendly refinement of the existing design system rather than a net-new visual identity; if Meridian has brand guidelines or a specific reference application in mind, we would want those before beginning D1. On "critical flows" for R3, we have assumed inventory browse, orders management, Reports, and Restocking as the four flows requiring end-to-end coverage — IT should confirm whether any additional flows (user authentication, warehouse switching) are considered critical. Finally, the vendor handoff documentation was thin, and we have assumed the codebase itself is the authoritative source of truth; our audit phase will surface any additional surprises before they affect timeline.
