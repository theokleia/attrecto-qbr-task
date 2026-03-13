# QBR Portfolio Health Report
**Period:** Q2 2025  
**Generated:** 2026-03-13 13:13  
**Projects Reviewed:** 2 | **Open Flags:** 8 | **Needs Review:** 7

---

## Executive Summary

Portfolio health is degraded across both active projects, with DivatKirály carrying the majority of risk: one open GDPR violation (pre-checked newsletter opt-in on the live registration form), two stalled security-relevant decisions unresolved for 194–199 days, and an uncontrolled scope change (SKU search) accepted without formal change order or client sign-off. Project Phoenix has two medium-severity stalled decisions — unconfirmed spec items owned by Zsuzsa and an unverified staging bug fix owned by Gábor — but presents no immediate compliance exposure. The single most critical concern is the unconfirmed GDPR fix on DivatKirály's registration form: if Zsófia Varga cannot provide written confirmation of production deployment within one business day, this requires immediate legal and compliance escalation.

---

## 🔴 Immediate Attention Required

### DivatKirály

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> A security-relevant decision to send confirmation emails after password changes was informally agreed upon 194 days ago but never formally resolved, assigned, or added to a tracked backlog item.
**Evidence:** _Gábor Nagy (PM) wrote on 2025-07-03: 'Let's add the email after password modification to the to-do list.' — this is an acknowledgment and informal queue entry, not a confirmed decision with an owner o_
**Days open:** 194 business days
**Owner:** gabor.nagy@kisjozsitech.hu
**Action:** Direct Gábor Nagy to confirm whether the confirmation email after password change was actually implemented or formally added to the backlog with an owner and acceptance criteria; if not, escalate to the BA (Eszter Varga) to update the specification and assign a developer, given the security implications of this feature gap.

**Stalled Decision** — `MEDIUM` [Rule+LLM-confirmed]
> A client-requested CSV export feature for the DivatKirály project has had no scheduling decision for 199 days after Eszter Varga directed a capacity question to Gábor, who has never responded in the thread.
**Evidence:** _eszter.varga@kisjozsitech.hu wrote on 2025-06-25T14:05:00: 'Gábor, what do you think, does it fit into the current schedule?' — no reply from Gábor or any other party appears in the thread, leaving th_
**Days open:** 199 business days
**Owner:** eszter.varga@kisjozsitech.hu
**Action:** Identify Gábor (likely a Tech Lead or Engineering Manager on DivatKirály) and require an explicit scheduling decision within 2 business days; if the feature is deprioritized, formally communicate that to the Account Manager (zoltan.kiss@kisjozsitech.hu) so the client (Béla, bela.ugyfel@nagyker.hu) can be informed and expectations reset.

**Uncontrolled Scope Change** — `MEDIUM` [Rule+LLM-confirmed]
> A new SKU-based search requirement surfaced informally via a delayed client mention, was not in the original specification, and has been accepted into scope without formal change control or client sign-off on cost/timeline impact.
**Evidence:** _Eszter (email18_msg1): 'in last week's meeting, the client mentioned it would be good if the search worked not only for product names but also for item numbers (SKU). I forgot to mention this until no_
**Owner:** peter.kovacs@kisjozsitech.hu
**Action:** Direct Péter to halt implementation of the SKU search feature until a formal change request is raised, the ~0.5 day backend effort plus testing is officially estimated and documented, and the client provides written approval acknowledging this is out-of-scope additional work. Ensure the JIRA ticket Anna creates is linked to a change order rather than treated as a standard backlog item, and confirm whether this affects the current sprint timeline or budget baseline.

**Stalled Decision** — `LOW` [LLM-confirmed]
> A 'nice to have' feature request for a 'NEW' badge on product pages was raised on 2025-06-16 with an explicit sizing/prioritization question and has received zero responses in 206 days.
**Evidence:** _'How big of a task would this be? Could we fit it into the current sprint if it's not a huge effort?' — asked by anna.nagy@kisjozsitech.hu on 2025-06-16; no reply exists in the thread._
**Days open:** 206 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Direct the engineering lead or scrum master to provide a quick effort estimate for the 'NEW' badge feature and make an explicit prioritization decision — either schedule it in an upcoming sprint or formally defer/close it as out of scope, then communicate the outcome to Anna Nagy to close the loop.

**Stalled Decision** — `LOW` [LLM-confirmed]
> A 'nice to have' feature request for a 'NEW' badge on product pages was raised by Anna Nagy on 2025-06-16 and has received zero responses or decisions in 206 days.
**Evidence:** _The sole message in the thread is Anna Nagy's 2025-06-16 request: 'How big of a task would this be? Could we fit it into the current sprint if it's not a huge effort?' — no reply, no estimation, no ac_
**Days open:** 206 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Direct the team lead or product owner to formally triage this request: either schedule a quick estimation (it was flagged as potentially low-effort), defer it to the backlog with a target sprint, or explicitly reject it as out of scope — then close the thread with a documented decision to prevent further drift.

---

## 🟡 Monitor Closely

### Project Phoenix

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> Zsuzsa's June 9 message resolved the SSO scope question but left two other open issues unaddressed — minimum password length (Gábor, email1_msg1) and implicit sprint re-planning (Péter, email1_msg3) — with no follow-up in 211 days.
**Evidence:** _Zsuzsa's final message (email1_msg4, 2025-06-09) states 'We can remove it from the scope for now. Are the other points okay?' — the trailing question received no reply. Gábor's unresolved query (email_
**Days open:** 211 business days
**Owner:** varga.zsuzsa@kisjozsitech.hu
**Action:** Direct Zsuzsa (varga.zsuzsa@kisjozsitech.hu) to issue an explicit written confirmation on: (1) the minimum password length for section 3.2, and (2) whether the sprint plan was updated to reflect SSO removal. Péter (kovacs.peter@kisjozsitech.hu) should confirm sprint re-planning is complete. Both items must be closed in writing before the specification is treated as final.

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> A staging environment bug in profile picture upload was prematurely closed by the reporter on 2025-06-09, resurfaced on 2025-06-29 with a root cause identified (filename-with-spaces bug in Gábor's commit), but the thread ends with only an acknowledgment of fault and no confirmed fix as of the last message on 2025-06-30.
**Evidence:** _kiss.anna closed the issue speculatively: 'Maybe it got fixed after yesterday's deployment? It's not happening for me now either. Let's leave it for now.' Twenty days later, nagy.istvan reopened it: '_
**Days open:** 211 business days
**Owner:** horvath.gabor@kisjozsitech.hu
**Action:** Direct horvath.gabor to provide an immediate status update on the filename-handling fix; if no fix has been deployed, assign a formal ticket with a deadline within the current sprint. Verify on staging that profile picture uploads with space-containing filenames return the correct renamed path from the API before closing.

---

## Incidents This Quarter

**[DivatKirály]** **Fwd: Re: DivatKirály - User registration process** — 🔴 Open
> A live GDPR compliance violation exists on the DivatKirály registration form where the newsletter subscription checkbox is pre-checked by default, and the fix has not been confirmed as completed — additionally, a developer proposed an incorrect scope expansion that was immediately stopped by the BA.
_Eszter (2025-06-26T15:03): 'The client indicated that due to GDPR, the newsletter subscription checkbox cannot be checked by default. It currently is. Please fix it.' Zsófia (2025-06-27T09:12) respond_
**Action:** Immediately confirm with Zsófia Varga whether the newsletter checkbox fix has been deployed to production (no resolution signal exists in the thread). Verify that ONLY the newsletter checkbox was changed and the Terms & Conditions checkbox logic remains intact. Given the GDPR regulatory exposure, require written confirmation of the fix and a QA sign-off before closing. Escalate to legal/compliance if the fix cannot be confirmed within 1 business day.

---

## Cross-Project Patterns

**[Project Phoenix] RECURRING_BLOCKER** — `MEDIUM`
> Gábor (horvath.gabor@kisjozsitech.hu) is linked to unresolved technical issues in at least two threads: an open minimum password length decision in email1 and an unconfirmed bug fix for a filename-with-spaces commit error in email4, suggesting he is a recurring point of incomplete delivery or follow-through.
**Threads:** email1, email4
**Action:** The Director should directly request a written status update from Gábor on both the password length specification and the profile picture upload bug fix, with a hard deadline, and consider assigning a second owner to verify closure on each item.

**[DivatKirály] RECURRING_BLOCKER** — `HIGH`
> Gábor Nagy is a non-responder and decision bottleneck across multiple threads: he never responded to Eszter Varga's capacity question about the CSV export feature (email11, 199 days stalled), and he is the named owner of an unresolved security decision about password-change confirmation emails (email10, 194 days stalled).
**Threads:** email10, email11
**Action:** The Director should directly engage Gábor Nagy to obtain formal decisions on both items and assess whether his workload or role clarity is creating a systemic bottleneck; escalate ownership if he cannot respond within 48 hours.

**[DivatKirály] SYSTEMIC_PROCESS_FAILURE** — `HIGH`
> Multiple client-facing feature requests and compliance issues are entering the project without formal tracking, scheduling, or sign-off: the CSV export request (email11) has no scheduling decision, the 'NEW' badge request (email16) has zero response after 206 days, and a new SKU-based search requirement (email18) was accepted into scope without change control — indicating a systemic absence of intake and triage process.
**Threads:** email11, email16, email18
**Action:** The Director should mandate a formal backlog triage session to capture and prioritize all untracked requests, and enforce a change control gate requiring written sign-off on scope, cost, and timeline before any new requirement is accepted.

**[DivatKirály] IMPLICIT_COMMITMENT** — `MEDIUM`
> Informal agreements are being made without formal resolution or backlog tracking across multiple threads: a security feature (password-change confirmation email, email10) was informally agreed upon 194 days ago with no ticket, and a scope addition (SKU-based search, email18) was accepted verbally without client sign-off — together suggesting the team routinely treats informal agreement as sufficient commitment.
**Threads:** email10, email18
**Action:** The Director should require that any agreed feature or scope change — regardless of how it surfaces — be logged in the tracked backlog within 24 hours, with an assigned owner and acceptance criteria, before any development work begins.

**[DivatKirály] SYSTEMIC_PROCESS_FAILURE** — `HIGH`
> A live GDPR violation on the registration form (email17) remains unconfirmed as fixed, while a separate security-relevant decision (password-change confirmation emails, email10) has been stalled for 194 days — indicating that compliance and security concerns are not being treated with appropriate urgency or tracked to verified closure.
**Threads:** email17, email10
**Action:** The Director should immediately verify the GDPR fix deployment status in email17 and escalate to legal/DPO if unresolved, then establish a compliance-flagged fast-track lane in the backlog to ensure security and regulatory items are resolved within a defined SLA.

---

## 🔵 Needs PM Review

_The items below were detected by the rule engine but could not be confirmed with high confidence. Please review with the relevant PM before the QBR._

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 55%]
> The minimum password length for the new login page (point 3.2) was raised as an open question on 2025-06-02 and has never been answered in the thread, leaving a security-relevant specification gap unresolved for over 200 days.
**Evidence:** _horvath.gabor@kisjozsitech.hu wrote: 'I don't see any mention of the minimum password length. Should it be 8 characters, like in other modules?' (emai_

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 55%]
> JIRA-112 (profile picture bug) was acknowledged as being investigated by Gábor on 2025-06-30, but no resolution has been recorded in this thread, and the item has been open for 196 days with no follow-up visible.
**Evidence:** _Péter confirms 'Yes, Gábor is looking into it' (email3_msg1, 2025-06-30T10:05), which is an acknowledgment-only signal. No subsequent message in the t_

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 55%]
> A confirmed bug in the image upload logic (filenames with spaces causing 404s) was identified and attributed to Gábor's commit on 2025-06-29, but the thread ends with only an acknowledgment of intent to fix — no resolution is documented 197 days later.
**Evidence:** _Gábor's final message (email4_msg4, 2025-06-30): 'I'll check it immediately. This is clearly my mistake' — this is an acknowledgment-only signal with _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 62%]
> A client CSV export request forwarded on 2025-06-25 has received no decision or follow-up after the BA asked Gábor for a scheduling assessment, leaving the feature request unresolved for 199 days.
**Evidence:** _Eszter Varga (BA) asked on 2025-06-25T14:05: 'Gábor, what do you think, does it fit into the current schedule?' — no response from Gábor or any other _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 62%]
> A client CSV export request forwarded on 2025-06-25 received only a feasibility acknowledgment from the BA and a question directed at Gábor, with no decision, assignment, or resolution recorded in 199 days.
**Evidence:** _Eszter Varga (BA) wrote on 2025-06-25T14:05: 'It's technically feasible, but we need to assess the development effort. Gábor, what do you think, does _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 35%]
> Anna's clarification question about whether the 'Add to Cart' button change requires a color swap or just size/bold styling was never answered within this thread, but the low business impact and age of the thread suggest it may have been resolved outside this email chain.
**Evidence:** _email14_msg1 (Anna, 2025-05-26): 'Does the client want a different color instead of the current green, or just for it to be larger/bold? This isn't cl_

**[DivatKirály]** Uncontrolled Scope Change — [Unvalidated, confidence: 35%]
> A BA raised a 'nice to have' NEW badge feature request on 2025-06-16, but the thread contains only the initial inquiry with no engineering response, sprint commitment, or scope acceptance — making uncontrolled scope change unconfirmable at this time.
**Evidence:** _anna.nagy@kisjozsitech.hu wrote: 'A "nice to have" requirement came up... How big of a task would this be? Could we fit it into the current sprint if _

---

## Recommended Director Actions

1. **[DivatKirály — Fwd: Re: DivatKirály - User registration process]** Immediately confirm with Zsófia Varga whether the newsletter checkbox fix has been deployed to production (no resolution signal exists in the thread). Verify that ONLY the newsletter checkbox was changed and the Terms & Conditions checkbox logic remains intact. Given the GDPR regulatory exposure, require written confirmation of the fix and a QA sign-off before closing. Escalate to legal/compliance if the fix cannot be confirmed within 1 business day.
2. **[Project Phoenix — Project Phoenix - New Login Page Specification]** Direct Zsuzsa (varga.zsuzsa@kisjozsitech.hu) to issue an explicit written confirmation on: (1) the minimum password length for section 3.2, and (2) whether the sprint plan was updated to reflect SSO removal. Péter (kovacs.peter@kisjozsitech.hu) should confirm sprint re-planning is complete. Both items must be closed in writing before the specification is treated as final.
3. **[Project Phoenix — Project Phoenix - Staging Environment Anomaly]** Direct horvath.gabor to provide an immediate status update on the filename-handling fix; if no fix has been deployed, assign a formal ticket with a deadline within the current sprint. Verify on staging that profile picture uploads with space-containing filenames return the correct renamed path from the API before closing.
4. **[DivatKirály — User Profile Page - Data Modification Flow]** Direct Gábor Nagy to confirm whether the confirmation email after password change was actually implemented or formally added to the backlog with an owner and acceptance criteria; if not, escalate to the BA (Eszter Varga) to update the specification and assign a developer, given the security implications of this feature gap.
5. **[DivatKirály — Fwd: Request regarding report export]** Identify Gábor (likely a Tech Lead or Engineering Manager on DivatKirály) and require an explicit scheduling decision within 2 business days; if the feature is deprioritized, formally communicate that to the Account Manager (zoltan.kiss@kisjozsitech.hu) so the client (Béla, bela.ugyfel@nagyker.hu) can be informed and expectations reset.
6. **[DivatKirály — DivatKirály - Weekly status and development progre]** Direct Péter to halt implementation of the SKU search feature until a formal change request is raised, the ~0.5 day backend effort plus testing is officially estimated and documented, and the client provides written approval acknowledging this is out-of-scope additional work. Ensure the JIRA ticket Anna creates is linked to a change order rather than treated as a standard backlog item, and confirm whether this affects the current sprint timeline or budget baseline.
7. **[DivatKirály — Small request: "New" label on the product page]** Direct the engineering lead or scrum master to provide a quick effort estimate for the 'NEW' badge feature and make an explicit prioritization decision — either schedule it in an upcoming sprint or formally defer/close it as out of scope, then communicate the outcome to Anna Nagy to close the loop.

---

⚠️ **AI-GENERATED REPORT** — Validate flagged items with responsible PMs before acting.
Generated by QBR Portfolio Health Analyzer v2.2 | Model: claude-sonnet-4-6
Run date: 2026-03-13 13:13