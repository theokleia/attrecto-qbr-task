# Problem Framing

**Date:** 2026-03-12

---

## The Stated Problem

> *"Analyze a collection of project emails and generate a concise, high-signal report that tells the Director exactly where to focus their limited attention."*

This is what the task asks for. It is not wrong — but it is incomplete.

---

## The Real Problem

**The Director of Engineering does not have an email problem. They have a visibility problem.**

Email is one symptom of a deeper issue: critical project information is fragmented across multiple systems, and no single view exists that aggregates it into an actionable picture. The DoE cannot see what they cannot find, and what they cannot find is often what matters most.

The email data provided illustrates this perfectly:

| What happened | Where it lived | Did the DoE see it in time? |
|--------------|----------------|----------------------------|
| GDPR compliance violation (newsletter pre-checked) | Email thread | No — the client found it first |
| Developer blocked 30+ days on CI/CD | Email thread | Unclear — PM had to follow up twice |
| Production login outage (env var in deploy script) | Email thread | Only after the client panicked |
| Scope creep: SSO, CSV export, SKU search | Email threads | Only when team members happened to escalate |
| Design handoff update (Zeplin V3 mockup) | Wrong-thread message | Lost entirely — no response |

None of these were tracked in Jira. All of them were consequential. **The problem is not that the emails are hard to read — it is that the entire pipeline from "issue exists" to "manager knows" is broken.**

---

## Why Email-Only Is the Wrong Foundation

Treating email as the primary data source for a QBR system has three fundamental weaknesses:

**1. Email captures what people chose to write, not what actually happened.**
Jira captures every ticket, comment, status change, and assignment — regardless of whether someone felt like sending an email about it. Email is biased toward the communicative and the urgent; it systematically underrepresents routine progress and quiet failures.

**2. Email is noisy by design.**
14% of the messages in the provided dataset are completely off-topic. A production-grade system based on email classification will always fight this noise floor. Jira has no equivalent noise problem — every entry is intentionally project-related.

**3. Email has no ground truth.**
There is no way to know from email alone whether an issue was resolved. A Jira ticket has a status. An email thread just ends — and "it stopped being discussed" does not mean "it was fixed."

---

## The Meta-Problem: Email Is a Process Failure Signal

Here is the insight that reframes the entire solution:

**When important project decisions live in email instead of Jira, that is not a data source — that is evidence of a broken process.**

In a healthy software development team:
- Bugs are filed as Jira tickets before they are discussed in email
- Client feedback is captured in Jira before the team responds
- Blockers are escalated in Jira, not through multi-week email chains
- Compliance issues are linked to Jira tickets with legal notes attached

The fact that the CI/CD blocker lasted 30 days in an email thread, or that the GDPR violation was discovered by the client rather than flagged internally, tells us something damning: **the team is not using Jira as intended**. The email layer is filling the gap that proper process would eliminate.

This means a smart system should do two things:
1. Use Jira as the primary data source (where the managed work lives)
2. Use email as an exception detector (to catch what slipped past Jira)

And it should flag the pattern itself: *"3 of your projects have recurring compliance issues that appear only in email. This is a process problem, not a project problem."*

---

## The Support Layer Gap

A mature software development company has a third layer between "client reports issue" and "Jira ticket exists":

```
Client → support@company.com → Support system (Zendesk / Jira Service Management)
                                        ↓
                               Triage → Dev ticket in Jira
```

In the provided email data, clients are emailing team members directly. This means:
- No auto-ticket creation
- No SLA tracking
- No visibility for the DoE unless they are CC'd
- Resolution time is unmeasured

The **absence of a support system** is itself a finding that belongs in the QBR. A Director of Engineering seeing this pattern should ask: *"Why are our clients emailing developers directly instead of going through a support channel?"*

---

## Redefining the Problem

The real problem the system should solve is not:

> ❌ "Summarize the emails so the DoE doesn't have to read them."

It is:

> ✅ "Give the DoE a unified, accurate, noise-free view of portfolio health — using Jira as the ground truth, email as the exception detector, and support tickets as the client satisfaction layer — so they can walk into any QBR fully prepared without manual data collection."

---

## What Success Looks Like

The system is successful when:

1. The DoE can prepare for a QBR in under 30 minutes using only the generated report
2. No critical issue is missed because it only existed in an email thread
3. Cross-project patterns are surfaced automatically — without anyone having to compile them manually
4. The report is trusted — the DoE acts on its recommendations without needing to verify them independently
5. Over time, the patterns flagged in the report lead to process improvements that reduce the number of exceptions
