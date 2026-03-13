# QBR Portfolio Health Analyzer

Automated QBR (Quarterly Business Review) preparation system for a Director of Engineering. Ingests project email threads, detects delivery risks, and generates a structured Portfolio Health Report.

See [Blueprint.md](Blueprint.md) for the full architectural design document.

---

## What It Does

Analyzes raw project email `.txt` files and produces a Markdown report surfacing:

- **Stalled Decisions** — questions or tasks open for ≥ 5 business days without a substantive response
- **Uncontrolled Scope Changes** — new requirements introduced informally without logging or estimation
- **Operational Incidents** — production issues or client-impact events

The pipeline runs in four stages:

| Stage | What it does | LLM? |
|-------|-------------|------|
| A — Rule Engine | Detects flag candidates using deterministic rules | No |
| B — LLM Validator | Confirms or rejects each candidate, assesses severity | Yes |
| C — Cross-Thread Analyzer | Finds systemic patterns across multiple threads | Yes |
| D — Report Generator | Produces the final Markdown report | Yes |

---

## Quick Start

### Requirements

- Python 3.10+
- `anthropic` package (for live LLM calls): `pip install anthropic`

> **Windows users:** The pipeline uses Unicode characters in its output (✓, →). Run with `python -X utf8` to avoid encoding errors on Windows terminals:
> ```
> python -X utf8 analyzer.py ../../input/AI_Developer_files --mock
> ```
> On macOS/Linux the flag is not needed.

### Run in mock mode (no API key required)

```bash
cd solution/src
python analyzer.py ../../input/AI_Developer_files --mock
```

> ⚠️ **Analyzing historical data?** The reference date defaults to the last day of the *current* quarter. If running against past data (e.g., the provided Q2 2025 sample), set `ANALYSIS_REFERENCE_DATE=2025-07-31` in `.env` — otherwise "days open" calculations will be inflated by the gap between then and now.

Output: `solution/output/sample-report.md`

### Run with live LLM calls (claude-sonnet-4-6)

1. Copy `.env.example` to `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

2. Run:
   ```bash
   cd solution/src
   python analyzer.py ../../input/AI_Developer_files
   ```

The analyzer auto-detects `.env` in the parent directory. If no API key is found, it falls back to mock mode automatically.

---

## Input Format

Place email `.txt` files and `Colleagues.txt` in the same directory. Both RFC-style and parenthetical header formats are supported:

**Format A (RFC-style):**
```
From: István Nagy <nagy.istvan@kisjozsitech.hu>
Date: Mon, 02 Jun 2025 10:30:00 +0200
Subject: Project Phoenix - Login Page
```

**Format B (Parenthetical):**
```
From: Gábor Nagy (gabor.nagy@kisjozsitech.hu)
Date: 2025.06.09 10:15
Subject: DivatKirály - Weekly Status
```

Multiple messages per file are supported (standard email thread format).

---

## AI Models

| Model | Used for | Why |
|-------|----------|-----|
| `claude-sonnet-4-6` | Stages B, C, D (validation, pattern analysis, report) | Best structured JSON output, strong multilingual reasoning |
| `gpt-5-nano` | Noise filter micro-classifier (Stage 1b) | Minimal cost for short binary classification prompts |

Both configurable via `.env`. The pipeline is provider-agnostic at the interface level — swapping models requires only an `.env` change.

**Mock mode** uses rule-based heuristics instead of LLM calls. Useful for testing the pipeline without API credits. Note: mock mode produces more false positives than the live LLM version — this is expected behavior.

---

## Output

The report at `output/sample-report.md` contains:

- **Executive Summary** — portfolio health in 2–3 sentences
- **🔴 Immediate Attention Required** — HIGH severity open flags
- **🟡 Monitor Closely** — MEDIUM/LOW open flags
- **🟢 On Track** — projects with no open flags
- **Incidents This Quarter** — all FLAG 3 entries (open and resolved)
- **Cross-Project Patterns** — systemic issues spanning multiple threads
- **🔵 Needs PM Review** — low-confidence flags awaiting validation
- **Recommended Director Actions** — numbered, specific, actionable

Every flag includes a confidence label: `[Rule+LLM-confirmed]`, `[LLM-confirmed]`, or `[Needs PM Review]`.

---

## Project Structure

```
(repo root)/
├── input/
│   └── AI_Developer_files/   # Provided email .txt files + Colleagues.txt
└── solution/
    ├── Blueprint.md              # Architectural design document
    ├── README.md                 # This file
    ├── .env.example              # Environment variable template
    ├── src/
    │   ├── analyzer.py           # Main entry point
    │   ├── email_parser.py       # Ingestion & preprocessing (Stage 1)
    │   ├── ai_classifier.py      # Rule engine + LLM validator (Stages A-C)
    │   └── report_generator.py   # Report generation (Stage D)
    ├── mock_data/
    │   └── jira_mock.json        # Mock Jira tickets for future Option B integration
    └── output/
        ├── sample-report.md      # Generated report (from sample run)
        └── run-log.json          # Machine-readable run record
```

---

## Architecture Notes

**Why hybrid rules + LLM?** The rule engine (Stage A) reduces LLM calls by ~80% at scale with a representative corpus. The LLM only processes candidates already detected by rules — it never invents flags from scratch. With the provided 18-email sample — intentionally dense with flaggable content — Stage B call rates will be higher than this figure.

**Why temperature = 0?** All LLM stages run at temperature 0 for fully deterministic output. This makes the golden test set reliable and PM validation consistent across runs.

**Bilingual support:** Hungarian and English scope/resolution signals are handled. Stage B prompts include explicit instructions for mixed-language threads.

**Project detection:** Thread-to-project mapping uses subject line patterns first, then participant email lookup against `Colleagues.txt` team groupings as fallback.

**Jira integration (mock_data):** `jira_mock.json` is a design artifact only — it is not read by the current PoC implementation. It contains realistic Jira tickets aligned with the email data to illustrate the data structure that Option B would consume. Implementing live Jira API ingestion (Option B architecture) requires `JIRA_BASE_URL` and `JIRA_API_TOKEN` in `.env`.

---

## Limitations of the PoC

As documented in the Blueprint:

- Continuous mode (real-time monitoring) is not implemented — batch only
- Prompt versioning strategy is not implemented
- Data retention / GDPR deletion policy is not implemented
- RAG vector store uses in-memory simplified approach (Stage C groups per project)
- `acknowledged_items.json` suppression mechanism is not implemented in this version
- Project-to-team mapping from `Colleagues.txt` uses positional group ordering calibrated for the provided sample data — a production implementation would require a configurable mapping

- The text-based pipeline produces a higher proportion of low-confidence items than a structured-source implementation would. In production, this is addressed by integrating a structured source of truth (Option B — Jira as primary input).

These are explicitly flagged as production readiness gaps, not oversights.
