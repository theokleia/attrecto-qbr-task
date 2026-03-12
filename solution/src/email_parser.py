"""
email_parser.py — QBR Automation System
Parses project email .txt files into structured thread objects.

Handles:
- Format A: RFC-style headers (From: Name <email>, RFC 2822 dates)
- Format B: Parenthetical headers (From: Name (email), YYYY.MM.DD HH:MM dates)
- Format C: Bare headers (From: Name email, no brackets)
- UTF-8 with Hungarian characters (ő, ú, á, é, etc.)
- Multiple messages per file separated by blank lines
"""

import re
import os
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


# ── Data classes ────────────────────────────────────────────────────────────

@dataclass
class EmailMessage:
    message_id: str
    thread_id: str
    sender_email: str
    sender_name: str
    sender_role: str          # from Colleagues.txt or "[inferred]"
    to_emails: list[str]
    cc_emails: list[str]
    date: Optional[datetime]
    subject: str
    body: str
    project: str              # inferred from subject
    raw_headers: dict


@dataclass
class EmailThread:
    thread_id: str
    subject: str
    project: str
    messages: list[EmailMessage] = field(default_factory=list)
    participants: set[str] = field(default_factory=set)

    @property
    def first_date(self) -> Optional[datetime]:
        dated = [m for m in self.messages if m.date]
        return min(dated, key=lambda m: m.date).date if dated else None

    @property
    def last_date(self) -> Optional[datetime]:
        dated = [m for m in self.messages if m.date]
        return max(dated, key=lambda m: m.date).date if dated else None

    def messages_after(self, dt: datetime) -> list[EmailMessage]:
        """Messages after dt. Compares dates after stripping timezone info."""
        def _naive(d):
            if d and d.tzinfo is not None:
                from datetime import timezone
                return d.astimezone(timezone.utc).replace(tzinfo=None)
            return d
        dt_naive = _naive(dt)
        return [m for m in self.messages if m.date and _naive(m.date) > dt_naive]


# ── Header format regexes ────────────────────────────────────────────────────

# Format A: Name <email>
RE_EMAIL_ANGLE = re.compile(r'([^<]+?)\s*<([^>]+)>')
# Format B: Name (email)
RE_EMAIL_PAREN = re.compile(r'(.+?)\s*\(([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})\)')
# Format C: Name email (bare, no brackets)
RE_EMAIL_BARE = re.compile(r'^(.+?)\s+([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})\s*$')
# Standalone email anywhere in a string
RE_EMAIL_ANYWHERE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

# Date formats
RE_DATE_RFC = re.compile(
    r'(\w{3},\s+\d{1,2}\s+\w{3}\s+\d{4}\s+\d{2}:\d{2}:\d{2}\s+[+-]\d{4})'
)
RE_DATE_HU = re.compile(r'(\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2})')

DATE_FORMATS = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%Y.%m.%d %H:%M",
]

# Known header field names
HEADER_FIELDS = {'from', 'to', 'cc', 'date', 'subject', 'reply-to', 'message-id'}

# Project detection from subject
PROJECT_PATTERNS = [
    (re.compile(r'Project Phoenix', re.IGNORECASE), 'Project Phoenix'),
    (re.compile(r'DivatKirály|DivatKiraly|divatkiraly', re.IGNORECASE), 'DivatKirály'),
]


# ── Colleagues directory loader ───────────────────────────────────────────────

def load_colleagues(colleagues_path: str) -> tuple[dict[str, dict], dict[str, str]]:
    """
    Returns:
      directory: {email: {name, role}} for all known team members
      participant_project_map: {email: project_name} inferred from team groupings

    The Colleagues.txt lists team members in project order. Each new "Project Manager"
    entry marks the start of a new project team. The first PM's team is assigned
    to the first project name found in any email subject.
    """
    directory = {}
    participant_project_map = {}

    if not os.path.exists(colleagues_path):
        return directory, participant_project_map

    with open(colleagues_path, encoding='utf-8') as f:
        content = f.read()

    # Pattern: Role: Name (email)
    pattern = re.compile(
        r'([A-Za-zÀ-ÖØ-öø-ÿ /\(\)]+?):\s+([A-Za-zÀ-ÖØ-öø-ÿ\s]+?)\s+\(([^)]+)\)'
    )

    # Split into project groups: each "Project Manager" entry starts a new group
    groups: list[list[str]] = []  # list of email lists per group
    current_group: list[str] = []

    for match in pattern.finditer(content):
        role, name, email = match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
        email_lower = email.lower()
        directory[email_lower] = {'name': name, 'role': role}

        # New project group starts at each "Project Manager" entry
        if 'project manager' in role.lower():
            if current_group:
                groups.append(current_group)
            current_group = [email_lower]
        else:
            current_group.append(email_lower)

    if current_group:
        groups.append(current_group)

    # Map group indices to project names based on known project patterns
    # Group 0 → Project Phoenix (first PM team)
    # Groups 1+ → DivatKirály (subsequent teams in the sample data)
    project_names = ['Project Phoenix', 'DivatKirály', 'DivatKirály']
    for i, group in enumerate(groups):
        project = project_names[i] if i < len(project_names) else 'Unknown'
        for email in group:
            participant_project_map[email] = project

    return directory, participant_project_map


# ── Parsing helpers ───────────────────────────────────────────────────────────

def parse_name_email(raw: str) -> tuple[str, str]:
    """Extract (name, email) from various header value formats."""
    raw = raw.strip()
    m = RE_EMAIL_ANGLE.match(raw)
    if m:
        return m.group(1).strip(), m.group(2).strip().lower()
    m = RE_EMAIL_PAREN.match(raw)
    if m:
        return m.group(1).strip(), m.group(2).strip().lower()
    m = RE_EMAIL_BARE.match(raw)
    if m:
        return m.group(1).strip(), m.group(2).strip().lower()
    # Last resort: just extract email
    emails = RE_EMAIL_ANYWHERE.findall(raw)
    if emails:
        return raw.split('@')[0].strip(), emails[0].lower()
    return raw, ''


def parse_address_list(raw: str) -> list[str]:
    """Parse comma-separated address list into list of email strings."""
    emails = []
    for part in raw.split(','):
        part = part.strip()
        if not part:
            continue
        _, email = parse_name_email(part)
        if email:
            emails.append(email)
        else:
            # May just be a bare email
            found = RE_EMAIL_ANYWHERE.findall(part)
            emails.extend(e.lower() for e in found)
    return emails


def parse_date(raw: str) -> Optional[datetime]:
    """Try each date format in order; return None if all fail."""
    raw = raw.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            pass
    return None


def detect_project(subject: str) -> str:
    for pattern, name in PROJECT_PATTERNS:
        if pattern.search(subject):
            return name
    return 'Unknown'


def resolve_identity(email: str, name: str, directory: dict) -> dict:
    """Look up email in directory; return role or [inferred]."""
    entry = directory.get(email.lower())
    if entry:
        return {'name': entry['name'], 'role': entry['role'], 'inferred': False}
    return {'name': name or email.split('@')[0], 'role': '[inferred]', 'inferred': True}


# ── Message block parser ───────────────────────────────────────────────────────

def parse_message_block(block: str, thread_id: str, msg_index: int,
                        directory: dict) -> Optional[EmailMessage]:
    """Parse a single message block (all headers + body)."""
    lines = block.split('\n')
    headers = {}
    body_lines = []
    in_body = False
    i = 0

    while i < len(lines):
        line = lines[i]
        if in_body:
            body_lines.append(line)
            i += 1
            continue

        # Detect header line: "Field: value"
        colon_pos = line.find(':')
        if colon_pos > 0:
            field_name = line[:colon_pos].strip().lower()
            if field_name in HEADER_FIELDS:
                value = line[colon_pos + 1:].strip()
                # Handle header continuation (indented next line)
                while i + 1 < len(lines) and lines[i + 1].startswith((' ', '\t')):
                    i += 1
                    value += ' ' + lines[i].strip()
                headers[field_name] = value
                i += 1
                continue

        # Blank line after at least one header = start of body
        if line.strip() == '' and headers:
            in_body = True
            i += 1
            continue

        # If no headers yet and blank line, skip
        if line.strip() == '' and not headers:
            i += 1
            continue

        # Content before headers detected (some files have Subject first)
        colon_pos = line.find(':')
        if colon_pos > 0:
            field_name = line[:colon_pos].strip().lower()
            value = line[colon_pos + 1:].strip()
            headers[field_name] = value
            i += 1
            continue

        # Otherwise treat as body
        in_body = True
        body_lines.append(line)
        i += 1

    if not headers:
        return None

    # Extract From
    from_raw = headers.get('from', '')
    sender_name, sender_email = parse_name_email(from_raw)
    identity = resolve_identity(sender_email, sender_name, directory)

    # Subject + project
    subject = headers.get('subject', '').strip()
    project = detect_project(subject)

    # Date
    date_raw = headers.get('date', '')
    parsed_date = parse_date(date_raw)
    if not parsed_date:
        # Try extracting date substring
        m = RE_DATE_RFC.search(date_raw)
        if m:
            parsed_date = parse_date(m.group(1))
        else:
            m = RE_DATE_HU.search(date_raw)
            if m:
                parsed_date = parse_date(m.group(1))

    # To / Cc
    to_emails = parse_address_list(headers.get('to', ''))
    cc_emails = parse_address_list(headers.get('cc', ''))

    body = '\n'.join(body_lines).strip()

    return EmailMessage(
        message_id=f"{thread_id}_msg{msg_index}",
        thread_id=thread_id,
        sender_email=sender_email,
        sender_name=identity['name'],
        sender_role=identity['role'],
        to_emails=to_emails,
        cc_emails=cc_emails,
        date=parsed_date,
        subject=subject,
        body=body,
        project=project,
        raw_headers=headers,
    )


# ── Thread splitter ───────────────────────────────────────────────────────────

def split_into_message_blocks(content: str) -> list[str]:
    """
    Split a .txt file containing multiple concatenated messages into individual blocks.
    Messages are separated by a blank line followed by a header line (From: / Subject:).
    """
    blocks = []
    current = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Detect new message start: blank line followed by a header-looking line
        is_header_start = (
            line.strip() == '' and
            i + 1 < len(lines) and
            re.match(r'^(From|Subject|Date|To|Cc):', lines[i + 1].strip(), re.IGNORECASE)
        )
        if is_header_start and current:
            block_text = '\n'.join(current).strip()
            if block_text:
                blocks.append(block_text)
            current = []
        else:
            current.append(line)

    if current:
        block_text = '\n'.join(current).strip()
        if block_text:
            blocks.append(block_text)

    # If only one block (no separator found), return as-is
    return blocks if blocks else [content.strip()]


# ── Public API ────────────────────────────────────────────────────────────────

def parse_email_file(filepath: str, directory: dict,
                     participant_project_map: dict = None) -> EmailThread:
    """Parse a single .txt email file into an EmailThread."""
    filename = os.path.basename(filepath)
    thread_id = os.path.splitext(filename)[0]  # e.g. "email1"

    with open(filepath, encoding='utf-8', errors='replace') as f:
        content = f.read()

    blocks = split_into_message_blocks(content)
    messages = []
    for i, block in enumerate(blocks):
        msg = parse_message_block(block, thread_id, i, directory)
        if msg:
            messages.append(msg)

    # Sort by date (None dates go last)
    messages.sort(key=lambda m: m.date if m.date else datetime.max)

    # Determine thread subject from first message
    subject = messages[0].subject if messages else thread_id

    # Determine project by scanning ALL message subjects and bodies
    # (some threads start with a subject that doesn't name the project)
    project = 'Unknown'
    for msg in messages:
        candidate = detect_project(msg.subject)
        if candidate != 'Unknown':
            project = candidate
            break
    if project == 'Unknown' and messages:
        # Fallback: scan first 200 chars of each message body
        for msg in messages:
            candidate = detect_project(msg.body[:200])
            if candidate != 'Unknown':
                project = candidate
                break

    # Final fallback: use participant → project map from Colleagues.txt
    if project == 'Unknown' and participant_project_map:
        votes: dict[str, int] = {}
        for msg in messages:
            p = participant_project_map.get(msg.sender_email.lower())
            if p:
                votes[p] = votes.get(p, 0) + 1
        if votes:
            project = max(votes, key=votes.get)

    # Build participant set
    participants = set()
    for msg in messages:
        if msg.sender_email:
            participants.add(msg.sender_email)
        participants.update(msg.to_emails)
        participants.update(msg.cc_emails)

    thread = EmailThread(
        thread_id=thread_id,
        subject=subject,
        project=project,
        messages=messages,
        participants=participants,
    )
    return thread


def load_email_corpus(email_dir: str, colleagues_path: str) -> dict[str, list[EmailThread]]:
    """
    Load all .txt email files from a directory.
    Returns: {project_name: [EmailThread, ...]}
    """
    directory, participant_project_map = load_colleagues(colleagues_path)
    threads_by_project: dict[str, list[EmailThread]] = {}

    txt_files = sorted(
        f for f in os.listdir(email_dir)
        if f.endswith('.txt') and f != 'Colleagues.txt'
    )

    parse_warnings = []
    for filename in txt_files:
        filepath = os.path.join(email_dir, filename)
        try:
            thread = parse_email_file(filepath, directory, participant_project_map)
            project = thread.project
            if project not in threads_by_project:
                threads_by_project[project] = []
            threads_by_project[project].append(thread)
        except Exception as e:
            parse_warnings.append(f"PARSE_WARNING: {filename} — {e}")

    if parse_warnings:
        for w in parse_warnings:
            print(w)

    return threads_by_project


if __name__ == '__main__':
    # Quick smoke test
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else '../input/AI_Developer_files'
    colleagues = os.path.join(data_dir, 'Colleagues.txt')
    corpus = load_email_corpus(data_dir, colleagues)
    for project, threads in corpus.items():
        print(f"\n{'='*60}")
        print(f"Project: {project} — {len(threads)} thread(s)")
        for t in threads:
            print(f"  [{t.thread_id}] {t.subject[:60]} — {len(t.messages)} msg(s), "
                  f"{t.first_date.date() if t.first_date else 'no date'} → "
                  f"{t.last_date.date() if t.last_date else 'no date'}")
