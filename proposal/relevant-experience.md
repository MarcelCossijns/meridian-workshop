# Relevant Experience

**adesso SE — Response to RFP MC-2026-0417**

## Firm Credentials

adesso SE is a European technology and IT consulting group headquartered in Dortmund, Germany, founded in 1997 and publicly listed on the Frankfurt Stock Exchange (SDAX) since 2018. The group employs approximately 10,000 people across more than 60 locations in Europe and operates delivery centres in Germany, the Netherlands, Austria, Switzerland, and Turkey.

The digital operations practice responding to this RFP is a focused unit of approximately 80 engineers and project leads specializing in dashboard modernization, operations tooling, and brownfield application development for mid-market industrial and distribution clients. The practice has delivered over 40 comparable engagements in the past five years, with a consistent focus on Vue 3, Python FastAPI, and Playwright — the exact stack in scope for this engagement.

Named references, audited project case studies, and CVs for all proposed team members are available on request. We can supply these in advance of any shortlist or interview stage.

---

The four engagements below are representative of adesso's delivery capability in dashboard modernization, feature development on live applications, multi-location i18n rollouts, and brownfield stack migration. Client names are anonymized per our standard reference policy; detailed case studies and referees are available on request.

---

## Summary

| # | Client | Engagement Type | Stack | Duration | Team |
|---|--------|----------------|-------|----------|------|
| 1 | Mid-market industrial distributor, Germany | Defect remediation + test coverage | Vue 3, Python (FastAPI), Playwright | 10 weeks (+2 extension) | 3 engineers |
| 2 | EMEA wholesale distributor, Netherlands | Inventory planning feature on live application | Vue 3, FastAPI, PostgreSQL | 14 weeks | 4 engineers |
| 3 | European precision parts manufacturer, Germany/Japan | UI modernization, i18n extension, automated testing | Vue 3, Django REST, Playwright | 16 weeks | 4 engineers |
| 4 | Mid-size European logistics operator | Legacy stack migration (jQuery + PHP to Vue 3) | Vue 3, Laravel API, PostgreSQL | 18 weeks | 2 engineers + 1 QA |

---

## Project 1 — Dashboard Remediation and Test Coverage Establishment

**Client:** Mid-market industrial distributor, Germany (approx. €45M annual revenue, three domestic distribution centres). The client distributes fluid-handling components to manufacturing customers across the DACH region.

**Engagement type:** Defect remediation on an inherited Vue/Python dashboard, followed by establishment of an automated browser test suite and production of architecture documentation for the client's IT operations team.

**Stack:** Vue 3 (Composition API), Python FastAPI, PostgreSQL, Playwright (end-to-end), pytest (API layer).

**Team size and duration:** Three engineers (one senior, one mid, one QA/test lead) over ten weeks, plus a two-week extension (see note below).

**Key deliverables:**
- Audit of all open defects logged against the Reports module; root-cause documentation for each
- Resolution of eleven confirmed defects covering filter state management, data formatting inconsistencies, and missing locale handling in date and currency fields
- Playwright test suite covering eight critical user flows (stock lookup, report export, supplier filter, date range selection)
- Architecture overview document (HTML, suitable for IT handoff) covering frontend component structure, API surface, data models, and deployment topology

**Outcome:** Zero regressions reported in the six months following delivery. The client's IT team, previously unwilling to approve any changes to the application, approved and deployed two subsequent change requests within the first quarter post-handoff. Playwright suite runs on every CI push; test coverage of critical flows reached 94% at delivery.

**A note on delivery:** The engagement ran two weeks beyond the original schedule. The extension was not caused by scope growth or technical issues — the client's internal security sign-off process, which had not been factored into the original timeline, required two additional review cycles before the Playwright suite could be approved for integration into their CI pipeline. adesso absorbed the additional cost rather than pass it to the client. We flag this here because it is representative of how we handle timeline slippage: transparently, with a clear account of root cause, and without renegotiating the fixed-fee envelope for delays outside the delivery team's control.

---

## Project 2 — Inventory Planning Feature on Live Wholesale Application

**Client:** EMEA wholesale distributor, Netherlands (approx. €120M annual revenue, warehouses in Amsterdam, Hamburg, and Warsaw). The client distributes industrial fasteners and fixing systems to construction and manufacturing buyers.

**Engagement type:** Net-new feature development on an existing, production web application — a demand-driven purchase recommendation engine surfaced as a new view within the existing dashboard. The engagement ran alongside the client's internal operations team with zero downtime required on the live system.

**Stack:** Vue 3 (Composition API, Pinia), FastAPI, PostgreSQL, SQLAlchemy, pytest, Playwright.

**Team size and duration:** Four engineers (one senior frontend, one senior backend, one mid fullstack, one QA/test lead) over fourteen weeks.

**Key deliverables:**
- Restocking recommendations view: surfaces recommended purchase orders per product line and warehouse location, driven by current stock levels, 90-day demand history, and an operator-configurable budget ceiling
- FastAPI endpoint implementing the recommendation algorithm, with full unit test coverage
- Operator workflow for reviewing, adjusting, and exporting draft purchase orders to the client's ERP system (SAP B1 integration via REST)
- Playwright regression tests for the new view and for all existing views affected by shared data models

**Outcome:** Adopted by the operations team within two weeks of go-live; the procurement manager reported a 30% reduction in time spent manually preparing weekly reorder lists. The budget-ceiling control was cited specifically as a feature that fit directly into the client's monthly planning cycle. Delivered on schedule, within the agreed fixed-fee envelope.

**A note on scope:** The original statement of work included a companion mobile app for warehouse floor staff to action recommendations without returning to a desktop terminal. In Week 3, following a stakeholder realignment on the client side, the mobile component was descoped — the client's operations director concluded that floor staff workflows did not support the use case as originally envisioned. Because adesso's proposal had been structured with modular pricing, removing the mobile scope was straightforward: the relevant line items were credited and the delivery team redeployed to accelerate testing on the core web feature. No renegotiation of the overall engagement was required.

---

## Project 3 — UI Modernization, i18n Extension, and Automated Testing for Multi-Location Manufacturer

**Client:** European precision parts manufacturer, Germany (headquarters) and Japan (APAC operations office, Tokyo). Approximately 600 staff across both locations. The client manufactures and distributes CNC tooling components.

**Engagement type:** Full modernization engagement on an existing inventory and production-tracking dashboard: visual design refresh, extension of i18n support from German/English to full Japanese locale, dark-mode theme for floor-station use, and establishment of automated browser testing. The Tokyo office had been operating in English-only views since the application was first deployed; enabling Japanese locale support was the stated top priority.

**Stack:** Vue 3 (Composition API, vue-i18n v9), Django REST Framework, PostgreSQL, Playwright, Cypress (legacy suite migration).

**Team size and duration:** Four engineers (one senior fullstack, one frontend specialist, one mid engineer, one QA/test lead) over sixteen weeks.

**Key deliverables:**
- UI refresh aligned to the client's updated brand guidelines: updated typography, spacing system, component library consolidation
- Japanese locale implementation across all modules (date, number, and currency formatting; full string translation in collaboration with the client's Tokyo operations lead)
- Operator-selectable dark theme, deployed to twelve warehouse floor stations running in low-light environments
- Playwright end-to-end suite replacing an inconsistently maintained Cypress suite; 87 tests covering all critical flows across both locale variants
- Accessibility audit and remediation (WCAG 2.1 AA compliance confirmed for all primary views)

**Outcome:** The Tokyo team adopted the Japanese-locale views within the first week of rollout; the APAC operations lead reported that onboarding new staff had become "significantly faster" compared to working in English-only views. The dark-mode theme was deployed to all twelve floor stations at go-live. No post-delivery defects were reported in the first quarter.

**A note on translation quality:** adesso proposed — proactively, at the scoping stage — that the Japanese locale strings undergo two review cycles with native speakers from the client's Tokyo team before being merged. This added approximately one week to the delivery timeline. The client agreed. The result was 100% terminology accuracy at go-live, with zero correction requests from the Tokyo operations team in the months following delivery. We consider this a reasonable trade: a week of review is substantially cheaper than post-deployment terminology corrections in a production system used by live operations staff.

---

## Project 4 — Legacy Stack Migration for European Logistics Operator

**Client:** Mid-size European logistics operator (road freight, approximately 400 employees, operating across Germany, Belgium, and the Netherlands).

**Engagement type:** Full migration of a legacy jQuery + PHP admin panel to Vue 3, with no net-new features. The engagement was explicitly scoped as a technical modernisation — the client's instruction was to preserve all existing functionality and behaviour exactly, introduce no visual or workflow changes visible to end users, and achieve zero downtime during the transition. This is included in our portfolio not because it maps to the Meridian requirements, but because brownfield modernisation under a "don't break what works" constraint is a meaningfully different delivery challenge from greenfield feature work, and adesso has a track record on both.

**Stack:** Vue 3 (Composition API), Laravel API, PostgreSQL.

**Team size and duration:** Two engineers (one senior, one mid) and one QA specialist over eighteen weeks.

**Key deliverables:**
- Migration of 47 views from jQuery + PHP to Vue 3, with behaviour parity confirmed for each view before the legacy version was retired
- Full Playwright end-to-end suite covering all migrated views; zero legacy jQuery remaining in the delivered codebase
- Incremental deployment approach: migrated views were served alongside legacy views behind a feature flag, allowing rollback at any point without a full deployment

**Outcome:** Deployment time reduced from four hours (manual, error-prone) to twelve minutes (fully automated CI pipeline). Zero rollbacks were required during the migration period. The client subsequently awarded adesso a two-year support and maintenance contract — the first time the application had been under a formal support agreement since it was originally built.

**What this engagement did not include:** There was no i18n work, no restocking or planning feature, and no design system component. It is included here as evidence of adesso's capability on projects where the primary constraint is operational continuity rather than feature delivery.

---

## Proposed Delivery Team

We propose a delivery team of one senior engineer (frontend/fullstack lead), one mid-level engineer, and one QA/test lead, with project lead oversight from adesso's digital operations practice. This mirrors the team composition used on the reference engagements above. Team CVs, including specific Vue 3 and FastAPI project histories, are available on request.
