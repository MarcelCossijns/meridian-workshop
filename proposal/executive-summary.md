# Executive Summary

**RFP MC-2026-0417 — Meridian Components Inventory Dashboard Modernization**
adesso | Submitted May 8, 2026

---

Meridian Components is operating a business-critical inventory dashboard that is, by any fair assessment, unfinished. The Reports module shipped with defects that remain in production. Filters do not behave correctly. Internationalisation gaps affect staff at your London and Tokyo warehouses. There is no automated test coverage — a gap your IT team has rightly identified as a gating risk before any further development can proceed. Meanwhile, the operations team is working without a Restocking view that was part of the original scope and was never delivered.

This is not a modernisation project. It is a remediation and completion engagement, and it requires a vendor who will be direct about that distinction.

adesso brings strong, current capability in Vue 3 and Python FastAPI — the exact stack your previous vendor left in place. We do not propose to replatform or redesign for its own sake. We propose to complete what was started, resolve what is broken, and add what your operations team actually needs to run the business.

R. Tanaka's situation is concrete and resolvable. The Restocking recommendations view she has been waiting for — purchase order guidance driven by stock levels, demand forecasting, and an operator-defined budget ceiling — is well-scoped and buildable within this engagement. The Reports defects her team works around daily are auditable and fixable. Neither requires architectural risk.

Our proposed scope addresses all four required deliverables directly:

- **R1 — Reports remediation:** Full audit and resolution of filter behaviour, i18n gaps, and API pattern inconsistencies across the module.
- **R2 — Restocking view:** New purpose-built view with stock-level inputs, demand signals, and a configurable budget ceiling for purchase order recommendations.
- **R3 — Automated browser testing:** End-to-end Playwright coverage across inventory, orders, Reports, and the new Restocking view — meeting IT's gate requirement.
- **R4 — Architecture documentation:** Current-state documentation of the full stack, suitable for internal IT handoff and future vendor continuity.

We also propose to scope the three desired deliverables (UI modernisation, full i18n, dark mode) as a defined optional phase, priced separately, so Meridian retains flexibility on scope without creating ambiguity in the core engagement.

The engagement is structured as a 10-week fixed-fee delivery across three phases: stabilisation, feature build, and test and documentation. Fixed-fee pricing reflects our confidence in the scope and protects Meridian from the cost uncertainty that characterised the previous engagement.

We are ready to start.
