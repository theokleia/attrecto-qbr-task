# QBR Portfolio Health Report
**Period:** Q2 2025  
**Generated:** 2026-03-13 08:38  
**Projects Reviewed:** 2 | **Open Flags:** 8 | **Needs Review:** 7

---

## Executive Summary

The portfolio carries six open flags across two active projects — Project Phoenix and DivatKirály — with DivatKirály accounting for the majority of risk, including an unresolved GDPR violation, an uncontrolled scope change, and three stalled decisions ranging from 194 to 206 days without follow-up. Project Phoenix carries two medium-severity stalled decisions: an unsigned specification review (211 days dormant) and a confirmed image-upload bug that has gone unresolved for over nine months despite being diagnosed and acknowledged. The single most critical concern is the live GDPR violation on DivatKirály's registration form, where the newsletter checkbox remains pre-checked by default and Zs ófia Varga has not confirmed the fix is deployed to production — this requires same-day escalation and written client notification before any other portfolio work is prioritised.

---

## 🔴 Immediate Attention Required

### DivatKirály

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> A security-relevant decision to send confirmation emails after password changes was informally agreed upon in July 2025 but never formally resolved, assigned, or tracked — it has been open for 194 days with no follow-up.
**Evidence:** _Gábor Nagy (PM) wrote on 2025-07-03: 'Let's add the email after password modification to the to-do list.' — this is a soft acknowledgment and task-list addition, not a formal decision, acceptance crit_
**Days open:** 194 business days
**Owner:** gabor.nagy@kisjozsitech.hu
**Action:** Direct Gábor Nagy to confirm whether the confirmation email after password change was actually implemented and tested; if not, ensure it is formally added to the specification and assigned to a developer with a target sprint, given its security relevance.

**Stalled Decision** — `MEDIUM` [Rule+LLM-confirmed]
> A client-requested CSV export feature for the DivatKirály project has had no response from Gábor or any other stakeholder for 199 days after Eszter Varga asked 'Gábor, what do you think, does it fit into the current schedule?' on 2025-06-25.
**Evidence:** _The thread ends with eszter.varga@kisjozsitech.hu asking 'Gábor, what do you think, does it fit into the current schedule?' (email11_msg1, 2025-06-25T14:05:00). There is no subsequent reply from Gábor_
**Days open:** 199 business days
**Owner:** eszter.varga@kisjozsitech.hu
**Action:** Identify who 'Gábor' is (likely a Tech Lead or Engineering Manager on DivatKirály) and require him to provide a scheduling decision within 2 business days; if the feature is feasible, ensure it is added to the backlog with a target sprint; escalate to the PM if no response is received, given the client (Béla, nagyker.hu) is waiting on this capability.

**Uncontrolled Scope Change** — `MEDIUM` [Rule+LLM-confirmed]
> A new SKU-based search requirement surfaced informally via a delayed client mention, confirmed as out-of-scope by the BA, and accepted into the backlog without documented client sign-off or formal change control.
**Evidence:** _Eszter (email18_msg1): 'in last week's meeting, the client mentioned it would be good if the search worked not only for product names but also for item numbers (SKU). I forgot to mention this until no_
**Owner:** peter.kovacs@kisjozsitech.hu
**Action:** Direct Péter Kovács to halt implementation of the SKU search extension until a formal change request is raised, the client provides written approval, and the effort (~0.5 backend day + testing per Gábor) is reflected in an updated project timeline and budget. Verify whether the JIRA ticket Anna was asked to create has been logged and whether it is linked to a change control record. Confirm with Eszter that the client has been explicitly told this is extra-scope work and that their acceptance is documented.

**Stalled Decision** — `LOW` [LLM-confirmed]
> A 'nice to have' feature request for a 'NEW' badge on product pages was raised on 2025-06-16 with an explicit sizing/prioritization question, and has received zero responses in 206 days.
**Evidence:** _Anna Nagy asked 'How big of a task would this be? Could we fit it into the current sprint if it's not a huge effort?' on 2025-06-16 — the thread contains only this single message with no replies, no e_
**Days open:** 206 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Direct the engineering lead or scrum master to provide a quick effort estimate for the 'NEW' badge feature and formally close the loop with Anna Nagy — either schedule it in a future sprint, add it to the backlog with a priority label, or explicitly decline it as out of scope for DivatKirály, so the decision is no longer hanging open.

**Stalled Decision** — `LOW` [LLM-confirmed]
> A 'nice to have' feature request for a 'NEW' badge on product pages was raised by Anna Nagy on 2025-06-16 with no response or decision recorded in the thread, leaving it open for 206 days.
**Evidence:** _The sole message in the thread is Anna Nagy's 2025-06-16 request: 'How big of a task would this be? Could we fit it into the current sprint if it's not a huge effort?' — no reply, estimation, acceptan_
**Days open:** 206 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Direct the team lead or product owner to formally triage this backlog item: either estimate and schedule it, explicitly defer it to a future sprint, or close it as 'won't do' — then reply to the thread so the decision is documented and Anna Nagy is informed.

---

## 🟡 Monitor Closely

### Project Phoenix

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> Zsuzsa's June 9 message resolved the SSO scope question but left the remaining specification points (including the unresolved minimum password length from point 3.2) without explicit team sign-off, and no further response has been recorded in 211 days.
**Evidence:** _Zsuzsa wrote on 2025-06-09: 'We can remove it from the scope for now. Are the other points okay?' — this is an open question with no reply in the thread. Additionally, Gábor raised an unresolved issue_
**Days open:** 211 business days
**Owner:** varga.zsuzsa@kisjozsitech.hu
**Action:** Direct Zsuzsa Varga or the team lead (Péter Kovács, kovacs.peter@kisjozsitech.hu) to formally confirm: (1) whether the remaining specification points are accepted by the team, and (2) whether the minimum password length for point 3.2 is confirmed as 8 characters consistent with other modules — then document the decisions and close the specification review loop before any login page implementation proceeds.

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> A confirmed bug in the image upload logic — where filenames containing spaces cause a 404 — was identified by a Senior Developer on 2025-06-29 and acknowledged by the responsible Junior Developer on 2025-06-30, but no fix, resolution signal, or follow-up has been recorded in the thread since, leaving the issue open for over 9 months as of today.
**Evidence:** _nagy.istvan diagnosed the root cause on 2025-06-29: 'it only happens if the image name contains spaces. The system renames it, but the frontend somehow requests the old, space-containing name from the_
**Days open:** 211 business days
**Owner:** horvath.gabor@kisjozsitech.hu
**Action:** The Director should directly follow up with horvath.gabor@kisjozsitech.hu to confirm whether a fix was implemented after 2025-06-30 and, if not, assign a tracked ticket with a deadline. nagy.istvan@kisjozsitech.hu should be asked to verify the fix given his diagnosis of the root cause. If no fix exists, this should be prioritised as a staging-environment bug that blocks reliable QA of the profile picture upload feature.

---

## Incidents This Quarter

**[DivatKirály]** **Fwd: Re: DivatKirály - User registration process** — 🔴 Open
> A live GDPR compliance violation exists on the DivatKirály registration form where the newsletter subscription checkbox is pre-checked by default, and as of the last message the fix has not been confirmed as implemented — additionally, a developer nearly introduced a second error by also unchecking the mandatory Terms & Conditions checkbox.
_Eszter Horvath (2025-06-26T15:03): 'the newsletter subscription checkbox cannot be checked by default. It currently is. Please fix it.' Client email confirms: 'The newsletter subscription is automatic_
**Action:** Immediately confirm with Zsófia Varga whether the newsletter checkbox fix has been deployed to production; if not, escalate for same-day resolution given the active GDPR violation. Verify that the Terms & Conditions checkbox was NOT modified. Once fixed, request written confirmation from Eszter Horvath that the client has been notified and the issue is closed. Consider a brief compliance review of other registration form defaults.

---

## Cross-Project Patterns

**[Project Phoenix] SYSTEMIC_PROCESS_FAILURE** — `HIGH`
> At least two distinct technical issues across Project Phoenix (unresolved password length specification in email1 and an unpatched image upload bug in email4) have been acknowledged but left without formal resolution or follow-up for over 9 months each, indicating a systemic failure to close out identified issues once initial acknowledgement occurs.
**Threads:** email1, email4
**Action:** The Director should mandate a formal issue-closure protocol requiring every flagged item to have an assigned owner, a documented resolution, and a deadline; immediately schedule a review meeting to force closure on both the password length specification (email1, owner: varga.zsuzsa@kisjozsitech.hu) and the filename-space 404 bug (email4, owner: horvath.gabor@kisjozsitech.hu).

**[DivatKirály] RECURRING_BLOCKER** — `HIGH`
> Gábor Nagy is a consistent non-responder across multiple threads: he failed to respond to a scheduling question about CSV export (email11, 199 days) and owns a stalled security decision about password-change confirmation emails (email10, 194 days), indicating he is a systemic bottleneck for decisions and client requests.
**Threads:** email10, email11
**Action:** The Director should immediately audit all open items assigned to or pending response from Gábor Nagy, establish a mandatory response SLA, and consider reassigning ownership of the CSV export decision and password-change confirmation to an available stakeholder to unblock both threads.

**[DivatKirály] SYSTEMIC_PROCESS_FAILURE** — `HIGH`
> Multiple client-facing feature requests and compliance-relevant decisions (email10, email11, email16) have been left without formal response, assignment, or tracking for 194–206 days, indicating a systemic absence of a backlog triage or decision-tracking process on the DivatKirály project.
**Threads:** email10, email11, email16
**Action:** The Director should mandate a formal backlog review meeting within one week to triage all open items from these threads, assign explicit owners and deadlines, and implement a lightweight decision-tracking mechanism (e.g., a shared log or ticket system) to prevent further items from going unresolved.

**[DivatKirály] IMPLICIT_COMMITMENT** — `MEDIUM`
> An uncontrolled scope addition (SKU-based search, email18) was accepted into the backlog without formal change control, while a separate client-requested CSV export feature (email11) has gone unacknowledged for 199 days — together these suggest client requests are being handled ad hoc with no consistent scope management process, creating implicit delivery commitments that are neither tracked nor formally agreed.
**Threads:** email18, email11
**Action:** The Director should require all client-originated requests to go through a formal change request process with documented client sign-off before backlog entry, and retroactively clarify with the client the status of both the CSV export and SKU search items to avoid misaligned delivery expectations.

---

## 🔵 Needs PM Review

_The items below were detected by the rule engine but could not be confirmed with high confidence. Please review with the relevant PM before the QBR._

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 45%]
> The minimum password length requirement (raised in point 3.2 on 2025-06-02) was never explicitly answered in the thread, leaving a potential specification gap open for 216 days.
**Evidence:** _horvath.gabor@kisjozsitech.hu wrote: 'I don't see any mention of the minimum password length. Should it be 8 characters, like in other modules?' — no _

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 55%]
> JIRA-112 (profile picture bug) was acknowledged as being investigated by Gábor as of 2025-06-30, but no resolution is evidenced in this thread, and with 196 days elapsed the ticket status is unknown from available data.
**Evidence:** _Péter confirms 'Yes, Gábor is looking into it' (email3_msg1, 2025-06-30T10:05) — this is acknowledgment only, not resolution. No subsequent message in_

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 45%]
> A confirmed bug in the profile picture upload logic (filenames with spaces causing 404s) was attributed to Gábor's commit on 2025-06-29, and Gábor acknowledged it on 2025-06-30, but no resolution or follow-up has been recorded in the thread since then — leaving the fix status unknown after 197 days.
**Evidence:** _nagy.istvan: 'This isn't a cache issue; it's a bug in the image upload logic. Gábor, didn't your last commit touch this part?' — horvath.gabor: 'Yes, _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 62%]
> A client CSV export request forwarded on 2025-06-25 has received no decision or follow-up after the BA asked Gábor for a scheduling assessment, leaving the feature request unresolved for 199 days.
**Evidence:** _Eszter Varga (BA) asked on 2025-06-25T14:05: 'Gábor, what do you think, does it fit into the current schedule?' — no response from Gábor or any other _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 62%]
> A client CSV export request forwarded on 2025-06-25 received only a feasibility acknowledgment from the BA and a question directed at Gábor, with no decision, assignment, or resolution recorded in 199 days.
**Evidence:** _Eszter Varga (BA) wrote on 2025-06-25T14:05: 'It's technically feasible, but we need to assess the development effort. Gábor, what do you think, does _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 35%]
> Anna's unanswered question about whether the 'Add to Cart' button change requires a color swap or just a size/bold adjustment has no documented resolution in the thread, though the broader design feedback session appears largely concluded.
**Evidence:** _Anna asks in email14_msg1: 'Does the client want a different color instead of the current green, or just for it to be larger/bold? This isn't clear.' _

**[DivatKirály]** Uncontrolled Scope Change — [Unvalidated, confidence: 55%]
> A BA introduced an unvetted 'NEW' badge feature mid-sprint with no engineering response or formal scope decision recorded in the thread.
**Evidence:** _anna.nagy@kisjozsitech.hu wrote: 'A "nice to have" requirement came up: products uploaded in the last 30 days should have a small "NEW" badge on their_

---

## Recommended Director Actions

1. **[DivatKirály — Fwd: Re: DivatKirály - User registration process]** Immediately confirm with Zsófia Varga whether the newsletter checkbox fix has been deployed to production; if not, escalate for same-day resolution given the active GDPR violation. Verify that the Terms & Conditions checkbox was NOT modified. Once fixed, request written confirmation from Eszter Horvath that the client has been notified and the issue is closed. Consider a brief compliance review of other registration form defaults.
2. **[Project Phoenix — Project Phoenix - New Login Page Specification]** Direct Zsuzsa Varga or the team lead (Péter Kovács, kovacs.peter@kisjozsitech.hu) to formally confirm: (1) whether the remaining specification points are accepted by the team, and (2) whether the minimum password length for point 3.2 is confirmed as 8 characters consistent with other modules — then document the decisions and close the specification review loop before any login page implementation proceeds.
3. **[Project Phoenix — Project Phoenix - Staging Environment Anomaly]** The Director should directly follow up with horvath.gabor@kisjozsitech.hu to confirm whether a fix was implemented after 2025-06-30 and, if not, assign a tracked ticket with a deadline. nagy.istvan@kisjozsitech.hu should be asked to verify the fix given his diagnosis of the root cause. If no fix exists, this should be prioritised as a staging-environment bug that blocks reliable QA of the profile picture upload feature.
4. **[DivatKirály — User Profile Page - Data Modification Flow]** Direct Gábor Nagy to confirm whether the confirmation email after password change was actually implemented and tested; if not, ensure it is formally added to the specification and assigned to a developer with a target sprint, given its security relevance.
5. **[DivatKirály — Fwd: Request regarding report export]** Identify who 'Gábor' is (likely a Tech Lead or Engineering Manager on DivatKirály) and require him to provide a scheduling decision within 2 business days; if the feature is feasible, ensure it is added to the backlog with a target sprint; escalate to the PM if no response is received, given the client (Béla, nagyker.hu) is waiting on this capability.
6. **[DivatKirály — DivatKirály - Weekly status and development progre]** Direct Péter Kovács to halt implementation of the SKU search extension until a formal change request is raised, the client provides written approval, and the effort (~0.5 backend day + testing per Gábor) is reflected in an updated project timeline and budget. Verify whether the JIRA ticket Anna was asked to create has been logged and whether it is linked to a change control record. Confirm with Eszter that the client has been explicitly told this is extra-scope work and that their acceptance is documented.
7. **[DivatKirály — Small request: "New" label on the product page]** Direct the engineering lead or scrum master to provide a quick effort estimate for the 'NEW' badge feature and formally close the loop with Anna Nagy — either schedule it in a future sprint, add it to the backlog with a priority label, or explicitly decline it as out of scope for DivatKirály, so the decision is no longer hanging open.

---

⚠️ **AI-GENERATED REPORT** — Validate flagged items with responsible PMs before acting.
Generated by QBR Portfolio Health Analyzer | Model: claude-sonnet-4-6
Run date: 2026-03-13 08:38