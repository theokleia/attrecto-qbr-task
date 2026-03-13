# QBR Portfolio Health Report
**Period:** Q2 2025  
**Generated:** 2026-03-13 08:41  
**Projects Reviewed:** 2 | **Open Flags:** 8 | **Needs Review:** 7

---

## Executive Summary

DivatKirály carries the portfolio's most urgent risk: a live GDPR violation on the registration form (pre-checked newsletter opt-in) reported 2025-06-26 with no confirmed production fix as of 2025-06-27, compounded by an uncontrolled scope change (SKU search) already moving toward implementation without formal sign-off. Project Phoenix is stable by comparison but has two stalled decisions exceeding 200 days — an unresolved password spec (Zsuzsa/Gábor) and an unconfirmed bug fix for filename-space 404s (Gábor Horváth) — both requiring immediate owner follow-up. The single most critical action is confirming today whether the DivatKirály GDPR checkbox fix is live in production; if not, this is a same-day escalation.

---

## 🔴 Immediate Attention Required

### DivatKirály

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> A security-relevant decision to send confirmation emails after password changes was informally agreed upon but never formally resolved, documented, or assigned to a developer, and has been open for 194 days.
**Evidence:** _Gábor Nagy (PM) wrote 'Let's add the email after password modification to the to-do list' on 2025-07-03, but no follow-up message confirms it was added to a backlog, assigned, or implemented. The thre_
**Days open:** 194 business days
**Owner:** gabor.nagy@kisjozsitech.hu
**Action:** Ask Gábor Nagy to confirm whether the password-change confirmation email was actually added to the backlog and if so, what its current implementation status is; if not yet implemented, escalate as a security gap and assign it to a developer with a concrete delivery date given the 194-day delay.

**Stalled Decision** — `MEDIUM` [Rule+LLM-confirmed]
> A client-requested CSV export feature for the DivatKirály project has had no scheduling decision for 199 days after Eszter Varga directed a capacity question to Gábor, who has never responded in the thread.
**Evidence:** _eszter.varga@kisjozsitech.hu wrote on 2025-06-25T14:05:00: 'Gábor, what do you think, does it fit into the current schedule?' — no reply from Gábor or any other party appears in the thread, and no res_
**Days open:** 199 business days
**Owner:** eszter.varga@kisjozsitech.hu
**Action:** Identify Gábor (likely the Engineering Lead or Sprint Owner for DivatKirály) and require him to provide a scheduling decision within 2 business days; if the feature is deprioritized, formally communicate that to Zoltán Kiss and the client to close the loop on the outstanding request.

**Uncontrolled Scope Change** — `MEDIUM` [Rule+LLM-confirmed]
> A new SKU-based search requirement surfaced informally via the Client Relationship Manager a week after the client meeting, was not in the original specification, and has been accepted into scope without a formal change control decision on timeline or cost impact.
**Evidence:** _Eszter Horvath (2025-06-28T11:30): 'in last week's meeting, the client mentioned it would be good if the search worked not only for product names but also for item numbers (SKU). I forgot to mention t_
**Owner:** peter.kovacs@kisjozsitech.hu
**Action:** Direct the PM (Péter Kovacs) to obtain written client sign-off on the SKU search requirement as a formal scope change before Gábor begins implementation next week; ensure the JIRA ticket references an approved change request, and confirm whether this extra development affects the project budget or delivery timeline.

**Stalled Decision** — `LOW` [LLM-confirmed]
> A 'nice to have' feature request for a 'NEW' badge on product pages was raised on 2025-06-16 with an explicit sizing/prioritization question and has received zero responses in 206 days.
**Evidence:** _'How big of a task would this be? Could we fit it into the current sprint if it's not a huge effort?' — asked by anna.nagy@kisjozsitech.hu on 2025-06-16; no reply, estimate, or decision is present any_
**Days open:** 206 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Direct the engineering lead to provide a quick effort estimate (story points or hours) for the 'NEW' badge feature so the BA and product owner can make an explicit backlog prioritization decision — either schedule it, defer it to a future sprint, or formally close it as out of scope for DivatKirály.

**Stalled Decision** — `LOW` [LLM-confirmed]
> A 'nice to have' feature request for a 'NEW' badge on product pages was raised by Anna Nagy on 2025-06-16 and has received zero responses in 206 days, leaving sprint inclusion and effort estimation completely unresolved.
**Evidence:** _The sole message in the thread is Anna Nagy's 2025-06-16 request: 'How big of a task would this be? Could we fit it into the current sprint if it's not a huge effort?' — no reply, no effort estimate, _
**Days open:** 206 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Direct the engineering lead or scrum master for DivatKirály to formally triage this ticket: either provide a quick effort estimate and schedule it in an upcoming sprint, or explicitly backlog/reject it so the BA can close the loop — the 206-day silence suggests it has been forgotten entirely.

---

## 🟡 Monitor Closely

### Project Phoenix

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> Zsuzsa's June 9 message resolved the SSO scope question but left two other open issues unaddressed — minimum password length (Gábor, email1_msg1) and implicit spec sign-off — with no follow-up response in 211 days.
**Evidence:** _Zsuzsa's final message (email1_msg4, 2025-06-09) states 'We can remove it from the scope for now. Are the other points okay?' — the trailing question received no reply in the thread. Gábor's unresolve_
**Days open:** 211 business days
**Owner:** varga.zsuzsa@kisjozsitech.hu
**Action:** Direct Zsuzsa (varga.zsuzsa@kisjozsitech.hu) to immediately confirm: (1) the minimum password length requirement from Gábor's open question, and (2) explicit team sign-off on the remaining spec points. Escalate to Péter (kovacs.peter@kisjozsitech.hu) as the senior stakeholder who issued the coordination request, and ensure a formal spec approval is recorded before any further login page development proceeds.

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> A confirmed bug in the image upload logic (filenames with spaces causing 404s) was identified by a Senior Developer on 2025-06-29, attributed to a Junior Developer's commit, but the thread ends with only an acknowledgment ('I'll check it immediately') and no confirmed fix as of the last message on 2025-06-30 — leaving the issue unresolved with 211 days elapsed since original report.
**Evidence:** _nagy.istvan: 'it only happens if the image name contains spaces. The system renames it, but the frontend somehow requests the old, space-containing name from the API, which returns a 404. This isn't a_
**Days open:** 211 business days
**Owner:** horvath.gabor@kisjozsitech.hu
**Action:** Direct the Engineering Director to immediately follow up with horvath.gabor@kisjozsitech.hu for a status update on the filename-space bug fix; if no fix has been committed, assign a senior developer to review and resolve the image upload logic within the current sprint, and verify the fix is deployed and tested on staging before closing the issue.

---

## Incidents This Quarter

**[DivatKirály]** **Fwd: Re: DivatKirály - User registration process** — 🔴 Open
> A live GDPR compliance violation exists on the DivatKirály registration form where the newsletter subscription checkbox is pre-checked by default, reported urgently by the client on 2025-06-26, and as of the last message (2025-06-27) the fix has not been confirmed as completed — with an additional risk that the developer nearly incorrectly unchecked the Terms & Conditions checkbox as well.
_Eszter Horvath (2025-06-26T15:03): 'The client indicated that due to GDPR, the newsletter subscription checkbox cannot be checked by default. It currently is. Please fix it.' Zsófia Varga (2025-06-27T_
**Action:** Immediately verify with Zsófia Varga whether the newsletter checkbox fix has been deployed to production and confirm the Terms & Conditions checkbox was left unchanged; if not yet deployed, escalate as a blocking GDPR compliance issue requiring same-day resolution and notify the client (via Eszter Horvath) once confirmed fixed.

---

## Cross-Project Patterns

**[Project Phoenix] SYSTEMIC_PROCESS_FAILURE** — `HIGH`
> At least two separate technical issues across Project Phoenix — an unresolved spec question (email1) and an unconfirmed bug fix (email4) — have both been left without formal closure or follow-up for over 211 days, indicating a systemic failure to track and close open action items to resolution.
**Threads:** email1, email4
**Action:** The Director should mandate a formal issue-tracking process for Project Phoenix requiring every open action item to have a named owner, a due date, and a documented resolution; immediately audit email1 (password length spec sign-off) and email4 (image upload bug fix confirmation) to obtain and record their current status.

**[DivatKirály] RECURRING_BLOCKER** — `HIGH`
> Gábor Nagy is a non-responder bottleneck across multiple threads: he is the unresponsive owner of a stalled security decision in email10 and the silent capacity decision-maker whose non-response has blocked the CSV export feature for 199 days in email11.
**Threads:** email10, email11
**Action:** The Director should directly intervene with Gábor Nagy to obtain decisions on both the password-change confirmation email (email10) and the CSV export scheduling (email11), and assess whether his workload or role clarity is causing a systemic response failure.

**[DivatKirály] SYSTEMIC_PROCESS_FAILURE** — `HIGH`
> Multiple client-facing feature requests and compliance issues across threads (email11, email16, email17, email18) are being handled informally with no formal change control, scheduling decisions, or documented resolutions, indicating a systemic absence of intake and tracking process for the DivatKirály project.
**Threads:** email11, email16, email17, email18
**Action:** The Director should mandate a formal backlog review meeting to triage all open requests (CSV export, NEW badge, SKU search), confirm the GDPR fix is live, and enforce a change control process requiring written sign-off before any new scope is accepted.

**[DivatKirály] IMPLICIT_COMMITMENT** — `MEDIUM`
> Informally accepted or untracked client requests appear across email11 (CSV export forwarded by client), email16 (NEW badge raised by client), and email18 (SKU search relayed by CRM), collectively implying a pattern where client requests enter the project without formal acknowledgment, effort estimation, or prioritization, creating implicit delivery expectations.
**Threads:** email11, email16, email18
**Action:** The Director should ensure all three requests receive a formal written response to the client stating current status, and establish a single intake channel so no client request is treated as committed without explicit project manager sign-off.

---

## 🔵 Needs PM Review

_The items below were detected by the rule engine but could not be confirmed with high confidence. Please review with the relevant PM before the QBR._

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 55%]
> The minimum password length requirement for the new login page (raised by Gábor on 2025-06-02 in reference to point 3.2) remains unanswered 216 days later, representing a potential specification gap that could cause implementation inconsistency or a security compliance issue.
**Evidence:** _horvath.gabor@kisjozsitech.hu wrote: 'I don't see any mention of the minimum password length. Should it be 8 characters, like in other modules?' — no _

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 55%]
> JIRA-112 (profile picture bug) was acknowledged as being investigated by Gábor on 2025-06-30, but no resolution is recorded in this thread and 196 days have elapsed with no follow-up visible here.
**Evidence:** _Péter confirms 'Yes, Gábor is looking into it' (email3_msg1, 2025-06-30T10:05) — this is acknowledgment only, not resolution. No subsequent message in_

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 55%]
> A confirmed bug in the image upload logic (filenames with spaces causing 404s) was identified and attributed to Gábor's commit on 2025-06-29, but the thread ends with only an acknowledgment of intent to fix — no resolution is documented 197 days later.
**Evidence:** _Gábor's final message (email4_msg4, 2025-06-30): 'I'll check it immediately. This is clearly my mistake' — this is an acknowledgment-only signal with _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 62%]
> A client CSV export request forwarded on 2025-06-25 has received no decision or follow-up after the BA asked Gábor for a scheduling assessment, leaving the feature request unresolved for 199 days.
**Evidence:** _Eszter Varga asked 'Gábor, what do you think, does it fit into the current schedule?' on 2025-06-25T14:05:00; no response from Gábor or any other part_

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 35%]
> A client CSV export request forwarded on 2025-06-25 received only a feasibility acknowledgment from the BA and an unanswered question to Gábor about scheduling, with no decision or resolution visible in the thread after 199 days.
**Evidence:** _Eszter Varga wrote on 2025-06-25T14:05: 'we need to assess the development effort. Gábor, what do you think, does it fit into the current schedule?' —_

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 30%]
> Anna's clarification question about whether the 'Add to Cart' button change requires a color swap or just resizing/bolding was never answered within this thread, but the overall business impact is low and the issue may have been resolved outside this email chain.
**Evidence:** _email14_msg1 (Anna, 2025-05-26): 'Does the client want a different color instead of the current green, or just for it to be larger/bold? This isn't cl_

**[DivatKirály]** Uncontrolled Scope Change — [Unvalidated, confidence: 45%]
> A BA proposed adding a 'NEW' badge feature mid-sprint as a 'nice to have', but the thread has no engineering response, no acceptance decision, and no sprint impact assessment — the scope change risk is real but unconfirmed as it may still be pending triage.
**Evidence:** _anna.nagy@kisjozsitech.hu (2025-06-16): 'A "nice to have" requirement came up: products uploaded in the last 30 days should have a small "NEW" badge o_

---

## Recommended Director Actions

1. **[DivatKirály — Fwd: Re: DivatKirály - User registration process]** Immediately verify with Zsófia Varga whether the newsletter checkbox fix has been deployed to production and confirm the Terms & Conditions checkbox was left unchanged; if not yet deployed, escalate as a blocking GDPR compliance issue requiring same-day resolution and notify the client (via Eszter Horvath) once confirmed fixed.
2. **[Project Phoenix — Project Phoenix - New Login Page Specification]** Direct Zsuzsa (varga.zsuzsa@kisjozsitech.hu) to immediately confirm: (1) the minimum password length requirement from Gábor's open question, and (2) explicit team sign-off on the remaining spec points. Escalate to Péter (kovacs.peter@kisjozsitech.hu) as the senior stakeholder who issued the coordination request, and ensure a formal spec approval is recorded before any further login page development proceeds.
3. **[Project Phoenix — Project Phoenix - Staging Environment Anomaly]** Direct the Engineering Director to immediately follow up with horvath.gabor@kisjozsitech.hu for a status update on the filename-space bug fix; if no fix has been committed, assign a senior developer to review and resolve the image upload logic within the current sprint, and verify the fix is deployed and tested on staging before closing the issue.
4. **[DivatKirály — User Profile Page - Data Modification Flow]** Ask Gábor Nagy to confirm whether the password-change confirmation email was actually added to the backlog and if so, what its current implementation status is; if not yet implemented, escalate as a security gap and assign it to a developer with a concrete delivery date given the 194-day delay.
5. **[DivatKirály — Fwd: Request regarding report export]** Identify Gábor (likely the Engineering Lead or Sprint Owner for DivatKirály) and require him to provide a scheduling decision within 2 business days; if the feature is deprioritized, formally communicate that to Zoltán Kiss and the client to close the loop on the outstanding request.
6. **[DivatKirály — DivatKirály - Weekly status and development progre]** Direct the PM (Péter Kovacs) to obtain written client sign-off on the SKU search requirement as a formal scope change before Gábor begins implementation next week; ensure the JIRA ticket references an approved change request, and confirm whether this extra development affects the project budget or delivery timeline.
7. **[DivatKirály — Small request: "New" label on the product page]** Direct the engineering lead to provide a quick effort estimate (story points or hours) for the 'NEW' badge feature so the BA and product owner can make an explicit backlog prioritization decision — either schedule it, defer it to a future sprint, or formally close it as out of scope for DivatKirály.

---

⚠️ **AI-GENERATED REPORT** — Validate flagged items with responsible PMs before acting.
Generated by QBR Portfolio Health Analyzer | Model: claude-sonnet-4-6
Run date: 2026-03-13 08:41