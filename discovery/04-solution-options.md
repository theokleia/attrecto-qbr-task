# Solution Options: QBR Portfolio Health Analyzer

**Date:** March 2026
**Purpose:** Comparative analysis of architectural approaches considered during discovery. Documents the reasoning behind the PoC implementation choice and outlines the recommended path for a production system.

---

## Context

The core problem is the same across all options: a Director of Engineering spends 2–4 hours manually preparing a QBR that should take 20 minutes to review. The options differ in **what data they use** and **how reliably they can detect and validate issues**.

The task brief explicitly required analysis of project email `.txt` files — this determined Option A as the PoC implementation. Option D (establishing Jira as a reliable single source of truth) represents the recommended long-term architectural investment — it fixes the root cause that Options A, B, and C all work around. Once Option D is in place, Option C becomes the natural reporting layer.

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

## Option B: Extraction-First Email Architecture *(Email-Based Production Approach)*

**How it works:** Before any analysis, each email is processed by an LLM to extract a structured representation: questions asked, decisions pending, action items assigned, scope references, incidents, named participants, dates, and resolution signals. Downstream analysis — flag detection, staleness calculation, cross-thread pattern matching — operates on this clean structured JSON rather than raw email text.

```
raw email → LLM extraction → structured JSON per email
                                        │
                          deterministic rule engine
                          (staleness, scope signals,
                           incident patterns)
                                        │
                              LLM cross-thread analysis
                                        │
                                    report
```

| | |
|---|---|
| **Data source** | Project email threads |
| **Integration required** | None — same file input as Option A |
| **Setup complexity** | Low — same deployment as Option A |
| **Deployment** | Standalone script or scheduled job |

**Pros:**
- Cleaner separation of concerns: LLM does understanding, rules do analysis, each layer is independently testable
- Better recall on non-English content — Hungarian "megnézem" vs "megoldva" is handled in context, not via keyword lists
- Better precision on scope signals — "while I'm in there" is classified correctly only when surrounding context is a change request
- Simpler validation logic — instead of validating a heuristic candidate, Stage B aggregates pre-extracted structured data
- Extraction schema is explicit and auditable — the system's "understanding" of each email is visible and correctable

**Cons:**
- Higher LLM cost — every email is processed, not just rule-detected candidates; at 3,000 emails per quarter this is meaningful (mitigated by using a smaller extraction model, Haiku-class)
- Extraction errors become upstream errors — a missed question in extraction means it never gets flagged; requires a golden test set at the extraction layer
- Schema design is critical and non-trivial — the extraction schema determines what the system can and cannot detect; changing it requires re-extracting historical data
- Same data completeness ceiling as Option A — email still captures only a partial picture of project reality

**Best for:** Organisations where email is the primary communication channel and a Jira integration is not feasible. The correct email-native production architecture when Option A's hybrid heuristics are not precise enough.

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

Option D is not a replacement for Options B or C — it addresses a different layer of the problem. Options A and B both have the same data completeness ceiling: they can only surface what exists in email. Option D raises that ceiling by ensuring decisions and blockers are recorded in a structured system before analysis begins. Option C integrates that structured data directly. Whether Option B or C is the right reporting layer — and whether automation or process discipline is the right path to data completeness — should be grounded in a proper discovery conversation with the client.

**Best for:** Organisations where poor Jira hygiene is the primary pain point — important decisions are routinely made in meetings or email and never formally recorded. If the client's Jira is already well-maintained, the marginal value of Option D is lower and jumping directly to Option B is the right move.

---

## Future Vision: Conversational Interface *(Requires Option C)*

**"What are the riskiest things in DivatKirály right now?"**

The analytical engine in Options B and C produces structured data at every stage. That structured output can power a conversational interface where the Director asks natural language questions about their portfolio instead of reading a static report.

This is the logical end state — not a replacement for the QBR report, but an always-on intelligence layer the Director can query between quarters.

**Why this requires Option C, not Options A or B:**

A conversational interface is only as useful as the data behind it. Options A and B are both email-based — they give the Director incomplete, inferred, and potentially stale information. Telling a Director "this decision appears stalled based on email thread patterns" is useful in a quarterly report. Having them ask "is the payment gateway issue resolved?" and receiving an uncertain, email-inferred answer is not useful — it erodes trust faster than it builds it.

With Jira integrated as the backbone (Option C), every answer is grounded in authoritative, real-time data. The conversational layer becomes a genuine productivity tool, not a sophisticated approximation.

**Architecture note:** The pipeline already produces structured JSON at every stage (Stages A–C). Adding a conversational layer requires changes only to the presentation layer — not to the analytical engine. The groundwork is in place.

---

## Decision for This PoC

**Option A** was implemented because the task brief explicitly specified email `.txt` file analysis as the input. The architecture was designed to be source-agnostic so that Options B and C can be built on the same analytical foundation — adding Jira or additional sources requires new ingestion parsers, not changes to Stages A–D.

The mock Jira data (`mock_data/jira_mock.json`) is included to demonstrate what Option C multi-source integration would look like and to validate that the data structures are compatible.

**Option D** was not in scope for this engagement, which was explicitly defined as a QBR reporting tool. However, it represents the recommended long-term architectural investment: fixing Jira completeness at the source rather than compensating for it in the reporting layer. If the client's primary pain point is "we can never trust Jira because half the decisions happen in email," Option D is the correct intervention — Option B or C alone will not solve it.
