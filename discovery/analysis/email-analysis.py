"""
Email Analysis Script — Discovery Tool
Generates a static HTML report from the provided email data.
FOR INTERNAL USE ONLY — not a submission artifact.

Run from project root:
    py -3 discovery/analysis/email-analysis.py

Output: discovery/analysis/email-analysis-report.html
"""

import os
import re
from datetime import datetime
from collections import defaultdict

# ── Config ────────────────────────────────────────────────────────────────────
INPUT_DIR = os.path.join(os.path.dirname(__file__), "../../input/AI_Developer_files")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "email-analysis-report.html")

# ── Classifiers ───────────────────────────────────────────────────────────────
# Ordered by specificity — first match wins
PROJECT_KEYWORDS = {
    "Project Phoenix": [
        "phoenix", "login page", "jira-112", "staging environment",
        "ci/cd pipeline", "profile picture", "kovacs.peter@kisjozsitech",
        "varga.zsuzsa@kisjozsitech", "nagy.istvan@kisjozsitech",
        "kiss.anna@kisjozsitech", "horvath.gabor@kisjozsitech",
        "szabo.eszter@kisjozsitech", "new login page",
    ],
    "DivatKirály": [
        "divatkirály", "divatkir", "barion", "zeplin", "sku",
        "newsletter", "gdpr", "webshop", "divat", "divatkiraly",
        "anna.nagy@kisjozsitech", "gabor.kiss@kisjozsitech",
        "bence.szab", "zsofia.varga@kisjozsitech",
        "eszter.horvath@kisjozsitech", "solar panel",
    ],
    "E-commerce (KisJózsiTech)": [
        "weekly status", "product list", "product page",
        "payment gateway", "csv", "report export",
        "gabor.nagy@kisjozsitech", "eszter.varga@kisjozsitech",
        "peter.kovacs@kisjozsitech", "bence.toth@kisjozsitech",
        "anna.horvath@kisjozsitech", "zoltan.kiss@kisjozsitech",
        "cannot log in", "user profile page", "friday surprise",
        "registration module", "homepage design",
    ],
}

ISSUE_KEYWORDS = {
    "Bug / Technical Issue": [
        "bug", "error", "anomaly", "not working", "broken", "fix",
        "404", "cache", "wrong", "faulty", "mistake", "acting up",
        "doesn't work", "issue",
    ],
    "Scope Creep": [
        "nice to have", "new requirement", "wasn't included",
        "not in the estimate", "extra development", "new ticket",
        "not in the current specification", "not in the spec",
        "not mentioned in", "came up", "we also need",
        "could we implement", "would it be possible",
    ],
    "Blocker / Dependency": [
        "blocked", "stuck", "can't proceed", "pending", "waiting for",
        "slipped", "forgot", "still pending", "sidelined",
        "sidetracked", "my question is still open", "cannot continue",
        "can't continue", "can i not proceed",
    ],
    "Compliance / Legal": [
        "gdpr", "legal", "compliance", "terms and conditions",
        "cannot be checked", "data protection", "must be unchecked",
        "by default", "regulation",
    ],
    "Spec Gap": [
        "specification", "spec", "not mentioned", "unclear",
        "doesn't mention", "not in the description", "undocumented",
        "not documented", "not specified", "missing from the spec",
        "spec doesn't", "not clear",
    ],
    "Process / Communication": [
        "wrong thread", "not meant for here", "apologies, this",
        "sorry, this", "organize in a different thread",
        "separate email", "separate conversation", "not for here",
        "got lost", "information will get lost",
    ],
    "Production Incident": [
        "production server", "live since", "client cannot log in",
        "all hands on deck", "login is not working live",
        "wrong environment variable", "db connection string",
        "fix is out",
    ],
}

TOOL_KEYWORDS = {
    "Jira":    ["jira", "jira-"],
    "GitHub":  ["github", "commit", "push", "branch", "pull request"],
    "Zeplin":  ["zeplin"],
    "Barion":  ["barion"],
    "CI/CD":   ["ci/cd", "pipeline", "pre-commit hook", "deploy script", "deployment"],
    "Staging": ["staging", "test environment"],
}

NOISE_KEYWORDS = [
    "lunch", "pizza", "mexican", "cake", "birthday", "marzipan",
    "chocolate", "fried chicken", "mashed potato", "restaurant",
    "food", "wine", "gadget", "gift", "chip in", "surprise",
    "pastry", "booking for", "weekly menu",
]

# ── Parsers ───────────────────────────────────────────────────────────────────
def parse_emails(filepath):
    with open(filepath, encoding="utf-8", errors="replace") as f:
        content = f.read()

    messages = []
    blocks = re.split(r'\n(?=From: )', content.strip())
    for block in blocks:
        if not block.strip():
            continue
        msg = {}

        def extract(pattern):
            m = re.search(pattern, block, re.M)
            raw = m.group(1).strip() if m else ""
            return re.sub(r'^[A-Za-z\-]+:\s*', '', raw).strip()

        msg["from"]     = extract(r'^From:\s*(.+)')
        msg["to"]       = extract(r'^To:\s*(.+)')
        msg["subject"]  = extract(r'^Subject:\s*(.+)')
        msg["date_raw"] = extract(r'^Date:\s*(.+)')

        msg["date"] = None
        for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%Y.%m.%d %H:%M", "%Y.%m.%d %H:%M:%S"):
            try:
                msg["date"] = datetime.strptime(msg["date_raw"].strip(), fmt)
                break
            except Exception:
                pass

        body_match = re.search(r'\n\n(.+)', block, re.DOTALL)
        msg["body"] = body_match.group(1).strip() if body_match else ""
        msg["full_text"] = (block).lower()  # use entire block for matching
        msg["file"] = os.path.basename(filepath)
        messages.append(msg)
    return messages

def classify_project(msg):
    text = msg["full_text"]
    for project, keywords in PROJECT_KEYWORDS.items():
        if any(k in text for k in keywords):
            return project
    return "Unknown / Cross-project"

def classify_project_thread(msgs):
    """Classify a thread by checking ALL messages, not just the first."""
    for msg in msgs:
        result = classify_project(msg)
        if result != "Unknown / Cross-project":
            return result
    return "Unknown / Cross-project"

def classify_issues(msg):
    text = msg["full_text"]
    return [t for t, keywords in ISSUE_KEYWORDS.items() if any(k in text for k in keywords)]

def find_tools(msg):
    text = msg["full_text"]
    return [tool for tool, keywords in TOOL_KEYWORDS.items() if any(k in text for k in keywords)]

def is_noise(msg):
    return any(k in msg["full_text"] for k in NOISE_KEYWORDS)

# ── Main analysis ─────────────────────────────────────────────────────────────
def analyze():
    all_messages = []
    for fname in sorted(os.listdir(INPUT_DIR)):
        if fname.endswith(".txt") and fname != "Colleagues.txt":
            all_messages += parse_emails(os.path.join(INPUT_DIR, fname))

    total = len(all_messages)
    noise_msgs = [m for m in all_messages if is_noise(m)]

    project_counts = defaultdict(int)
    for m in all_messages:
        project_counts[classify_project(m)] += 1

    issue_counts = defaultdict(int)
    for m in all_messages:
        for issue in classify_issues(m):
            issue_counts[issue] += 1

    tool_counts = defaultdict(int)
    for m in all_messages:
        for tool in find_tools(m):
            tool_counts[tool] += 1

    thread_stats = []
    zero_reply_threads = []
    for fname in sorted(os.listdir(INPUT_DIR)):
        if fname.endswith(".txt") and fname != "Colleagues.txt":
            msgs = parse_emails(os.path.join(INPUT_DIR, fname))
            # Filter out ghost blocks (no from, no subject, no body)
            real_msgs = [m for m in msgs if m["from"] or m["subject"]]
            dated = [m for m in real_msgs if m["date"]]
            if len(dated) >= 2:
                dated.sort(key=lambda m: m["date"])
                gap = dated[-1]["date"] - dated[0]["date"]
                days = gap.days
            else:
                days = 0
            subjects = list({m["subject"][:55] for m in real_msgs if m["subject"]})
            project = classify_project_thread(real_msgs)
            thread_stats.append({
                "file":      fname,
                "messages":  len(real_msgs),
                "days_span": days,
                "subject":   subjects[0] if subjects else "—",
                "noise":     sum(1 for m in real_msgs if is_noise(m)),
                "project":   project,
            })
            # Flag threads with only 1 real, non-noise message (unanswered)
            non_noise = [m for m in real_msgs if not is_noise(m)]
            if len(non_noise) == 1 and non_noise[0]["subject"]:
                zero_reply_threads.append({
                    "file":    fname,
                    "project": project,
                    "subject": non_noise[0]["subject"][:70],
                    "from":    non_noise[0]["from"][:40],
                })
    thread_stats.sort(key=lambda t: t["days_span"], reverse=True)

    # Blocker threads = noise-free threads with 14d+ gap
    unresolved = [t for t in thread_stats if t["days_span"] >= 14 and t["noise"] == 0]

    return {
        "total": total,
        "noise_count": len(noise_msgs),
        "noise_pct": round(len(noise_msgs) / total * 100) if total else 0,
        "project_counts": dict(sorted(project_counts.items(), key=lambda x: -x[1])),
        "issue_counts": dict(sorted(issue_counts.items(), key=lambda x: -x[1])),
        "tool_counts": dict(sorted(tool_counts.items(), key=lambda x: -x[1])),
        "thread_stats": thread_stats,
        "unresolved": unresolved,
        "zero_reply": zero_reply_threads,
    }

# ── HTML generation ───────────────────────────────────────────────────────────
COLORS = {
    "project": "#4f8ef7",
    "issue":   "#e05c5c",
    "tool":    "#5cb85c",
    "warn":    "#f0ad4e",
}

def bar(value, max_val, color):
    pct = int(value / max_val * 100) if max_val else 0
    return (f'<div style="background:#eee;border-radius:4px;height:18px;width:100%;">'
            f'<div style="background:{color};width:{pct}%;height:18px;border-radius:4px;"></div></div>')

def render_html(data):
    max_issue = max(data["issue_counts"].values(), default=1)
    max_tool  = max(data["tool_counts"].values(), default=1)
    max_proj  = max(data["project_counts"].values(), default=1)

    issue_rows = "".join(
        f'<tr><td>{k}</td><td style="width:50%">{bar(v,max_issue,COLORS["issue"])}</td><td><b>{v}</b></td></tr>'
        for k, v in data["issue_counts"].items()
    )
    tool_rows = "".join(
        f'<tr><td>{k}</td><td style="width:50%">{bar(v,max_tool,COLORS["tool"])}</td><td><b>{v}</b></td></tr>'
        for k, v in data["tool_counts"].items()
    )
    proj_rows = "".join(
        f'<tr><td>{k}</td><td style="width:50%">{bar(v,max_proj,COLORS["project"])}</td><td><b>{v}</b></td></tr>'
        for k, v in data["project_counts"].items()
    )
    thread_rows = "".join(
        f'<tr><td>{t["file"]}</td><td>{t["project"]}</td>'
        f'<td>{t["subject"]}</td><td>{t["messages"]}</td>'
        f'<td><b style="color:{"#e05c5c" if t["days_span"]>=14 else "#333"}">{t["days_span"]}d</b></td>'
        f'<td>{"⚠️ " + str(t["noise"]) if t["noise"] else "—"}</td></tr>'
        for t in data["thread_stats"]
    )
    unresolved_rows = "".join(
        f'<tr><td>⚠️ {t["file"]}</td><td>{t["project"]}</td><td>{t["subject"]}</td><td><b>{t["days_span"]}d</b></td></tr>'
        for t in data["unresolved"]
    ) or '<tr><td colspan="4" style="color:#888">None detected</td></tr>'

    zero_reply_rows = "".join(
        f'<tr><td>🔴 {t["file"]}</td><td>{t["project"]}</td><td>{t["subject"]}</td><td>{t["from"]}</td></tr>'
        for t in data["zero_reply"]
    ) or '<tr><td colspan="4" style="color:#888">None detected</td></tr>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Email Data Discovery Report</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin:0; background:#f5f7fa; color:#333; }}
  .container {{ max-width:1000px; margin:40px auto; padding:0 20px; }}
  h1 {{ color:#1a1a2e; border-bottom:3px solid #4f8ef7; padding-bottom:10px; }}
  h2 {{ color:#555; margin-top:40px; font-size:1em; text-transform:uppercase; letter-spacing:1px; }}
  .kpi-grid {{ display:grid; grid-template-columns:repeat(5,1fr); gap:16px; margin:24px 0; }}
  .kpi {{ background:white; border-radius:8px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,0.08); text-align:center; }}
  .kpi .value {{ font-size:2.2em; font-weight:700; color:#4f8ef7; }}
  .kpi .label {{ font-size:0.85em; color:#888; margin-top:4px; }}
  .kpi.warn .value {{ color:#e05c5c; }}
  table {{ width:100%; border-collapse:collapse; background:white; border-radius:8px; overflow:hidden; box-shadow:0 1px 4px rgba(0,0,0,0.08); margin-bottom:32px; }}
  th {{ background:#1a1a2e; color:white; padding:10px 14px; text-align:left; font-size:0.85em; }}
  td {{ padding:9px 14px; border-bottom:1px solid #f0f0f0; font-size:0.9em; vertical-align:middle; }}
  tr:last-child td {{ border-bottom:none; }}
  .note {{ background:#fffbea; border-left:4px solid #f0ad4e; padding:12px 16px; border-radius:4px; font-size:0.9em; margin-bottom:24px; }}
  .insight {{ background:#e8f4fd; border-left:4px solid #4f8ef7; padding:12px 16px; border-radius:4px; font-size:0.9em; margin-bottom:24px; }}
</style>
</head>
<body>
<div class="container">
  <h1>Email Data — Discovery Analysis Report</h1>
  <p style="color:#888;font-size:0.9em;">Internal use only &middot; Generated {datetime.now().strftime("%Y-%m-%d %H:%M")} &middot; Source: input/AI_Developer_files/</p>
  <div class="note">This report is for understanding the raw data before designing the solution. It is <strong>not</strong> a submission artifact.</div>

  <h2>Summary KPIs</h2>
  <div class="kpi-grid">
    <div class="kpi"><div class="value">{data["total"]}</div><div class="label">Total messages parsed</div></div>
    <div class="kpi"><div class="value">{len(data["project_counts"])}</div><div class="label">Projects detected</div></div>
    <div class="kpi warn"><div class="value">{data["noise_count"]}</div><div class="label">Noise messages ({data["noise_pct"]}%)</div></div>
    <div class="kpi warn"><div class="value">{len(data["unresolved"])}</div><div class="label">Threads with 14d+ gap (blockers)</div></div>
    <div class="kpi warn"><div class="value">{len(data["zero_reply"])}</div><div class="label">Unanswered requests (0 replies)</div></div>
  </div>

  <h2>Messages by Project</h2>
  <table><tr><th>Project</th><th>Distribution</th><th>Count</th></tr>{proj_rows}</table>

  <h2>Issue Types Detected</h2>
  <div class="insight">Note: a single message can match multiple issue types. Counts represent message-level matches, not unique incidents.</div>
  <table><tr><th>Issue Type</th><th>Frequency</th><th>Matches</th></tr>{issue_rows}</table>

  <h2>Tools Mentioned in Emails</h2>
  <div class="insight">These are tools the teams are already using. Each represents a potential integration point for the QBR system.</div>
  <table><tr><th>Tool</th><th>Frequency</th><th>Mentions</th></tr>{tool_rows}</table>

  <h2>Potential Blockers (threads with 14d+ gap)</h2>
  <table>
    <tr><th>File</th><th>Project</th><th>Subject</th><th>Duration</th></tr>
    {unresolved_rows}
  </table>

  <h2>Unanswered Requests (0 replies — no Jira ticket found)</h2>
  <div class="insight">These are single-message threads with no response. They represent decisions or requests that have been completely ignored and are at highest risk of falling through the cracks.</div>
  <table>
    <tr><th>File</th><th>Project</th><th>Subject</th><th>Sender</th></tr>
    {zero_reply_rows}
  </table>

  <h2>All Thread Analysis</h2>
  <table>
    <tr><th>File</th><th>Project</th><th>Subject</th><th>Msgs</th><th>Duration</th><th>Noise</th></tr>
    {thread_rows}
  </table>
</div>
</body>
</html>"""

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Analyzing emails...")
    data = analyze()
    html = render_html(data)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nResults:")
    print(f"  Total messages : {data['total']}")
    print(f"  Noise messages : {data['noise_count']} ({data['noise_pct']}%)")
    print(f"  Projects found : {list(data['project_counts'].keys())}")
    print(f"  Tools found    : {list(data['tool_counts'].keys())}")
    print(f"  Blocker threads: {len(data['unresolved'])}")
    print(f"\nReport written to: {OUTPUT_FILE}")
