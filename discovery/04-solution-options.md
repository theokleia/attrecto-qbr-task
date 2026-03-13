# Solution Options: QBR Portfolio Health Analyzer

**Date:** March 2026
**Purpose:** Comparative analysis of architectural approaches considered during discovery. Documents the reasoning behind the PoC implementation choice and outlines the recommended path for a production system.

---

## Context

The core problem is the same across all options: a Director of Engineering spends 2–4 hours manually preparing a QBR that should take 20 minutes to review. The options differ in **what data they use** and **how reliably they can detect and validate issues**.

The task brief explicitly required analysis of project email `.txt` files — this determined Option A as the PoC implementation. Option D (email-driven Jira population) represents the recommended long-term architectural investment — it fixes the root cause that Options A, B, and C all work around. Once Option D is in place, Option B becomes the natural reporting layer, evolving to Option C at scale.

---

## Option A: Email-Only Analysis *(Current PoC Implementation)*

**How it works:** The system reads email thread `.txt` files, applies a rule engine to detect flag candidates (stalled decisions, scope changes, incidents), then uses an LLM to validate and contextualize them. Output: a structured Markdown report.

| | |
|---|---|
| **Data source** | Project email threads only |
| **Integration required** | None — files are the input |
| **Setup complexity** | Minimal — copy files, run script |
| **Deployment** | Standalone Python script |

**Pros:**
- Zero external dependencies — works with just email exports
- Lowest friction for initial adoption (no API credentials, no Jira access needed)
- Directly addresses the task brief requirement
- Demonstrates the full analytical pipeline (rules → LLM → cross-thread → report)
- Good foundation: the pipeline architecture is data-source agnostic

**Cons:**
- Email captures only 30–40% of real project communication
- Resolution status is inferred, not confirmed — an issue "resolved in email" may still be open in Jira
- No ground truth: the system cannot verify whether a flagged decision was actually made
- Cross-project patterns are limited to what surfaces in email threads
- Not suitable for continuous/real-time alerting without significant additional work

**Best for:** PoC, proof of concept, demo, or organisations with no Jira/ticketing system.

---

## Option B: Jira-First + Email as Exception Layer *(Recommended for Production)*

**How it works:** Jira is the authoritative data source. The system pulls ticket status, sprint data, and issue history via the Jira API. Email analysis runs in parallel as an **exception detector** — surfacing issues that exist only in email and never made it into a ticket. The two sources are cross-referenced: a flag found in email is validated against Jira before surfacing to the Director.

| | |
|---|---|
| **Data source** | Jira (primary) + email threads (exception layer) |
| **Integration required** | Jira API credentials (`JIRA_BASE_URL`, `JIRA_API_TOKEN`) |
| **Setup complexity** | Moderate — API setup per client instance |
| **Deployment** | Scheduled job or event-driven pipeline |

**Pros:**
- Jira is already where engineers work — no behavioral change required from the team
- Resolution status is confirmed, not inferred — "closed" means closed
- Dramatically reduces false positives: email flags cross-referenced against ticket state
- Supports continuous operation naturally (Jira webhooks or polling)
- Detects the most critical failure mode: **issues that exist only in email, never ticketed**
- Higher Director confidence — every flag has a Jira ticket or a documented absence of one

**Cons:**
- Requires Jira API access per client (onboarding effort)
- Jira data quality depends on team discipline — unmaintained boards produce noise
- Does not capture communication outside Jira and email (Slack, verbal, standup notes)
- Jira-only analysis misses the semantic content: *why* something is stalled, not just *that* it is

**Best for:** Production deployment at software agencies already using Jira as their primary project management tool (which is the majority).

---

## Option C: Multi-Source Intelligence *(Enterprise / Long-Term Vision)*

**How it works:** All project communication channels feed into a unified ingestion layer. Jira provides structured ticket data; email provides async context; Git commit history provides delivery cadence signals; Slack (or Teams) provides real-time team dynamics; support/helpdesk systems provide client-reported issues. Each source has its own parser; the analytical engine is unchanged.

| | |
|---|---|
| **Data source** | Jira + Email + Git + Slack/Teams + Support system |
| **Integration required** | API access for each source |
| **Setup complexity** | High — multiple integrations per client |
| **Deployment** | Continuous event-driven pipeline with persistent state |

**Pros:**
- Complete picture: nothing slips through because it lives in only one channel
- Detects systemic issues invisible in any single source (e.g., Slack discussion → no Jira ticket → no email → production incident)
- Enables the highest-confidence flag detection and the richest Director context
- Natural foundation for the conversational interface (see Future Vision below)
- Cross-project pattern detection becomes significantly more reliable

**Cons:**
- High integration overhead — each new source requires parser + auth setup
- Data privacy complexity increases significantly (Slack messages, Git history)
- Requires dedicated engineering effort to build and maintain
- Client onboarding is substantially more complex

**Best for:** Large agencies or enterprise clients with mature tooling, engineering capacity, and a need for portfolio-level risk visibility across 10+ concurrent projects.

---

## Option D: Jira as Single Source of Truth *(The Root Cause Fix)*

**The core idea:** Options A, B, and C all treat Jira incompleteness as a given and work around it. Option D reframes the problem entirely: **establish Jira as the single, authoritative source of truth for project status — and build reporting on top of that foundation.**

This is a strategic recommendation, not a specific technical solution. The mechanism for achieving Jira completeness can vary:

- **Process discipline:** Daily standups with a mandatory rule that every decision, blocker, or scope change raised verbally or by email is entered into Jira before the meeting ends. No automation required — just a culture change enforced by the PM.
- **AI-assisted automation:** The system monitors the inbox and proposes Jira tickets for human approval when an email contains a decision, issue, or scope change. A reviewer approves or rejects the draft before it is written to Jira.
- **Hybrid:** Process discipline as the primary mechanism, automation as a safety net that catches what slips through.

The specific path depends on the organisation's maturity, tooling, and appetite for change. What matters is the outcome: **every significant project event lives in Jira, not scattered across email threads.**

| | |
|---|---|
| **Goal** | Jira reflects complete project reality — not just what was manually ticketed |
| **Mechanism** | Process change, AI automation, or hybrid — chosen per client context |
| **Integration required** | Jira API write access (if automation path chosen) |
| **Setup complexity** | Low (process only) to High (full automation with review workflow) |
| **Deployment** | Ongoing discipline or continuous monitor, depending on approach |

**Pros:**
- Fixes the root cause rather than working around it — Jira incompleteness is eliminated at the source
- Once Jira is complete, Options B and C become dramatically more reliable — they report from ground truth, not inference
- Eliminates "ghost issues" — decisions and problems that existed only in email threads and were never visible to the Director
- The process-discipline path requires zero technical investment and can start immediately
- The automation path scales without requiring behavioural change from the team

**Cons:**
- Process discipline requires sustained management commitment — without enforcement it regresses quickly
- AI automation carries misclassification risk — writing a wrong ticket to Jira is harder to undo than a wrong line in a report
- Ticket routing logic is non-trivial regardless of mechanism: which project? what issue type? who is the assignee?
- Requires explicit client sign-off before AI writes to their production Jira
- Does not replace Options B or C for QBR reporting — it enables them to work correctly

**Relationship to Options B and C:**

Option D is not a replacement for Options B or C — it addresses a different layer of the problem. Options B and C are reporting tools; Option D is about data quality. A reporting tool built on complete Jira data is inherently more reliable than one compensating for its absence. Whether Option B or C is the right reporting layer — and whether automation or process discipline is the right path to Jira completeness — should be grounded in a proper discovery conversation with the client. The actual pain points, team maturity, and appetite for change determine which combination makes sense.

**Best for:** Organisations where poor Jira hygiene is the primary pain point — important decisions are routinely made in meetings or email and never formally recorded. If the client's Jira is already well-maintained, the marginal value of Option D is lower and jumping directly to Option B is the right move.

---

## Future Vision: Conversational Interface *(Requires Option B or C)*

**"What are the riskiest things in DivatKirály right now?"**

The analytical engine in Options B and C produces structured data at every stage. That structured output can power a conversational interface where the Director asks natural language questions about their portfolio instead of reading a static report.

This is the logical end state — not a replacement for the QBR report, but an always-on intelligence layer the Director can query between quarters.

**Why this requires Option B or C, not Option A:**

A conversational interface is only as useful as the data behind it. Email-only analysis gives the Director incomplete, inferred, and potentially stale information. Telling a Director "this decision appears stalled based on email thread patterns" is useful in a quarterly report. Having them ask "is the payment gateway issue resolved?" and receiving an uncertain, email-inferred answer is not useful — it erodes trust faster than it builds it.

With Jira as the backbone (Option B) or full multi-source (Option C), every answer is grounded in authoritative, real-time data. The conversational layer becomes a genuine productivity tool, not a sophisticated approximation.

**Architecture note:** The pipeline already produces structured JSON at every stage (Stages A–C). Adding a conversational layer requires changes only to the presentation layer — not to the analytical engine. The groundwork is in place.

---

## Decision for This PoC

**Option A** was implemented because the task brief explicitly specified email `.txt` file analysis as the input. The architecture was designed to be source-agnostic so that Options B and C can be built on the same analytical foundation — adding Jira or additional sources requires new ingestion parsers, not changes to Stages A–D.

The mock Jira data (`mock_data/jira_mock.json`) is included to demonstrate what Option B cross-referencing would look like and to validate that the data structures are compatible.

**Option D** was not in scope for this engagement, which was explicitly defined as a QBR reporting tool. However, it represents the recommended long-term architectural investment: fixing Jira completeness at the source rather than compensating for it in the reporting layer. If the client's primary pain point is "we can never trust Jira because half the decisions happen in email," Option D is the correct intervention — Option B or C alone will not solve it.
