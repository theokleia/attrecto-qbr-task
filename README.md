# QBR Portfolio Health Analyzer

**Candidate:** Tekla
**Task:** AI Developer Assessment — QBR Automation System
**Date:** March 2026

---

## My Approach

When I received this task, my first instinct was to question whether the stated requirement was actually the right thing to build.

The brief asks for a system that mines project emails to generate a QBR health report. Reading the emails and the requirements, it became clear the problem lies deeper: **Jira is incomplete**: decisions are made in email threads and never ticketed, so the Director cannot trust the project management tool that should be the source of truth. An email-mining QBR tool compensates for that gap. It does not fix it.

Before writing a line of code, I spent time mapping out the full solution landscape:

- **Option A (what was asked):** Email-only analysis — low friction, zero dependencies, directly addresses the brief. ✅ Implemented as the PoC.
- **Option B (reporting layer):** Jira-first + email as exception layer — confirms resolution status from authoritative data, dramatically reduces false positives.
- **Option C (enterprise path):** Multi-source intelligence — Jira + email + Git + Slack, full portfolio visibility.
- **Option D (where I'd start the engagement — discovery determines the path forward):** Establish Jira as the single source of truth for project status. The mechanism is secondary — it could be process discipline (decisions made in email or meetings get ticketed before end of day), AI-assisted automation (inbox monitoring that proposes Jira tickets for human approval), or a hybrid. The goal is a reliable data foundation; what gets built on top of it depends on what discovery reveals.

The deliberation and reasoning behind each option is documented in [`discovery/04-solution-options.md`](discovery/04-solution-options.md).

**My decision:** I implemented Option A as specified, because the task brief was explicit and a PoC that demonstrates the analytical engine has real value regardless of the data source. The architecture is deliberately source-agnostic — plugging in Jira as a data source requires new ingestion parsers, not changes to the analytical engine.

**My honest position:** If this were a real client engagement, I would start the conversation with Option D — not to prescribe it before listening, but because I would want to validate whether Jira incompleteness is actually the primary pain point before writing any reporting code. What comes next depends entirely on what discovery reveals: if the data foundation is the core problem, that is where effort should go first; if the pain lies elsewhere, the direction changes. Option A is a valid PoC that demonstrates the analytical engine works regardless of the data source; it is not the architecture I would recommend for production without that discovery conversation first.

---

## What This Repo Contains

```
├── discovery/               # BA discovery work — done before any code
│   ├── 01-user-persona.md       # Director of Engineering persona
│   ├── 02-problem-framing.md    # Root cause analysis, meta-problem definition
│   ├── 03-discovery-questions.md  # 42 discovery questions with assumed answers
│   ├── 04-solution-options.md   # Options A–D comparison + architectural decision
│   └── analysis/
│       └── email-analysis.py    # Input data analysis — KPIs and statistics on the 18 email files
│
└── solution/                # The implemented PoC (Option A) — see solution/README.md for setup and usage
    ├── README.md                # Technical setup and usage guide
    ├── Blueprint.md             # Full system architecture (v2.2)
    ├── src/
    │   ├── email_parser.py      # Ingestion — parses .txt files into structured threads
    │   ├── ai_classifier.py     # Noise filter + Stages A (rules), B (LLM), C (patterns)
    │   ├── report_generator.py  # Stage D — renders the Markdown QBR report
    │   └── analyzer.py          # Entry point — wires the pipeline, CLI interface
    ├── mock_data/
    │   └── jira_mock.json       # Mock Jira data — demonstrates Option B data structure
    ├── output/
    │   ├── sample-report.md     # Live run output against the 18 provided email files
    │   ├── run-log.json         # Machine-readable run record
    │   └── filtered_noise.json  # Threads excluded by noise filter (never discarded)
    └── .env.example             # Required environment variables
```

---

## Discovery Documents

The discovery folder documents the analytical work done before implementation. It is a deliverable in its own right — not background notes.

| File | What it contains |
|------|-----------------|
| `01-user-persona.md` | Who the system is for and what they actually need |
| `02-problem-framing.md` | Why the stated problem is a symptom of a deeper one |
| `03-discovery-questions.md` | over 40 questions across user, data, delivery, integration, and AI readiness dimensions — each with an assumed answer and its impact on the solution design |
| `04-solution-options.md` | Full architectural comparison of Options A–D, including the recommended production path and the root-cause fix (Option D) |
