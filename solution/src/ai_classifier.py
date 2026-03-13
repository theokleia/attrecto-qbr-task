"""
ai_classifier.py — QBR Automation System
Stage A: Deterministic rule engine (no LLM)
Stage B: LLM contextual validator (claude-sonnet-4-6)

Outputs structured flag candidates and confirmed flags in JSON format.
"""

import json
import os
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Optional

from email_parser import EmailThread, EmailMessage


# ── Configuration ─────────────────────────────────────────────────────────────

STALLED_THRESHOLD_DAYS = int(os.environ.get('STALLED_THRESHOLD_DAYS', '5'))
CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', '0.70'))
# Reference date for "days open" calculation. Defaults to last day of current quarter.
# Override with ANALYSIS_REFERENCE_DATE env var (YYYY-MM-DD).
def get_reference_date() -> datetime:
    """
    Returns the analysis reference date. Evaluated at call time (not import time)
    so it remains accurate in long-running processes.
    Priority: ANALYSIS_REFERENCE_DATE env var → last day of current quarter.
    """
    import calendar
    _env_date = os.environ.get('ANALYSIS_REFERENCE_DATE')
    if _env_date:
        return datetime.strptime(_env_date, '%Y-%m-%d')
    today = datetime.now()
    quarter_end_month = ((today.month - 1) // 3 + 1) * 3
    last_day = calendar.monthrange(today.year, quarter_end_month)[1]
    return datetime(today.year, quarter_end_month, last_day)

# Module-level alias for use as default argument value (evaluated once at import).
# For long-running services, call get_reference_date() directly instead.
ANALYSIS_REFERENCE_DATE = get_reference_date()

# ── Noise filter: Signal lists ────────────────────────────────────────────────

TECHNICAL_SIGNALS = [
    # English
    "deploy", "deployment", "api", "bug", "fix", "server", "database", "frontend",
    "backend", "ci/cd", "ci ", "build", "release", "staging", "production",
    "sprint", "ticket", "jira", "github", "pull request", "feature",
    "endpoint", "function", "error", "exception", "timeout", "latency",
    "migration", "schema", "query", "security", "vulnerability", "gdpr",
    "compliance", "contract", "invoice", "deadline", "milestone",
    "requirement", "specification", "scope", "estimate", "client",
    "callback", "webhook", "import", "export", "csv", "login", "auth",
    # Hungarian
    "hiba", "javítás", "fejlesztés", "kiadás", "szerver", "adatbázis",
    "telepítés", "specifikáció", "ügyfél", "határidő", "projekt",
]

SOCIAL_SIGNALS = [
    # English
    "birthday", "lunch", "restaurant", "dinner", "party", "weekend",
    "vacation", "holiday", "coffee", "drinks", "celebrate", "surprise",
    # Hungarian
    "születésnap", "ebéd", "étterem", "vacsora", "buli", "hétvége",
    "szabadság", "kávé", "ünnep", "meglepetés",
]

RE_VERSION_NUMBER = re.compile(r'\bv?\d+\.\d+')
RE_JIRA_REF = re.compile(r'\b[A-Z]{2,}-\d+\b')  # e.g. PROJ-123


def is_noise_heuristic(thread: 'EmailThread') -> tuple[bool, str]:
    """
    Tier 1: Fast heuristic noise check — no LLM, no cost.
    A thread is noise only when ALL messages lack technical/project content
    AND at least one social signal is present.
    Returns (is_noise, reason).
    """
    all_text = ' '.join(
        (m.body + ' ' + m.subject).lower() for m in thread.messages
    )

    # Bail immediately if technical content detected
    if (
        any(sig in all_text for sig in TECHNICAL_SIGNALS)
        or RE_VERSION_NUMBER.search(all_text)
        or RE_JIRA_REF.search(all_text)
    ):
        return False, "technical_content_detected"

    # Bail if project name appears anywhere in the thread
    from email_parser import PROJECT_PATTERNS
    for pattern, _ in PROJECT_PATTERNS:
        if pattern.search(all_text):
            return False, "project_name_detected"

    # Need a positive social signal to classify as noise
    if not any(sig in all_text for sig in SOCIAL_SIGNALS):
        return False, "no_social_signals"

    return True, "social_only_no_technical_content"


def is_noise_llm(thread: 'EmailThread') -> tuple[str, float]:
    """
    Tier 2: LLM micro-classifier for ambiguous threads (~10% of volume).
    Uses OpenAI gpt-5-nano (or MICRO_CLASSIFIER_MODEL env override).
    Returns (classification, confidence) where classification is "PROJECT" or "NOISE".
    Safe default on any failure: returns ("PROJECT", 0.0) — analyze rather than skip.
    """
    openai_key = os.environ.get('OPENAI_API_KEY')
    if not openai_key:
        return "PROJECT", 0.0

    model = os.environ.get('MICRO_CLASSIFIER_MODEL', 'gpt-5-nano')

    # Build compact thread text (cap at 5 messages × 300 chars to limit tokens)
    parts = []
    for msg in thread.messages[:5]:
        parts.append(f"From: {msg.sender_email}\nBody: {msg.body[:300]}")
    thread_repr = "\n---\n".join(parts)

    prompt = (
        "Is this email thread primarily about a work project, or primarily social/off-topic?\n"
        'Return ONLY valid JSON: {"classification": "PROJECT" or "NOISE", "confidence": 0.0-1.0}\n\n'
        f"Thread:\n{thread_repr}"
    )

    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0,
        )
        raw = response.choices[0].message.content.strip()
        raw = re.sub(r'^```json\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)
        result = json.loads(raw)
        return result.get("classification", "PROJECT"), float(result.get("confidence", 0.5))
    except ImportError:
        return "PROJECT", 0.0
    except Exception as e:
        print(f"  Noise filter L2 API error: {e} — defaulting to PROJECT (safe)")
        return "PROJECT", 0.0


def run_noise_filter(threads: list, use_mock: bool = False) -> tuple[list, list[dict]]:
    """
    Apply tiered noise filter before Stage A.

    Tier 1 — Heuristic (no LLM, ~90% of noise caught here)
    Tier 2 — LLM micro-classifier (ambiguous threads only, ~10% of volume)

    All filtered threads are logged and never permanently discarded.

    Returns:
        project_threads  — threads that passed the filter (passed to Stage A)
        noise_log        — list of dicts for filtered_noise.json
    """
    project_threads = []
    noise_log = []

    for thread in threads:
        # ── Tier 1: Heuristic ──
        is_noise_t1, reason_t1 = is_noise_heuristic(thread)
        if is_noise_t1:
            noise_log.append({
                "thread_id": thread.thread_id,
                "subject": thread.subject,
                "project": thread.project,
                "messages": len(thread.messages),
                "tier": 1,
                "classification": "NOISE",
                "confidence": 1.0,
                "reason": reason_t1,
            })
            print(f"  [Noise L1] {thread.thread_id} excluded: {reason_t1}")
            continue

        # ── Tier 2: LLM for ambiguous threads ──
        # Only call L2 if: no technical signals AND ≤2 messages AND unknown project
        # This targets ~10% of threads as specified in Blueprint Section 1.5
        all_text = ' '.join(m.body.lower() for m in thread.messages)
        is_ambiguous = (
            not any(sig in all_text for sig in TECHNICAL_SIGNALS)
            and len(thread.messages) <= 2
            and thread.project == 'Unknown'
        )

        if is_ambiguous and not use_mock:
            classification, confidence = is_noise_llm(thread)
            if classification == "NOISE" and confidence >= 0.75:
                noise_log.append({
                    "thread_id": thread.thread_id,
                    "subject": thread.subject,
                    "project": thread.project,
                    "messages": len(thread.messages),
                    "tier": 2,
                    "classification": "NOISE",
                    "confidence": confidence,
                    "reason": "llm_micro_classifier",
                })
                print(f"  [Noise L2] {thread.thread_id} excluded: confidence={confidence:.2f}")
                continue

        project_threads.append(thread)

    return project_threads, noise_log


# ── Stage A: Signal lists (EN + HU, bilingual) ────────────────────────────────

SCOPE_SIGNALS_PRIMARY = [
    # English
    "not in the spec", "not in the specification", "new requirement",
    "new request", "client mentioned", "client asked", "nice to have",
    "came up in the meeting", "forgot to mention", "additional requirement",
    "wasn't in the estimate", "not estimated", "out of scope",
    "new feature", "extra effort", "wasn't included",
    # Hungarian
    "nem szerepel a specifikációban", "nem volt benne a specben",
    "új igény", "az ügyfél kérte", "az ügyfél megemlítette",
    "nice to have", "jó lenne ha", "felmerült", "szóba jött",
    "elfelejtettük megemlíteni", "kiegészítő követelmény",
    "nem volt becslésben", "nem volt tervezve",
]

SCOPE_SIGNALS_SECONDARY = [
    # English
    "also add", "while i'm", "while we're", "could we also", "came up",
    "while i am", "while we are", "can we also",
    # Hungarian
    "amíg ott vagyok", "amíg már benne vagyok", "közben megcsinálnám",
    "mi lenne ha", "lehetne még",
]

INCIDENT_SIGNALS = [
    # English
    "urgent", "client cannot", "not working", "outage", "down", "production issue",
    "live issue", "all hands", "critical bug", "security", "data breach",
    "gdpr", "compliance violation", "blocked", "cannot log in", "login broken",
    # Hungarian
    "sürgős", "nem működik", "leállt", "éles hiba", "kritikus",
    "biztonsági", "adatvédelem", "nem tud belépni",
]

RESOLUTION_SIGNALS = [
    # English
    "fixed", "resolved", "done", "completed", "it works now", "working now",
    "closing", "removing from scope", "not needed", "deployed", "live now",
    "pushed the fix", "fix is out", "problem solved",
    # Hungarian
    "megoldva", "kész", "javítottam", "már működik", "törölve",
    "kivettük", "megjavítottam", "kijavítottuk",
]

ACKNOWLEDGMENT_ONLY = [
    # English
    "i'll look into", "will check", "let me check", "looking into",
    "investigating", "will get back", "will follow up",
    # Hungarian
    "megnézem", "megcsinálom", "visszajelzek", "utánanézek",
    "rámézek", "megnézöm",
]

QUESTION_ENDINGS = ['?']
QUESTION_STARTERS = [
    'should', 'would', 'could', 'can', 'is it', 'are there', 'do we',
    'have you', 'has this', 'what is', 'what are', 'when will', 'who will',
    'how should', 'has anyone', 'any update', 'any news', 'please advise',
    'could you', 'can you', 'please confirm', 'can someone',
    # Hungarian
    'megcsinálod', 'megnézed', 'tudod', 'vissza tudsz', 'mikor',
    'hogyan', 'mi lesz', 'mi a',
]


# ── Data classes ──────────────────────────────────────────────────────────────

@dataclass
class Candidate:
    flag_type: str          # STALLED_DECISION | UNCONTROLLED_SCOPE_CHANGE | OPERATIONAL_INCIDENT
    thread_id: str
    project: str
    evidence: str
    confidence: str         # HIGH | LOW (Stage A assessment)
    raised_by: str          # email of person who raised the issue
    raised_date: Optional[datetime]
    days_open: Optional[int]
    subject: str


@dataclass
class ConfirmedFlag:
    flag_type: str
    thread_id: str
    project: str
    subject: str
    severity: str           # HIGH | MEDIUM | LOW
    confidence_score: float
    status: str             # OPEN | RESOLVED_IN_QUARTER | NEEDS_PM_REVIEW
    summary: str
    evidence: str
    owner: str
    recommended_action: str
    days_open: Optional[int]
    false_positive_reason: Optional[str]


# ── Business day calculation ──────────────────────────────────────────────────

def _to_naive(dt: datetime) -> datetime:
    """Convert timezone-aware datetime to naive UTC. Naive datetimes pass through unchanged."""
    if dt.tzinfo is not None:
        from datetime import timezone
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def business_days_between(start: datetime, end: datetime) -> int:
    """Count business days (Mon-Fri) between two datetimes. Both normalized to UTC-naive."""
    if not start or not end:
        return 0
    start = _to_naive(start)
    end = _to_naive(end)
    if end <= start:
        return 0
    count = 0
    current = start.date() if hasattr(start, 'date') else start
    end_date = end.date() if hasattr(end, 'date') else end
    current += timedelta(days=1)
    while current <= end_date:
        if current.weekday() < 5:  # Monday=0, Friday=4
            count += 1
        current += timedelta(days=1)
    return count


# ── Stage A helper functions ───────────────────────────────────────────────────

def extract_questions(message: EmailMessage) -> list[str]:
    """Extract sentences that look like questions from a message body."""
    sentences = re.split(r'(?<=[.!?])\s+', message.body)
    questions = []
    for sent in sentences:
        sent_stripped = sent.strip()
        if not sent_stripped:
            continue
        if sent_stripped.endswith('?'):
            questions.append(sent_stripped)
            continue
        lower = sent_stripped.lower()
        if any(lower.startswith(s) for s in QUESTION_STARTERS):
            questions.append(sent_stripped)
    return questions


def is_substantive_response_to_any(question: str, later_messages: list[EmailMessage]) -> str:
    """
    Two-stage check: fast heuristic → LLM sub-call for ambiguous cases.
    Returns: "RESOLVED" | "UNRESOLVED" | "UNCERTAIN"
    """
    full_text = ' '.join(m.body.lower() for m in later_messages)

    # Stage 1a: High-confidence resolution signals
    if any(sig in full_text for sig in RESOLUTION_SIGNALS):
        return "RESOLVED"

    # Stage 1b: Only acknowledgment signals present → still stalled
    has_ack = any(ack in full_text for ack in ACKNOWLEDGMENT_ONLY)
    if has_ack and not any(sig in full_text for sig in RESOLUTION_SIGNALS):
        return "UNRESOLVED"

    # Stage 2: Insufficient signal either way → uncertain (will go to Stage B)
    if not later_messages:
        return "UNRESOLVED"

    return "UNCERTAIN"


def count_matches(text: str, signals: list[str]) -> int:
    return sum(1 for sig in signals if sig in text)


# ── Stage A: Rule engine ───────────────────────────────────────────────────────

def detect_stalled_candidates(thread: EmailThread,
                               reference_date: datetime = ANALYSIS_REFERENCE_DATE,
                               threshold_days: int = STALLED_THRESHOLD_DAYS) -> list[Candidate]:
    candidates = []
    for msg in thread.messages:
        if not msg.date:
            continue
        questions = extract_questions(msg)
        for q_text in questions:
            later = thread.messages_after(msg.date)
            resolution_status = is_substantive_response_to_any(q_text, later)

            if resolution_status == "RESOLVED":
                continue

            days_elapsed = business_days_between(msg.date, reference_date)
            if days_elapsed < threshold_days:
                continue

            confidence = "HIGH" if resolution_status == "UNRESOLVED" else "LOW"

            candidates.append(Candidate(
                flag_type="STALLED_DECISION",
                thread_id=thread.thread_id,
                project=thread.project,
                evidence=q_text[:400],
                confidence=confidence,
                raised_by=msg.sender_email,
                raised_date=msg.date,
                days_open=days_elapsed,
                subject=thread.subject,
            ))
    return candidates


def detect_scope_candidates(thread: EmailThread) -> list[Candidate]:
    candidates = []
    for msg in thread.messages:
        body_lower = msg.body.lower()
        has_primary = any(sig in body_lower for sig in SCOPE_SIGNALS_PRIMARY)
        has_secondary = any(sig in body_lower for sig in SCOPE_SIGNALS_SECONDARY)
        secondary_count = count_matches(body_lower, SCOPE_SIGNALS_SECONDARY)

        if has_primary or (has_secondary and secondary_count >= 2):
            confidence = "HIGH" if has_primary else "LOW"
            # Extract the triggering sentence as evidence
            sentences = re.split(r'(?<=[.!?])\s+', msg.body)
            evidence_sentences = [
                s for s in sentences
                if any(sig in s.lower() for sig in SCOPE_SIGNALS_PRIMARY + SCOPE_SIGNALS_SECONDARY)
            ]
            evidence = ' '.join(evidence_sentences[:2]) or msg.body[:300]

            candidates.append(Candidate(
                flag_type="UNCONTROLLED_SCOPE_CHANGE",
                thread_id=thread.thread_id,
                project=thread.project,
                evidence=evidence[:400],
                confidence=confidence,
                raised_by=msg.sender_email,
                raised_date=msg.date,
                days_open=None,
                subject=thread.subject,
            ))
    return candidates


def detect_incident_candidates(thread: EmailThread) -> list[Candidate]:
    candidates = []
    for msg in thread.messages:
        body_lower = msg.body.lower()
        subject_lower = thread.subject.lower()
        combined = body_lower + ' ' + subject_lower

        if any(sig in combined for sig in INCIDENT_SIGNALS):
            # Check if resolved later
            later = thread.messages_after(msg.date) if msg.date else []
            later_text = ' '.join(m.body.lower() for m in later)
            is_resolved = any(sig in later_text for sig in RESOLUTION_SIGNALS)

            candidates.append(Candidate(
                flag_type="OPERATIONAL_INCIDENT",
                thread_id=thread.thread_id,
                project=thread.project,
                evidence=msg.body[:400],
                confidence="HIGH",
                raised_by=msg.sender_email,
                raised_date=msg.date,
                days_open=None,
                subject=thread.subject,
            ))
            break  # one candidate per thread for incidents

    return candidates


def run_stage_a(threads: list[EmailThread]) -> list[Candidate]:
    """Run all Stage A detectors across all threads. Deduplicate per thread."""
    all_candidates = []
    seen = set()  # (thread_id, flag_type) dedup key

    for thread in threads:
        for detector in [detect_stalled_candidates, detect_scope_candidates, detect_incident_candidates]:
            for candidate in detector(thread):
                # STALLED: dedup by evidence (multiple questions per thread allowed)
                # SCOPE / INCIDENT: dedup by thread (one flag per thread type)
                if candidate.flag_type == "STALLED_DECISION":
                    # Hash full evidence to allow distinct stalled questions per thread
                    key = (candidate.thread_id, candidate.flag_type, hash(candidate.evidence))
                else:
                    key = (candidate.thread_id, candidate.flag_type)
                if key not in seen:
                    seen.add(key)
                    all_candidates.append(candidate)

    return all_candidates


# ── Stage B: LLM validator ────────────────────────────────────────────────────

def build_stage_b_prompt(candidate: Candidate, thread: EmailThread) -> str:
    # Build thread JSON (safe for LLM)
    thread_data = []
    for msg in thread.messages:
        thread_data.append({
            "message_id": msg.message_id,
            "from": msg.sender_email,
            "from_role": msg.sender_role,
            "date": msg.date.isoformat() if msg.date else None,
            "body": msg.body[:800],  # truncate very long messages
        })

    candidate_data = asdict(candidate)
    candidate_data['raised_date'] = candidate.raised_date.isoformat() if candidate.raised_date else None

    return f"""You are a delivery risk analyst validating a flag candidate for a Director of Engineering.
A deterministic rule engine has identified this as a POTENTIAL risk. Your task is to:
1. Confirm whether this is a genuine risk, a false positive, or uncertain.
2. Assess severity based on business impact.
3. Identify specific evidence supporting or refuting the flag.
4. Provide a recommended action.

TODAY'S DATE: {ANALYSIS_REFERENCE_DATE.date().isoformat()}
STALLED THRESHOLD: {STALLED_THRESHOLD_DAYS} business days
FLAG TYPE: {candidate.flag_type}
LANGUAGE NOTE: The thread may contain Hungarian text. Analyze it as-is; do not translate.
Hungarian resolution signals include: megoldva, kész, javítottam, már működik, törölve.
Hungarian acknowledgment-only signals include: megnézem, utánanézek, visszajelzek.

ANTI-HALLUCINATION RULES:
- Every conclusion must reference specific text from the thread.
- If the thread shows the issue was resolved AFTER the candidate was detected, mark confirmed=false.
- "I'll look into it" / "megnézem" = acknowledgment only, NOT resolution.
- Off-topic personal content (food, birthdays, social plans) is NEVER a flag.
- If you are uncertain, set confirmed="UNCERTAIN" — do NOT force a binary verdict.

CANDIDATE:
{json.dumps(candidate_data, default=str, indent=2)}

THREAD:
{json.dumps(thread_data, indent=2)}

Return ONLY valid JSON — no markdown, no preamble:
{{
  "confirmed": true or false or "UNCERTAIN",
  "false_positive_reason": "string or null",
  "uncertainty_reason": "string or null",
  "flag_type": "{candidate.flag_type}",
  "severity": "HIGH or MEDIUM or LOW",
  "confidence_score": 0.0,
  "summary": "one sentence for the Director",
  "evidence": "specific quote or observation from the thread",
  "days_open": null,
  "owner": "email address of responsible person or null",
  "status": "OPEN or RESOLVED_IN_QUARTER",
  "recommended_action": "specific, actionable instruction for the Director"
}}"""


def call_llm(prompt: str) -> tuple[Optional[dict], int]:
    """
    Call Claude Sonnet 4.6 via Anthropic API.
    Returns (parsed_json_dict, tokens_used). tokens_used is 0 on failure.
    """
    try:
        import anthropic
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return None, 0

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        tokens = response.usage.input_tokens + response.usage.output_tokens

        # Strip markdown code fences if present
        raw = re.sub(r'^```json\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)

        return json.loads(raw), tokens

    except ImportError:
        return None, 0
    except Exception as e:
        print(f"  LLM API error: {e}")
        return None, 0


def mock_stage_b(candidate: Candidate, thread: 'EmailThread' = None) -> dict:
    """
    Mock Stage B response when no API key is available.
    Checks thread content for resolution signals to set accurate status.
    """
    flag = candidate.flag_type

    if flag == "OPERATIONAL_INCIDENT":
        # Check all later messages in the thread for resolution signals
        is_resolved = False
        if thread and candidate.raised_date:
            later = thread.messages_after(candidate.raised_date)
            later_text = ' '.join(m.body.lower() for m in later)
            is_resolved = any(sig in later_text for sig in RESOLUTION_SIGNALS)
        else:
            # Fallback: check evidence text itself
            is_resolved = any(sig in candidate.evidence.lower() for sig in RESOLUTION_SIGNALS)

        return {
            "confirmed": True,
            "false_positive_reason": None,
            "uncertainty_reason": None,
            "flag_type": flag,
            "severity": "HIGH",
            "confidence_score": 0.85,
            "summary": f"Production incident in {candidate.project}: {candidate.subject[:60]}",
            "evidence": candidate.evidence[:200],
            "days_open": candidate.days_open,
            "owner": candidate.raised_by,
            "status": "RESOLVED_IN_QUARTER" if is_resolved else "OPEN",
            "recommended_action": (
                "Verify root cause was addressed and a post-mortem action item is tracked."
                if is_resolved else
                "Review incident — confirm resolution path and assign owner."
            ),
        }

    elif flag == "STALLED_DECISION":
        confirmed = candidate.confidence == "HIGH"
        return {
            "confirmed": confirmed,
            "false_positive_reason": None if confirmed else "Question appears resolved in thread context.",
            "uncertainty_reason": None if confirmed else "Resolution signals detected but context unclear.",
            "flag_type": flag,
            "severity": "HIGH" if (candidate.days_open or 0) > 14 else "MEDIUM",
            "confidence_score": 0.78 if confirmed else 0.55,
            "summary": f"Open question unresolved for {candidate.days_open} business days: {candidate.evidence[:80]}",
            "evidence": candidate.evidence[:200],
            "days_open": candidate.days_open,
            "owner": candidate.raised_by,
            "status": "OPEN",
            "recommended_action": f"Follow up with {candidate.raised_by} on this open question before the QBR.",
        }

    else:  # UNCONTROLLED_SCOPE_CHANGE
        confirmed = candidate.confidence == "HIGH"
        return {
            "confirmed": confirmed,
            "false_positive_reason": None if confirmed else "Phrase appears in context of normal discussion, not a scope change.",
            "uncertainty_reason": None,
            "flag_type": flag,
            "severity": "MEDIUM",
            "confidence_score": 0.72 if confirmed else 0.52,
            "summary": f"Potential untracked scope change in {candidate.project}: {candidate.evidence[:80]}",
            "evidence": candidate.evidence[:200],
            "days_open": None,
            "owner": candidate.raised_by,
            "status": "OPEN",
            "recommended_action": "Verify whether this change was formally logged and estimated.",
        }


def run_stage_b(candidates: list[Candidate],
                threads_by_id: dict[str, EmailThread],
                use_mock: bool = False) -> tuple[list[ConfirmedFlag], list[ConfirmedFlag], list[ConfirmedFlag], int]:
    """
    Validate each candidate with LLM or mock.
    Returns: (confirmed_flags, needs_review_flags, false_positive_flags, tokens_used)
    """
    confirmed = []
    needs_review = []
    false_positives = []
    stage_tokens = 0

    for candidate in candidates:
        thread = threads_by_id.get(candidate.thread_id)
        if not thread:
            continue

        if use_mock:
            result = mock_stage_b(candidate, thread)
        else:
            prompt = build_stage_b_prompt(candidate, thread)
            result, tokens = call_llm(prompt)
            stage_tokens += tokens
            if result is None:
                # API failed — route to needs_review
                result = mock_stage_b(candidate)
                result["confirmed"] = "UNCERTAIN"
                result["uncertainty_reason"] = "LLM API unavailable — manual review required."
                result["confidence_score"] = 0.0

        # Route by confidence
        is_uncertain = result.get("confirmed") == "UNCERTAIN"
        is_low_confidence = result.get("confidence_score", 1.0) < CONFIDENCE_THRESHOLD
        is_false_positive = result.get("confirmed") == False

        flag = ConfirmedFlag(
            flag_type=result.get("flag_type", candidate.flag_type),
            thread_id=candidate.thread_id,
            project=candidate.project,
            subject=candidate.subject,
            severity=result.get("severity", "MEDIUM"),
            confidence_score=result.get("confidence_score", 0.0),
            status=result.get("status", "OPEN"),
            summary=result.get("summary", ""),
            evidence=result.get("evidence", ""),
            owner=result.get("owner") or candidate.raised_by,
            recommended_action=result.get("recommended_action", ""),
            days_open=result.get("days_open") or candidate.days_open,
            false_positive_reason=result.get("false_positive_reason"),
        )

        if is_false_positive:
            false_positives.append(flag)
            reason = result.get('false_positive_reason', 'no reason given')[:80]
            print(f"  x False positive [{candidate.thread_id}] {candidate.flag_type}: {reason}")
        elif is_uncertain or is_low_confidence:
            flag.status = "NEEDS_PM_REVIEW"
            needs_review.append(flag)
            print(f"  ? Needs review [{candidate.thread_id}]: confidence={result.get('confidence_score', '?')}")
        else:
            confirmed.append(flag)
            print(f"  ✓ Confirmed [{candidate.thread_id}] {flag.flag_type} — {flag.severity}")

    return confirmed, needs_review, false_positives, stage_tokens


# ── Stage C: Cross-thread pattern analysis ────────────────────────────────────

def run_stage_c(confirmed_flags: list[ConfirmedFlag],
                project: str,
                use_mock: bool = False) -> list[dict]:
    """
    Find patterns across multiple threads within a project.
    Returns list of cross-thread pattern dicts.
    """
    if len(confirmed_flags) < 2:
        return []

    if use_mock:
        return _mock_stage_c(confirmed_flags, project)

    flag_summaries = [
        {
            "flag_type": f.flag_type,
            "thread_id": f.thread_id,
            "subject": f.subject,
            "summary": f.summary,
            "owner": f.owner,
            "severity": f.severity,
        }
        for f in confirmed_flags
    ]

    prompt = f"""You are analyzing ALL validated flag summaries for a single project to find risk patterns
that span multiple email threads. These patterns are invisible when threads are viewed in isolation.

Look for:
1. The same topic or client request appearing across multiple threads without formal resolution
2. The same participant appearing as a non-responder or bottleneck across multiple threads
3. A series of informal references that together imply an implicit commitment with no formal tracking
4. Any combination of individually-minor flags that collectively indicate systemic risk

STRICT RULES:
- A pattern requires evidence in AT LEAST 2 distinct thread IDs. Do not report single-thread patterns.
- Every pattern must cite specific thread IDs and evidence from each.
- If no genuine cross-thread patterns exist, return an empty array. Do not invent patterns.

Return ONLY valid JSON:
{{
  "cross_thread_patterns": [
    {{
      "pattern_type": "RECURRING_BLOCKER or IMPLICIT_COMMITMENT or SYSTEMIC_PROCESS_FAILURE or OTHER",
      "description": "one sentence for the Director",
      "threads_involved": ["thread_id_1", "thread_id_2"],
      "severity": "HIGH or MEDIUM or LOW",
      "recommended_action": "specific action for the Director"
    }}
  ]
}}

ALL VALIDATED FLAG SUMMARIES FOR PROJECT "{project}":
{json.dumps(flag_summaries, indent=2)}"""

    result, _ = call_llm(prompt)
    if result:
        return result.get("cross_thread_patterns", [])
    return _mock_stage_c(confirmed_flags, project)


def _mock_stage_c(flags: list[ConfirmedFlag], project: str) -> list[dict]:
    """Simple mock: detect same owner appearing in multiple STALLED_DECISION flags."""
    from collections import Counter
    owner_counts = Counter(f.owner for f in flags if f.flag_type == "STALLED_DECISION" and f.owner)
    patterns = []
    for owner, count in owner_counts.items():
        if count >= 2:
            threads = [f.thread_id for f in flags if f.owner == owner][:3]
            patterns.append({
                "pattern_type": "RECURRING_BLOCKER",
                "description": f"{owner} appears as unresponsive owner in {count} stalled threads in {project}.",
                "threads_involved": threads,
                "severity": "MEDIUM",
                "recommended_action": f"Discuss workload or communication issues with {owner} before the QBR.",
            })
    return patterns


# ── Public API ────────────────────────────────────────────────────────────────

def classify_threads(threads_by_project: dict[str, list[EmailThread]],
                     use_mock: bool = False) -> dict:
    """
    Run full A→B→C classification pipeline.
    Returns structured result dict ready for Stage D.
    """
    if not use_mock:
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            print("  No ANTHROPIC_API_KEY found — running in mock mode.")
            use_mock = True

    results = {}

    for project, threads in threads_by_project.items():
        print(f"\n[Stage A] {project} — {len(threads)} threads")

        # Noise filter (before Stage A)
        filtered_threads, noise_log = run_noise_filter(threads, use_mock)
        noise_count = len(threads) - len(filtered_threads)
        if noise_count > 0:
            print(f"  -> Noise filter: {noise_count} thread(s) excluded, {len(filtered_threads)} remaining")
        threads = filtered_threads
        threads_by_id = {t.thread_id: t for t in threads}

        # Stage A
        candidates = run_stage_a(threads)
        print(f"  -> {len(candidates)} candidates detected")

        # Stage B
        print(f"[Stage B] Validating {len(candidates)} candidates...")
        confirmed_flags, needs_review, false_positives, tokens_used = run_stage_b(candidates, threads_by_id, use_mock)

        # Stage C
        print(f"[Stage C] Cross-thread patterns for {project}...")
        patterns = run_stage_c(confirmed_flags, project, use_mock)
        if patterns:
            print(f"  -> {len(patterns)} pattern(s) found")
        else:
            print(f"  → No cross-thread patterns found")

        results[project] = {
            "threads_analyzed": len(threads),
            "threads_noise_filtered": noise_count,
            "confirmed_flags": confirmed_flags,
            "needs_review": needs_review,
            "false_positives": false_positives,
            "tokens_used": tokens_used,
            "cross_thread_patterns": patterns,
            "noise_log": noise_log,
        }

    return results
