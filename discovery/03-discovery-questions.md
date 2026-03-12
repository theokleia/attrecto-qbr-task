# Discovery Questions

**Date:** 2026-03-12
**Format:** Question → Assumed Answer → How it shapes the solution

These are questions a Product Designer or Business Analyst would ask before designing any solution. Since no real client is available to interview, each question includes the assumed answer based on the task brief, email data analysis, and industry knowledge of software development agencies.

---

## About the User (Director of Engineering)

**Q1: How many projects does the DoE oversee simultaneously?**
*Assumed answer:* 5–15 active projects at any time, varying in size and phase.
*Impact on solution:* The report must aggregate across projects, not just list them. An executive summary with top N flags is essential — no DoE reads 12 per-project reports before a meeting.

**Q2: How do they currently prepare for a QBR?**
*Assumed answer:* Manually — asking PMs for status emails, scanning Jira, relying on memory and notes.
*Impact on solution:* The system must eliminate manual data collection entirely. Zero-configuration-per-QBR is the goal.

**Q3: How much time do they have to review the report before the meeting?**
*Assumed answer:* 20–30 minutes, often less.
*Impact on solution:* Executive summary must be the first thing they see. Details are available but not required. No report longer than one screen for the summary view.

**Q4: What actions can they actually take based on the report?**
*Assumed answer:* Escalate to a PM, re-assign resources, schedule an emergency call with a client, flag a compliance issue to legal, decide to extend a deadline.
*Impact on solution:* Every flagged item must include a suggested owner and next action. A flag without an action is just noise with better formatting.

**Q5: Do they prefer to read reports or have them presented to them?**
*Assumed answer:* Read independently before the meeting, then present key points verbally.
*Impact on solution:* The HTML report is the primary artifact. It should be printable/shareable for use in the meeting itself.

**Q6: What is the cost of a false positive (wrong flag) vs. a false negative (missed risk)?**
*Assumed answer:* False negatives are more costly — a missed GDPR issue or production outage can damage client relationships or have legal consequences. A false positive wastes 5 minutes. A false negative can cost a contract.
*Impact on solution:* Err on the side of flagging more rather than less for compliance and production incident categories. Apply stricter filtering to lower-severity categories to avoid noise fatigue.

---

## About the Data

**Q7: Are emails the only source of project information, or are other tools in use?**
*Assumed answer:* Based on the email data, teams use Jira (project management), GitHub (code), CI/CD pipelines, Zeplin (design), and Barion (payment). Email is used for communication that should be in these tools.
*Impact on solution:* Jira is the primary data source. Email is the exception layer. Other tools are future integration candidates.

**Q8: Is there a dedicated support/helpdesk system for client-reported issues?**
*Assumed answer:* No — clients email team members directly (evidenced by the data). This is a gap.
*Impact on solution:* Recommend support system adoption as part of the Blueprint. Flag client-direct emails as a risk pattern in the QBR report.

**Q9: What is the typical email volume per project per quarter?**
*Assumed answer:* ~100–300 project-related emails per project per quarter for an active team. Multiply by 10+ projects = 1,000–3,000 emails per QBR cycle.
*Impact on solution:* Batch processing is required at scale. Cost per analysis run must be controlled. The Blueprint must address scalability.

**Q10: What counts as "resolved" for an email-flagged item?**
*Assumed answer:* A Jira ticket was created and closed, or an explicit confirmation reply was sent within a reasonable timeframe.
*Impact on solution:* The system should cross-reference email flags against Jira. If a matching closed ticket exists, the flag is downgraded. If no ticket exists and no resolution reply was found, it stays flagged.

**Q11: Is email always sent to a shared project mailbox, or to individual team members?**
*Assumed answer:* Based on the data, emails go to individual team members (no shared inbox). Some clients email PMs or Account Managers directly.
*Impact on solution:* The system needs access to multiple inboxes or a forwarding rule to a shared collection address. This is an integration design decision.

---

## About Delivery & Ownership

**Q12: Do you want to own and run the system after delivery, or have it operated as a managed service?**
*Assumed answer:* The client owns and operates it after delivery — they have internal engineering capacity to maintain it.
*Impact on solution:* The system must be self-contained, fully documented, and maintainable by the client's own engineers. README.md and Blueprint.md are essential deliverables, not afterthoughts. No runtime dependency on the vendor.

**Q13: What is the expected report cadence — quarterly only, or more frequent?**
*Assumed answer:* Quarterly for the formal QBR presentation, but the underlying monitoring should run continuously or weekly. A surprise in a quarterly report means the system failed to warn months earlier.
*Impact on solution:* Report generation should be schedulable (cron job or similar). The architecture must support both on-demand and scheduled runs without manual intervention.

---

## Internal Strategic Decisions *(questions the dev company asks itself, not the client)*

**S1: Should we offer this as a productizable service or a fully custom build per client?**
*Strategic consideration:* A productizable core (shared engine, per-client configuration) is more scalable and profitable than a fully custom build each time. However, each client's toolstack differs enough that some customization is always required.
*Recommended position:* Build a configurable core system (`.env`-driven) with pluggable data source connectors. Sell the initial build as a project, offer connector development as add-on modules. This allows reuse of 70–80% of the codebase across clients.

**S2: Which integrations are most valuable to lead with commercially?**
*Strategic consideration:* Jira is nearly universal in software development teams — the highest ROI integration. Email is the lowest-friction starting point (no API key required if forwarding rules are set up). CI/CD and GitHub integrations are high-value but require more client-side setup.
*Recommended position:* Lead with Jira + Email as the Phase 1 offering. CI/CD, GitHub, and support system integrations are Phase 2 upsells. This creates a natural expansion path and recurring engagement.

**S3: What is the right support model post-delivery?**
*Strategic consideration:* A build-and-handover model is clean but leaves revenue on the table. A maintenance contract (monthly retainer for updates, new integrations, model prompt tuning) creates recurring revenue.
*Recommended position:* Offer a tiered post-delivery package: (a) documentation + 30-day support included, (b) optional 12-month maintenance contract for updates and new connectors.

**S4: Should we recommend the client adopt a support/helpdesk system as part of this engagement?**
*Strategic consideration:* The email data shows clients contacting developers directly — a clear process gap. Recommending and implementing a support system (Zendesk, Jira Service Management) is a natural expansion of this engagement and removes the gap our QBR system was designed to work around.
*Recommended position:* Yes — surface this as a finding in the QBR report and propose support system implementation as a complementary project. This is an organic upsell grounded in real data, not a sales pitch.

---

## About Priorities and Scope

**Q15: Which issue types are highest priority for the DoE?**
*Assumed answer:* Based on the data analysis and the DoE persona:
1. Compliance / Legal (highest — GDPR, data protection, contractual obligations)
2. Production Incidents (high — client-facing, reputational risk)
3. Blockers / Dependencies (high — team velocity, delivery risk)
4. Spec Gaps (medium — delivery quality, scope creep)
5. Process / Communication (medium — team health, long-term efficiency)
6. Noise / Off-topic (low — not worth reporting, but worth measuring as a team health signal)

*Impact on solution:* Risk categories are color-coded and sorted by severity in the report. Compliance and Production flags appear first.

**Q16: Should the system suggest root causes, or only describe symptoms?**
*Assumed answer:* Root causes are more valuable but harder to generate accurately. The system should attempt root cause analysis but mark it as "suggested" rather than "confirmed."
*Impact on solution:* The AI analysis prompt should include a root cause step, but the output should be clearly labeled as AI-generated inference, not factual conclusion.

**Q17: Should the report show resolved items, or only open/unresolved ones?**
*Assumed answer:* Open items are primary. Resolved items should appear in a separate "recently closed" section as context — especially for the QBR presentation where wins deserve recognition.
*Impact on solution:* Report has two sections: "Requires Attention" (open flags) and "Recently Resolved" (closed in this quarter). Both inform the QBR narrative.

---

## About Current Processes

**Q21: What does your full development workflow look like, from brief to deployment?**
*Assumed answer:* Requirements arrive via a client brief or discovery call, get translated into Jira epics/stories by a PM or BA, then are developed in sprints. Design specs come via Zeplin. QA happens in a staging environment. Deployment is via a CI/CD pipeline. There is no formal sign-off gate between design and development — gaps are discovered reactively.
*Impact on solution:* Each handoff point is a potential data source. Jira captures what enters the system; Zeplin and CI/CD capture what happens to it. The Blueprint should describe integration at every handoff point.

**Q22: Which tools are currently in use across the full SDLC?**
*Assumed answer:* Based on email analysis: Jira (PM), Zeplin (design), GitHub (code), CI/CD pipeline (custom or GitHub Actions), Barion (payment), and staging environment (internal QA). No dedicated support system in use.
*Impact on solution:* These are the exact integration candidates described in Concept D's tool roadmap. The discovery questions confirm which integrations are Phase 1 (already in use) vs. Phase 2 (new adoption required).

**Q23: How are bugs currently reported and tracked?**
*Assumed answer:* No standardized path. Clients report issues by emailing team members directly. Internal bugs are found during development or QA and may or may not get entered as Jira tickets — some are handled informally in email.
*Impact on solution:* This is the support layer gap. The QBR system should surface client-direct emails as a risk pattern. The Blueprint should recommend a support system (Zendesk / Jira Service Management) as a complementary engagement.

**Q24: When a bug is fixed, how is the fix verified and communicated back to the client?**
*Assumed answer:* Manually — a developer notifies a PM via email or chat, the PM follows up with the client, and the client confirms in the same email thread. No automated deploy notification or SLA tracking.
*Impact on solution:* Resolution tracking is a critical gap. The QBR report needs a "time to resolve" metric, which cannot be derived from email alone. Jira ticket close dates (or support system SLAs) are the only reliable source.

**Q25: When a production incident occurs, how does it escalate to the Director of Engineering?**
*Assumed answer:* Based on email evidence — it escalates when a client complains directly, or when a PM realizes the issue is beyond their authority and emails the DoE manually. There is no automated alerting or incident management system.
*Impact on solution:* Production incidents should be the highest-priority flag in the QBR report. The system should also recommend incident escalation automation (CI/CD failure → Jira incident → DoE notification) as part of the Phase 2 roadmap.

---

## About AI & Automation Readiness

**Q26: Has your organization used automation tools before? Which ones, and for what?**
*Assumed answer:* Limited automation — CI/CD pipelines are in place, suggesting engineering familiarity with automation tooling. However, the pipelines are fragile (one bad env var caused a production outage) and appear to be maintained by a single person. No automation exists for reporting, issue detection, or QBR preparation.
*Impact on solution:* The team has the infrastructure mindset to maintain an automated system, but the implementation skill level may be uneven. The delivered system must be robust to single-engineer knowledge silos (documented, containerized, configuration-driven).

**Q27: Has anyone on the team used AI tools (ChatGPT, Copilot, etc.) in their work?**
*Assumed answer:* Likely yes at the individual level (developers using Copilot or ChatGPT for code generation), but no organizational adoption or policy in place.
*Impact on solution:* The AI analytical layer of the QBR system should be explainable. The report should show *why* something was flagged, not just that it was. This builds trust with an audience that may be skeptical of AI-generated assessments.

**Q28: What is your organization's policy on AI use and data handling?**
*Assumed answer:* No formal policy — typical for a mid-size agency that hasn't yet reached AI governance maturity. Data sensitivity is moderate (project communications, not regulated personal health or financial data).
*Impact on solution:* The Blueprint must include a data privacy section. Email content should not be retained beyond the analysis run. PII (names, email addresses) should be anonymized in the report output or handled in accordance with GDPR (relevant for Hungarian companies under EU jurisdiction).

**Q29: Would the team trust an AI-generated risk assessment for QBR purposes?**
*Assumed answer:* Conditionally — if the system shows its evidence (linking flags to specific email threads or Jira tickets), trust will be higher. If it produces unexplained scores, it will be dismissed.
*Impact on solution:* Every AI-generated flag must include a source reference (email subject + date, or Jira ticket ID) and a brief explanation. Labels like "AI-inferred" vs. "data-confirmed" distinguish analytical output from factual retrieval.

**Q30: Is there a budget for AI model API costs, or must this be a zero-cost solution?**
*Assumed answer:* Moderate budget available — the client is paying for a custom-built system, so API costs are a line item in the operational budget. However, costs must be predictable and proportional to usage.
*Impact on solution:* The model strategy (claude-sonnet-4-6 for most tasks, claude-opus-4-6 for core analytics only) is designed to keep per-run costs low. The Blueprint should include an estimated cost-per-QBR-run calculation to make this concrete for the client.

**Q31: Are there any AI services or providers the organization already has contracts with, or must avoid?**
*Assumed answer:* Unknown — but for a European agency, data residency preferences may favor EU-hosted models or providers with GDPR-compliant data processing agreements.
*Impact on solution:* The `.env` configuration allows swapping API providers without code changes. The Blueprint should note that model provider substitution is supported as a configuration option.

**Q32: What language(s) do your teams communicate in?**
*Assumed answer:* Hungarian primary, English in technical and vendor contexts. Many threads are bilingual — Hungarian in the narrative, English in code references, error messages, and tool names.
*Impact on solution:* Rule engine signal lists require bilingual coverage (Hungarian and English scope change indicators, resolution signals, incident keywords). LLM prompts must explicitly instruct the model to handle mixed-language threads and not default to English-only pattern matching. Report output language should be configurable for clients operating in different markets.

---

## About Integration

**Q18: What Jira fields are most relevant for QBR health metrics?**
*Assumed answer:* Issue type, status, priority, assignee, due date, created date, sprint, labels, and any custom "blocker" or "risk" fields.
*Impact on solution:* The Jira client fetches these specific fields. The `.env` configuration allows filtering by project key and issue type to avoid ingesting irrelevant data.

**Q19: Would teams accept having their emails automatically analyzed?**
*Assumed answer:* If properly scoped (project-related inboxes only, no personal email, clear data handling policy), yes — especially if it reduces manual reporting burden.
*Impact on solution:* The Blueprint must include a data privacy section. PII handling (names, email addresses) must be addressed explicitly. Email content should not be stored longer than the analysis run.

**Q20: Should the system integrate with CI/CD or GitHub in addition to Jira and email?**
*Assumed answer:* Yes — these are natural next integration points. CI/CD failure rates and GitHub PR cycle times are valuable QBR metrics.
*Impact on solution:* The Blueprint describes these as Phase 2 integrations. The architecture is designed to accept additional data sources without requiring a full rebuild.
