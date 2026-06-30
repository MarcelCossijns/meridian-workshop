# Delivery Timeline — MC-2026-0417

## Overview

We propose a 10-week engagement structured across three phases, with a built-in buffer week to absorb integration feedback and ensure a clean sign-off. The sequencing is deliberate: architecture documentation (R4) ships at the end of Week 2 so Meridian IT has something concrete to review while the core delivery work is underway — rather than waiting until the end of the engagement. Browser test coverage (R3) is built in parallel with the Reports remediation (R1), meaning every fix is tested before it ships.

Phase 1 (Weeks 1–2) is entirely non-invasive. We read the codebase, audit the defects, set up our tooling, and deliver the architecture overview. No production changes until Phase 2.

Phase 2 is the engine of the engagement. Reports remediation and automated testing run in lockstep — we do not consider a defect closed until a test covers the corrected behavior. By the end of Week 5, Meridian IT receives a working, releasable test suite covering all R1 fixes and core inventory views. This is the IT sign-off milestone: IT can approve production deployment of the Reports remediation at that point, without waiting for the Restocking feature to complete. The Restocking view follows immediately in Weeks 5–6, informed by the codebase familiarity we have built up by then. Once R2 ships, the test suite is extended in Phase 3 to cover Restocking flows, giving Meridian a single comprehensive suite across all critical paths.

Phase 3 is polish, regression, and handoff preparation. Desired deliverables (D1 UI modernization, D2 full i18n, D3 dark mode) are scoped here — their inclusion depends on budget confirmation and Phase 2 pace. A dedicated stakeholder review session with R. Tanaka's operations team is scheduled before final delivery, giving Meridian the opportunity to validate the Restocking feature against real workflows before sign-off.

If Meridian elects not to proceed with D1–D3, Phase 3 becomes a dedicated stabilisation and handoff phase: extended regression testing, final documentation review, knowledge transfer session with Meridian IT, and stakeholder acceptance sign-off. The 10-week timeline and fixed fee remain unchanged.

Week 10 is a managed buffer. If Phase 3 completes cleanly, it becomes the formal handoff and documentation wrap-up. If any items need a final pass, we have the runway to address them without schedule pressure.

---

## Phased Schedule

| Phase | Weeks | Activities | Primary Deliverables |
|---|---|---|---|
| 1 — Onboarding & Audit | 1–2 | Codebase review, defect audit (Reports), environment setup, test scaffolding | R4 Architecture documentation (end of Week 2) |
| 2 — Core Delivery | 3–4 | Reports module remediation | R1 Reports fixes (end of Week 4) |
| 2 — Core Delivery | 3–5 | Browser test suite built alongside R1, covering Reports fixes and core inventory views | R3 (foundation) — releasable test suite; IT sign-off on R1 deployment (end of Week 5) |
| 2 — Core Delivery | 5–6 | Restocking recommendations view | R2 Restocking feature (end of Week 6) |
| 3 — Polish & Handoff | 7–9 | R3 extended to cover R2 (Restocking) flows; D1/D2/D3 (if in scope); full regression pass; stakeholder review with Tanaka's team | R3 (final) — complete test suite covering all critical flows; D1 UI modernization, D2 i18n, D3 dark mode (conditional) |
| Buffer & Sign-off | 10 | Final fixes, documentation wrap-up, formal handoff | Signed delivery confirmation |

---

> **Note on R4 (Architecture Documentation):** Delivering the architecture overview at the close of Week 2 is intentional. Meridian IT has indicated that test coverage is a gating requirement for any changes. Providing a clear current-state architecture map early gives IT the context to begin their own review and alignment work in parallel — rather than receiving it as an afterthought at the end of the engagement.

---

## Assumptions & Dependencies

The schedule above assumes Meridian fulfills the following obligations. Delays in any of these items may push phase start dates by an equivalent amount.

- **Repository and environment access** — granted to the engagement team by end of Week 1. This includes source repository permissions, access to any staging or development environment, and relevant credentials.
- **Stakeholder availability for phase gate reviews** — R. Tanaka and J. Okafor (or a designated delegate) are available at the close of each phase to review deliverables and provide written sign-off.
- **Phase gate sign-off turnaround** — returned within 5 business days of deliverable submission. Sign-off is required before the next phase begins; delays beyond this window will trigger a formal change order discussion with Meridian's project sponsor to adjust the affected phase start date and fee basis accordingly.
- **IT team contact for architecture review handoff** — a named IT contact is available during Week 2 to receive and review the R4 architecture documentation, ask clarifying questions, and confirm alignment before Phase 2 begins.
