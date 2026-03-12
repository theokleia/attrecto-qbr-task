# QBR Portfolio Health Report
**Period:** Q2 2025  
**Generated:** 2026-03-12 19:38  
**Projects Reviewed:** 2 | **Open Flags:** 14 | **Needs Review:** 0

---

## Executive Summary

Portfolio review for Q2 2025 identified 14 open flags across 2 projects. Project Phoenix, DivatKirály require immediate attention due to high-severity open issues. 0 items are pending PM validation before the QBR.

---

## 🔴 Immediate Attention Required

### Project Phoenix

**Stalled Decision** — `HIGH` [LLM-confirmed]
> Open question unresolved for 38 business days: Are the other points okay?
**Evidence:** _Are the other points okay?_
**Days open:** 38 business days
**Owner:** varga.zsuzsa@kisjozsitech.hu
**Action:** Follow up with varga.zsuzsa@kisjozsitech.hu on this open question before the QBR.

**Stalled Decision** — `HIGH` [LLM-confirmed]
> Open question unresolved for 23 business days: Gábor is looking into the profile picture bug, right?
**Evidence:** _Gábor is looking into the profile picture bug, right?_
**Days open:** 23 business days
**Owner:** kiss.anna@kisjozsitech.hu
**Action:** Follow up with kiss.anna@kisjozsitech.hu on this open question before the QBR.

**Stalled Decision** — `HIGH` [LLM-confirmed]
> Open question unresolved for 23 business days: Can I add this to the shared documentation?
**Evidence:** _Can I add this to the shared documentation?_
**Days open:** 23 business days
**Owner:** horvath.gabor@kisjozsitech.hu
**Action:** Follow up with horvath.gabor@kisjozsitech.hu on this open question before the QBR.

**Uncontrolled Scope Change** — `MEDIUM` [LLM-confirmed]
> Potential untracked scope change in Project Phoenix: Implementing this will require extra effort, as our current user management syst
**Evidence:** _Implementing this will require extra effort, as our current user management system doesn't support it natively; we'd need to pull in and configure a separate library. This wasn't included in the estim_
**Owner:** nagy.istván@kisjozsitech.hu
**Action:** Verify whether this change was formally logged and estimated.

### DivatKirály

**Stalled Decision** — `HIGH` [LLM-confirmed]
> Open question unresolved for 26 business days: Gábor, what do you think, does it fit into the current schedule?
**Evidence:** _Gábor, what do you think, does it fit into the current schedule?_
**Days open:** 26 business days
**Owner:** eszter.varga@kisjozsitech.hu
**Action:** Follow up with eszter.varga@kisjozsitech.hu on this open question before the QBR.

**Stalled Decision** — `HIGH` [LLM-confirmed]
> Open question unresolved for 33 business days: How big of a task would this be?
**Evidence:** _How big of a task would this be?_
**Days open:** 33 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Follow up with anna.nagy@kisjozsitech.hu on this open question before the QBR.

**Stalled Decision** — `HIGH` [LLM-confirmed]
> Open question unresolved for 33 business days: Could we fit it into the current sprint if it's not a huge effort?
**Evidence:** _Could we fit it into the current sprint if it's not a huge effort?_
**Days open:** 33 business days
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Follow up with anna.nagy@kisjozsitech.hu on this open question before the QBR.

**Uncontrolled Scope Change** — `MEDIUM` [LLM-confirmed]
> Potential untracked scope change in DivatKirály: Hi everyone,
A "nice to have" requirement came up: products uploaded in the last
**Evidence:** _Hi everyone,
A "nice to have" requirement came up: products uploaded in the last 30 days should have a small "NEW" badge on their image on both the listing page and the product detail page._
**Owner:** anna.nagy@kisjozsitech.hu
**Action:** Verify whether this change was formally logged and estimated.

**Uncontrolled Scope Change** — `MEDIUM` [LLM-confirmed]
> Potential untracked scope change in DivatKirály: Oh, and in last week's meeting, the client mentioned it would be good if the sea
**Evidence:** _Oh, and in last week's meeting, the client mentioned it would be good if the search worked not only for product names but also for item numbers (SKU). I forgot to mention this until now, sorry._
**Owner:** eszter.horvath@kisjozsitech.hu
**Action:** Verify whether this change was formally logged and estimated.

---

## Incidents This Quarter

**[Project Phoenix]** **URGENT: Client Feedback on Demo** — ✅ Resolved
> Production incident in Project Phoenix: URGENT: Client Feedback on Demo
_Hi all!
I just spoke with the client after yesterday's demo. They were very pleased with the progress, but had a few observations.
The images in the main slider are loading too slowly.
The "Contact" b_
**Action:** Verify root cause was addressed and a post-mortem action item is tracked.

**[DivatKirály]** **User Profile Page - Data Modification Flow** — 🔴 Open
> Production incident in DivatKirály: User Profile Page - Data Modification Flow
_Hi everyone,
On the profile page, should we send a confirmation email to the user after a password change? The specification doesn't mention it, but it would be useful from a security perspective.
Tha_
**Action:** Review incident — confirm resolution path and assign owner.

**[DivatKirály]** **Fwd: Request regarding report export** — 🔴 Open
> Production incident in DivatKirály: Fwd: Request regarding report export
_Hi everyone,
Forwarding the client's request. They would like to be able to download monthly reports not only in PDF but also in CSV format. Can we implement this in the next sprint?
Thanks,
Zoli
--- _
**Action:** Review incident — confirm resolution path and assign owner.

**[DivatKirály]** **Re: DivatKirály webshop - Homepage design feedback** — 🔴 Open
> Production incident in DivatKirály: Re: DivatKirály webshop - Homepage design feedback
_Hi everyone,
Thanks Anna. Eszter, please ask about the button color.
What's more urgent though: they also complained about the logo size. Bence, could you enlarge it by 15% in the header and check if _
**Action:** Review incident — confirm resolution path and assign owner.

**[DivatKirály]** **DivatKirály - Payment Gateway API Integration** — 🔴 Open
> Production incident in DivatKirály: DivatKirály - Payment Gateway API Integration
_Hi Péter,
Sorry, urgent server maintenance took up my time last week, this task got a bit sidelined. My question about the callback is still open, I can't proceed without it.
Gábor_
**Action:** Review incident — confirm resolution path and assign owner.

**[DivatKirály]** **Fwd: Re: DivatKirály - User registration process** — 🔴 Open
> Production incident in DivatKirály: Fwd: Re: DivatKirály - User registration process
_Hi everyone,
Sorry to write here, but this is urgent. The client indicated that due to GDPR, the newsletter subscription checkbox cannot be checked by default. It currently is. Please fix it.
Thanks,
_
**Action:** Review incident — confirm resolution path and assign owner.

**[DivatKirály]** **URGENT: Client cannot log in!** — ✅ Resolved
> Production incident in DivatKirály: URGENT: Client cannot log in!
_Hi Gábor,
The client just called, no one in the company has been able to log into the system since yesterday's update. Please look into it immediately, there's a lot of panic!
Thanks,
Zoli_
**Action:** Verify root cause was addressed and a post-mortem action item is tracked.

---

## Cross-Project Patterns

**[DivatKirály] RECURRING_BLOCKER** — `MEDIUM`
> anna.nagy@kisjozsitech.hu appears as unresponsive owner in 2 stalled threads in DivatKirály.
**Threads:** email16, email16, email16
**Action:** Discuss workload or communication issues with anna.nagy@kisjozsitech.hu before the QBR.

---

## Recommended Director Actions

1. **[Project Phoenix — Project Phoenix - New Login Page Specification]** Follow up with varga.zsuzsa@kisjozsitech.hu on this open question before the QBR.
2. **[Project Phoenix — RE: Project Phoenix - New Login Page Specification]** Follow up with kiss.anna@kisjozsitech.hu on this open question before the QBR.
3. **[Project Phoenix — RE: FW: Question about CI/CD Pipeline]** Follow up with horvath.gabor@kisjozsitech.hu on this open question before the QBR.
4. **[DivatKirály — User Profile Page - Data Modification Flow]** Review incident — confirm resolution path and assign owner.
5. **[DivatKirály — Fwd: Request regarding report export]** Follow up with eszter.varga@kisjozsitech.hu on this open question before the QBR.
6. **[DivatKirály — Fwd: Request regarding report export]** Review incident — confirm resolution path and assign owner.
7. **[DivatKirály — Re: DivatKirály webshop - Homepage design feedback]** Review incident — confirm resolution path and assign owner.
8. **[DivatKirály — DivatKirály - Payment Gateway API Integration]** Review incident — confirm resolution path and assign owner.
9. **[DivatKirály — Small request: "New" label on the product page]** Follow up with anna.nagy@kisjozsitech.hu on this open question before the QBR.
10. **[DivatKirály — Fwd: Re: DivatKirály - User registration process]** Review incident — confirm resolution path and assign owner.
11. **[Project Phoenix — Project Phoenix - New Login Page Specification]** Verify whether this change was formally logged and estimated.
12. **[DivatKirály — Small request: "New" label on the product page]** Verify whether this change was formally logged and estimated.

---

⚠️ **AI-GENERATED REPORT** — Validate flagged items with responsible PMs before acting.
Generated by QBR Portfolio Health Analyzer | Model: claude-sonnet-4-6
Run date: 2026-03-12 19:38