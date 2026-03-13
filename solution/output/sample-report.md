# QBR Portfolio Health Report
**Period:** Q2 2025  
**Generated:** 2026-03-13 13:48  
**Projects Reviewed:** 2 | **Open Flags:** 7 | **Needs Review:** 8

---

## Executive Summary

Portfolio health is degraded across both active projects, with 6 open flags spanning compliance violations, stalled decisions, and uncontrolled scope — several exceeding 200 days without resolution. The single most critical concern is DivatKirály's open GDPR incident: a pre-checked newsletter subscription checkbox flagged by the client on 2025-06-26 remains unconfirmed as fixed in production, a developer already attempted an incorrect scope of fix that had to be intercepted by the BA, and unresolved compliance exposure on a live system cannot wait for sprint cycles. Separately, Project Phoenix carries two unresolved blockers — an unconfirmed bug fix for filename-space 404s and a spec sign-off gap on the login page — both stalled for 211 days and at risk of compounding delivery debt if not closed this sprint.

---

## 🔴 Immediate Attention Required

### DivatKirály

**Stalled Decision** — `MEDIUM` [Rule+LLM-confirmed]
> A client-requested CSV export feature for DivatKirály has had no scheduling decision for 199 days after Eszter Varga directed the question to Gábor with no recorded response.
**Evidence:** _eszter.varga@kisjozsitech.hu wrote on 2025-06-25T14:05:00: 'Gábor, what do you think, does it fit into the current schedule?' — this direct scheduling question to Gábor has received no reply in the th_
**Days open:** 199 business days
**Owner:** eszter.varga@kisjozsitech.hu
**Action:** Identify who 'Gábor' is (likely a Tech Lead or Engineering Manager on DivatKirály) and obtain an immediate scheduling decision on the CSV export feature; if the feature has already been scoped or delivered outside this thread, close the flag with documentation, otherwise add it to the backlog with a committed sprint target and notify the client via Zoltán Kiss.

**Uncontrolled Scope Change** — `MEDIUM` [Rule+LLM-confirmed]
> A new SKU-based search requirement surfaced informally via a delayed client mention, confirmed as out-of-scope by the BA, and accepted into the backlog without documented client sign-off on cost or timeline impact.
**Evidence:** _Eszter (email18_msg1): 'in last week's meeting, the client mentioned it would be good if the search worked not only for product names but also for item numbers (SKU). I forgot to mention this until no_
**Owner:** peter.kovacs@kisjozsitech.hu
**Action:** Direct Péter Kovács to halt scheduling of the SKU search work until a formal change request is signed by the client, including effort estimate (~0.5 backend day + testing per Gábor in email18_msg3), impact on timeline, and any cost implications; verbal 'we'll do it' (email18_msg4) is insufficient change governance for a project in active delivery.

**Stalled Decision** — `LOW` [Rule+LLM-confirmed]
> A 'nice to have' feature request for a 'NEW' badge on product pages was raised on 2025-06-16 with an explicit sizing/prioritization question and has received zero responses in 206 days.
**Evidence:** _'How big of a task would this be? Could we fit it into the current sprint if it's not a huge effort?' — asked by anna.nagy@kisjozsitech.hu on 2025-06-16; no reply, estimate, or decision exists anywher_
**Days open:** 206 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Direct the tech lead or a senior developer to provide a quick effort estimate for the 'NEW' badge feature, then make an explicit backlog/sprint decision: either schedule it, defer it to a future release, or formally close it as out of scope — and communicate the outcome to Anna Nagy to close the loop.

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
> A GDPR-violating pre-checked newsletter subscription checkbox was flagged by the client on 2025-06-26 and remains unresolved as of the last message, with a developer also proposing an incorrect scope of fix that had to be stopped by the BA.
_Client email (2025-06-26 14:55): 'the newsletter subscription is automatically checked during registration. According to GDPR, this must be unchecked by default.' Eszter escalated urgently at 15:03. Z_
**Action:** Confirm with Zsófia Varga immediately whether the newsletter checkbox fix has been deployed to production; verify that only the newsletter checkbox was changed (not Terms and Conditions); request a test confirmation from Eszter Horváth to close the loop with the client, given the GDPR compliance risk and the near-miss scope error.

---

## Cross-Project Patterns

**[Project Phoenix] SYSTEMIC_PROCESS_FAILURE** — `HIGH`
> Multiple open technical issues across Project Phoenix have stalled for 211 days with no confirmed resolution, indicating a systemic failure to close and formally verify action items after initial acknowledgment.
**Threads:** email1, email4
**Evidence:**
  - `email1`: Minimum password length question raised by Gábor and implicit spec sign-off remain unaddressed for 211 days after Zsuzsa's June 9 message, with no follow-up response recorded.
  - `email4`: A confirmed image upload bug (filenames with spaces causing 404s) was acknowledged by Horvath Gábor with 'I'll check it immediately' on 2025-06-30, but no confirmed fix exists — also 211 days elapsed with no closure.
**Action:** The Director should mandate a formal issue-tracking protocol for Project Phoenix: every raised defect or open question must have a named owner, a due date, and a confirmed-closed status update. An immediate audit of both threads should be scheduled to determine current state of the password length spec, the sign-off, and the image upload bug fix.

**[DivatKirály] SYSTEMIC_PROCESS_FAILURE** — `HIGH`
> Multiple client-raised feature and compliance requests across the project are going unresolved for extended periods (199–206 days), indicating a systemic failure in the team's intake, triage, and response process for DivatKirály.
**Threads:** email11, email16, email17
**Evidence:**
  - `email11`: CSV export feature request directed to Gábor by Eszter Varga with no recorded response for 199 days — no scheduling decision made.
  - `email16`: NEW badge feature request raised by Anna Nagy on 2025-06-16 with an explicit sizing/prioritization question; zero responses or decisions in 206 days.
  - `email17`: A GDPR-violating pre-checked newsletter checkbox flagged by the client on 2025-06-26 remains unresolved as of the last message, with an incorrect fix scope also proposed internally.
**Action:** The Director should mandate an immediate audit of all open client-raised items across DivatKirály threads, establish a formal SLA for first-response and resolution, and assign a single accountable owner to each open item with a deadline for closure or explicit deferral.

**[DivatKirály] IMPLICIT_COMMITMENT** — `MEDIUM`
> Client requests are being informally acknowledged or redirected without formal tracking or documented decisions, creating a pattern of implicit commitments with no audit trail across multiple threads.
**Threads:** email11, email18
**Evidence:**
  - `email11`: Eszter Varga forwarded the client's CSV export request to Gábor, implying the team would handle it, but no formal decision, ticket, or timeline was recorded — leaving the client with an unconfirmed expectation for 199 days.
  - `email18`: A new SKU-based search requirement surfaced informally via a delayed client mention, was confirmed out-of-scope by the BA, yet was accepted into the backlog without documented client sign-off on cost or timeline impact — creating an undocumented delivery obligation.
**Action:** The Director should require that all client requests — regardless of how they surface — be logged in the formal backlog within 48 hours with an explicit status (accepted/deferred/rejected), and that any scope additions require written client acknowledgment of impact before entering the backlog.

---

## 🔵 Needs PM Review

_The items below were detected by the rule engine but could not be confirmed with high confidence. Please review with the relevant PM before the QBR._

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 55%]
> The minimum password length for the new login page (point 3.2) was raised as an open question on 2025-06-02 and has never been explicitly answered in the thread, leaving a security-relevant specification gap unresolved for over 216 days.
**Evidence:** _horvath.gabor@kisjozsitech.hu wrote: 'I don't see any mention of the minimum password length. Should it be 8 characters, like in other modules?' (emai_

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 55%]
> JIRA-112 (profile picture bug) was acknowledged as being investigated by Gábor on 2025-06-30, but no resolution has been recorded in this thread, and the item has been open for 196 days with no follow-up visible.
**Evidence:** _Péter confirms 'Yes, Gábor is looking into it' (email3_msg1, 2025-06-30T10:05), which is an acknowledgment-only signal. No subsequent message in the t_

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 45%]
> A confirmed bug in the profile picture upload logic (filenames with spaces causing 404s) was attributed to Gábor's commit on 2025-06-30, but the thread ends with only an acknowledgment and no confirmed fix, leaving resolution status unknown after 197 days.
**Evidence:** _Gábor stated on 2025-06-30: 'I rewrote the filename validation to replace special characters. It's possible the frontend isn't receiving the modified _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 55%]
> A security-relevant decision about sending confirmation emails after password changes was raised on 2025-07-02 and only reached a 'add to to-do list' acknowledgment from the PM, with no confirmed implementation or formal specification update in 194 days.
**Evidence:** _PM stated 'Let's add the email after password modification to the to-do list' (email10_msg3, 2025-07-03T10:45:00), but no subsequent message in the th_

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 62%]
> A client CSV export request forwarded on 2025-06-25 has received no decision or follow-up after the BA asked Gábor for a scheduling assessment, leaving the feature request unresolved for 199 days.
**Evidence:** _Eszter Varga (BA) asked on 2025-06-25T14:05: 'Gábor, what do you think, does it fit into the current schedule?' — no response from Gábor or any other _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 62%]
> A client CSV export request forwarded on 2025-06-25 received only a feasibility acknowledgment from the BA and a question directed at Gábor, with no decision, assignment, or resolution recorded in 199 days.
**Evidence:** _Eszter Varga (BA) wrote on 2025-06-25T14:05: 'It's technically feasible, but we need to assess the development effort. Gábor, what do you think, does _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 35%]
> Anna's unanswered clarification question about whether the 'Add to Cart' button change requires a color swap or just size/bold formatting remains unresolved in this thread, though the overall project context is 221 days old and the item may be stale or handled elsewhere.
**Evidence:** _email14_msg1: 'Does the client want a different color instead of the current green, or just for it to be larger/bold? This isn't clear.' — No subseque_

**[DivatKirály]** Uncontrolled Scope Change — [Unvalidated, confidence: 55%]
> A BA introduced a new 'NEW badge' UI requirement mid-sprint with no engineering response or formal scope decision recorded in the thread.
**Evidence:** _anna.nagy@kisjozsitech.hu wrote: 'A "nice to have" requirement came up: products uploaded in the last 30 days should have a small "NEW" badge on their_

---

## Recommended Director Actions

1. **[DivatKirály — Fwd: Re: DivatKirály - User registration process]** Confirm with Zsófia Varga immediately whether the newsletter checkbox fix has been deployed to production; verify that only the newsletter checkbox was changed (not Terms and Conditions); request a test confirmation from Eszter Horváth to close the loop with the client, given the GDPR compliance risk and the near-miss scope error.
2. **[Project Phoenix — Project Phoenix - New Login Page Specification]** Direct Zsuzsa (varga.zsuzsa@kisjozsitech.hu) to immediately confirm: (1) the minimum password length requirement from Gábor's open question, and (2) explicit team sign-off on the remaining spec points. Escalate to Péter (kovacs.peter@kisjozsitech.hu) as the senior stakeholder who issued the coordination request, and ensure a formal spec approval is recorded before any further login page development proceeds.
3. **[Project Phoenix — Project Phoenix - Staging Environment Anomaly]** Direct the Engineering Director to immediately follow up with horvath.gabor@kisjozsitech.hu for a status update on the filename-space bug fix; if no fix has been committed, assign a senior developer to review and resolve the image upload logic within the current sprint, and verify the fix is deployed and tested on staging before closing the issue.
4. **[DivatKirály — Fwd: Request regarding report export]** Identify who 'Gábor' is (likely a Tech Lead or Engineering Manager on DivatKirály) and obtain an immediate scheduling decision on the CSV export feature; if the feature has already been scoped or delivered outside this thread, close the flag with documentation, otherwise add it to the backlog with a committed sprint target and notify the client via Zoltán Kiss.
5. **[DivatKirály — DivatKirály - Weekly status and development progre]** Direct Péter Kovács to halt scheduling of the SKU search work until a formal change request is signed by the client, including effort estimate (~0.5 backend day + testing per Gábor in email18_msg3), impact on timeline, and any cost implications; verbal 'we'll do it' (email18_msg4) is insufficient change governance for a project in active delivery.
6. **[DivatKirály — Small request: "New" label on the product page]** Direct the tech lead or a senior developer to provide a quick effort estimate for the 'NEW' badge feature, then make an explicit backlog/sprint decision: either schedule it, defer it to a future release, or formally close it as out of scope — and communicate the outcome to Anna Nagy to close the loop.

---

⚠️ **AI-GENERATED REPORT** — Validate flagged items with responsible PMs before acting.
Generated by QBR Portfolio Health Analyzer v2.2 | Model: claude-sonnet-4-6
Run date: 2026-03-13 13:48