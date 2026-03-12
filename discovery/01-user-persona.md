# User Persona: The Director of Engineering

**Date:** 2026-03-12
**Based on:** Task brief + email data analysis + industry knowledge of DoE role

---

## Who They Are

**Name (fictional):** Dávid Molnár
**Role:** Director of Engineering
**Company type:** Mid-size software development agency — 30–150 engineers, 5–15 active client projects at any given time
**Reports to:** CTO or CEO
**Direct reports:** Project Managers, Tech Leads (2–6 people)

---

## Responsibilities

- Overseeing technical delivery across all active client projects simultaneously
- Ensuring teams have what they need to deliver on time and within scope
- Identifying and resolving risks before they escalate to client complaints
- Preparing and presenting quarterly performance reviews to senior leadership
- Making staffing decisions: who gets allocated where, when to hire, when to escalate
- Maintaining client relationships at the executive level when things go wrong
- Continuously improving delivery processes across teams

---

## The QBR Context

The Quarterly Business Review is a recurring meeting where the DoE presents project portfolio health to the CEO, CFO, and/or key clients. The stakes are high:

- A missed risk that surfaces in the QBR without prior warning is embarrassing
- A production incident that wasn't escalated properly can cost client relationships
- An undetected compliance violation (like a pre-checked GDPR checkbox) can have legal consequences
- Good news is expected to be brief; problems require root cause and remediation plan

**Preparation time available:** 2–4 hours the day before. Sometimes less.

---

## Current Situation (Without the System)

The DoE currently prepares the QBR by:
1. Asking PMs to send status update emails
2. Scanning Jira manually for overdue items
3. Chasing down team leads for verbal updates
4. Relying on memory and scattered notes

**What gets missed:**
- Issues that were "handled" in email but never entered into Jira
- Patterns that span multiple projects (nobody owns the cross-project view)
- Compliance or legal signals buried in routine thread replies
- Decisions that were requested but never made — sitting unanswered in email

---

## Pain Points

| Pain | Severity | Evidence from data |
|------|----------|-------------------|
| Information is scattered across email, Jira, Slack, verbal conversations | Critical | Issues like the GDPR violation and the CI/CD blocker lived only in email |
| Manual QBR prep is time-consuming and error-prone | High | No automated aggregation exists |
| No cross-project view — each PM only sees their own project | High | Spec gaps, wrong-thread messages appear in all 3 projects simultaneously |
| Client-reported issues arrive through too many hops | High | Client emails team member directly → no ticket → no visibility |
| Can't tell what's truly urgent vs. what's noise | Medium | 14% of email content is off-topic (lunch, birthdays) |
| No early warning for compliance/legal issues | Critical | GDPR violation was caught by the client, not internally |

---

## Goals

**Primary:** Walk into the QBR fully prepared — no surprises, no "I didn't know about that."

**Secondary:**
- Spend less than 30 minutes reviewing the pre-generated report before the meeting
- Have specific data to back up decisions ("Project X is at risk because...")
- Identify systemic issues across projects, not just per-project firefighting
- Trust that the report catches what matters and filters out noise

---

## How They Consume Reports

- **Format:** Executive summary first, details available on demand — not walls of text
- **Time:** Skims in 10–15 minutes, digs into flagged items only
- **Device:** Desktop or large monitor — this is a work artifact, not a mobile view
- **Frequency:** Quarterly for formal QBR, but would welcome a weekly digest version
- **Action-oriented:** Every flagged item should suggest a next action or owner, not just describe the problem

---

## What "Good" Looks Like

> *"I opened the report, saw three red flags at the top, understood what each one was and why it mattered, and knew exactly what to do before the meeting started."*

A good QBR report for this persona:
- Takes under 20 minutes to review
- Has an executive summary with no more than 5 flagged items
- Separates "act now" from "watch this" from "context only"
- Links everything back to a Jira ticket or email thread as evidence
- Highlights cross-project patterns, not just per-project lists
- Is automatically generated — requires minimal manual input (PM confirms uncertain flags before the meeting, not during it)

---

## What They Do NOT Want

- A dump of every email or Jira ticket
- Issues they already know about without context on resolution
- False alarms (noise flagged as risk)
- A tool that requires them to configure or maintain it weekly
- Anything that requires reading more than one screen to get the key message

---

## Current Process Context

*Assumed state of their development and support workflows, based on the email data analysis and typical practices at a mid-size dev agency.*

### Development Process (SDLC)

The team follows an **agile/sprint-based workflow** with Jira as the primary project management tool. Sprints are visible in Jira but sprint planning and retrospectives are informal enough that scope changes (e.g., SSO, CSV export, SKU search) get discovered mid-sprint rather than caught in planning. This is evidenced by late-stage feature requests appearing in email threads across all three projects.

Specs arrive via Zeplin (design handoff) and are shared as mockup links in email. There is no formal spec review gate — developers begin implementation based on the mockup and flag gaps reactively, often in email, not in Jira.

**Tools in current use:**
| Phase | Tool | Evidence |
|-------|------|----------|
| Project management | Jira | Referenced in email threads |
| Design handoff | Zeplin | V3 mockup update mentioned in thread |
| Code / version control | GitHub (implied) | Referenced in CI/CD context |
| Deployment | CI/CD pipeline (custom or Jenkins/GitHub Actions) | 8 threads reference pipeline |
| Testing | Staging environment | Staging issues appear in 3 threads |
| Payment processing | Barion API | DivatKirály payment gateway thread |
| Communication | Email (primary async channel) | All 18 thread files |

**Gaps in current tooling:**
- No dedicated support/helpdesk system — clients email team members directly
- No automated incident creation from CI/CD failures or payment gateway errors
- No design-to-Jira trigger — Zeplin changes are communicated via email, not tracked as tickets

### Bug Reporting and Tracking

There is no standardized bug reporting path. The email data shows:
- Clients reporting bugs directly to PMs or Account Managers (login outage report to Zoltán Kiss)
- Bugs discovered internally during development but logged informally in email rather than as Jira tickets
- The GDPR checkbox violation was caught by the client, not during internal QA

This creates a three-tier visibility gap:
1. **Client-reported bugs**: Enter the system only if someone manually creates a ticket
2. **Dev-discovered bugs**: Sometimes in Jira, sometimes discussed in email and forgotten
3. **Production incidents**: Handled reactively, no automated detection or alerting

### Fix Verification and Client Communication

Fix verification appears to happen manually — a developer signals completion in email, a PM follows up with the client, and client confirmation is sought via the same email thread. There is no formal SLA tracking or automated notification when a fix is deployed.

Urgent client communications (e.g., production outages) escalate through personal email chains, creating a situation where the DoE has no visibility unless CC'd on the right thread at the right time.

### Prior Automation Experience

Based on the email data evidence and typical agency profile: **limited automation, not zero**. The team has CI/CD pipelines in place (a non-trivial automation investment), but the pipelines are fragile (one bad env var caused a production outage, and only one developer understood how to fix it). This suggests CI/CD was set up but not hardened or documented.

There is no evidence of AI tooling in use for any part of the development, QA, or communication workflow. The team relies on manual human judgment for issue prioritization and QBR preparation.
