# QBR Portfolio Health Analyzer — System Blueprint

**Author:** Tekla
**Version:** 2.2
**Date:** March 2026  
**Artifact type:** Architectural Blueprint + PoC Design

> **v2.1 Change Summary:** Six substantive amendments from a second adversarial cross-review (March 2026): (1) PII scanning architecture corrected — email addresses in structured header metadata are no longer redacted, only body-text occurrences; (2) `is_substantive_response_to()` redesigned as a two-stage heuristic with LLM sub-call fallback, explicitly acknowledged as the hardest function in the system; (3) SCOPE_SIGNALS list extended to bilingual EN/HU with co-occurrence guard to reduce false positive rate; (4) Failure Mode Matrix added covering every pipeline stage; (5) Low-confidence routing path added — gray-zone LLM outputs route to a "Needs PM Review" queue rather than being silently suppressed or blindly reported; (6) Known-issue acknowledgment mechanism added so the Director can suppress recurring known items. Secondary fixes: Assumptions confidence values corrected; Stage D temperature set to 0; PM incentive misalignment in validation layer acknowledged; PoC scope explicitly defined; strategic observations forward-referenced in Executive Summary; batch/continuous state management gap honestly acknowledged; prompt versioning and data retention gaps noted.

> **v2.2 Change Summary:** Five production-readiness improvements: (1) Pipeline Observability section added — structured stage-boundary logging and `run-log.json` run record now part of the design; (2) Continuous mode gap strengthened — Temporal, Restate, and Celery named explicitly as recommended workflow orchestrators; (3) Redis named as the production state backend for acknowledged items, thread state, and run history; (4) Data Residency Option added to Section 1.4 — Stages B, C, and D can be redirected to a local vLLM/Ollama endpoint via three environment variables, addressing contractual restrictions on sending client emails to third-party AI providers; (5) Proactive concurrency cap added to Stage B — `MAX_CONCURRENT_LLM_CALLS` limits simultaneous LLM requests for large corpora.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Framing — A BA Perspective](#problem-framing)
3. [Assumptions & Constraints Log](#assumptions--constraints-log)
4. [PoC Scope Definition](#poc-scope-definition)
5. [System Architecture Overview](#system-architecture-overview)
6. [Section 1 — Data Ingestion & Initial Processing](#section-1--data-ingestion--initial-processing)
7. [Section 2 — The Analytical Engine (Multi-Step AI Logic)](#section-2--the-analytical-engine-multi-step-ai-logic)
8. [Section 3 — Cost & Robustness Considerations](#section-3--cost--robustness-considerations)
9. [Section 4 — Monitoring & Trust](#section-4--monitoring--trust)
10. [Section 5 — Architectural Risk & Mitigation](#section-5--architectural-risk--mitigation)
11. [Out-of-Scope Notes (Strategic Observations)](#out-of-scope-notes-strategic-observations)

---

## Executive Summary

This blueprint describes an AI-powered **Portfolio Health Analyzer** designed to assist a Director of Engineering in preparing for Quarterly Business Reviews (QBRs). The system ingests raw project email communications, applies a multi-step hybrid analytical pipeline to surface high-signal risks and unresolved issues, and generates a prioritized "Portfolio Health Report."

The core value proposition is **noise reduction**: transforming hundreds of email threads into a focused, actionable set of attention flags that tell the Director exactly where to direct limited time and attention before a high-stakes review.

**Architectural philosophy:** The stated task is a QBR preparation tool, but a sound architecture should not artificially constrain the system to a quarterly batch model when the underlying problem — surfacing risks before they compound — is inherently continuous. The analytical engine is stateless and event-compatible at the email-processing level, which means it is compatible with both batch and continuous operation. However, full continuous mode requires meaningful orchestration-layer infrastructure (message queues, persistent state, real-time deduplication) that is not included in this PoC. The PoC implements batch mode only; the continuous evolution path is documented honestly in Section 5.2.

**Core design principle:** Deterministic rule logic identifies flag candidates. LLM reasoning validates, contextualizes, and prioritizes those candidates. AI should never do what a rule can do reliably — it should do what rules cannot.

**Strategic context:** Three observations about the system's broader context are documented in the [Out-of-Scope Notes](#out-of-scope-notes-strategic-observations) at the end of this document: the batch/continuous evolution path, email as a weak but architecturally expandable signal source, and the conversational interface as the likely end state. These are not afterthoughts — they reflect deliberate architectural decisions made throughout this document.

---

## Problem Framing

*Before designing a solution, a business analyst must interrogate the problem itself. The assumptions documented here would normally be confirmed with the client; they are stated explicitly here to demonstrate analytical rigor.*

### What the System Is Solving

The stated request is: *"analyze project emails and generate a QBR-ready portfolio health report."*

The underlying problem is: *A Director of Engineering cannot manually synthesize hundreds of asynchronous communication threads across multiple projects before a high-stakes quarterly meeting. Critical risks, stalled decisions, production incidents, and unresolved blockers are buried in email noise — they surface too late, or not at all.*

### What the System Is NOT

This system is **not** a project management tool. It does not replace Jira, Slack, or direct team communication. It is a **signal extraction layer** sitting on top of existing communication artifacts.

### Key Observations from the Provided Data

Before finalizing the architecture, I analyzed all 18 provided email threads. Several observations directly shaped the design:

**1. Multiple projects, multiple team structures.** The data contains at least three distinct projects (Project Phoenix, a second platform project, and a DivatKirály webshop project). Each has its own PM, BA, developers, and account manager. Identity resolution across projects is non-trivial.

**2. Name/email disambiguation is a real data quality problem.** The name "Péter Kovács" appears with *two different email addresses*: `kovacs.peter@kisjozsitech.hu` (PM on Project Phoenix) and `peter.kovacs@kisjozsitech.hu` (Senior Developer on DivatKirály). These are plausibly two different people. A system that conflates display names will produce incorrect risk attributions. Email address is the only reliable canonical identifier.

**3. Noise emails are deliberate test cases — requiring nuanced handling.** Multiple threads contain off-topic messages within otherwise project-relevant threads: a misdirected restaurant reservation (email2), a birthday surprise (email8), a team lunch debate (email13). The system cannot discard entire threads — it must filter individual off-topic messages while preserving the project context of the thread.

**4. Not all issues that look open are actually open.** Email 9 shows a production outage resolved within 24 minutes in the same thread. Email 4 shows a staging bug reported, apparently dropped, then re-surfaced and resolved. Thread-level temporal analysis is essential to avoid false positives.

**5. Some risks are subtle and require reasoning, not pattern matching.** Email 17 shows a developer deciding to also uncheck the Terms & Conditions checkbox while fixing a GDPR issue — an unauthorized scope expansion stopped by the BA ("STOP!"). No keyword match would detect this. It requires understanding the semantic difference between what was requested and what was proposed.

**6. Scope changes enter via informal channels as a systemic pattern.** Email 18: SKU search requirement relayed verbally. Email 1: Google SSO in a "final" specification without estimation. Email 16: "NEW" badge as a "nice to have" mid-sprint. This reflects how software organizations actually operate.

**7. Unresolved requests at quarter-end represent real delivery risk.** Email 11: a client CSV export request forwarded but never assigned, estimated, accepted, or rejected.

**8. Spec-vs-implementation conflicts cause silent delays.** Email 15: Barion payment API specified POST callbacks; actual endpoint returns GET. Blocked a developer for two weeks.

**9. Cross-thread patterns are invisible to single-thread analysis.** The export issue in email 11 appears as a single forwarded request. Prior client mentions in other threads would together indicate an implicit commitment approaching a deadline — invisible to any single-thread system.

---

## Assumptions & Constraints Log

*Explicit assumptions are the mark of a professional analyst. All of these would be confirmed with the client in a real engagement. Confidence values reflect the probability that the assumption holds reliably in production — not the importance of the assumption.*

| # | Assumption | Risk if Wrong | Confidence |
|---|-----------|--------------|------------|
| A1 | Email address is the canonical unique identifier for a person | Identity mis-attribution across projects | **Medium** — collisions are common in real orgs (two "Péter Kovács"); the system handles this but it is not guaranteed to be error-free |
| A2 | A "quarter" is a standard calendar quarter (Q1=Jan-Mar, etc.) | Wrong time window for analysis | Medium |
| A3 | Stalled threshold default = 5 business days; **must be configurable per organization** | Over/under-flagging for teams with different response norms | Medium |
| A4 | Emails are UTF-8 encoded; content is mixed EN/HU language | Parser failures on Hungarian characters (ő, ú, á, etc.) | **Medium** — this is a known active risk requiring explicit mitigation, not a safe assumption |
| A5 | The Director receives the report directly, not filtered through intermediate management | Wrong tone/depth/scope in output | Medium |
| A6 | Project emails **may** contain sensitive content including credentials, customer data, and PII | GDPR violation; LLM API data exposure | **High — active mitigation required at every stage** |
| A7 | The PoC operates on batch files, not a live email server integration | Architecture mismatch for production | Known limitation, stated explicitly |
| A8 | Emails within a single .txt file belong to a single project-level thread grouping | Cross-contamination of analysis | High |
| A9 | The Colleagues.txt directory is authoritative but not necessarily complete | Role inference failures for unlisted participants (clients, new hires, vendors) | Medium — directory is primary source; inference is labeled fallback |
| A10 | Prompt content is version-controlled alongside code | Undetected regression when prompts are changed | **Low confidence — this is a gap, not an assumption; see Section 4.5** |

---

## PoC Scope Definition

*A blueprint without an explicit PoC boundary creates evaluation risk — the reviewer may judge the PoC against the full production architecture. This section defines exactly what the PoC implements and what it deliberately defers.*

### What the PoC Implements

| Capability | Included in PoC |
|-----------|----------------|
| Email parser supporting both Format A (RFC angle-bracket) and Format B (parenthetical) | ✅ Yes |
| UTF-8 / Hungarian character handling | ✅ Yes |
| Identity resolution from Colleagues.txt directory | ✅ Yes |
| Tiered noise filter (L1 heuristic + L2 LLM micro-classifier) | ✅ Yes |
| Credential & PII scanner with body/header separation | ✅ Yes |
| Stage A: Deterministic rule engine for all three flag types | ✅ Yes |
| Stage B: LLM contextual validator with `is_substantive_response_to()` LLM sub-call | ✅ Yes |
| Stage C: Cross-thread pattern analysis (simplified in-memory, not full vector store) | ✅ Simplified |
| Low-confidence routing to "Needs PM Review" queue | ✅ Yes |
| Stage D: Portfolio report in Markdown format | ✅ Yes |
| PM validation routing / web UI | ❌ Not in PoC — simulated via JSON output |
| Full RAG vector store (Qdrant/pgvector) | ❌ Not in PoC — in-memory approximation |
| Known-issue acknowledgment persistence across runs | ❌ Not in PoC — JSON config file approach |
| Live email server integration | ❌ Not in PoC |
| Continuous / real-time operation mode | ❌ Not in PoC |
| Prompt version control system | ❌ Not in PoC — manual discipline required |

### What the PoC Produces

Given the 18 provided `.txt` email files, the PoC produces:
1. `sample-report.md` — Markdown QBR report formatted as defined in Stage D
2. `run-log.json` — machine-readable run record with stage-by-stage counts
3. `filtered_noise.json` — log of all threads excluded by the noise filter

---

## System Architecture Overview

### The Core Design Decision: Hybrid Rules + AI

The analytical engine uses a **hybrid architecture**: deterministic rule logic identifies candidates; LLM reasoning validates, contextualizes, and prioritizes them.

| Concern | Pure LLM approach | Hybrid rules + AI |
|---------|------------------|-------------------|
| Explainability | "The AI flagged it" | "Rule: question unanswered > 5 days. LLM confirmed: no resolution found, severity HIGH" |
| Reliability | Non-deterministic across calls | Rule triggers are deterministic; only severity assessment varies |
| Cost | LLM call for every thread | LLM called only for rule-confirmed candidates (~15% of threads) |
| Auditability | Hard to reproduce | Rule logic logged; LLM reasoning captured separately |

**The principle: AI should never do what a rule can reliably do. AI should do what rules cannot** — understand context, detect semantic risk patterns, synthesize narrative, and handle the cases where deterministic logic is insufficient.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          INPUT LAYER                                │
│  .txt email files ──► File Watcher / Scheduled Batch / API hook    │
│         [Supports both quarterly batch and continuous modes]        │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INGESTION & PREPROCESSING                        │
│                                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  Email Parser    │  │   Identity       │  │   Thread         │  │
│  │  (Format A + B,  │─►│   Resolver       │─►│   Reconstructor  │  │
│  │   date-agnostic, │  │  dir=primary,    │  │  (chronological, │  │
│  │   UTF-8 safe)    │  │  infer=fallback) │  │   project-scoped)│  │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
│                                                       │             │
│                          ┌────────────────────────────┘             │
│                          ▼                                          │
│           ┌───────────────────────────────────────┐                 │
│           │   Credential & PII Scanner            │                 │
│           │   BODY TEXT: redact PII/credentials   │ ← mandatory    │
│           │   HEADERS: preserve as clean metadata │   security     │
│           │   (email addresses in headers are      │   gate         │
│           │    NEVER redacted — they are the key) │                 │
│           └──────────────────┬────────────────────┘                 │
│                              ▼                                      │
│           ┌───────────────────────────────────────┐                 │
│           │   Tiered Noise Filter                 │                 │
│           │   L1: Heuristic (fast, no LLM cost)   │                 │
│           │   L2: LLM micro-classifier            │                 │
│           │       (ambiguous cases only)          │                 │
│           └──────────────────┬────────────────────┘                 │
└──────────────────────────────┼──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       ANALYTICAL ENGINE                             │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  STAGE A — Deterministic Rule Engine                         │  │
│  │  Output: typed candidates with timestamps, owners, ages      │  │
│  └──────────────────────────────┬───────────────────────────────┘  │
│                                 │                                   │
│  ┌──────────────────────────────▼───────────────────────────────┐  │
│  │  STAGE B — LLM Contextual Validator (per candidate)          │  │
│  │  ┌─────────────────────────────────────────────────────┐     │  │
│  │  │  HIGH confidence → confirmed flag                   │     │  │
│  │  │  LOW confidence  → "Needs PM Review" queue          │     │  │
│  │  │  FALSE POSITIVE  → discarded + logged               │     │  │
│  │  └─────────────────────────────────────────────────────┘     │  │
│  └──────────────────────────────┬───────────────────────────────┘  │
│                                 │                                   │
│  ┌──────────────────────────────▼───────────────────────────────┐  │
│  │  STAGE C — Cross-Thread Pattern Analyzer (per project)       │  │
│  │  RAG-based retrieval across all project threads              │  │
│  └──────────────────────────────┬───────────────────────────────┘  │
│                                 │                                   │
│  ┌──────────────────────────────▼───────────────────────────────┐  │
│  │  STAGE D — Portfolio Report Generator                        │  │
│  │  Acknowledged items filtered; "Needs PM Review" appended     │  │
│  └──────────────────────────────┬───────────────────────────────┘  │
└─────────────────────────────────┼───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          OUTPUT LAYER                               │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐  ┌─────────────┐  │
│  │ 🔴 Critical │  │ 🟡 Monitor  │  │🟢 On     │  │ 🔵 Needs    │  │
│  │   Flags     │  │   Flags     │  │  Track   │  │ PM Review   │  │
│  └─────────────┘  └─────────────┘  └──────────┘  └─────────────┘  │
│                                                                     │
│  Delivery: Markdown/PDF  |  Slack alert  |  Email digest           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Section 1 — Data Ingestion & Initial Processing

### 1.1 Format Heterogeneity

The provided emails use two distinct header formats that must both be handled:

**Format A — RFC-style:**
```
From: István Nagy <nagy.istvan@kisjozsitech.hu>
Date: Mon, 02 Jun 2025 10:30:00 +0200
```

**Format B — Parenthetical:**
```
From: Gábor Nagy (gabor.nagy@kisjozsitech.hu)
Date: 2025.06.09 10:15
```

Format B also uses `YYYY.MM.DD HH:MM` dates. The parser implements multi-format fallback: try RFC first, then parenthetical, then log as `PARSE_WARNING_UNKNOWN_FORMAT` rather than crashing. Hungarian characters (ő, ú, á, é, etc.) are preserved with explicit UTF-8 enforcement at every read/write boundary.

### 1.2 Identity Resolution: Directory-Primary, Inference-Fallback

**Tier 1 (Primary) — Directory lookup:** Colleagues.txt is the authoritative source for known team members. Email address → role and display name.

**Tier 2 (Fallback) — Contextual inference:** Participants not in the directory (external clients, new hires, vendors) receive an `[inferred]` role label from a lightweight LLM call. Inferred roles are never treated as ground truth.

**The Péter Kovács collision:** Two distinct people share this display name in the dataset. The system uses email address as the primary key and never merges on display name alone. All collisions are logged for human review.

**Why not directory-only:** The provided dataset already contains participants absent from Colleagues.txt (e.g., `bela.ugyfel@nagyker.hu`, `ugyfel@divatkiralynagyker.hu`). Real-world directories are always partially stale. Silent failures are worse than labeled uncertainty.

### 1.3 Scalable Ingestion

| Scale | Approach |
|-------|----------|
| PoC | Local `.txt` files, synchronous processing |
| Small production | Scheduled batch + shared folder |
| Medium production | Message queue (SQS/Service Bus) + worker pool |
| Large production | Kafka / Pub/Sub streaming |

### 1.4 Credential & PII Scanning — Mandatory Security Gate

**Critical architectural correction from v2.0:** The previous version included email addresses in the PII redaction pattern list. This was a logical error. Email addresses are the canonical unique identifier for every participant — redacting them from the data passed to the LLM would break identity resolution, cause `owner` fields in flag output to be null or hallucinated, and destroy cross-thread attribution.

**The correct architecture separates two data structures:**

```
┌─────────────────────────────────────────────────────────┐
│  STRUCTURED METADATA  (passed to LLM as-is, no redaction│
│  From:  nagy.istvan@kisjozsitech.hu                      │
│  To:    kovacs.peter@kisjozsitech.hu                     │
│  Date:  2025-06-02T10:30:00                              │
│  Subject: Project Phoenix - Login Page Specification     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  BODY TEXT  (PII/credential scan applied before LLM)    │
│  "Here's the Barion API key: [REDACTED_API_KEY]         │
│   Please contact [REDACTED_EMAIL] if you have issues."  │
│   DB string: [REDACTED_DB_CONNECTION]                   │
└─────────────────────────────────────────────────────────┘
```

The rule of thumb: email addresses in **header fields** are project identity data and must be preserved. Email addresses appearing in **body text** as customer contact information or third-party references are PII and must be redacted.

```python
BODY_SENSITIVE_PATTERNS = {
    # API keys and tokens — NOT email addresses in general
    "api_key_generic":  r"(?i)(api[_\-]?key|token|secret)[\"'\s:=]+[A-Za-z0-9_\-]{20,}",
    "bearer_token":     r"Bearer\s+[A-Za-z0-9\-._~+/]+=*",
    "db_connection":    r"(mysql|postgres|mongodb|redis):\/\/[^\s]+",
    "ip_address":       r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "hu_phone":         r"(\+36|06)[\s\-]?\d{2}[\s\-]?\d{3}[\s\-]?\d{4}",
    # Email addresses in body text — ONLY when they are not team participants
    # Implementation: cross-reference body emails against known participant list;
    # redact only those NOT present in the project's participant set
    "third_party_email": r"(?<![Ff]rom:|[Tt]o:|[Cc]c:)[^\S\r\n][a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Z|a-z]{2,}",
}
```

**GDPR note:** Even with redaction, sending employee communications to an external LLM API requires a Data Processing Agreement (DPA) with the provider. For EU-based organizations, the provider must offer GDPR-compliant data processing. This is a legal requirement.

**Data retention:** Project email data must not be retained in the system's storage beyond the period necessary for analysis. A documented retention and deletion policy is required before production deployment. This is not designed in this blueprint and is flagged as a production readiness gap.

**Data Residency Option — On-Premise LLM Inference**

For organizations where sending employee or client communications to an external AI provider is prohibited by contract, GDPR data processing restrictions, or internal policy, the pipeline supports full on-premise operation. Stages B, C, and D call the LLM through a configurable base URL. Redirecting to a local inference server requires three environment variables:

```env
LOCAL_LLM_BASE_URL=http://localhost:11434/v1   # Ollama, vLLM, or LM Studio endpoint
LOCAL_LLM_MODEL=qwen2.5:7b                     # Model running locally
USE_LOCAL_LLM=true                             # Switches all LLM calls to local endpoint
```

Compatible inference servers: [Ollama](https://ollama.com) (simplest for development), [vLLM](https://github.com/vllm-project/vllm) (production-grade, GPU-accelerated), LM Studio (desktop). Any server exposing an OpenAI-compatible `/v1/chat/completions` endpoint works without code changes.

**Practical note:** A 7B parameter model on a mid-range GPU (e.g., RTX 3080) can process the PoC's 18 email threads in approximately 90 seconds — adequate for a quarterly batch job. For continuous mode at scale, a dedicated inference server is recommended.

This directly addresses the contractual data residency concern identified in discovery (Q-J): whether processing client emails with a third-party AI provider violates the vendor's client agreements. With `USE_LOCAL_LLM=true`, no email content leaves the organization's infrastructure.

### 1.5 Tiered Noise Filter

**Tier 1 — Heuristic (no LLM):** Applied when all three conditions are true:
- No technical terms, JIRA references, version numbers, or project names in subject/body
- All participants are internal team members only
- Body contains exclusively personal/social content with no project-relevant sentences

**Important edge case:** The Tier 1 heuristic must not trigger on phrases like "Let's discuss the restaurant app deployment" (technical project topic) or "I'll be at the client site" (project-relevant). The heuristic applies only when personal content is the *sole* content of all messages in the thread.

**Tier 2 — LLM micro-classifier (ambiguous cases, ~10% of threads):**
```
Is this email thread primarily about a work project, or primarily social/off-topic?
Return ONLY: {"classification": "PROJECT" | "NOISE", "confidence": 0.0-1.0}
Thread: {{thread_text}}
```
Model: `gpt-5-nano`. Cost: < 200 tokens per call.

All filtered threads are logged with tier, confidence, and reason. They are never permanently discarded.

---

## Section 2 — The Analytical Engine (Multi-Step AI Logic)

### 2.1 Attention Flag Definitions

Three Attention Flags are defined. FLAGS 1 and 2 address process risks; FLAG 3 addresses operational/business risk independently.

---

#### 🚩 FLAG 1: STALLED DECISION

**Definition:** A question, decision request, or assigned action item explicitly raised in project communications that has received no substantive response, and has been open for ≥ N business days (default: 5, configurable).

**Examples from data:** email5 (CI/CD question, ~30 days unresolved), email15 (API callback question, ~14 days blocked), email11 (CSV export request, open at quarter-end).

---

#### 🚩 FLAG 2: UNCONTROLLED SCOPE CHANGE

**Definition:** A new requirement, client request, or functional change introduced informally — without formal logging, estimation, or explicit PM/BA acceptance or rejection.

**Subtle variant:** Developer-initiated scope expansion during a fix ("while I'm in there..."). Email 17 demonstrates this pattern — caught by the BA, but ideally caught by the system earlier.

---

#### 🚩 FLAG 3: OPERATIONAL INCIDENT / CLIENT IMPACT

**Definition:** A production incident, client-reported system failure, or security event that directly impacted end users — regardless of resolution status.

**Behavioral note — Goodhart's Law risk:** If teams know that production incidents appear in the Director's QBR report, they may have an incentive to handle incidents informally (phone calls, Slack DMs) to avoid email detection. The system should be framed as a visibility tool, not a penalty mechanism. Report language for FLAG 3 should be neutral and factual, not accusatory. This incentive dynamic should be discussed with the Director before deployment.

**FLAG 3 fires for resolved incidents too.** The report distinguishes `OPEN` from `RESOLVED_IN_QUARTER` to preserve historical visibility without inflating the current risk count.

---

### 2.2 Stage A: Deterministic Rule Engine

The rule engine produces *flag candidates* — not final flags. No LLM at this stage.

```python
def detect_stalled_candidates(thread, threshold_days=5):
    candidates = []
    for msg in thread.messages:
        questions = extract_questions(msg)
        for q in questions:
            days_elapsed = business_days_between(q.date, thread.last_message_date)
            if days_elapsed >= threshold_days:
                addressed = is_substantive_response_to_any(
                    question=q,
                    later_messages=thread.messages_after(q.date)
                )
                if not addressed:
                    candidates.append(Candidate(
                        flag_type="STALLED_DECISION",
                        evidence=q.text,
                        asked_by=q.sender,
                        asked_date=q.date,
                        days_open=days_elapsed
                    ))
    return candidates
```

**⚠️ Critical design note: `is_substantive_response_to_any()` is the hardest function in the system.**

This function determines whether any later message *actually resolves* an earlier question — not merely acknowledges it. This is the central reliability challenge of FLAG 1. The distinction between:
- "I'll look into it" → **acknowledgment**, NOT a resolution, question remains stalled
- "Here's the fix: run `create_test_db.sh`" → **resolution**, question is closed
- "This was a nice-to-have, removing from scope" → **resolution** (by closure, not answer)

A naive keyword-overlap implementation will produce significant false positives (flagging resolved questions as stalled) and false negatives (treating acknowledgments as resolutions).

**Implemented as a two-stage function:**

```python
def is_substantive_response_to_any(question, later_messages):
    """
    Stage 1: Fast heuristic filter
    Stage 2: LLM sub-call for ambiguous cases
    Returns: True (resolved), False (unresolved), "UNCERTAIN" (route to Stage B anyway)
    """
    # Stage 1: High-confidence resolution signals (fast, no LLM)
    RESOLUTION_SIGNALS = [
        "fixed", "resolved", "done", "completed", "it works now", "working now",
        "closing", "removing from scope", "not needed", "megoldva", "kész", 
        "javítottam", "már működik", "törölve", "kivettük"
    ]
    ACKNOWLEDGMENT_ONLY = [
        "i'll look into", "will check", "let me check", "megnézem", 
        "megcsinálom", "visszajelzek", "utánanézek"
    ]
    
    full_response_text = " ".join(m.body.lower() for m in later_messages)
    
    if any(sig in full_response_text for sig in RESOLUTION_SIGNALS):
        return True   # Resolved — do not generate candidate
    
    if all(ack in full_response_text for ack in ACKNOWLEDGMENT_ONLY 
           and not any(sig in full_response_text for sig in RESOLUTION_SIGNALS)):
        return False  # Only acknowledgments — still stalled
    
    # Stage 2: Ambiguous — use LLM mini-call to decide
    return llm_check_resolution(question, later_messages)  
    # Returns True / False; "UNCERTAIN" routes the candidate to Stage B with low confidence
```

This design makes the rule engine's core judgment function honest about its own uncertainty, rather than forcing a binary decision in cases where the evidence is genuinely ambiguous.

**Bilingual SCOPE_SIGNALS (EN + HU):**

```python
# Co-occurrence guard: at least ONE primary signal + context check required
# Single-word matches alone do not trigger a candidate — reduces false positive rate

SCOPE_SIGNALS_PRIMARY = [
    # English
    "not in the spec", "not in the specification", "new requirement", 
    "new request", "client mentioned", "client asked", "nice to have",
    "came up in the meeting", "forgot to mention", "additional requirement",
    # Hungarian
    "nem szerepel a specifikációban", "nem volt benne a specben",
    "új igény", "az ügyfél kérte", "az ügyfél megemlítette",
    "nice to have", "jó lenne ha", "felmerült", "szóba jött",
    "elfelejtettük megemlíteni", "kiegészítő követelmény",
]

SCOPE_SIGNALS_SECONDARY = [
    # English — require co-occurrence with a primary signal for candidate generation
    "also add", "while i'm", "while we're", "could we also", "came up",
    # Hungarian
    "amíg ott vagyok", "amíg már benne vagyok", "közben megcsinálnám",
]

def detect_scope_candidates(thread):
    candidates = []
    for msg in thread.messages:
        body_lower = msg.body.lower()
        has_primary = any(sig in body_lower for sig in SCOPE_SIGNALS_PRIMARY)
        has_secondary = any(sig in body_lower for sig in SCOPE_SIGNALS_SECONDARY)
        
        # Require at least a primary signal, or two secondary signals co-occurring
        if has_primary or (has_secondary and count_matches(body_lower, SCOPE_SIGNALS_SECONDARY) >= 2):
            candidates.append(Candidate(
                flag_type="UNCONTROLLED_SCOPE_CHANGE",
                evidence=msg.body[:300],
                introduced_by=msg.sender,
                introduced_date=msg.date,
                confidence="HIGH" if has_primary else "LOW"
            ))
    return candidates
```

---

### 2.3 Stage B: LLM Contextual Validator with Low-Confidence Routing

**Model:** `claude-sonnet-4-6` (default; configurable via .env)
**Temperature:** 0 (deterministic — for all stages including Stage D; see note)

**On temperature for all stages:** v2.0 used 0.3 for Stage D on the grounds of "readability." This was wrong. Non-deterministic output means two runs of the same data can produce differently-worded reports, making the golden test set unreliable and PM validation inconsistent. Readability must be achieved through prompt engineering (clear structure, good examples) not through temperature. All stages run at temperature = 0.

**Proactive concurrency cap**

For the PoC's 18 threads, Stage B calls execute sequentially without issue. At the scale described in Q9 (1,000–3,000 emails), uncontrolled concurrency causes two problems: API 429 rate-limit errors and unpredictable cost spikes. The solution is a proactive cap, not just reactive backoff:

```env
MAX_CONCURRENT_LLM_CALLS=10   # Default: 10 simultaneous Stage B calls
```

At the default setting, a 1,000-thread corpus processes in batches of 10, providing predictable throughput and cost. The value is configurable because the optimal setting depends on the provider's rate-limit tier and the organization's cost budget. The failure mode matrix entry for API 429 (exponential backoff → `NEEDS_REVIEW`) remains the fallback; the concurrency cap is the proactive layer that should prevent those situations from occurring.

**Prompt — Contextual Validator:**

```
You are a delivery risk analyst validating a flag candidate for a Director of Engineering.
A deterministic rule engine has identified this as a POTENTIAL risk. Your task is to:
1. Confirm whether this is a genuine risk, a false positive, or uncertain.
2. Assess severity based on business impact.
3. Identify specific evidence supporting or refuting the flag.
4. Provide a recommended action.

TODAY'S DATE: {{today_date}}
STALLED THRESHOLD: {{threshold_days}} business days
FLAG TYPE: {{flag_type}}
LANGUAGE NOTE: The thread may contain Hungarian text. Analyze it as-is; do not translate.
Hungarian resolution signals include: megoldva, kész, javítottam, már működik, törölve.
Hungarian acknowledgment-only signals include: megnézem, utánanézek, visszajelzek.

ANTI-HALLUCINATION RULES:
- Every conclusion must reference specific text from the thread.
- If the thread shows the issue was resolved AFTER the candidate was detected,
  mark confirmed=false, explain what resolved it.
- "I'll look into it" / "megnézem" = acknowledgment only, NOT resolution.
- Off-topic personal content (food, birthdays, social plans) is NEVER a flag.
- If you are uncertain, set confirmed=UNCERTAIN — do NOT force a binary verdict.

CANDIDATE:
{{candidate_json}}

THREAD (metadata preserved, body text PII-redacted):
{{thread_json}}

Return ONLY valid JSON — no markdown, no preamble:
{
  "confirmed": true | false | "UNCERTAIN",
  "false_positive_reason": "string or null",
  "uncertainty_reason": "string or null — required if confirmed=UNCERTAIN",
  "flag_type": "STALLED_DECISION | UNCONTROLLED_SCOPE_CHANGE | OPERATIONAL_INCIDENT",
  "severity": "HIGH | MEDIUM | LOW",
  "confidence_score": 0.0-1.0,
  "summary": "one sentence for the Director",
  "evidence": "specific quote or observation from the thread",
  "days_open": number | null,
  "owner": "email address of responsible person | null",
  "status": "OPEN | RESOLVED_IN_QUARTER",
  "recommended_action": "specific, actionable instruction for the Director"
}
```

**Low-confidence routing logic:**

```python
CONFIDENCE_THRESHOLD = 0.70  # Configurable

def route_stage_b_output(result):
    if result["confirmed"] == "UNCERTAIN" or result["confidence_score"] < CONFIDENCE_THRESHOLD:
        return route_to_needs_review_queue(result)
    elif result["confirmed"] == False:
        return log_false_positive(result)
    else:
        return route_to_confirmed_flags(result)
```

The "Needs PM Review" queue is a first-class output — not a discard pile. It appears in the final report in its own section, giving the Director visibility without claiming certainty. A PM can then mark each item as: "Confirmed — add to report" / "False positive — discard" / "Known issue — acknowledge."

---

### 2.4 Known-Issue Acknowledgment Mechanism

**The problem it solves:** Without an acknowledgment mechanism, the same open FLAG 1 item (e.g., an ongoing unresolved architectural question) appears in every QBR report indefinitely. The Director starts ignoring the report when it repeatedly surfaces items they are already tracking.

**Implementation:** A JSON configuration file (`acknowledged_items.json`) maintained per project, checkable into version control:

```json
{
  "project": "DivatKirály",
  "acknowledged_items": [
    {
      "flag_type": "STALLED_DECISION",
      "summary_pattern": "CSV export feature",
      "acknowledged_by": "director@company.com",
      "acknowledged_date": "2025-07-01",
      "reason": "Tracked in JIRA-447, scheduled for Q3",
      "expiry_date": "2025-09-30"
    }
  ]
}
```

**Rules:**
- Acknowledged items are **not** removed from the system — they are suppressed in the report with a note: *"1 acknowledged item not shown — see acknowledged_items.json"*
- Acknowledgments have a mandatory expiry date. After expiry, the item resurfaces unless re-acknowledged.
- Acknowledging an item does not close it — the underlying rule still runs. If the item escalates in severity (e.g., days_open increases significantly past the acknowledgment date), it resurfaces regardless of expiry.
- In the PoC: implemented as a static JSON file read at Stage D. In production: a lightweight database table with a simple UI.

---

### 2.5 Stage C: Cross-Thread Pattern Analysis

**The problem:** Individual threads look harmless; patterns across threads reveal systemic risk.

**Implementation:** RAG-based retrieval is the primary production architecture. For the PoC, all Stage B validated outputs per project are grouped and submitted to a single cross-thread analysis prompt.

**Cross-thread prompt:**

```
You are analyzing ALL validated flag summaries for a single project to find risk patterns
that span multiple email threads. These patterns are invisible when threads are viewed in isolation.

Look for:
1. The same topic or client request appearing across multiple threads without formal resolution
2. The same participant appearing as a non-responder or bottleneck across multiple threads
3. A series of informal references that together imply an implicit commitment with no formal tracking
4. Any combination of individually-minor flags that collectively indicate systemic risk

STRICT RULES:
- A pattern requires evidence in AT LEAST 2 distinct thread IDs. Do not report single-thread patterns.
- Every pattern must cite specific thread IDs and evidence from each.
- Do not combine unrelated issues into a false pattern.
- If no genuine cross-thread patterns exist, return an empty array. Do not invent patterns.

Return ONLY valid JSON:
{
  "cross_thread_patterns": [
    {
      "pattern_type": "RECURRING_BLOCKER | IMPLICIT_COMMITMENT | SYSTEMIC_PROCESS_FAILURE | OTHER",
      "description": "one sentence for the Director",
      "threads_involved": ["thread_id_1", "thread_id_2"],
      "severity": "HIGH | MEDIUM | LOW",
      "evidence": {
        "thread_id_1": "specific reference",
        "thread_id_2": "specific reference"
      },
      "recommended_action": "specific action for the Director"
    }
  ]
}

ALL VALIDATED FLAG SUMMARIES FOR THIS PROJECT:
{{project_flag_summaries_json}}
```

---

### 2.6 Stage D: Portfolio Report Generator

**Model:** `claude-sonnet-4-6` (default; configurable via .env)
**Temperature:** 0

**Prompt:**

```
You are preparing a QBR Portfolio Health Report for a Director of Engineering.
This Director is technical, time-constrained, and needs to make fast, accurate decisions.

STYLE: Direct language. No corporate filler. Every flag: description + evidence + action.
Sort within projects: HIGH → MEDIUM → LOW. 
GREEN projects: one line only.
Do NOT include acknowledged items in the main report — only the suppression summary line.
Include per-flag confidence label: [Rule+LLM-confirmed] | [LLM-flagged, unvalidated] | [Needs PM Review].

REPORT STRUCTURE:
---
# QBR Portfolio Health Report
**Period:** {{quarter_label}}
**Generated:** {{date}}
**Projects Reviewed:** {{project_count}} | **Open Flags:** {{open_flag_count}} | **Needs Review:** {{needs_review_count}}

## Executive Summary
[2-3 sentences: portfolio health overview, single most critical concern]

## 🔴 Immediate Attention Required
[RED projects — HIGH severity open flags]

## 🟡 Monitor Closely
[AMBER projects — MEDIUM/LOW open flags]

## 🟢 On Track
[GREEN projects — one line each]

## Incidents This Quarter
[All FLAG 3 entries — OPEN and RESOLVED_IN_QUARTER — with resolution time where known]

## Cross-Project Patterns
[Stage C findings spanning multiple projects, if any]

## 🔵 Needs PM Review
[All low-confidence outputs — clearly labeled as unverified, awaiting PM input]

## Recommended Director Actions
[Numbered, specific, actionable — what to ask or decide in the QBR]

---
⚠️ AI-GENERATED REPORT — Validate flagged items with responsible PMs before acting.
Acknowledged items suppressed: {{acknowledged_count}} (see acknowledged_items.json for details)
Generated by QBR Portfolio Health Analyzer v2.2
---

INPUT DATA:
{{all_project_summaries_json}}
```

---

### 2.7 Hallucination Mitigation: Summary

| Mitigation Layer | Where Applied | Mechanism |
|-----------------|--------------|-----------|
| Rules-before-AI | Stages A→B | LLM never invents a candidate; validates rule-detected ones only |
| `is_substantive_response_to()` two-stage design | Stage A | Acknowledgments explicitly distinguished from resolutions; LLM sub-call for ambiguous cases |
| Evidence-mandatory | Stage B | Every confirmed flag must cite specific thread text |
| Explicit uncertainty channel | Stage B | `confirmed: "UNCERTAIN"` is a valid output that routes to review queue |
| Low-confidence routing | Stage B→output | Uncertain flags never silently suppressed or blindly reported |
| Temperature = 0 | All stages | Fully deterministic output; golden test set comparisons are reliable |
| Directory-primary roles | Preprocessing | LLM cannot hallucinate roles for known participants |
| Header/body PII separation | Pre-LLM gate | Email addresses preserved for attribution; body-only credentials redacted |
| Bilingual signal lists | Stages A, B | Hungarian-language risks not missed; LLM prompt handles mixed EN/HU |
| Cross-thread evidence requirement | Stage C | Patterns require ≥2 threads with specific evidence each |
| Golden test set | Monitoring | Detects accuracy/hallucination changes after model updates |
| Known-issue acknowledgment | Stage D | Prevents Director habituation from suppressing genuine new risks |
| "AI-generated" watermark | Report footer | Structural defense against Director over-trust |

---

## Section 3 — Cost & Robustness Considerations

### 3.1 Cost Management

The hybrid architecture reduces LLM call volume by approximately 81% vs. an all-LLM approach (see v2.0 cost table). The key driver: Stage B is called only for rule-detected candidates (~15% of threads), not all threads.

The low-confidence routing path adds a small number of additional Stage B calls (for `is_substantive_response_to()` LLM sub-calls in ambiguous cases), estimated at 5–8% of threads. This is a deliberate trade-off: slightly higher cost for significantly higher reliability in the most failure-prone detection step.

### 3.2 Robustness Against Misleading Information

See also: Failure Mode Matrix in Section 3.3.

| Failure Mode | Example | Mitigation |
|-------------|---------|-----------|
| Question resolved after candidate detection | Email 9: outage resolved in same thread | `is_substantive_response_to()` checks full thread; Stage B validates resolution signals |
| Acknowledgment mistaken for resolution | "I'll look into it" | Explicit acknowledgment-only pattern list in Stage A; Stage B prompt calls this out |
| Off-topic content inside project thread | Birthday messages in status thread | Noise filter operates at message level, not thread level; messages are filtered individually |
| Hungarian scope signals missed | "jó lenne ha", "nem szerepel a specben" | Bilingual SCOPE_SIGNALS list; Stage B prompt handles mixed-language threads |
| Scope false positive from common phrases | "it came up in testing" | Co-occurrence guard: single secondary signal alone does not trigger a candidate |
| Format parsing failure | Non-standard date/header | Multi-format fallback; unparseable emails logged as `PARSE_WARNING`, not silently dropped |
| Cross-thread false pattern | Same word in unrelated contexts | Cross-thread prompt requires ≥2 threads with specific evidence per thread |

### 3.3 Failure Mode Matrix

*A system designed only for the happy path is not a production system. This matrix defines the system's behavior at every potential failure point.*

| Stage | Failure Mode | Detection | Behavior | Director Sees |
|-------|-------------|-----------|----------|---------------|
| Email Parser | Unparseable email (unknown format) | `PARSE_WARNING` log entry | Email skipped; rest of thread analyzed | Nothing — but log is reviewable |
| Email Parser | UTF-8 encoding error | Exception caught | Email flagged as `ENCODING_ERROR`; skipped | Nothing — but audit log records it |
| Identity Resolver | Email not in directory | No exception | Role labeled `[inferred]` | Inferred role label on the flag |
| Noise Filter L2 | LLM API error | Exception caught | Thread treated as `PROJECT` (safe default: analyze rather than skip) | Normal analysis — may produce false positives |
| Credential Scanner | Regex pattern miss (novel API key format) | None (silent) | Unredacted credential reaches LLM | Mitigated by: DPA with provider; credential not stored; logged token counts don't capture content |
| Stage A | Rule engine crash (bug in code) | Exception caught | Thread skipped; logged as `STAGE_A_ERROR` | Nothing — reported in system health summary |
| Stage B | LLM API 429 rate limit | HTTP 429 response | Exponential backoff (3 retries); then route to `NEEDS_REVIEW` queue | Item appears in 🔵 Needs PM Review section |
| Stage B | LLM returns malformed JSON | JSON parse error | Retry once with explicit JSON repair prompt; if still fails → `NEEDS_REVIEW` | Item appears in 🔵 Needs PM Review section |
| Stage B | LLM returns `confirmed: "UNCERTAIN"` | Confidence check | Route to `NEEDS_REVIEW` queue | Item appears in 🔵 Needs PM Review section |
| Stage C | Vector store unavailable (production) | Connection error | Skip cross-thread analysis; report generated without Stage C | Report includes: ⚠️ *Cross-thread analysis unavailable — contact system administrator* |
| Stage D | Report generation fails mid-run | Exception caught | Partial report saved up to last successful project; report marked `INCOMPLETE` | Report header shows: ⚠️ *INCOMPLETE — [N] of [M] projects analyzed. Remaining projects failed; see error log.* |
| Stage D | All stages complete but zero flags found | Zero-flag check | Report generated with all-GREEN status + explicit note | Report shows all GREEN with: *No attention flags detected in this period. Verify with PMs that this reflects actual project health.* |
| PM Validation | PM does not respond before QBR deadline | Timeout | Unvalidated items remain in report with `[Unvalidated]` label | `[Unvalidated]` label visible; Director can choose to act or defer |
| Golden Test Set | Accuracy drops > 10% from baseline | Automated comparison | Alert to maintenance owner; production report generation **not** paused — flagged for review | Report includes: ⚠️ *System accuracy alert — contact maintenance owner before acting on flags* |

---

## Section 4 — Monitoring & Trust

### 4.1 The Trust Problem

An AI-generated report that a Director acts on without verification is a trust-critical system. The most dangerous long-term failure mode is not hallucination — it is **over-trust**: once the system builds a track record, the Director stops verifying individual flags. The "AI-generated, validate before acting" watermark on every report is a structural trust architecture decision, not cosmetic.

The design must also defend against the opposite failure: the Director dismissing the report because it surfaces too many known or low-confidence items. The low-confidence routing, the acknowledgment mechanism, and the PoC precision target of > 80% are all defenses against this erosion.

### 4.2 PM Validation Layer — Including Incentive Misalignment

For the first three quarterly cycles, each flagged item undergoes a **PM Validation Step** before reaching the Director:

1. System generates draft report with all flags
2. Each flag is routed to the relevant PM: "Does this accurately describe a real issue? [Yes / No / Partially — if No, brief reason]"
3. PM feedback is logged (not auto-applied to the report)
4. Director receives report with per-flag labels: `[PM-validated]`, `[PM-disputed: note included]`, `[Unvalidated]`
5. PM corrections feed a calibration log for threshold tuning

**Acknowledged incentive misalignment:** The PM being asked to validate a flag about *their own project* has a personal incentive to mark it as a false positive. This is a structural conflict of interest built into the validation design. The mitigation is not to remove the PM from the loop (they have the best context), but to make their disputes *visible* to the Director rather than silently suppressing flagged items. A disputed flag with a PM's reasoning attached is more useful to the Director than a silently removed flag.

For flags that are disputed by the PM but involve client impact or delivery timeline, an explicit **escalation path** to the Director's attention (bypassing the PM) should be defined — for example, any FLAG 3 item marked as a false positive by the responsible PM is automatically shown to the Director with both the flag and the PM's dispute reason.

### 4.3 Key Metrics

| Metric | Measurement | Target |
|--------|------------|--------|
| Flag precision | % of flags confirmed as real by PM review | > 80% |
| Flag recall | % of real issues flagged (measured post-QBR) | > 70% |
| False positive rate | % of flags marked incorrect by PMs | < 20% |
| Noise filter false exclusion | % of filtered threads with project-relevant content | < 5% |
| Cross-thread pattern precision | % of cross-thread patterns confirmed by PMs | > 60% |
| "Needs Review" resolution rate | % of review-queue items resolved by PMs before QBR | > 85% |
| Rule candidate → confirmed flag rate | Ratio for threshold calibration | Monitored, no fixed target |
| JSON schema failure rate | Prompt drift detection | Alert at > 5% |
| API error rate | Model instability detection | Alert at > 2% |

### 4.4 Golden Test Set & Drift Detection

**Composition:** 12–15 email threads with manually labeled expected outputs covering high-confidence positives, high-confidence negatives, and edge cases.

**Governance:** Named owner (designated BA or technical PM). Updated quarterly. New production edge cases added within one cycle. **Version-locked to prompt versions** — this is critical: if a prompt is changed, the test set must be re-run against the new prompt and a new baseline recorded. A golden test set that is not version-locked to its prompts detects nothing reliable.

**Drift alert:** If accuracy drops > 10% from the version-locked baseline, the maintenance owner is alerted. Production report generation continues but the report includes a system accuracy warning.

### 4.5 Prompt Versioning — Acknowledged Gap

This blueprint does not define a prompt versioning strategy. Prompts are code: changing them without version control creates silent regressions. A production deployment requires:

- Prompts stored in version control alongside application code (same repository, same release tag)
- A changelog documenting why each prompt change was made and what test results validated it
- A policy defining who is authorized to change production prompts
- A requirement to re-run the golden test set before any prompt change reaches production

This is explicitly flagged as a production readiness gap not addressed in the PoC.

### 4.6 Pipeline Observability

A pipeline that fails silently is worse than a pipeline that fails loudly. The most dangerous failure mode is not a crash — it is a successful-looking run that produces an empty or incomplete report because a stage produced zero outputs without surfacing a warning.

**Stage-boundary logging (stdout)**

Every stage boundary emits a one-line log to stdout:

```
[Stage A] 7 candidates found across 3 projects (Project Phoenix: 4, DivatKirály: 3)
[Stage B] 5 confirmed | 1 needs-review | 1 false-positive | mode: mock
[Stage C] 1 cross-project pattern detected
[Stage D] Report written → output/sample-report.md
[Run complete] Duration: 4.2s | Tokens used: 1,840 (mock: 0 real)
```

**Zero-flag warning:** If Stage B produces zero confirmed flags, stdout shows:

```
[WARNING] Zero confirmed flags — verify with PMs that this reflects actual project health.
```

This warning is also injected into the report body (already in the failure mode matrix — this section defines architecturally *where* it originates).

**Run log (`output/run-log.json`)**

Each pipeline execution writes a machine-readable run record alongside the report:

```json
{
  "run_id": "2025-Q2-20250615T143022",
  "quarter": "Q2 2025",
  "mode": "mock",
  "started_at": "2025-06-15T14:30:22Z",
  "completed_at": "2025-06-15T14:30:26Z",
  "duration_seconds": 4.2,
  "stages": {
    "stage_a": {"candidates_total": 7, "by_project": {"Project Phoenix": 4, "DivatKirály": 3}},
    "stage_b": {"confirmed": 5, "needs_review": 1, "false_positives": 1, "tokens_used": 1840},
    "stage_c": {"patterns_found": 1},
    "stage_d": {"output_path": "output/sample-report.md", "projects_in_report": 2}
  },
  "warnings": [],
  "errors": []
}
```

The run log enables: audit trails, regression detection (flag count drops between runs), and future integration with monitoring dashboards. Token count is 0 in mock mode and reflects actual API usage in live mode.

---

## Section 5 — Architectural Risk & Mitigation

### 5.1 Low-Probability, High-Impact Risk: Context Collapse

**Likelihood in practice: Low.** Modern LLMs used in this pipeline (claude-sonnet-4-6, gpt-5-nano) have context windows of 128k–200k tokens. A typical email thread — even a long one spanning weeks with 50+ messages — sits well within 20,000–30,000 tokens. Context overflow from a single email thread is not a realistic failure mode under normal operating conditions.

**Why it remains worth noting:** If it did occur — for example in an unusually long multi-party thread, or if the system were extended to include document attachments — truncation would produce **confident-but-wrong analysis**: worse than no analysis, because it generates authoritative-sounding incorrect information. This would compound the over-trust failure mode (see Section 5.3) in a particularly dangerous way.

**Scale mitigation — RAG-based retrieval (recommended for production):**

```
Per-project email store
        │
        ├──► Vector database (pgvector / Qdrant / Pinecone)
        │    [Each email: date + sender + subject + body excerpt embedded]
        │
        └──► Rule engine on metadata (dates, senders, subjects)
             — does NOT require full body for candidate detection
                     │
                     ▼
             LLM retrieves only relevant emails via vector query
             per specific analysis question
             [Never processes full corpus at once]
```

This architecture makes the system robust even if corpora grow significantly (multi-year history, document attachments, large teams). It is not required for the current PoC use case.

**For the PoC:** In-memory simplified approach — Stage B summaries grouped per project, submitted to Stage C. Demonstrates the pattern without vector infrastructure. Context limits are not a concern at this scale.

### 5.2 Batch/Continuous Duality — Honest Assessment of the Gap

The claim in earlier versions that "the analytical logic is identical in both modes" requires qualification. It is true at the level of individual email analysis. It is **not** true at the orchestration layer.

Continuous mode requires:
- A **persistent state store** tracking open questions, scope changes, and unresolved incidents per project
- A **state reconciliation mechanism** for emails arriving out of order or retroactively added to a thread
- An **incremental update strategy** so that each new email updates the project state without full re-analysis of historical threads
- A **deduplication layer** so that a flag raised on Monday is not raised again on Tuesday for the same underlying issue

None of this is designed in this blueprint. It is flagged here rather than hidden in the "continuous mode is a configuration decision" framing of earlier versions. The PoC does not implement continuous mode, and evolving to it requires meaningful additional architectural work.

**Recommended infrastructure for continuous mode:**

The persistent state store, incremental processing, and deduplication layer described above map to established components:

- **Workflow orchestration:** [Temporal](https://temporal.io), [Restate](https://restate.dev), or Celery with a Redis backend. Any of these provides durable task execution with checkpointing — if the pipeline crashes after Stage A, it resumes from Stage B rather than restarting from scratch.
- **State store:** Redis. Fast, well-understood for operational data, supports TTL-based expiry (acknowledged items expire after N days automatically), and atomic updates that prevent race conditions under concurrent runs. The PoC's `acknowledged_items.json` file should be replaced with a Redis key-value store in any production deployment running more frequently than quarterly.
- **Message queue:** Redis Streams, RabbitMQ, or SQS to receive email events in real time instead of batch-scanning a directory.

These are named here so the architectural path from PoC to production is unambiguous rather than deferred to "requires additional architectural work."

### 5.3 Secondary Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Model API deprecation | Medium | High | Provider-agnostic interface; fallback prompts tested for 2+ providers |
| Identity resolution collision | High in real orgs | Medium | Email = canonical key; collisions logged; never auto-merged |
| GDPR / data exposure | Medium | Critical | Mandatory PII scan; DPA required; header/body separation; data retention policy (gap — not designed) |
| Director over-trusts output | High post-adoption | High | AI-generated watermark; PM validation; per-flag confidence labels; acknowledgment mechanism |
| PM incentive misalignment in validation | High | Medium | Disputed flags made visible to Director; FLAG 3 disputes escalated automatically |
| Goodhart's Law on incident reporting | Medium | Medium | System framed as visibility tool; report language neutral; Director briefed on this risk before deployment |
| Prompt version drift | High without governance | High | Named prompt owner; version control required; golden test set version-locked |
| Batch/continuous state management | High if continuous pursued | High | Explicitly out of PoC scope; requires separate architecture phase |
| Scope creep in the system itself | Medium | Medium | Formal roadmap; features tracked in Jira; quarterly architecture review |

---

## Out-of-Scope Notes — Strategic Observations

*These observations are forward-referenced in the Executive Summary because they reflect deliberate architectural decisions made throughout this document, not afterthoughts.*

### 1. Batch vs. Continuous: The Architecture Supports Both, But the Path Is Non-Trivial

The analytical pipeline at the email-analysis level is stateless and event-compatible. The QBR's real value is as a review of already-tracked issues, not a discovery session — and that requires continuous operation. The infrastructure path (message queue, persistent state store, incremental updates, deduplication) is documented as a known gap in Section 5.2. It is achievable, but it is not "just a configuration change."

### 2. Email Is a Weak Signal — By Design

Email captures 30–40% of real project communication. The ingestion layer is source-agnostic: additional data sources (Jira, Git, Slack, standup notes) require new parsers, not new analytical logic. This is an architectural opportunity, not an apology.

### 3. The Conversational Interface Is the Likely End State

A static report is the right starting point. The likely end state: "What are the riskiest things in DivatKirály right now?" The analytical engine produces structured JSON at every stage; rendering it as a static report or as conversational responses is a presentation-layer decision requiring no changes to Stages A–C.

---

