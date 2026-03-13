# QBR Portfolio Health Report
**Period:** Q2 2025  
**Generated:** 2026-03-13 10:08  
**Projects Reviewed:** 2 | **Open Flags:** 7 | **Needs Review:** 8

---

## Executive Summary

DivatKirály is the portfolio's highest-risk project, carrying an unresolved HIGH-severity GDPR violation (pre-checked newsletter opt-in on the live registration form), an uncontrolled scope change accepted without sign-off, and three stalled decisions — one 199 days old — while Project Phoenix has two medium-severity stalled items including an unconfirmed staging bug fix and a 211-day-old spec gap on login page requirements. The single most critical concern is the DivatKirály GDPR incident: as of 2025-06-27 Zsófia Varga has not confirmed the fix is deployed to production, a near-miss on the mandatory T&C checkbox indicates elevated implementation risk, and every additional day of inaction on a live client system compounds legal exposure.

---

## 🔴 Immediate Attention Required

### DivatKirály

**Stalled Decision** — `MEDIUM` [Rule+LLM-confirmed]
> A client-requested CSV export feature for the DivatKirály project has had no response from the engineering lead (Gábor) for 199 days after the BA explicitly asked 'Gábor, what do you think, does it fit into the current schedule?'
**Evidence:** _eszter.varga@kisjozsitech.hu asked on 2025-06-25T14:05:00: 'Gábor, what do you think, does it fit into the current schedule?' — no reply from Gábor or any other party appears in the thread, leaving th_
**Days open:** 199 business days
**Owner:** eszter.varga@kisjozsitech.hu
**Action:** Directly contact Gábor (engineering lead) to obtain a scheduling decision on the CSV export feature; if Gábor is unavailable or unresponsive, escalate to the sprint planning owner to formally triage this client request into the backlog or next sprint, and close the loop with Zoli and the client (Béla) on expected delivery timeline.

**Uncontrolled Scope Change** — `MEDIUM` [Rule+LLM-confirmed]
> A new SKU-based search requirement surfaced informally via a delayed client mention, was not in the original specification, and has been accepted into scope without formal change control or client sign-off on cost/timeline impact.
**Evidence:** _Eszter (email18_msg1): 'in last week's meeting, the client mentioned it would be good if the search worked not only for product names but also for item numbers (SKU). I forgot to mention this until no_
**Owner:** peter.kovacs@kisjozsitech.hu
**Action:** Direct Péter to halt scheduling of the SKU search work until a formal change request is raised, the client provides written approval, and the effort (~0.5 day backend + testing per Gábor) is reflected in the project plan and budget. Verify whether 'extra development' implies a billable change order or an absorbed cost, and ensure this is documented before Gábor begins work next week.

**Stalled Decision** — `LOW` [Rule+LLM-confirmed]
> A 'nice to have' feature request for a 'NEW' badge on product pages was raised on 2025-06-16 with an explicit sizing/prioritization question and has received zero responses in 206 days.
**Evidence:** _'How big of a task would this be? Could we fit it into the current sprint if it's not a huge effort?' — asked by anna.nagy@kisjozsitech.hu on 2025-06-16; no reply, estimate, or decision exists anywher_
**Days open:** 206 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Direct the tech lead or a senior developer to provide a quick effort estimate for the 'NEW' badge feature, then make an explicit backlog/sprint decision: either schedule it, defer it to a future release, or formally close it as out of scope — and communicate the outcome to Anna Nagy to close the loop.

**Stalled Decision** — `LOW` [LLM-confirmed]
> A 'nice to have' feature request for a 'NEW' badge on product pages was raised by Anna Nagy on 2025-06-16 and has received zero responses or decisions in 206 days.
**Evidence:** _The sole message in the thread is Anna Nagy's 2025-06-16 request: 'How big of a task would this be? Could we fit it into the current sprint if it's not a huge effort?' — no reply, no estimation, no ac_
**Days open:** 206 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Direct the team lead or product owner to formally triage this request: either estimate the effort and schedule it in an upcoming sprint, or explicitly reject/defer it as a backlog item — a 206-day unanswered question, even for a low-priority 'nice to have', represents unresolved backlog debt that should be closed out.

---

## 🟡 Monitor Closely

### Project Phoenix

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> Zsuzsa resolved the Google SSO scope question on 2025-06-09 but left two open items unanswered — minimum password length (Gábor's point 3.2 query) and explicit team confirmation that all remaining spec points are accepted — with no follow-up recorded in 211 days.
**Evidence:** _Zsuzsa's final message (email1_msg4, 2025-06-09) states 'We can remove it from the scope for now. Are the other points okay?' — the question 'Are the other points okay?' has received no reply in the t_
**Days open:** 211 business days
**Owner:** varga.zsuzsa@kisjozsitech.hu
**Action:** Direct Zsuzsa (varga.zsuzsa@kisjozsitech.hu) to immediately follow up with the team to: (1) confirm the minimum password length requirement for point 3.2 as raised by Gábor, and (2) obtain explicit sign-off from all reviewers that the remaining spec points are accepted. Péter (kovacs.peter@kisjozsitech.hu) should be looped in as the apparent decision authority to formally close the specification before any further development proceeds on the login page.

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> A staging environment bug in profile picture upload was prematurely closed by the reporter on 2025-06-09, resurfaced on 2025-06-29 with a root cause identified (filename-with-spaces bug in Gábor's commit), but the thread ends with only an acknowledgment of fault and no confirmed fix as of the last message on 2025-06-30.
**Evidence:** _kiss.anna closed the issue speculatively: 'Maybe it got fixed after yesterday's deployment? It's not happening for me now either. Let's leave it for now.' Twenty days later, nagy.istvan reopened it: '_
**Days open:** 211 business days
**Owner:** horvath.gabor@kisjozsitech.hu
**Action:** Direct horvath.gabor to provide an immediate status update on the filename-handling fix; if no fix has been deployed, assign a formal ticket with a deadline within the current sprint. Verify on staging that profile picture uploads with space-containing filenames return the correct renamed path from the API before closing.

---

## Incidents This Quarter

**[DivatKirály]** **Fwd: Re: DivatKirály - User registration process** — 🔴 Open
> A live GDPR compliance violation exists on the DivatKirály registration form where the newsletter subscription checkbox is pre-checked by default, reported urgently by the client on 2025-06-26, and as of the last message (2025-06-27) the fix has not been confirmed as completed — with an additional risk that the developer nearly incorrectly unchecked the Terms & Conditions checkbox as well.
_Eszter Horvath (2025-06-26T15:03): 'The client indicated that due to GDPR, the newsletter subscription checkbox cannot be checked by default. It currently is. Please fix it.' — Zsófia Varga (2025-06-2_
**Action:** Immediately confirm with Zsófia Varga whether the newsletter checkbox has been corrected to unchecked-by-default (and only that checkbox); obtain explicit written confirmation of deployment to production. Given the near-miss of also unchecking the mandatory T&C checkbox, a peer code review of the change is strongly recommended before release. Escalate to legal/compliance if the fix cannot be confirmed within 1 business day, as this is an active GDPR violation on a live client system.

---

## Cross-Project Patterns

**[Project Phoenix] SYSTEMIC_PROCESS_FAILURE** — `MEDIUM`
> At least two separate threads show issues being acknowledged or partially addressed but never formally closed, indicating a systemic pattern of incomplete resolution and lack of follow-through on open action items across Project Phoenix.
**Threads:** email1, email4
**Action:** The Director should institute a formal closure protocol requiring explicit written confirmation from all stakeholders before any open item or bug is marked resolved, and schedule a review of all currently 'acknowledged' items across the project to confirm actual completion status.

**[DivatKirály] RECURRING_BLOCKER** — `HIGH`
> Multiple client-facing feature requests and decisions have gone completely unanswered for extended periods (199–206 days), indicating a systemic failure in triaging and responding to incoming requests across the DivatKirály project.
**Threads:** email11, email16
**Action:** The Director should establish a mandatory SLA for responding to client feature requests and engineering sizing questions, and audit whether Gábor (engineering lead) and Anna Nagy's ownership queue have additional unresolved items beyond these two threads.

**[DivatKirály] SYSTEMIC_PROCESS_FAILURE** — `HIGH`
> Scope changes are entering the DivatKirály project through informal channels without change control (email18), while simultaneously client requests that should trigger formal scoping discussions are receiving no response at all (email11, email16), suggesting the project lacks any structured intake and prioritization process.
**Threads:** email11, email16, email18
**Action:** The Director should immediately implement a formal change request and feature intake process for DivatKirály, requiring written acknowledgment within a defined window and mandatory sign-off on scope, cost, and timeline before any new work is accepted or deferred.

**[DivatKirály] IMPLICIT_COMMITMENT** — `HIGH`
> A live GDPR violation (email17) and an uncontrolled scope addition (email18) both reflect reactive, undocumented handling of client-raised issues, collectively implying the team is making or avoiding commitments informally without proper tracking or legal/contractual review.
**Threads:** email17, email18
**Action:** The Director should require that all compliance-related incidents and scope changes be logged in the project tracker with a named owner, resolution deadline, and client confirmation, and should verify with legal counsel that the GDPR fix in email17 has been fully deployed and documented.

---

## 🔵 Needs PM Review

_The items below were detected by the rule engine but could not be confirmed with high confidence. Please review with the relevant PM before the QBR._

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 45%]
> The minimum password length requirement for the new login page was raised on 2025-06-02 and has never been explicitly answered in the thread, leaving a potential specification gap open for over 216 days.
**Evidence:** _horvath.gabor: 'I don't see any mention of the minimum password length. Should it be 8 characters, like in other modules?' (email1_msg1, 2025-06-02T10_

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 62%]
> JIRA-112 (profile picture bug) was acknowledged as being investigated by Gábor on 2025-06-30, but no resolution has been recorded in this thread, and the item has been open for 196 days with no follow-up visible.
**Evidence:** _Péter confirms in email3_msg1: 'Yes, Gábor is looking into it' — this is an acknowledgment only, not a resolution. No subsequent message in the thread_

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 45%]
> A confirmed bug in the profile picture upload logic (filenames with spaces causing 404s) was acknowledged by the responsible developer Gábor on 2025-06-30, but no resolution confirmation exists in the thread, and the issue has been open for 197 days.
**Evidence:** _nagy.istvan: 'This isn't a cache issue; it's a bug in the image upload logic. Gábor, didn't your last commit touch this part?' — horvath.gabor: 'Yes, _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 55%]
> A security-relevant decision about sending confirmation emails after password changes was raised on 2025-07-02 and only reached a 'add to to-do list' acknowledgment from the PM, with no confirmed implementation or formal specification update in 194 days.
**Evidence:** _PM stated 'Let's add the email after password modification to the to-do list' (email10_msg3, 2025-07-03T10:45:00), but no subsequent message in the th_

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 62%]
> A client CSV export request forwarded on 2025-06-25 has received no decision or follow-up after the BA asked Gábor for a scheduling assessment, leaving the feature request unresolved for 199 days.
**Evidence:** _Eszter Varga (BA) asked on 2025-06-25T14:05: 'Gábor, what do you think, does it fit into the current schedule?' — no response from Gábor or any other _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 62%]
> A client CSV export request forwarded on 2025-06-25 received only a feasibility acknowledgment from the BA and a question directed at Gábor, with no scheduling decision, acceptance, or rejection recorded in 199 days.
**Evidence:** _Eszter Varga (BA) wrote on 2025-06-25T14:05: 'It's technically feasible, but we need to assess the development effort. Gábor, what do you think, does _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 35%]
> Anna's unanswered clarification question about the 'Add to Cart' button color vs. size change has no documented resolution in the thread, though the broader design feedback session appears largely concluded with the logo fix approved for go-live.
**Evidence:** _Anna asks in email14_msg1: 'Does the client want a different color instead of the current green, or just for it to be larger/bold? This isn't clear.' _

**[DivatKirály]** Uncontrolled Scope Change — [Unvalidated, confidence: 45%]
> A BA has proposed adding a 'NEW' badge feature mid-sprint as a 'nice to have', but there is no evidence yet that the scope change was accepted or incorporated without proper change control.
**Evidence:** _anna.nagy@kisjozsitech.hu wrote: 'A "nice to have" requirement came up: products uploaded in the last 30 days should have a small "NEW" badge on their_

---

## Recommended Director Actions

1. **[DivatKirály — Fwd: Re: DivatKirály - User registration process]** Immediately confirm with Zsófia Varga whether the newsletter checkbox has been corrected to unchecked-by-default (and only that checkbox); obtain explicit written confirmation of deployment to production. Given the near-miss of also unchecking the mandatory T&C checkbox, a peer code review of the change is strongly recommended before release. Escalate to legal/compliance if the fix cannot be confirmed within 1 business day, as this is an active GDPR violation on a live client system.
2. **[Project Phoenix — Project Phoenix - New Login Page Specification]** Direct Zsuzsa (varga.zsuzsa@kisjozsitech.hu) to immediately follow up with the team to: (1) confirm the minimum password length requirement for point 3.2 as raised by Gábor, and (2) obtain explicit sign-off from all reviewers that the remaining spec points are accepted. Péter (kovacs.peter@kisjozsitech.hu) should be looped in as the apparent decision authority to formally close the specification before any further development proceeds on the login page.
3. **[Project Phoenix — Project Phoenix - Staging Environment Anomaly]** Direct horvath.gabor to provide an immediate status update on the filename-handling fix; if no fix has been deployed, assign a formal ticket with a deadline within the current sprint. Verify on staging that profile picture uploads with space-containing filenames return the correct renamed path from the API before closing.
4. **[DivatKirály — Fwd: Request regarding report export]** Directly contact Gábor (engineering lead) to obtain a scheduling decision on the CSV export feature; if Gábor is unavailable or unresponsive, escalate to the sprint planning owner to formally triage this client request into the backlog or next sprint, and close the loop with Zoli and the client (Béla) on expected delivery timeline.
5. **[DivatKirály — DivatKirály - Weekly status and development progre]** Direct Péter to halt scheduling of the SKU search work until a formal change request is raised, the client provides written approval, and the effort (~0.5 day backend + testing per Gábor) is reflected in the project plan and budget. Verify whether 'extra development' implies a billable change order or an absorbed cost, and ensure this is documented before Gábor begins work next week.
6. **[DivatKirály — Small request: "New" label on the product page]** Direct the tech lead or a senior developer to provide a quick effort estimate for the 'NEW' badge feature, then make an explicit backlog/sprint decision: either schedule it, defer it to a future release, or formally close it as out of scope — and communicate the outcome to Anna Nagy to close the loop.

---

⚠️ **AI-GENERATED REPORT** — Validate flagged items with responsible PMs before acting.
Generated by QBR Portfolio Health Analyzer | Model: claude-sonnet-4-6
Run date: 2026-03-13 10:08