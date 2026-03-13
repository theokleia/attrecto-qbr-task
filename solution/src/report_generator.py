"""
report_generator.py — QBR Automation System
Stage D: Portfolio Report Generator

Takes confirmed flags and cross-thread patterns from Stages A-C and
produces a structured Markdown QBR Portfolio Health Report.
"""

import json
import os
from datetime import datetime
from typing import Optional

from ai_classifier import ConfirmedFlag, ANALYSIS_REFERENCE_DATE


# ── Severity ordering ─────────────────────────────────────────────────────────

SEVERITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

FLAG_TYPE_LABELS = {
    "STALLED_DECISION": "Stalled Decision",
    "UNCONTROLLED_SCOPE_CHANGE": "Uncontrolled Scope Change",
    "OPERATIONAL_INCIDENT": "Operational Incident",
}


# ── LLM-powered report generation (Stage D) ───────────────────────────────────

def call_llm_for_report(project_summaries: dict, use_mock: bool = False) -> Optional[str]:
    """
    Use LLM to generate the executive summary and narrative sections.
    Returns markdown string or None.
    """
    if use_mock:
        return None

    try:
        import anthropic
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return None

        # Build condensed summaries for the prompt
        condensed = {}
        for project, data in project_summaries.items():
            flags = data.get("confirmed_flags", [])
            condensed[project] = {
                "open_flags": [
                    {
                        "type": f.flag_type,
                        "severity": f.severity,
                        "summary": f.summary,
                        "owner": f.owner,
                        "recommended_action": f.recommended_action,
                    }
                    for f in flags if f.status != "RESOLVED_IN_QUARTER"
                ],
                "incidents": [
                    {
                        "summary": f.summary,
                        "status": f.status,
                        "days_open": f.days_open,
                    }
                    for f in flags if f.flag_type == "OPERATIONAL_INCIDENT"
                ],
            }

        prompt = f"""You are preparing a QBR Portfolio Health Report for a Director of Engineering.
This Director is technical, time-constrained, and needs to make fast, accurate decisions.

Write ONLY the Executive Summary section (2-3 sentences): portfolio health overview and single most critical concern.
Be direct. No filler. Reference specific projects and issues.

Portfolio data:
{json.dumps(condensed, indent=2)}

Return ONLY the executive summary text, no headers, no JSON."""

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=400,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()

    except Exception:
        return None


# ── Markdown builders ─────────────────────────────────────────────────────────

def deduplicate_flags(flags: list) -> list:
    """Remove flags from the same thread with the same flag type, keeping the first (highest severity after sort)."""
    seen = set()
    result = []
    for flag in flags:
        key = (flag.thread_id, flag.flag_type)
        if key not in seen:
            seen.add(key)
            result.append(flag)
    return result


def flag_confidence_label(flag: ConfirmedFlag) -> str:
    if flag.confidence_score >= 0.85:
        return "[Rule+LLM-confirmed]"
    elif flag.confidence_score >= 0.70:
        return "[LLM-confirmed]"
    else:
        return "[Needs PM Review]"


def render_flag_block(flag: ConfirmedFlag) -> str:
    lines = []
    label = flag_confidence_label(flag)
    lines.append(f"**{FLAG_TYPE_LABELS.get(flag.flag_type, flag.flag_type)}** — "
                 f"`{flag.severity}` {label}")
    lines.append(f"> {flag.summary}")
    if flag.evidence:
        lines.append(f"**Evidence:** _{flag.evidence[:200]}_")
    if flag.days_open:
        lines.append(f"**Days open:** {flag.days_open} business days")
    if flag.owner:
        lines.append(f"**Owner:** {flag.owner}")
    lines.append(f"**Action:** {flag.recommended_action}")
    return '\n'.join(lines)


def render_incident_block(flag: ConfirmedFlag) -> str:
    status_label = "✅ Resolved" if flag.status == "RESOLVED_IN_QUARTER" else "🔴 Open"
    lines = [
        f"**{flag.subject}** — {status_label}",
        f"> {flag.summary}",
    ]
    if flag.evidence:
        lines.append(f"_{flag.evidence[:200]}_")
    if flag.recommended_action:
        lines.append(f"**Action:** {flag.recommended_action}")
    return '\n'.join(lines)


def classify_project_health(flags: list[ConfirmedFlag]) -> str:
    """
    Classify project as RED / AMBER / GREEN based on open flags.
    An open OPERATIONAL_INCIDENT also elevates to RED — a project with an active
    production incident or compliance violation is never GREEN.
    """
    open_flags = [f for f in flags if f.status not in ("RESOLVED_IN_QUARTER", "NEEDS_PM_REVIEW")]
    open_non_incidents = [f for f in open_flags if f.flag_type != "OPERATIONAL_INCIDENT"]
    open_incidents = [f for f in open_flags if f.flag_type == "OPERATIONAL_INCIDENT"]

    if any(f.severity == "HIGH" for f in open_non_incidents):
        return "RED"
    if open_incidents:  # any open incident = at minimum AMBER; HIGH severity = RED
        return "RED" if any(f.severity == "HIGH" for f in open_incidents) else "AMBER"
    if open_non_incidents:
        return "AMBER"
    return "GREEN"


# ── Main report generator ─────────────────────────────────────────────────────

def generate_report(classification_results: dict,
                    quarter_label: str = "Q2 2025",
                    use_mock: bool = False) -> str:
    """
    Generate the full QBR Portfolio Health Report as a Markdown string.
    """
    now = datetime.now()
    total_open = 0
    total_needs_review = 0
    project_count = len(classification_results)

    # Pre-compute per-project health
    project_health = {}
    for project, data in classification_results.items():
        confirmed = data.get("confirmed_flags", [])
        needs_review = data.get("needs_review", [])
        health = classify_project_health(confirmed)
        project_health[project] = health
        total_open += sum(1 for f in confirmed if f.status == "OPEN")
        total_needs_review += len(needs_review)

    # Try LLM executive summary
    exec_summary = call_llm_for_report(classification_results, use_mock)
    if not exec_summary:
        # Fallback: generate deterministically
        red_projects = [p for p, h in project_health.items() if h == "RED"]
        amber_projects = [p for p, h in project_health.items() if h == "AMBER"]
        if red_projects:
            exec_summary = (
                f"Portfolio review for {quarter_label} identified {total_open} open flags "
                f"across {project_count} projects. "
                f"{', '.join(red_projects)} require{'s' if len(red_projects) == 1 else ''} "
                f"immediate attention due to high-severity open issues. "
                f"{total_needs_review} items are pending PM validation before the QBR."
            )
        else:
            exec_summary = (
                f"Portfolio review for {quarter_label}: {total_open} open flags across "
                f"{project_count} projects. No critical blockers detected. "
                f"{total_needs_review} items pending PM review."
            )

    lines = []

    # ── Header ──
    lines += [
        "# QBR Portfolio Health Report",
        f"**Period:** {quarter_label}  ",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')}  ",
        f"**Projects Reviewed:** {project_count} | "
        f"**Open Flags:** {total_open} | "
        f"**Needs Review:** {total_needs_review}",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        exec_summary,
        "",
        "---",
        "",
    ]

    # ── RED: Immediate Attention Required ──
    red_projects = {p: d for p, d in classification_results.items() if project_health[p] == "RED"}
    if red_projects:
        lines += ["## 🔴 Immediate Attention Required", ""]
        for project, data in red_projects.items():
            flags = data.get("confirmed_flags", [])
            open_flags = [f for f in flags
                          if f.flag_type != "OPERATIONAL_INCIDENT"
                          and f.status != "RESOLVED_IN_QUARTER"]
            open_flags.sort(key=lambda f: SEVERITY_ORDER.get(f.severity, 99))
            open_flags = deduplicate_flags(open_flags)

            lines += [f"### {project}", ""]
            for flag in open_flags:
                lines += [render_flag_block(flag), ""]
        lines += ["---", ""]

    # ── AMBER: Monitor Closely ──
    amber_projects = {p: d for p, d in classification_results.items() if project_health[p] == "AMBER"}
    if amber_projects:
        lines += ["## 🟡 Monitor Closely", ""]
        for project, data in amber_projects.items():
            flags = data.get("confirmed_flags", [])
            open_flags = [f for f in flags
                          if f.flag_type != "OPERATIONAL_INCIDENT"
                          and f.status != "RESOLVED_IN_QUARTER"]
            open_flags.sort(key=lambda f: SEVERITY_ORDER.get(f.severity, 99))
            open_flags = deduplicate_flags(open_flags)

            lines += [f"### {project}", ""]
            for flag in open_flags:
                lines += [render_flag_block(flag), ""]
        lines += ["---", ""]

    # ── GREEN: On Track ──
    green_projects = [p for p, h in project_health.items() if h == "GREEN"]
    if green_projects:
        lines += ["## 🟢 On Track", ""]
        for project in green_projects:
            lines.append(f"- **{project}** — No open attention flags this quarter.")
        lines += ["", "---", ""]

    # ── Incidents This Quarter ──
    all_incidents = []
    for project, data in classification_results.items():
        for flag in data.get("confirmed_flags", []):
            if flag.flag_type == "OPERATIONAL_INCIDENT":
                all_incidents.append((project, flag))

    if all_incidents:
        lines += ["## Incidents This Quarter", ""]
        for project, flag in all_incidents:
            lines += [f"**[{project}]** {render_incident_block(flag)}", ""]
        lines += ["---", ""]

    # ── Cross-Project Patterns ──
    all_patterns = []
    for project, data in classification_results.items():
        for p in data.get("cross_thread_patterns", []):
            all_patterns.append((project, p))

    if all_patterns:
        lines += ["## Cross-Project Patterns", ""]
        for project, pattern in all_patterns:
            severity = pattern.get("severity", "MEDIUM")
            evidence = pattern.get("evidence", {})
            evidence_lines = [f"  - `{tid}`: {ref}" for tid, ref in evidence.items()] if evidence else []
            pattern_lines = [
                f"**[{project}] {pattern.get('pattern_type', 'Pattern')}** — `{severity}`",
                f"> {pattern.get('description', '')}",
                f"**Threads:** {', '.join(pattern.get('threads_involved', []))}",
            ]
            if evidence_lines:
                pattern_lines += ["**Evidence:**"] + evidence_lines
            pattern_lines += [f"**Action:** {pattern.get('recommended_action', '')}", ""]
            lines += pattern_lines
        lines += ["---", ""]

    # ── Needs PM Review ──
    all_needs_review_raw = []
    for project, data in classification_results.items():
        for flag in data.get("needs_review", []):
            all_needs_review_raw.append((project, flag))

    # Deduplicate by (thread_id, flag_type) — same logic as confirmed sections
    seen_nr = set()
    all_needs_review = []
    for project, flag in all_needs_review_raw:
        key = (flag.thread_id, flag.flag_type)
        if key not in seen_nr:
            seen_nr.add(key)
            all_needs_review.append((project, flag))

    if all_needs_review:
        lines += [
            "## 🔵 Needs PM Review",
            "",
            "_The items below were detected by the rule engine but could not be confirmed "
            "with high confidence. Please review with the relevant PM before the QBR._",
            "",
        ]
        for project, flag in all_needs_review:
            lines += [
                f"**[{project}]** {FLAG_TYPE_LABELS.get(flag.flag_type, flag.flag_type)} — "
                f"[Unvalidated, confidence: {flag.confidence_score:.0%}]",
                f"> {flag.summary}",
                f"**Evidence:** _{flag.evidence[:150]}_",
                "",
            ]
        lines += ["---", ""]

    # ── Recommended Director Actions ──
    action_flags = []
    for project, data in classification_results.items():
        for flag in data.get("confirmed_flags", []):
            if flag.status == "OPEN" and flag.recommended_action:
                action_flags.append((flag.severity, project, flag))

    action_flags.sort(key=lambda x: SEVERITY_ORDER.get(x[0], 99))

    if action_flags:
        lines += ["## Recommended Director Actions", ""]
        seen_actions = set()
        action_num = 1
        for _, project, flag in action_flags:
            # Deduplicate: use (project, flag_type, subject) as key
            action_key = (project, flag.flag_type, flag.subject[:40])
            if action_key in seen_actions:
                continue
            seen_actions.add(action_key)
            lines.append(
                f"{action_num}. **[{project} — {flag.subject[:50]}]** {flag.recommended_action}"
            )
            action_num += 1
            if action_num > 12:
                break
        lines += ["", "---", ""]

    # ── Footer ──
    lines += [
        "⚠️ **AI-GENERATED REPORT** — Validate flagged items with responsible PMs before acting.",
        f"Generated by QBR Portfolio Health Analyzer v2.2 | Model: claude-sonnet-4-6",
        f"Run date: {now.strftime('%Y-%m-%d %H:%M')}",
    ]

    return '\n'.join(lines)


if __name__ == '__main__':
    print("report_generator.py — import and call generate_report() to use.")
