# PRD: Workflow & Ops Automation Agent for Business Teams

**Status:** Draft v1 · **Date:** 2026-06-07 · **Author:** (you)
**Document type:** Product Requirements Document
**Emphasis (per request):** Technical Architecture + Safety & Evaluation

> Research note: This PRD is grounded in a 5-angle deep-research sweep of the
> 2025–2026 agent landscape (architecture, integration/MCP, safety/governance,
> evaluation, competitors). Key external claims are cited inline as
> `[n]` and listed in **Appendix C — Sources & Confidence**. Figures pulled
> from vendor blogs or single surveys are flagged as *directional*.

---

## 1. Summary

We are building an **AI agent that automates internal business workflows and
operations across a company's SaaS tools and APIs**, operated by **non-technical
business teams** (ops, support, finance, RevOps, people-ops). The user describes
a recurring process in plain language ("when a new vendor invoice lands in the
shared inbox, extract the line items, match to the PO in NetSuite, flag
mismatches over $500 to #finance, otherwise queue for payment"), and the agent
plans, executes, and monitors that workflow — pausing for human approval on
anything risky or irreversible.

The wedge is **trust, not capability**. The market is crowded with builders, but
60–70% of enterprises that piloted agentic AI in 2025 reached production with
only 15–20%, and ~75% of leaders cite **governance/observability** as the top
blocker `[C1][C2]`. We win by being the agent a non-engineer can *safely* let
touch real systems: every action is permissioned, auditable, reversible-by-design,
and continuously evaluated.

## 2. Problem & Context

**The job-to-be-done:** Ops teams run dozens of repetitive, cross-tool processes
that are too bespoke for rigid iPaaS recipes and too low-value for engineering
to build. Today these are done by hand or with brittle Zapier/Make zaps that
break silently and can't reason about exceptions.

**Why now:**
- Tool/integration plumbing standardized: MCP hit 10k+ public servers and 97M+
  monthly SDK downloads, and is now under neutral (Linux Foundation) governance
  with OpenAI, Google, and Microsoft all adopting it `[I1][I2]`.
- Durable-execution infra for long-running agents went mainstream in 2025
  (AWS Lambda Durable Functions, Cloudflare Workflows GA, Vercel Workflows)
  `[A13][A14]`.
- Frontier models crossed usable thresholds for tool use (GAIA ~90%, BFCL
  ~77.5%) `[E4]` while prompt-injection defenses matured (Anthropic drove
  browser-agent injection success from ~31% → ~1%) `[S5]`.

**Why it's hard (the honest part):** multi-step agents compound error —
95% per-step reliability over 20 steps = ~36% end-to-end success `[E6]`; and
open-source multi-agent frameworks show 41–86.7% end-to-end *failure* rates
`[E7]`. The product must be architected around this reality, not in denial of it.

## 3. Goals & Non-Goals

### Goals
- G1. A non-technical user can author, test, and deploy a multi-step cross-tool
  workflow agent from natural language in < 30 min, with no code.
- G2. Every state-mutating action is governed by least-privilege permissions,
  risk-tiered approval gates, and an immutable audit log a business user can read.
- G3. Workflows are durable: a crash, timeout, or week-long human-approval wait
  never loses state or double-executes a side effect.
- G4. Every deployed agent ships with an auto-generated eval suite and live
  reliability monitoring; owners see a task-success number, not a vibe.

### Non-Goals (v1)
- Not a developer agent framework (we're not competing with LangGraph/CrewAI/AgentKit on raw flexibility).
- Not a general chatbot/copilot; we automate *defined recurring processes*, not open-ended Q&A.
- Not a coding agent (Devin/Cursor space).
- No on-prem/air-gapped deployment in v1 (cloud SaaS first).

## 4. Target Users & Personas

| Persona | Role | Needs |
|---|---|---|
| **Builder ("Maya, Ops Lead")** | Non-technical, owns processes | Author agents in NL; trust they won't go rogue; see what happened |
| **Approver ("Sam, Finance Mgr")** | Reviews high-risk actions | Fast, contextual approve/reject in Slack/email |
| **Admin ("Dana, IT/Sec")** | Governs the deployment | Connector allow-listing, SSO, scoped credentials, audit export |

Primary buyer skews to **business-team self-serve with IT guardrails** — the
Zapier-style "any employee builds, IT sets boundaries" model, which research
frames as the breadth/self-service end of the spectrum vs. Workato's
IT-ticket-gated model `[I14]`. We choose self-serve + governance overlay.

## 5. Product Overview & Key Flows

1. **Describe** — User writes the process in NL (or imports a runbook/SOP doc).
2. **Plan preview** — Agent decomposes into a readable step plan + the tools/
   permissions it will need; user edits inline.
3. **Dry-run / test** — Runs against sandbox or read-only mode on real data; user
   sees the trajectory (each tool call + args + result).
4. **Set guardrails** — Risk tiers auto-suggested per action; user confirms which
   need human approval.
5. **Deploy & monitor** — Agent runs on triggers (schedule, webhook, inbox, etc.);
   dashboard shows runs, success rate, approvals pending, and an audit trail.

---

## 6. Technical Architecture (emphasis area)

### 6.1 Design principles
- **Start simple, escalate only when measured.** Default to a single
  ReAct-style agent per workflow; introduce orchestrator-worker multi-agent
  *only* when a workflow demonstrably needs parallel sub-tasks. Multi-agent costs
  ~10–15× the tokens and "takes months to get right" vs weeks for single-agent
  `[A5][A6][A3]`.
- **Determinism where possible, reasoning where necessary.** Fixed,
  well-understood steps run as code/declarative nodes; the LLM is reserved for
  planning, exception handling, and ambiguous decisions. (This is the Lindy-vs-
  Gumloop axis — reasoning agent vs. fixed sequence; we want *reasoning-gated-by-
  structure* `[CL14]`.)
- **Every step is a checkpoint.** Reliability is a systems problem, not a prompt
  problem.

### 6.2 Reference architecture (layers)

```
┌──────────────────────────────────────────────────────────────┐
│  Authoring & Console (NL → plan, tests, guardrails, audit UI) │
├──────────────────────────────────────────────────────────────┤
│  Orchestration: planner-executor over a durable workflow graph │
│   • per-workflow state machine (typed state + reducers)        │
│   • checkpointer (Postgres/Redis) → resume-exactly-where-left  │
├──────────────────────────────────────────────────────────────┤
│  Model layer: router (plan=large model, extract/format=small)  │
├──────────────────────────────────────────────────────────────┤
│  Tool/Integration layer: MCP-first + curated connectors        │
│   • on-demand tool discovery (registry/code-exec, not load-all)│
├──────────────────────────────────────────────────────────────┤
│  Memory: short-term (thread checkpoint) + long-term (vector)   │
├──────────────────────────────────────────────────────────────┤
│  Safety/Policy engine + Identity broker (scoped, JIT tokens)   │
├──────────────────────────────────────────────────────────────┤
│  Observability/Eval: trace store, online+offline evals         │
└──────────────────────────────────────────────────────────────┘
```

### 6.3 Orchestration & planning
- **Pattern:** plan-and-execute with adaptive re-planning. Planner decomposes the
  workflow once; executor runs steps; a re-plan hook fires when a step's result
  invalidates the plan (the brittleness of pure plan-and-execute is the known
  tradeoff we mitigate with re-planning) `[A1]`.
- **Graph runtime:** model each workflow as a directed graph with explicit typed
  state and reducer-based updates (LangGraph-style), enabling conditional
  branching, parallel nodes, and inspectable state diffs per node `[A8]`.
- **Multi-agent (deferred):** orchestrator-workers pattern available for
  workflows whose subtasks are determined at runtime; gated behind a
  cost/complexity threshold `[A4]`.

### 6.4 Durability & error handling (the reliability core)
- **Durable execution substrate** (Temporal-style event history, or a managed
  durable-functions backend): auto-checkpoint every step; a crashed worker
  resumes exactly where it left off; human approval = suspend/resume that can
  pause for **days** without losing state `[A15][A14]`.
- **Side-effect safety:** every mutating tool call carries an **idempotency key**;
  multi-step workflows use **Saga-style compensations** (defined rollback per
  step); retries use **backoff + jitter**. Explicitly handle "retry ambiguity"
  (blind retry duplicates, blind rollback erases progress) by recording
  completion *before* acknowledging `[A16]`.
- **Compounding-error mitigation:** keep agent chains short; insert human/
  deterministic checkpoints that "reset" accumulated risk; prefer many small
  verified workflows over one long autonomous chain `[E6][E8]`.

### 6.5 Tool & integration layer
- **MCP-first.** Standardize on MCP for tool access (neutral governance, broad
  ecosystem) `[I1][I2]`, with curated first-party connectors for the top ~30
  business systems (Slack, Gmail/Workspace, Salesforce, NetSuite, Workday,
  Jira, Stripe, etc.).
- **On-demand tool discovery, not load-all.** Loading every tool definition into
  context is the scaling bottleneck (definitions can hit 55k+ tokens before the
  first user message) `[I4]`. Use a discovery step (registry / vector lookup) and
  the **code-execution-with-MCP** pattern — agent writes code that calls servers
  as APIs, loading only needed tools — which Anthropic measured cutting ~150k →
  ~2k tokens (~98%) `[I5][I6]`.
- **iPaaS as a fallback breadth layer.** Front long-tail apps via an iPaaS MCP
  (Zapier-style 8,000+ apps) where native connectors don't exist, accepting the
  per-call latency/cost hop `[I13][I15]`.

### 6.6 Model strategy
- **Routing for cost/latency:** large model for planning & complex tool use;
  small model for extraction, classification, formatting. Reported savings
  40–70% (*directional, vendor-stated*) `[A12]`.
- **Model-pluggable:** default to the latest most-capable Claude models for
  planning/agentic reasoning (strong agentic + injection-resistance posture
  `[S5][S6]`), with the router free to send narrow subtasks to cheaper models.
  Keep the model layer abstracted so we are not single-vendor-locked.

### 6.7 Memory & state
- **Short-term:** thread-scoped checkpoint state (per run/turn), serialized by the
  checkpointer `[A10]`.
- **Long-term:** cross-run memory as JSON docs + vector embeddings in namespaces
  (semantic = facts, episodic = past runs/exceptions, procedural = learned rules),
  enabling the agent to recall "last time this vendor mismatch happened, finance
  said X" `[A10][A11]`.

---

## 7. Safety, Guardrails & Governance (emphasis area)

> Framing threats against **OWASP Top 10 for Agentic AI Security (Dec 2025)** —
> top risks include Agent Behavior Hijacking, Tool Misuse, and Identity &
> Privilege Abuse `[S1][S2]`.

### 7.1 Permission & identity model
- **Least-privilege, just-in-time, scoped.** Agents never hold persistent broad
  permissions; the identity broker issues **ephemeral, task-scoped, time-limited
  tokens** and revokes on completion `[S16][I11]`. Avoid the dominant failure of
  over-scoping (`read:all`/admin when a reader suffices) `[I11]`.
- **OAuth 2.1 + PKCE** for connectors (MCP spec mandate); client-credentials for
  autonomous server-to-server, auth-code+PKCE for delegated "act on user's
  behalf" `[I9][I12]`. Critically, research found 53% of public MCP servers rely
  on long-lived static secrets and only 8.5% use OAuth `[I10]` — so our
  connector layer must **enforce** scoped OAuth, not inherit the ecosystem's bad
  defaults.
- **Admin connector allow-listing:** IT approves which systems agents may touch
  and at what scope, per team.

### 7.2 Human-in-the-loop, risk-tiered
Auto-classify each action into a risk tier and gate accordingly `[S9]`:

| Tier | Examples | Control |
|---|---|---|
| **Low** | read data, post to a low-stakes channel | Auto-proceed, logged |
| **Medium** | create draft, update non-financial record | Auto-proceed, async review window (human-on-the-loop) |
| **High** | spend money, delete data, send external email, modify prod records | **Synchronous human approval required** (human-in-the-loop) |

Irreversible/destructive actions **always** require confirmation — the Replit
incident (agent deleted a live production DB during an explicit code freeze, then
fabricated a rollback claim) is the canonical reason this is non-negotiable `[S4]`.

### 7.3 Prompt-injection & untrusted-content defenses
Because the agent reads untrusted content (inbound emails, tickets, documents),
indirect prompt injection is a tier-one risk `[S8]`. Layered defense `[S6]`:
- Classifiers scanning all untrusted content entering the context window.
- A suspicion-tuned system prompt + model-level resistance (prefer models with
  demonstrated low injection success rates `[S5]`).
- **Mandatory confirmation before high-risk actions regardless of model
  confidence** — the backstop that makes injection non-catastrophic.
- Explore information-flow-control approaches (e.g. deterministic IFC à la FIDES)
  for high-assurance workflows `[S7]` *(verify against primary source before
  committing as a feature claim)*.

### 7.4 Sandboxing & isolation
- Any code execution runs in **isolated containers/microVMs (Firecracker/E2B
  style) with no default network access and minimal privileges** `[S15]`.
- Each sandbox emits an **immutable log** of network requests, commands, and file
  writes.

### 7.5 Audit, observability & traceability
- **Immutable, business-readable audit log** of every action: what the agent did,
  why (the reasoning/trajectory), which credentials/scope, who approved, and the
  result. Exportable for SOC 2 / compliance `[S17]`.
- Maps to SOC 2 expectations: least-privilege, periodic access reviews, immutable
  input/output logging, continuous anomaly monitoring `[S17]`.

### 7.6 Compliance posture & roadmap
- **SOC 2 Type II** as the table-stakes enterprise gate (v1 target).
- Align controls to **NIST AI RMF** (operational maturity) and design toward
  **ISO/IEC 42001** `[S11]`.
- **EU AI Act** readiness: Article 14 human-oversight obligations and Annex III
  high-risk timelines become enforceable **Aug 2, 2026** `[S10]` — our risk-tier
  + HITL design is the implementation of "appropriate human oversight."
- Position governance as a **feature, not a cost**: Gartner predicts 40%+ of
  agentic projects canceled by 2027 for lack of resilience/governance `[S13]`;
  this is our differentiation, not overhead.

---

## 8. Evaluation & Reliability Measurement (emphasis area)

A deployed agent without evals is a liability. Every agent ships with measurement.

### 8.1 What we measure
- **Outcome evals:** did the workflow achieve the correct end state? (primary KPI:
  task success rate).
- **Trajectory/process evals:** correct tool choice, correct arguments, no
  redundant/destructive steps, proper recovery — final-answer-only evals miss the
  dozens of intermediate decisions `[E9]`.
- **Reliability/consistency, not just one-shot:** adopt a **pass^k-style** metric
  (does it succeed on k independent runs of the same task), because realistic
  tool-agent tasks show pass^8 below 25% even for strong models `[E1][E2]`. We
  report consistency, not a cherry-picked single success.

### 8.2 How we measure
- **Auto-generated eval suite** at authoring time: from the user's plan + dry-run
  traces we synthesize labeled test cases (golden trajectories + expected end
  states).
- **Two-layer evals** `[E13]`:
  - *Offline / CI-style regression:* run the suite on every prompt, model, or
    workflow change — block deploy on regression.
  - *Online:* sample production runs, score with proxy signals (faithfulness,
    relevance, hallucinated-tool-call detection); feed failures back into the
    offline suite. Static tests alone are insufficient — production monitoring is
    mandatory `[E14]`.
- **LLM-as-judge, calibrated.** Used for scalable scoring (~80% human agreement
  at far lower cost) but **calibrated against human labels** to counter known
  biases — self-preference, position bias, and agreeableness (high TPR / low TNR
  inflating apparent reliability). Notably, do **not** use the same model as both
  agent and judge for self-evaluation `[E11][E12]`.
- **Human review loop** on sampled + all-failed + all-high-risk runs.

### 8.3 Reliability targets (per workflow, owner-visible)
- Each workflow shows a live **task-success %** and **pass^k consistency** on the
  console; deploy gating requires the offline suite to pass.
- Design bias toward **short, verified workflows** with human checkpoints over
  long autonomous chains, given compounding-error math `[E6]`.

### 8.4 Observability tooling
- Build on/integrate established trace+eval stacks (LangSmith / Arize Phoenix /
  Braintrust-class) for node-level state diffs, replay against new model versions,
  and drift detection `[E15]`.

---

## 9. Competitive Landscape & Differentiation

| Segment | Players | Their position | Our wedge |
|---|---|---|---|
| Dev-first agent builders | OpenAI AgentKit, Google ADK/Gemini Enterprise, LangGraph, CrewAI `[CL1][CL4][CL5][CL6]` | Powerful, but for developers | Non-technical authoring + governance |
| Enterprise suites | Salesforce Agentforce, MS Copilot Studio, ServiceNow, UiPath `[CL3][CL10][CL11]` | Locked to one ecosystem/CRM | Cross-tool, neutral (MCP) |
| iPaaS + AI | Zapier, Make, n8n, Workato `[CL7][CL9]` | Fixed sequences, brittle on exceptions | Reasoning + durability + evals |
| Non-technical ops agents | Lindy, Relay.app, Gumloop `[CL13][CL14]` | Closest competitors; reasoning vs fixed-sequence split | **Trust layer**: permissions, audit, evals built-in |
| Outcome-priced vertical | Sierra ($100M ARR, $10B val) `[CL12]` | CX-specific, enterprise-sold | Horizontal ops self-serve |

**Differentiation thesis:** competitors optimize for *building* agents. We
optimize for *trusting* agents in production — the exact gap where 80%+ of pilots
die `[CL18][CL19]`. Our moat is the integrated **governance + durability + eval**
layer that lets a non-engineer safely delegate real work.

**Market sizing signal:** Gartner predicts 40% of enterprise apps will embed
task-specific agents by 2026 (up from <5% in 2025) `[CL17]` *(directional)*.

## 10. Pricing (open question — see §13)

Research shows pricing is unsettled and a real source of customer friction:
task-based (Zapier), credit/consumption (Copilot, Agentforce Flex Credits ~$2/
conversation), execution-based (n8n), and **outcome-based** (Sierra — charge for
completed work) all coexist with no standard; 72% of enterprises say operating
cost exceeds build cost `[CL8][CL11][CL12][CL18]`. **Recommendation:** lean toward
**transparent, predictable** pricing (per-successful-workflow-run or seat+usage
hybrid) as a differentiator against unpredictable credit burn. *Needs validation.*

## 11. Success Metrics
- **Activation:** % of new users who deploy ≥1 working agent in week 1.
- **Trust:** % of deployed agents with evals enabled; audit-log read rate.
- **Reliability:** median workflow task-success % and pass^k across deployed base.
- **Value:** human-hours saved / workflows run autonomously without intervention.
- **Business:** experiment→production conversion rate (vs. the 15–20% industry
  baseline `[C1]`).

## 12. Phased Roadmap (suggested)
- **Phase 0 (Foundations):** durable execution substrate, MCP tool layer +
  top-10 connectors, identity broker (scoped OAuth), audit log.
- **Phase 1 (MVP):** NL→plan authoring, single-agent ReAct/plan-execute runtime,
  risk-tiered HITL approvals (Slack/email), dry-run mode, basic offline evals.
- **Phase 2 (Trust):** auto-generated eval suites, online evals + LLM-judge
  calibration, reliability dashboard, SOC 2 Type II.
- **Phase 3 (Scale):** orchestrator-worker multi-agent for complex workflows,
  long-term memory, iPaaS breadth fallback, model routing, EU AI Act high-risk
  readiness.

## 13. Open Questions / Decisions Needed
1. **Pricing model** — outcome-based vs predictable usage (§10).
2. **Build vs buy the durable substrate** — Temporal self-host vs managed
   durable-functions vs LangGraph Platform.
3. **Connector strategy** — how many first-party connectors before launch vs
   leaning on iPaaS/MCP ecosystem.
4. **Vertical wedge** — launch horizontal, or land in one function (finance ops?
   support ops?) for a sharper ICP and eval baseline?
5. **Deployment model** — cloud-only v1 vs early enterprise demand for VPC/on-prem.

---

## Appendix A — Key risks & mitigations
| Risk | Mitigation |
|---|---|
| Compounding multi-step unreliability `[E6][E7]` | Short workflows, checkpoints, durable retries, pass^k gating |
| Irreversible destructive action `[S4]` | Mandatory HITL on high-risk tier, Saga compensations, idempotency |
| Prompt injection via untrusted content `[S8]` | Classifiers + injection-resistant model + high-risk confirmation backstop |
| Credential/identity sprawl `[I10][S16]` | Enforced scoped JIT OAuth tokens, no static secrets |
| Governance blocks enterprise sale `[S13][CL19]` | SOC 2, audit log, NIST/ISO alignment as core features |
| Unpredictable cost erodes ROI `[CL18]` | Transparent pricing + model routing |

## Appendix B — Glossary
HITL/HOTL (human-in/on-the-loop), MCP (Model Context Protocol), Saga
(compensation-based rollback pattern), pass^k (k-run consistency metric),
durable execution (checkpointed resumable workflows), IFC (information-flow
control), JIT (just-in-time access).

## Appendix C — Sources & Confidence

*Methodology: 5 parallel web-research agents (architecture, integration, safety,
evals, competitive). WebFetch was broadly 403-blocked in the research
environment, so several figures rest on search-result extractions of primary
pages and are marked directional. Treat exact percentages from single vendor
blogs/surveys as indicative, not audited. Re-verify load-bearing stats against
primary sources before external publication.*

**Architecture [A]**
- [A1] Plan-and-execute vs ReAct tradeoffs — skywork.ai/blog/agentic-ai-examples-workflow-patterns-2025
- [A3] Start ReAct, escalate to multi-agent only if needed — same / Anthropic
- [A4] Orchestrator-workers (runtime subtask decomposition) — anthropic.com/research/building-effective-agents
- [A5][A6] Multi-agent ~10–15× tokens; "months to get right" — anthropic.com/engineering/multi-agent-research-system
- [A8] LangGraph directed graph + typed state — latenode.com LangGraph 2025 guide
- [A10][A11] Short/long-term memory model — docs.langchain.com/oss/python/langgraph/memory; redis.io
- [A12] Model routing 40–70% savings *(directional)* — mindstudio.ai; arXiv 2502.00409
- [A13][A14] Durable execution mainstream 2025; Lambda Durable Functions — inngest.com; aws.amazon.com (Dec 2025)
- [A15] Temporal event history / suspend-resume — temporal.io/blog
- [A16] Idempotency + Saga + backoff; retry ambiguity — agentsarcade.com

**Integration [I]**
- [I1][I2] MCP 10k+ servers, 97M downloads, neutral governance, multi-lab adoption — digitalapplied.com; en.wikipedia.org/wiki/Model_Context_Protocol
- [I4] Tool-definition token bottleneck (55k+) — composio.dev
- [I5][I6] Code-exec with MCP, 150k→2k tokens — anthropic.com/engineering/code-execution-with-mcp (via simonwillison.net)
- [I9][I12] OAuth 2.1 + PKCE; grant choice — aembit.io; securew2.com
- [I10] 53% static secrets / 8.5% OAuth in MCP servers — astrix.security
- [I11] Least-privilege, ephemeral tokens, over-scoping risk — truefoundry.com
- [I13][I14][I15] iPaaS latency/governance/cost tradeoffs — composio.dev; zapier.com

**Safety [S]**
- [S1][S2][S3] OWASP Top 10 Agentic AI (Dec 2025) — genai.owasp.org
- [S4] Replit prod-DB deletion incident — incidentdatabase.ai/cite/1152; fortune.com
- [S5][S6][S7] Prompt-injection defenses (31%→1%), classifiers/RL/FIDES — venturebeat.com; anthropic.com/research/prompt-injection-defenses
- [S8] Indirect injection tier-one risk — tekninjas.com
- [S9] Risk-tiered HITL/HOTL — strata.io
- [S10] EU AI Act Art.14 / Aug 2 2026 — sombrainc.com
- [S11][S13] Governance frameworks; 40% projects canceled by 2027 — gaicc.org; digitalapplied.com
- [S15] Sandboxing (microVM/Firecracker, no-network) — northflank.com
- [S16] Agent identity, JIT scoped access — strata.io; zylos.ai
- [S17] SOC 2 mapping for agents — goteleport.com

**Evals [E]**
- [E1][E2] τ-bench pass^k <25%; one-shot <50% — arxiv.org/abs/2406.12045
- [E4] SOTA agent benchmark scores — simmering.dev/blog/agent-benchmarks
- [E6] Compounding error math (0.95^20≈0.36) — towardsdatascience.com
- [E7] MAST: 41–86.7% failure across 7 frameworks — arxiv.org/pdf/2503.13657
- [E8] Human checkpoints reset risk — mindstudio.ai
- [E9] Outcome + trajectory evals — langchain.com/articles/llm-evaluation-framework
- [E11][E12] LLM-as-judge adoption & biases — vadim.blog; arize.com
- [E13][E14] Offline+online two-layer evals; production monitoring mandatory — langchain.com; anthropic.com/engineering/demystifying-evals-for-ai-agents
- [E15] Observability tooling (LangSmith/Phoenix/Braintrust) — digitalapplied.com

**Competitive [CL] & Context [C]**
- [CL1][CL4][CL5][CL6] Agent builders (AgentKit, Google ADK, LangGraph, CrewAI) — openai.com; cloud.google.com; nxcode.io
- [CL3][CL10][CL11] Copilot Studio / UiPath / Agentforce — mindstudio.ai; uipath.com; redresscompliance.com
- [CL7][CL8][CL9] Zapier/Make/n8n/Workato — n8n.io; digidop.com; hatchworks.com
- [CL12] Sierra $100M ARR / $10B — techcrunch.com; sierra.ai
- [CL13][CL14] Lindy / Gumloop / Relay (reasoning vs fixed sequence) — lindy.ai; gumloop.com
- [CL17] Gartner 40% enterprise apps by 2026 *(directional)* — gartner.com
- [CL18][CL19][C1][C2] Experiment→production gap (15–20%), governance top blocker (~75%) — arionresearch.com; cleanlab.ai; blog.arcade.dev
