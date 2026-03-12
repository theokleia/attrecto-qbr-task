"""
analyzer.py — QBR Automation System
Main entry point. Wires together all pipeline stages.

Usage:
    python analyzer.py <email_dir> [--mock] [--output <path>]

Arguments:
    email_dir   Path to folder containing email .txt files and Colleagues.txt
    --mock      Use mock LLM responses (no API key required)
    --output    Output path for the report (default: ../output/sample-report.md)

Environment:
    ANTHROPIC_API_KEY   Required for live LLM calls (skip with --mock)
"""

import argparse
import os
import sys
from datetime import datetime

# Allow running from src/ directory
sys.path.insert(0, os.path.dirname(__file__))

from email_parser import load_email_corpus
from ai_classifier import classify_threads
from report_generator import generate_report


def load_env_file(env_path: str) -> None:
    """Load key=value pairs from a .env file into os.environ."""
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def main():
    parser = argparse.ArgumentParser(
        description='QBR Portfolio Health Analyzer — analyzes project emails and generates a report.'
    )
    parser.add_argument('email_dir', help='Directory containing email .txt files and Colleagues.txt')
    parser.add_argument('--mock', action='store_true',
                        help='Use mock LLM responses (no API key required)')
    parser.add_argument('--output', default=None,
                        help='Output path for the report Markdown file')
    parser.add_argument('--quarter', default='Q2 2025',
                        help='Quarter label for the report header (default: Q2 2025)')
    args = parser.parse_args()

    # ── Resolve paths ──
    email_dir = os.path.abspath(args.email_dir)
    if not os.path.isdir(email_dir):
        print(f"Error: '{email_dir}' is not a directory.")
        sys.exit(1)

    colleagues_path = os.path.join(email_dir, 'Colleagues.txt')
    if not os.path.exists(colleagues_path):
        print(f"Warning: Colleagues.txt not found at {colleagues_path}. Identity resolution will be inference-only.")

    # Default output path
    if args.output:
        output_path = os.path.abspath(args.output)
    else:
        src_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(src_dir, '..', 'output', 'sample-report.md')
    output_path = os.path.normpath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # ── Load .env if present ──
    env_candidates = [
        os.path.join(os.path.dirname(__file__), '..', '.env'),
        os.path.join(os.path.dirname(__file__), '..', '..', '.env'),
        os.path.join(os.getcwd(), '.env'),
    ]
    for env_path in env_candidates:
        if os.path.exists(env_path):
            load_env_file(env_path)
            break

    use_mock = args.mock
    if not use_mock and not os.environ.get('ANTHROPIC_API_KEY'):
        print("No ANTHROPIC_API_KEY found in environment or .env file.")
        print("Running in mock mode (--mock). For live LLM calls, set ANTHROPIC_API_KEY in .env")
        use_mock = True

    # ── Pipeline ──
    print(f"\n{'='*60}")
    print(f"QBR Portfolio Health Analyzer")
    print(f"Email source: {email_dir}")
    print(f"Mode: {'MOCK (no API calls)' if use_mock else 'LIVE (claude-sonnet-4-6)'}")
    print(f"{'='*60}")

    # Stage: Ingestion
    print("\n[Ingestion] Loading email corpus...")
    corpus = load_email_corpus(email_dir, colleagues_path)
    total_threads = sum(len(t) for t in corpus.values())
    print(f"  Loaded {total_threads} threads across {len(corpus)} project(s):")
    for project, threads in corpus.items():
        print(f"    {project}: {len(threads)} threads")

    # Stages A → B → C
    results = classify_threads(corpus, use_mock=use_mock)

    # Stage D: Report
    print(f"\n[Stage D] Generating report...")
    report_markdown = generate_report(results, quarter_label=args.quarter, use_mock=use_mock)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_markdown)

    print(f"\n{'='*60}")
    print(f"Report written to: {output_path}")

    # Quick summary
    total_confirmed = sum(len(d.get('confirmed_flags', [])) for d in results.values())
    total_review = sum(len(d.get('needs_review', [])) for d in results.values())
    print(f"Confirmed flags: {total_confirmed}")
    print(f"Needs PM review: {total_review}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
