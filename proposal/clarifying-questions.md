# Clarifying Questions — RFP MC-2026-0417

**Submitted by:** adesso SE  
**Submitted to:** J. Okafor, Director of Procurement — `procurement@meridiancomponents.example`  
**Submission date:** April 25, 2026 (per RFP §6 deadline of April 28)  
**Meridian response date:** May 2, 2026 (shared with all bidders)

---

## Q1 — Budget range

**adesso question:**  
RFP §3 specifies required and desired deliverables but does not state a budget envelope. To scope accurately and avoid pricing significantly outside Meridian's expectations, could you confirm an indicative range — or at minimum whether there is a not-to-exceed figure vendors should stay within?

**Meridian response:**  
Meridian does not publish a budget ceiling at this stage. Vendors should scope and price based on the requirements as stated. Price represents 15% of the evaluation weighting; we are primarily buying capability and approach, not the cheapest submission. We will address pricing directly in shortlist discussions.

---

## Q2 — Definition of "current standards" for D1 UI modernization

**adesso question:**  
RFP §3.2 references "current standards" for the UI modernization desired deliverable, but no design brief, brand guidelines, or reference application were provided. Could you clarify what "current standards" means in practice — for example, whether there is an existing brand identity vendors should align to, or whether clean, accessible, and responsive is the target?

**Meridian response:**  
Meridian does not maintain a formal brand guide for the dashboard. "Current standards" means clean, accessible, and consistently styled using the design tokens already present in the codebase. We are not looking for a visual rebrand or a new design language — we want the application to feel finished and professional. If a vendor has specific questions about a component or pattern, those can be raised at kickoff.

---

## Q3 — Critical flows for R3 automated browser testing

**adesso question:**  
RFP R3 refers to "critical user flows" without listing them explicitly. To ensure our proposed test coverage aligns with what Meridian's IT team considers a gate, could you confirm which flows must be covered as a minimum, and whether any flows (e.g. user authentication, warehouse switching) are considered out of scope for this requirement?

**Meridian response:**  
The following flows are considered critical for R3 purposes: (1) inventory browse with warehouse filter applied, (2) orders view including status filter, (3) Reports module — all filter interactions and data display, (4) Restocking view once delivered — budget input and recommendation output. Authentication and warehouse-switching flows are not currently considered critical. IT's gate requirement is satisfied when these four flows have stable, passing end-to-end test coverage that runs headless.

---

## Q4 — Format and audience for R4 architecture documentation

**adesso question:**  
R4 asks for a "current-state architecture overview suitable for handoff to Meridian IT" with format at vendor's discretion. To produce something genuinely useful rather than just meeting the requirement on paper: who is the primary reader — a developer, a sysadmin, or an IT manager? And is there a preferred format (HTML interactive, PDF, Markdown)?

**Meridian response:**  
The primary reader is our IT operations team — sysadmin level, comfortable with infrastructure concepts but not with application code. They need to understand what components exist, how data flows through the system, and what they would need to know to onboard a future vendor or approve a deployment. HTML is the preferred format as it can be stored in our internal wiki. Depth of code-level detail is less important than clarity of the overall picture.

---

## Q5 — i18n locales for D2 internationalization

**adesso question:**  
D2 requests extension of i18n support to remaining modules. The background materials mention the Tokyo warehouse as the primary motivation. Should vendors scope Japanese as the only additional locale, or is Meridian expecting support for additional languages (e.g. German for any EMEA expansion, or others)?

**Meridian response:**  
Japanese is the only locale required for D2 at this time. The London warehouse operates in English. There are no current plans to add further locales, but vendors should implement the translation file structure in a way that would make adding additional locales straightforward in future — this is not a gate requirement but will be noted positively in evaluation.

---

## Q6 — Stakeholder availability for phase gate sign-offs

**adesso question:**  
Our proposed delivery structure includes phase gate reviews at the end of each phase, with written sign-off required before the next phase begins. To hold to a 10-week schedule, we need sign-off returned within 5 business days of submission. Could you confirm that R. Tanaka and the relevant procurement or IT contact will be available to review and sign off on deliverables within that window — or flag any known constraints (e.g. planned leave, quarterly close periods) that we should factor into the schedule?

**Meridian response:**  
R. Tanaka and J. Okafor (or a named delegate) will be available for phase gate reviews and commit to a 5-business-day sign-off turnaround. Meridian is aware that delays on our side affect the delivery schedule and accepts that any sign-off delays beyond this window may push subsequent phase start dates by an equivalent amount. There are no planned leave or blackout periods during the proposed 10-week delivery window. Vendors should document this assumption in their proposal and include it in any contract terms.

---

*These questions and responses were shared with all registered bidders on May 2, 2026, per RFP §6.*
