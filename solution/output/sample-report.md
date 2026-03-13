# QBR Portfolio Health Report
**Period:** Q2 2025  
**Generated:** 2026-03-13 14:11  
**Projects Reviewed:** 2 | **Open Flags:** 8 | **Needs Review:** 7

---

## Executive Summary

DivatKirály is the portfolio's primary risk concentration, carrying an open GDPR violation (pre-checked newsletter checkbox, unresolved since June 2025), an uncontrolled scope change accepted without formal change control (SKU-based search), and three stalled decisions spanning up to 206 days — including an untracked password-change notification that represents a live security gap. Project Phoenix is stable by comparison but carries two medium-severity stalls: a login spec with unresolved sign-off after 211 days and a confirmed image-upload bug unaddressed for over 9 months. The single most critical concern is the DivatKirály GDPR checkbox issue: confirm with Zsófia Varga today whether the fix is live in production, as this is an active compliance liability, not a backlog item.

---

## 🔴 Immediate Attention Required

### DivatKirály

**Stalled Decision** — `MEDIUM` [LLM-confirmed]
> A security-relevant decision to send confirmation emails after password changes was informally agreed upon in July 2025 but never formally resolved, assigned, or tracked — it has been open for 194 days with no follow-up.
**Evidence:** _PM Gábor Nagy wrote on 2025-07-03: 'Let's add the email after password modification to the to-do list.' — this is a deferral to a backlog item, not a confirmed decision or implementation. No subsequen_
**Days open:** 194 business days
**Owner:** gabor.nagy@kisjozsitech.hu
**Action:** Direct Gábor Nagy (PM) to confirm whether the confirmation-email-after-password-change feature was formally added to the backlog and implemented. If not, escalate as a security gap: password change notifications are a standard security control and the absence of a formal decision or implementation record after 194 days represents both a delivery and a compliance risk on the DivatKirály project.

**Stalled Decision** — `MEDIUM` [Rule+LLM-confirmed]
> A client-requested CSV export feature for DivatKirály has had no scheduling decision for 199 days after Eszter Varga directed the question to Gábor with no recorded response.
**Evidence:** _eszter.varga@kisjozsitech.hu wrote on 2025-06-25T14:05:00: 'Gábor, what do you think, does it fit into the current schedule?' — this direct scheduling question to Gábor has received no reply in the th_
**Days open:** 199 business days
**Owner:** eszter.varga@kisjozsitech.hu
**Action:** Identify who 'Gábor' is (likely a Tech Lead or Engineering Manager on DivatKirály) and obtain an immediate scheduling decision on the CSV export feature; if the feature has already been scoped or delivered outside this thread, close the flag with documentation, otherwise add it to the backlog with a committed sprint target and notify the client via Zoltán Kiss.

**Uncontrolled Scope Change** — `MEDIUM` [Rule+LLM-confirmed]
> A new SKU-based search requirement surfaced informally via the Client Relationship Manager a week after the client meeting, was not in the original specification, and has been accepted into scope without a formal change control decision on timeline or cost impact.
**Evidence:** _Eszter Horvath (email18_msg1): 'in last week's meeting, the client mentioned it would be good if the search worked not only for product names but also for item numbers (SKU). I forgot to mention this _
**Owner:** peter.kovacs@kisjozsitech.hu
**Action:** Direct the PM (Péter Kovacs) to immediately initiate a formal change request for the 'Extend search by SKU' requirement: document the scope delta, obtain written client approval, assess impact on the current sprint and delivery timeline, and confirm whether this constitutes a billable extra. Verify that the JIRA ticket (requested by Anna Nagy) has been created and linked to a change log before Gábor begins implementation next week.

**Stalled Decision** — `LOW` [LLM-confirmed]
> A 'nice to have' feature request for a 'NEW' badge on product pages was raised on 2025-06-16 with an explicit sizing/prioritization question, and has received zero responses in 206 days.
**Evidence:** _Anna Nagy asked on 2025-06-16: 'How big of a task would this be? Could we fit it into the current sprint if it's not a huge effort?' — no reply, estimate, or prioritization decision is present anywher_
**Days open:** 206 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Direct the engineering lead to provide a quick effort estimate (story points or hours) for the 'NEW' badge feature, then have the product owner formally accept, defer to backlog, or close it as out-of-scope — the decision has been pending 206 days and should be resolved in the next sprint planning session to avoid continued backlog ambiguity.

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
> A confirmed bug in the image upload logic — where filenames containing spaces cause a 404 on the frontend — was identified by a Senior Developer on 2025-06-29, acknowledged by the responsible Junior Developer on 2025-06-30, but no resolution or fix has been confirmed in the thread as of today (2026-03-31), leaving the issue open for over 9 months.
**Evidence:** _nagy.istvan: 'it only happens if the image name contains spaces. The system renames it, but the frontend somehow requests the old, space-containing name from the API, which returns a 404. This isn't a_
**Days open:** 211 business days
**Owner:** horvath.gabor@kisjozsitech.hu
**Action:** Immediately follow up with horvath.gabor@kisjozsitech.hu to confirm whether the filename-space bug in the image upload logic was ever fixed; if not, assign a tracked ticket with a deadline and request nagy.istvan@kisjozsitech.hu to verify the fix on staging before closing, given this issue has been unresolved for over 9 months.

---

## Incidents This Quarter

**[DivatKirály]** **Fwd: Re: DivatKirály - User registration process** — 🔴 Open
> A GDPR-violating pre-checked newsletter subscription checkbox was flagged by the client on 2025-06-26 and remains unresolved as of the last message, with a developer also proposing an incorrect scope of fix that had to be stopped by the BA.
_Client email (2025-06-26 14:55): 'the newsletter subscription is automatically checked during registration. According to GDPR, this must be unchecked by default.' Eszter escalated urgently at 15:03. Z_
**Action:** Confirm with Zsófia Varga immediately whether the newsletter checkbox fix has been deployed to production; verify that only the newsletter checkbox was changed (not Terms and Conditions); request a test confirmation from Eszter Horváth to close the loop with the client, given the GDPR compliance risk and the near-miss scope error.

---

## Cross-Project Patterns

**[Project Phoenix] SYSTEMIC_PROCESS_FAILURE** — `HIGH`
> At least two distinct technical decisions or bug fixes have been acknowledged but left without formal resolution or follow-up for extended periods (211+ days and 9+ months respectively), indicating a systemic failure to close open action items on Project Phoenix.
**Threads:** email1, email4
**Evidence:**
  - `email1`: Zsuzsa resolved the Google SSO scope question on 2025-06-09 but left minimum password length (Gábor's point 3.2 query) and explicit team confirmation of remaining spec points unanswered, with no follow-up recorded in 211 days.
  - `email4`: A confirmed bug in the image upload logic (filenames with spaces causing a 404) was identified on 2025-06-29 and acknowledged on 2025-06-30, but no resolution or fix has been confirmed in over 9 months as of 2026-03-31.
**Action:** The Director should institute a mandatory open-item closure process for Project Phoenix: require owners (varga.zsuzsa@kisjozsitech.hu for email1, horvath.gabor@kisjozsitech.hu for email4) to provide written resolution status within 5 business days, and introduce a recurring review cadence (e.g., bi-weekly) to surface and formally close any stalled decisions or unresolved bugs before they age further.

**[DivatKirály] RECURRING_BLOCKER** — `HIGH`
> Gábor Nagy is a silent bottleneck across multiple threads: decisions routed to him in email11 received no recorded response, and he owns an unresolved security decision in email10 that has been open for 194 days.
**Threads:** email10, email11
**Evidence:**
  - `email10`: A security-relevant decision (confirmation emails after password changes) was informally agreed upon in July 2025 and is owned by gabor.nagy@kisjozsitech.hu with no follow-up in 194 days.
  - `email11`: Eszter Varga directed the CSV export scheduling question to Gábor with no recorded response in 199 days — Gábor is the implicit decision-maker who has not acted.
**Action:** The Director should directly engage Gábor Nagy to audit all open action items assigned to or routed through him, establish a response SLA, and determine whether he is under-resourced or whether decisions are being informally blocked at his level.

**[DivatKirály] SYSTEMIC_PROCESS_FAILURE** — `HIGH`
> Multiple client-facing requests — a CSV export feature (email11), a 'NEW' badge on product pages (email16), and an untracked SKU-based search requirement (email18) — have entered the project informally with no formal scheduling, change control, or resolution, indicating a systemic failure to capture and govern client requests.
**Threads:** email11, email16, email18
**Evidence:**
  - `email11`: A client-requested CSV export feature has had no scheduling decision for 199 days after being raised, with no formal tracking initiated.
  - `email16`: A client feature request for a 'NEW' badge on product pages was raised on 2025-06-16 with an explicit prioritization question and has received zero responses or decisions in 206 days.
  - `email18`: A new SKU-based search requirement surfaced informally via the Client Relationship Manager, was not in the original specification, and was accepted into scope without any formal change control decision on timeline or cost impact.
**Action:** The Director should mandate a single formal intake process for all client requests, require that every request receives a logged triage decision within a defined SLA, and conduct an immediate audit to formally accept, reject, or defer the three outstanding requests identified here.

**[DivatKirály] IMPLICIT_COMMITMENT** — `HIGH`
> Two separate security- and compliance-critical issues — an unresolved password-change confirmation email (email10) and an unresolved GDPR-violating pre-checked newsletter checkbox (email17) — have been acknowledged but never formally resolved, creating implicit commitments with legal and reputational exposure.
**Threads:** email10, email17
**Evidence:**
  - `email10`: A security-relevant decision to send confirmation emails after password changes was informally agreed upon in July 2025 but never formally assigned or tracked, remaining open for 194 days.
  - `email17`: A GDPR-violating pre-checked newsletter subscription checkbox was flagged by the client on 2025-06-26 and remains unresolved, with a developer also proposing an incorrect fix scope that had to be stopped by the BA — indicating the issue is active but ungoverned.
**Action:** The Director should treat both items as urgent compliance risks, assign a named owner with a hard deadline for each, and ensure legal or DPO review is obtained for the GDPR issue before the next client-facing release.

---

## 🔵 Needs PM Review

_The items below were detected by the rule engine but could not be confirmed with high confidence. Please review with the relevant PM before the QBR._

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 55%]
> The minimum password length requirement for the Project Phoenix login page was raised 216 days ago and has never received a documented answer in this thread, leaving a potential security-relevant specification gap unresolved.
**Evidence:** _horvath.gabor@kisjozsitech.hu wrote on 2025-06-02T10:15: 'I don't see any mention of the minimum password length. Should it be 8 characters, like in o_

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 62%]
> JIRA-112 (profile picture bug) was acknowledged as being investigated by Gábor on 2025-06-30, but no resolution has been recorded in this thread across 196 days, and the responsible party never responded directly.
**Evidence:** _Péter confirms 'Yes, Gábor is looking into it' (email3_msg1, 2025-06-30T10:05), which is an acknowledgment-only signal. No message from Gábor appears _

**[Project Phoenix]** Stalled Decision — [Unvalidated, confidence: 55%]
> A confirmed bug in the image upload logic (filenames with spaces causing 404s) was re-surfaced on 2025-06-29 and attributed to Gábor's commit, but the thread ends with only an acknowledgment from Gábor on 2025-06-30 and no documented resolution over the following 9 months.
**Evidence:** _nagy.istvan: 'This isn't a cache issue; it's a bug in the image upload logic. Gábor, didn't your last commit touch this part?' — horvath.gabor: 'Yes, _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 62%]
> A client CSV export request forwarded on 2025-06-25 has received no decision or follow-up after the BA asked Gábor for a scheduling assessment, leaving the feature request unresolved for 199 days.
**Evidence:** _Eszter Varga (BA) asked on 2025-06-25T14:05: 'Gábor, what do you think, does it fit into the current schedule?' — no response from Gábor or any other _

**[DivatKirály]** Stalled Decision — [Unvalidated, confidence: 45%]
> Anna's clarification question about the 'Add to Cart' button (color change vs. size/bold) was never answered in the thread, leaving that specific design decision open, though the higher-priority logo issue was resolved.
**Evidence:** _email14_msg1: 'Does the client want a different color instead of the current green, or just for it to be larger/bold? This isn't clear.' — email14_msg_

**[DivatKirály]** Uncontrolled Scope Change — [Unvalidated, confidence: 45%]
> A BA has proposed a 'nice to have' NEW badge feature mid-sprint but no acceptance or scope commitment has been recorded yet, leaving the risk potential but unconfirmed.
**Evidence:** _anna.nagy@kisjozsitech.hu wrote: 'A "nice to have" requirement came up: products uploaded in the last 30 days should have a small "NEW" badge on their_

---

## Recommended Director Actions

1. **[DivatKirály — Fwd: Re: DivatKirály - User registration process]** Confirm with Zsófia Varga immediately whether the newsletter checkbox fix has been deployed to production; verify that only the newsletter checkbox was changed (not Terms and Conditions); request a test confirmation from Eszter Horváth to close the loop with the client, given the GDPR compliance risk and the near-miss scope error.
2. **[Project Phoenix — Project Phoenix - New Login Page Specification]** Direct Zsuzsa (varga.zsuzsa@kisjozsitech.hu) to immediately follow up with the team to: (1) confirm the minimum password length requirement for point 3.2 as raised by Gábor, and (2) obtain explicit sign-off from all reviewers that the remaining spec points are accepted. Péter (kovacs.peter@kisjozsitech.hu) should be looped in as the apparent decision authority to formally close the specification before any further development proceeds on the login page.
3. **[Project Phoenix — Project Phoenix - Staging Environment Anomaly]** Immediately follow up with horvath.gabor@kisjozsitech.hu to confirm whether the filename-space bug in the image upload logic was ever fixed; if not, assign a tracked ticket with a deadline and request nagy.istvan@kisjozsitech.hu to verify the fix on staging before closing, given this issue has been unresolved for over 9 months.
4. **[DivatKirály — User Profile Page - Data Modification Flow]** Direct Gábor Nagy (PM) to confirm whether the confirmation-email-after-password-change feature was formally added to the backlog and implemented. If not, escalate as a security gap: password change notifications are a standard security control and the absence of a formal decision or implementation record after 194 days represents both a delivery and a compliance risk on the DivatKirály project.
5. **[DivatKirály — Fwd: Request regarding report export]** Identify who 'Gábor' is (likely a Tech Lead or Engineering Manager on DivatKirály) and obtain an immediate scheduling decision on the CSV export feature; if the feature has already been scoped or delivered outside this thread, close the flag with documentation, otherwise add it to the backlog with a committed sprint target and notify the client via Zoltán Kiss.
6. **[DivatKirály — DivatKirály - Weekly status and development progre]** Direct the PM (Péter Kovacs) to immediately initiate a formal change request for the 'Extend search by SKU' requirement: document the scope delta, obtain written client approval, assess impact on the current sprint and delivery timeline, and confirm whether this constitutes a billable extra. Verify that the JIRA ticket (requested by Anna Nagy) has been created and linked to a change log before Gábor begins implementation next week.
7. **[DivatKirály — Small request: "New" label on the product page]** Direct the engineering lead to provide a quick effort estimate (story points or hours) for the 'NEW' badge feature, then have the product owner formally accept, defer to backlog, or close it as out-of-scope — the decision has been pending 206 days and should be resolved in the next sprint planning session to avoid continued backlog ambiguity.

---

⚠️ **AI-GENERATED REPORT** — Validate flagged items with responsible PMs before acting.
Generated by QBR Portfolio Health Analyzer v2.2 | Model: claude-sonnet-4-6
Run date: 2026-03-13 14:11