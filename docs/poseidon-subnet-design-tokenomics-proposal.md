# Poseidon Subnet Design and Tokenomics Proposal

Date: May 15, 2026
Roadmap targets: Testnet 1 by June 30, 2026; Beta Testnet by September 30, 2026; Mainnet Launch by December 31, 2026
Scope: Testnet 1 with two subnets, Beta Testnet with four launch-candidate subnets, and Mainnet Launch with a two-subnet minimum plus a four-subnet target that is conditional on signed launch partners

## Table of Contents

| Section | What to Read For |
|---|---|
| [Executive Summary](#executive-summary) | Poseidon background, subnet definition, CPVSS context, and launch scope |
| [Design Principles](#design-principles) | The decentralization, centralization, and token-design principles that constrain the proposal |
| [$PSDN Single Token Model](#psdn-single-token-model) | Token utility, role-based staking, agent pool sizing, slashing, and contributor alignment |
| [Incentive and Emission Schedule](#incentive-and-emission-schedule) | Emission caps, canonical CPVSS allocation, revenue pressure model, lock-ups, and fee offsets |
| [CPVSS Overview](#cpvss-overview) | [Stage summary](#stage-summary), [IP registry](#ip-and-licensing-registry-integration), [Collection](#collection-stage), [Parsing](#parsing-stage), [Validation](#validation-stage), [Score](#score-stage), [Search](#search-stage), [beta flow](#end-to-end-beta-flow), and [testnet architecture](#recommended-testnet-architecture) |
| [Open Design Decisions](#open-design-decisions) | Items that should remain flexible until testnet data is available |
| [Milestone Roadmap](#milestone-roadmap) | Monthly gates, launch-partner blockers, campaign plan, and measurable milestone metrics |
| [Conclusion](#conclusion) | Decision scorecard and mainnet blockers |

## Executive Summary

### Background: Poseidon and Subnets

Poseidon is the Data Layer for AI.

Poseidon addresses a structural bottleneck in the AI stack: specialized, rights-cleared, high-quality data. Compute supply can expand with capital expenditure, and model techniques diffuse quickly once published. Data is less fungible. Valuable training data is often domain-specific, multi-modal, proprietary, operational, or newly generated, and it usually requires provenance, quality control, privacy handling, and licensing before it can be used by model developers.

Poseidon coordinates the lifecycle of AI dataset creation:

1. Define what data is needed.
2. Collect data from distributed suppliers.
3. Process and annotate it into AI-ready formats.
4. Validate quality and rights.
5. Register provenance and IP lineage.
6. Make the resulting dataset discoverable and monetizable through a marketplace.

This proposal updates the subnet definition used in earlier materials. A Poseidon subnet is the combination of a decentralized compute network and a CPVSS processing pipeline. The compute network supplies miner agents, validation agents, challengers, and execution capacity. The CPVSS pipeline defines how raw data moves through Collection, Parsing, Validation, Score, and Search until it becomes a usable dataset.

A subnet is therefore not a generic compute cluster and not merely a workflow template. It is a domain-specific data production system. Voice, video, robotics, healthcare, financial-document, and image data have different privacy, bandwidth, storage, validation, fraud-detection, and licensing requirements. Subnets allow each domain to specialize its processing stack and economics while sharing Poseidon infrastructure for provenance, IP management, interoperability, and marketplace access.

The design assumes an IP and licensing registry for provenance, licensing, royalty flows, commitments, and access rights. Story is the preferred integration candidate because it is purpose-built for programmable IP, but the CPVSS ledger should keep a chain-compatible abstraction so Testnet 1 is not blocked if the Story integration is not production-ready. By mainnet, Poseidon should either integrate Story for registered data assets or document the alternative registry it will use for rights-cleared, auditable, commercially defensible datasets.

### CPVSS Processing Pipeline Background

CPVSS stands for Collection, Parsing, Validation, Score, and Search. It is the operating pipeline that converts distributed raw data into AI-ready data assets.

CPVSS matters because raw data alone is not the product. A buyer needs data that matches a specification, avoids spam and duplicates, passes synthetic-fraud checks, includes usable metadata, meets quality thresholds, respects privacy and rights constraints, and can be discovered and licensed later. CPVSS is the control system that enforces those requirements.

At a high level:

1. **Collection** defines the requested data and captures submissions, metadata, consent, provenance, and contributor attribution.
2. **Parsing** uses decentralized compute to transform raw data into structured artifacts such as transcripts, labels, annotations, segments, summaries, or selected video frames.
3. **Validation** checks data quality, fraud, rights, and parser outputs through automated checks, human review, red herrings, stratified sampling, consensus, and challengers.
4. **Score** gives the subnet owner a final quality and usefulness decision, similar to an oracle role, while keeping score batches auditable and challengeable.
5. **Search** turns accepted datasets into a marketplace surface where buyers can discover, inspect, license, and pay for useful data.

The recent subnet strategy discussion reinforced that CPVSS should remain data-specific rather than drifting prematurely into generic compute. Generic compute routing can be a future extension if the miner network becomes deep enough, but Poseidon's near-term technical advantage is the combination of decentralized compute with domain-specific AI data workflows.

The practical reason to introduce subnets is that the current centralized CPVSS pattern becomes expensive and brittle as modalities expand. Poseidon absorbs every dollar of parsing and review cost, centralized reviewers can become susceptible to shirking or gaming, and a single internal roadmap cannot cover every modality at sufficient speed. A subnet turns the same pipeline into an open production system: miner agents compete to run standardized parsing recipes, validation agents stake behind quality decisions, subnet owners propose modality-specific pipelines, and Poseidon keeps the buyer-facing marketplace coherent.

For the first production targets, CPVSS should be grounded in audio and video. The audio pipeline can validate rights-cleared voice data, watermarking, metadata-based fraud controls, and buyer demand. The video pipeline can validate privacy filtering, task-relevance checks, frame selection, transcript or annotation generation, cost-efficient classical computer vision, and selective use of expensive vision-language models only where they improve output quality.

### Proposal Scope

The litepaper explains the broad Poseidon architecture. This proposal translates that architecture into a concrete subnet and tokenomics design for near-term launch, focused on voice and video data.

The design is deliberately hybrid. Collection, Parsing, and Validation benefit from decentralization because the work is distributed, parallelizable, and adversarially checkable. The Score stage should remain under subnet-owner authority because quality assessment determines rewards and commercial acceptance. Search and marketplace distribution should remain centrally managed by Poseidon at the network level to preserve buyer trust, coherent discovery, and revenue control.

The role of crypto is not to decentralize every decision. It is to coordinate independent actors, create accountable staking, preserve contribution and provenance records, route rewards, enforce penalties, and connect dataset revenue back to the participants who created useful data.

By June 30, 2026, Testnet 1 should demonstrate an end-to-end flow for both voice and video data: contribution, provenance tracking, miner-agent parsing, decentralized validation, subnet-owner scoring, reward allocation, points accounting, and dataset discovery through a Poseidon search portal.

By September 30, 2026, Beta Testnet should expand to four launch-candidate subnets, run a user campaign, operate a point system with anti-abuse controls, and demonstrate that partner-led subnets can run CPVSS repeatedly.

By December 31, 2026, Mainnet Launch should activate the signed launch-partner subnets with production-grade staking, reward policy, marketplace flow, partner operating commitments, and launch readiness metrics. The decision-ready minimum is two production subnets, one voice/audio and one video. The four-subnet mainnet target is conditional on closing two additional signed launch partners by November 30, 2026; if that gate is missed, Poseidon should launch a limited mainnet and explicitly label the remaining tracks as post-mainnet expansion.

## Design Principles

1. Decentralize where distributed work creates real value.
2. Centralize where authority, quality control, or commercial distribution needs a clear owner.
3. Keep raw data and large artifacts off-chain, but make provenance, commitments, scores, and reward history auditable.
4. Treat the beta as a working system, not just a protocol demo.
5. Leave room for design decisions in consensus, scoring, slashing, and marketplace economics.
6. Use one token, $PSDN, for the full network. Avoid subnet-specific tokens unless there is a clear technical or economic requirement.
7. Reduce long-term emissions to protect token value, but reserve enough targeted incentives to bootstrap contributors, miner agents, validation agents, and early buyers.
8. Design every reward around game theory: pay for useful verified work, not raw activity.

## $PSDN Single Token Model

Poseidon should use $PSDN as the single network token for staking, rewards, marketplace settlement, fee routing, and penalty accounting.

The design goal is not maximum token emissions. The design goal is a useful network where $PSDN captures value because participants need it to access work, stake behind claims, buy data, and receive rewards from real marketplace demand.

### Token Utility

$PSDN should support five core utilities:

1. Staking: miner agents, validation agents, subnet owners, and possibly curators stake $PSDN to participate in roles where bad behavior creates cost.
2. Rewards: contributors, miner agents, validation agents, and subnet owners receive $PSDN or $PSDN-denominated credits for useful verified work.
3. Settlement: buyers can pay in $PSDN, or fiat payments can be converted into $PSDN-denominated marketplace accounting.
4. Penalties: slashed $PSDN can be burned, routed to an insurance pool, or redistributed to honest participants.
5. Access: advanced marketplace placement, priority jobs, or subnet launch rights can require $PSDN staking or payment.

Access utility should be narrowly defined. $PSDN staking can gate subnet launch proposals, priority job routing for professional operators, premium marketplace APIs, curation programs, and buyer incentive campaigns. It should not let participants buy quality scores, bypass validation, or override marketplace trust rules; access staking is an anti-abuse and capacity-allocation mechanism, not a substitute for CPVSS quality.

### Role-Based Staking Model

> **Skin in the game principle:** any actor who can impose cost on the network should have enough $PSDN at risk that honest behavior is economically better than spam, low-effort work, collusion, or fraud.

The role-based staking model is one of the most important pieces of the tokenomics design because it makes participation economically accountable.

Not every actor should stake the same way. Staking should be required where the actor can impose real cost on the network, and optional or lightweight where high friction would block useful growth.

Assumption for the baseline estimate:

- Total $PSDN supply: 1,000,000,000 tokens.
- Proposed stake amount = total supply x role stake rate.
- Initial production design target: 16 registered and staked miner agents per subnet and 16 registered and staked validation agents per subnet.
- Per-artifact validation panels are smaller than the full staked pool: three validation agents for clear cases and up to seven for escalated cases.
- Beta Testnet availability target: at least 70% of registered agents active during the campaign period. This is an operating-readiness floor, not the denominator for automatically redistributing all rewards.
- Testnet 1 target remains two subnets, likely voice and video.
- Beta Testnet target expands to four launch-candidate subnets.
- Mainnet Launch has a two-subnet minimum and a four-subnet target. The two-subnet minimum should include one voice/audio subnet and one video subnet. The four-subnet target requires signed partner commitments.
- Mainnet launch partner assumption: Poseidon team and Kled team are planning tracks already known to Poseidon. A Korea-based healthcare/data partner such as Big Care and a major AI lab such as ElevenLabs are examples of target partner categories, not committed launch partners. They should not be presented externally as launch partners until signed.
- These are starting-point numbers for design discussion, not final launch parameters.
- Mainnet values should be adjusted by observed token price, participant cost, marketplace revenue, and attack frequency.

| Role | Stake Requirement | Proposed Stake With 1B $PSDN Supply | Initial Network Count Assumption | Why Stake Exists | Slash or Penalty Condition | Game-Theory Purpose |
|---|---|---:|---|---|---|---|
| Individual Contributor | No required stake. Optional stake can increase rewards through a capped multiplier. Past contributors can receive an initial airdrop based on verified contribution history. | Required: 0 $PSDN. Optional: 0-10,000 $PSDN. Reward multiplier capped at 1.25x so quality still matters more than wealth. | Open participation | Keep contribution open while giving serious contributors a way to signal long-term alignment | Duplicate data, fake data, fraudulent rights claims, repeated bad metadata; penalties should usually reduce rewards before slashing optional stake | Prevent low-cost Sybil supply without blocking useful individual contributors |
| Collection Operator | Required for large-scale campaigns or professional data suppliers | 50,000 $PSDN per active campaign, or 0.005% of supply | Campaign-based | Discourage spam, duplicate supply, and rights fraud at scale | Duplicate data, fake data, fraudulent rights claims, repeated bad metadata | Make professional collection operators internalize the cost of bad supply |
| Miner Agent | Required per active miner agent, not only per subnet | Beta floor: 50,000 $PSDN per miner agent. Mainnet target: 200,000 $PSDN per miner agent unless observed utilization is materially lower. With 16 miner agents per subnet, target aggregate miner-agent stake is 3,200,000 $PSDN per subnet, or 0.32% of supply | 16 registered miner agents per subnet for initial beta operation; scale up as job volume grows | Make low-quality parsing costly | Fraudulent output, repeated failed validation, refusal to reveal committed output, persistent missed deadlines | Prevent miner agents from farming bounties with low-cost invalid work |
| Validation Agent | Required per active validation agent | Beta floor: 20,000 $PSDN per validation agent. Mainnet target: 150,000 $PSDN per validation agent unless observed utilization is materially lower. With 16 validation agents per subnet, target aggregate validation-agent stake is 2,400,000 $PSDN per subnet, or 0.24% of supply | 16 registered validation agents per subnet; 3-agent and 7-agent artifact panels are sampled from this larger pool | Ensure validation agents perform independent review | Failed red herrings, provably low-effort validation, collusion, bad challenge behavior | Make honest validation more profitable than rubber-stamping |
| Subnet Owner | Required launch bond or quality bond | 2,500,000 $PSDN per subnet launch, or 0.25% of supply | 1 owner/operator group per subnet | Hold owners accountable for scoring and subnet quality | Repeated scoring abuse, unresolved fraud, marketplace delisting event | Prevent owners from extracting rewards while degrading network trust |
| Curator/Search Participant | Optional stake. Required only when a curator wants boosted placement or participates in a curation market | Optional: 0-100,000 $PSDN per promoted dataset or curation pool. This is a per-pool cap, not a global per-curator cap; if a curator promotes multiple pools, each pool needs separate stake and separate risk exposure | Optional role | Align discovery influence with quality without forcing every curator to stake | Promoting fake demand, low-quality datasets, or self-dealing | Prevent marketplace ranking from becoming pay-to-spam while keeping organic discovery open |
| Buyer | Usually no stake; optional anti-abuse deposit for incentive programs | 0 $PSDN for normal buyers; 25,000 $PSDN only for subsidized buyer programs, or 0.0025% of supply | Open demand side | Buyers should face low friction while incentive programs need anti-wash protection | Fraudulent payment, chargeback abuse, self-dealing for incentives | Keep demand easy while preventing reward farming |

The beta should probably use simulated or capped staking for most roles. Mainnet can harden staking once the actual attack patterns are visible. A practical beta approach is to record the required stake in the ledger and enforce only lightweight penalties until the team has enough data to tune slashing severity.

#### Staking Amount Formula

For each role:

```text
role_stake_tokens = total_psdn_supply x role_stake_rate
```

Using the 1,000,000,000 $PSDN supply assumption:

```text
miner_agent_beta_floor = 1,000,000,000 x 0.00005 = 50,000 $PSDN per miner agent
miner_agent_mainnet_target = 1,000,000,000 x 0.00020 = 200,000 $PSDN per miner agent
miner_agent_subnet_stake_target = 200,000 x 16 = 3,200,000 $PSDN per subnet

validation_agent_beta_floor = 1,000,000,000 x 0.00002 = 20,000 $PSDN per validation agent
validation_agent_mainnet_target = 1,000,000,000 x 0.00015 = 150,000 $PSDN per validation agent
validation_agent_subnet_stake_target = 150,000 x 16 = 2,400,000 $PSDN per subnet

subnet_owner_stake = 1,000,000,000 x 0.0025 = 2,500,000 $PSDN per subnet
```

#### Mainnet Launch Partner Assumption

For mainnet planning, distinguish signed launch tracks from target partner categories. Kled is a contribution provenance and audit-trail partner focused on on-chain contribution records, contributor reputation, and collection workflows. It is not assumed to be a domain-data buyer unless paired with a domain-specific campaign.

| Launch Track | Partner Status | Planning Role | Initial Subnet Focus | Mainnet Rule |
|---|---|---|---|---|
| Poseidon video reference track | Internal Poseidon-operated track | Core protocol, video workflow, marketplace integration, scoring policy, search/distribution | Video data pipeline with privacy filtering, frame selection, annotation, and buyer-facing discovery | Counts toward the two-subnet minimum if production-ready |
| Kled-backed provenance and collection track | Known planning track; domain campaign still required | Contribution provenance and audit-trail partner | On-chain contribution records, contributor reputation, collection workflows for voice or video campaigns | Counts as a subnet only when attached to a concrete voice/video dataset campaign |
| Korea-based healthcare/data partner, such as Big Care | Target category, not committed | Domain data partner | Healthcare-adjacent voice/video data collection and rights workflows | Counts only after signed LOI or launch agreement |
| Major AI lab, such as ElevenLabs | Target category, not committed | Demand and AI-quality partner | Voice/audio model data demand, quality evaluation, commercial dataset requirements | Counts only after signed LOI or launch agreement |

The four-subnet mainnet target is therefore conditional. Poseidon should not claim a four-subnet mainnet unless four subnet tracks have signed owners, approved data rights, and operating runbooks. If only two tracks are signed by November 30, 2026, the mainnet launch scope should be reduced to those signed tracks and the remaining two should become post-mainnet expansion milestones.

Using 16 registered miner agents and 16 registered validation agents per subnet, and using mainnet target stakes for the agent roles:

```text
mainnet_launch_subnets = 4
miner_agents_at_launch = 16 x 4 = 64 miner agents
validation_agents_at_launch = 16 x 4 = 64 validation agents

miner_agent_launch_stake = 3,200,000 x 4 = 12,800,000 $PSDN
validation_agent_launch_stake = 2,400,000 x 4 = 9,600,000 $PSDN
subnet_owner_launch_stake = 2,500,000 x 4 = 10,000,000 $PSDN

core_role_bonded_launch_stake = 32,400,000 $PSDN, or 3.24% of total supply
```

This is an equal-subnet launch assumption for planning and includes only miner agents, validation agents, and subnet owners. It excludes collection-operator campaign bonds and optional curator/search stakes because those are demand-driven and dataset-specific. Additional launch-period bonded stake should be reported separately once the number of collection campaigns, promoted datasets, and curation pools is known.

The stake should be high enough to make malicious behavior expensive, but not so high that only large holders can participate. If the market price of $PSDN rises sharply, the token-denominated stake can be reduced while preserving the same economic security in dollar terms.

#### Agent Pool, Panel Size, and Availability

The design uses three different agent-count concepts that should not be conflated:

| Concept | Planning Number | Meaning | Reward Implication |
|---|---:|---|---|
| Registered and staked pool | 16 miner agents and 16 validation agents per subnet | Target capacity bonded to the subnet for routing, redundancy, rotation, and economic security | Used for stake sizing and baseline per-agent reward caps |
| Active availability floor | >=70% of registered agents during Beta Testnet | Operating-readiness target. With 64 registered validation agents across four subnets, 70% means at least 45 active validation agents, or about 11 active per subnet on average | Falling below the availability floor should reduce usable epoch budget rather than increase payout for the remaining active agents |
| Per-artifact validation panel | 3 agents for normal cases; up to 7 agents for escalated cases | Review quorum for a specific artifact, sampled from the active validation-agent pool | Not every validation agent reviews every artifact; the larger staked pool enables parallelism, randomness, and anti-collusion rotation |

The reward model should not automatically redistribute the entire validation pool to the remaining active agents when availability is below the 16-agent target. Otherwise, 70% activity would create an unintended payout windfall. The correct interpretation is:

```text
registered_agent_target = 16 per subnet
active_agent_floor = registered_agent_target x 70%
per_artifact_panel = 3 for normal review, 7 for escalation

participant_reward_cap = role_epoch_pool / registered_agent_target
participant_reward = min(quality_point_reward, participant_reward_cap)
unused_epoch_pool = role_epoch_pool - sum(actual_participant_rewards)
```

Inactive agents earn zero. Active agents earn according to completed, useful, validated work, but unused budget should return to the unspent incentive reserve by default. Any runway extension or cross-subnet reallocation should require a quarterly policy decision. Unused budget should not mechanically raise active-agent APY.

Validation-agent stake is subnet-scoped by default. A validation agent can operate across multiple subnets, but each subnet requires its own stake or delegated stake because the agent can impose modality-specific review costs and collusion risk in each subnet. Reputation should have two layers: a global agent reputation for identity and long-term behavior, and a subnet-specific reliability score for modality expertise.

#### Slashing Severity

Slashing should be predictable enough to create credible skin in the game, but not so aggressive that honest participants leave after ambiguous mistakes. The default policy should distinguish mistakes, negligence, and fraud:

| Actor | Minor Failure | Repeated or Negligent Failure | Fraud, Collusion, or Rights Abuse | Notes |
|---|---:|---:|---:|---|
| Individual Contributor | Reward denial or 0-5% optional stake penalty | 5-25% optional stake penalty and reputation decay | 25-100% optional stake penalty, reward clawback, campaign ban | Required stake remains zero; most enforcement is reward denial and reputation |
| Collection Operator | 5-10% campaign bond penalty | 10-30% campaign bond penalty | 30-100% campaign bond penalty and campaign termination | Applies to professional or large-scale campaigns, not casual contributors |
| Miner Agent | 5-10% stake penalty for missed reveal or repeated low-quality output | 10-30% stake penalty for persistent invalid work | 30-100% stake penalty for forged output, collusion, or deliberate fraud | Locked rewards should be clawed back before principal stake is slashed |
| Validation Agent | 2-5% stake penalty for failed red herrings or late review | 5-20% stake penalty for repeated low-effort validation | 20-100% stake penalty for collusion, bribery, or provably dishonest votes | Red-herring failures should first reduce reliability score before severe slashing |
| Subnet Owner | Warning, score-batch rollback, or 0-5% launch-bond risk | 5-20% launch-bond penalty and marketplace demotion | 20-100% launch-bond penalty, delisting, or governance removal | Owner slashing requires Poseidon-level adjudication because owner authority is central to Score |
| Curator/Search Participant | Ranking loss or 0-5% pool stake penalty | 5-25% pool stake penalty | 25-100% pool stake penalty for fake demand or self-dealing | Curator stake is per promoted dataset or curation pool |
| Challenger | Challenge bond loss for frivolous or low-evidence claims | Higher bond requirement after repeated failed challenges | Temporary challenge ban for spam or extortion | Honest successful challengers should receive part of penalties or security-pool rewards |

Slashing should be cumulative within an epoch but capped by the actor's stake or campaign bond for that role. Repeat offenses across epochs should increase severity through reputation decay and higher future bond requirements.

#### Contributor Airdrop and Stake Multiplier

Individual contributors should be allowed to start with zero stake. Broad contribution supply is important during bootstrapping, and requiring every contributor to buy tokens before contributing would create unnecessary friction.

Recommended contributor design:

- Initial retroactive airdrop pool: 5,000,000 $PSDN, or 0.5% of total supply.
- Eligibility: verified past contribution, uniqueness, rights clarity, and usefulness after parsing and validation.
- Vesting: 25% liquid at claim, 75% locked for 6 months.
- Optional stake multiplier: contributors can stake up to 10,000 $PSDN to increase future contribution rewards.
- Multiplier cap: maximum 1.25x reward multiplier so staking improves alignment but does not overpower data quality.

Recommended formula:

```text
contributor_reward = base_quality_reward x stake_multiplier
stake_multiplier = min(1.25, 1 + 0.25 x contributor_stake / 10,000)
```

The multiplier should apply only after data passes quality, rights, and duplicate checks. This prevents wealthy contributors from buying rewards with low-quality data.

## Incentive and Emission Schedule

This section is the canonical incentive schedule. The CPVSS stage incentives and the emission budget should be read together: each stage has an incentive mechanism, a weekly emission cap, a lock-up or penalty rule, and a path to reduce emissions as marketplace fees grow.

The detailed CPVSS stage designs later in this document provide implementation options inside this schedule. They should not be treated as separate budgets.

### Emission Philosophy

The network should minimize emissions by default and use them only where they create durable supply-side or demand-side liquidity.

Recommended principles:

- Emit against verified usefulness, not activity volume.
- Treat emission schedules as caps, not calendar inflation. If no useful paid or validated work completes, no new $PSDN should be emitted for that work.
- Cap emissions per epoch and per subnet.
- Prefer job-triggered rewards: token release should follow completed work, validation, scoring, and challenge windows.
- Use stablecoin-floored payout accounting where needed so miner agents and validation agents can cover baseline operating cost, with $PSDN rewards as upside and alignment.
- Convert part of fiat or stablecoin buyer revenue into $PSDN demand through settlement, reward funding, buyback, burn, insurance, or treasury policy.
- Increase rewards when a subnet is supply-constrained and reduce them when marketplace demand can fund the work.
- Prefer delayed rewards, vesting, or clawback windows for work that may later be found low quality.
- Move from emission-funded rewards to fee-funded rewards as soon as a subnet has real buyer demand.
- Use staking locks to reduce circulating supply while forcing participants to internalize the cost of bad behavior.
- Treat role APY as a risk signal. If implied cap APY is too high relative to the stake at risk, the protocol should raise stake requirements, lower emissions, reduce utilization, or route excess to reserve.

### Canonical Emission Schedule

The emission design should bootstrap the network without making emissions the permanent business model. With a 1,000,000,000 $PSDN supply, the recommended starting point is to reserve 120,000,000 $PSDN, or 12% of supply, for a four-year network incentive program. This is a maximum cap, not an obligation to emit.

The operating rule should be "no job, no emission." Weekly epochs are settlement windows, not an automatic inflation clock. If a subnet has idle agents, no accepted jobs, failed validation, unresolved rights issues, or no useful scored output, the corresponding epoch budget should stay in reserve.

#### Epoch Design

Recommended epoch structure:

- Epoch length: 1 week.
- Settlement cadence: rewards are calculated weekly after parsing, validation, scoring, and fraud checks.
- Internal accounting can run daily, but token rewards should settle weekly to leave time for validation and red-herring detection.
- Challenge window: 14 days after each epoch before rewards become final.
- Emission decay: emissions decline each year and should be reduced faster when marketplace fees can fund rewards.

#### Four-Year Emission Cap

| Period | Annual Emission Cap | Percent of 1B Supply | Weekly Epoch Cap | Design Purpose |
|---|---:|---:|---:|---|
| Year 1 | 45,000,000 $PSDN | 4.5% | 865,385 $PSDN per week | Bootstrap supply, miner agents, validation agents, and early demand |
| Year 2 | 35,000,000 $PSDN | 3.5% | 673,077 $PSDN per week | Grow reliable subnets while marketplace revenue starts replacing subsidies |
| Year 3 | 25,000,000 $PSDN | 2.5% | 480,769 $PSDN per week | Shift toward fee-funded rewards |
| Year 4 | 15,000,000 $PSDN | 1.5% | 288,462 $PSDN per week | Maintain strategic incentives only |
| Total | 120,000,000 $PSDN | 12.0% | N/A | Four-year maximum emission budget |

The CPVSS allocation vector should default to the same 35/25/15/10/10/5 split in Years 2-4 unless governance or Poseidon policy explicitly changes it before the relevant year starts. The annual cap declines each year, but the stage mix remains constant by default so the reward model does not drift silently. Any future shift, such as reducing parsing subsidies as fee revenue grows or increasing security/challenge funding after observed attacks, should be published as an updated allocation table.

#### Canonical CPVSS Incentive, Emission, and Revenue-Sharing Schedule

The same top-level CPVSS allocation should govern both emission-funded incentives and fee-funded marketplace revenue. This avoids two competing reward systems. Emissions bootstrap the pool when buyer revenue is not yet sufficient; marketplace revenue later offsets or replaces the matching emission pool.

Assuming a Year 1 weekly emission cap of 865,385 $PSDN and a four-subnet target baseline, rounded to the nearest whole token:

| CPVSS Pool | Canonical Share | Year 1 Weekly Emission Cap | Four-Subnet Weekly Cap Diagnostic | Marketplace Revenue Recipients | Incentive and Penalty Logic |
|---|---:|---:|---:|---|---|
| Collection | 35% | 302,885 $PSDN | 75,721 $PSDN per subnet | Contributors, data rights holders, collection operators | Quality-weighted rewards after parsing, validation, and owner score. Optional contributor stake can add a capped multiplier. Duplicate, fake, or rights-invalid data loses rewards and may trigger clawback or campaign-bond loss. |
| Parsing | 25% | 216,346 $PSDN | 54,087 $PSDN per subnet; up to 3,380 $PSDN per registered miner-agent slot per week before utilization controls | Miner agents | Fixed bounty with quality multiplier for beta. Mainnet can evolve to competitive miner-agent markets. Failed validation reduces payout; fraudulent output, missed reveal, or repeated low-quality work can slash stake. |
| Validation | 15% | 129,808 $PSDN | 32,452 $PSDN per subnet; up to 2,028 $PSDN per registered validation-agent slot per week before utilization controls | Validation agents | Majority consensus with red-herring tasks for beta. Mainnet can add reputation weighting and challenge windows. Failed red herrings, low-effort validation, or collusion reduce rewards and can slash stake. |
| Score | 10% | 86,538 $PSDN | 21,635 $PSDN per subnet owner | Subnet owner/operator | Subnet-owner quality rewards are paid only when score batches pass validation, marketplace quality thresholds, and dispute windows. Scoring abuse can trigger challenge penalties, reputation loss, or launch-bond risk. |
| Search and Marketplace Demand | 10% | 86,538 $PSDN | Network-level pool | Poseidon marketplace, curators/search partners, buyer-demand programs | Supports discovery, dataset packaging, marketplace operations, buyer support, demand routing, and capped demand incentives. Wash demand, self-dealing, or bad curation delays rewards and can slash optional curator stake. |
| Network Security and Challenges | 5% | 43,269 $PSDN | Network-level pool | Challengers, red-herring/audit programs, insurance/burn/buyback reserve | Funds audits, red-herring creation, successful challenges, fraud reports, emergency reviews, and long-term token-value support. Correct challengers can earn part of penalties; failed or spam challenges lose challenge bonds. |

This table is the single source of truth for the top-level CPVSS split. If the mainnet launches with two signed production subnets rather than the four-subnet target, Poseidon should rerun the model with the active subnet count and either scale the launch emission budget to active capacity or publish explicit subnet weights.

These numbers are upper bounds. If a subnet does not produce useful validated work in an epoch, its unused emission should roll back to the unspent incentive reserve by default. There should be no automatic roll-forward and no automatic redistribution to active participants. Reallocation should require a quarterly governance or Poseidon policy decision with a public rationale, because roll-forward, burn, and cross-subnet reallocation have different token-supply and incentive effects.

The "up to" per-agent figures are cap diagnostics, not expected yields. They are anchored to the registered 16-agent capacity target. If only 70% of agents are active, the unused capacity should lower actual utilization rather than redistribute the full pool across 11 active agents.

#### Cap APY Diagnostic

The previous beta-floor stakes of 50,000 $PSDN for miner agents and 20,000 $PSDN for validation agents are too low if the Year 1 emission cap is interpreted as expected annual yield. They should therefore be treated as beta/testnet floors. For mainnet, agent stakes should be raised, emissions should be utilization-gated, and fee-funded revenue should offset emissions rather than stack on top of the full emission cap.

Using the Year 1 cap schedule, 16 registered agents per subnet, four launch subnets, and the proposed mainnet target stakes:

| Role | Mainnet Target Stake | Weekly Cap per Registered Slot | Annual Cap per Registered Slot | Cap APY if Fully Utilized | Modeled APY at 35% Utilization |
|---|---:|---:|---:|---:|---:|
| Miner Agent | 200,000 $PSDN | 3,380 $PSDN | 175,760 $PSDN | 88% | 31% |
| Validation Agent | 150,000 $PSDN | 2,028 $PSDN | 105,456 $PSDN | 70% | 25% |
| Subnet Owner | 2,500,000 $PSDN | 21,635 $PSDN | 1,125,000 $PSDN | 45% | 16% |

The cap APY is still high because Year 1 is a bootstrap budget. That is acceptable only if it remains a cap. It is not acceptable as a steady-state yield promise.

Recommended APY guardrails:

- Miner agents and validation agents: target realized bootstrap APY of roughly 20-60%, with exceptions only for scarce capacity, high-cost workloads, or short tactical campaigns.
- Subnet owners: target realized emission APY of roughly 10-30%, with upside coming primarily from real marketplace revenue and subnet growth.
- If trailing four-week realized APY exceeds the guardrail without a clear capacity shortage, new rewards should be throttled, staked requirements should rise, or unused emissions should return to reserve.
- Fee-funded revenue should first replace emissions for the same CPVSS pool. It should not automatically stack on top of the full emission cap unless Poseidon explicitly chooses a temporary growth subsidy.

The table above replaces separate incentive and revenue-share summaries: incentive mechanism, penalty design, emission budget, and fee-funded revenue split must be changed together.

#### Reward Formula by Epoch

For each role:

```text
role_epoch_pool = network_epoch_emission x role_allocation
subnet_epoch_pool = role_epoch_pool x subnet_weight / sum(all_subnet_weights)
participant_reward = subnet_epoch_pool x participant_quality_points / sum(all_participant_quality_points)
participant_reward = min(participant_reward, participant_epoch_reward_cap)
unused_epoch_pool = subnet_epoch_pool - sum(actual_participant_rewards)
```

Quality points should include:

- Valid work volume.
- Quality score.
- Difficulty of the job.
- Timeliness.
- Red-herring accuracy for validation agents.
- Marketplace demand signal, where applicable.
- Penalty adjustments for failed checks or disputes.
- Active availability versus registered capacity.
- Role APY guardrails.

#### Lock-Up and Vesting

| Role | Liquid at Epoch Settlement | Locked Reward | Lock-Up / Challenge Logic |
|---|---:|---:|---|
| Individual Contributor | 25% | 75% | Locked for 6 months for airdrops; normal contribution rewards can unlock over 90 days after rights and duplicate checks |
| Collection Operator | 40% | 60% | Locked for 90 days because rights issues may surface late |
| Miner Agent | 50% | 50% | Locked for 30-90 days depending on artifact risk and validation confidence |
| Validation Agent | 50% | 50% | Locked for 30-90 days; failed red herrings can claw back locked rewards |
| Subnet Owner | 30% | 70% | Locked for 6-12 months to align long-term subnet quality |
| Curator/Search Participant | 50% | 50% | Locked for 30-90 days to detect fake demand or self-dealing |
| Buyer Incentive Program | 0-25% | 75-100% | Buyer incentives should be conservative and delayed to reduce wash trading |

The 14-day challenge window and the role lock-up periods are separate mechanisms. The 14-day window gates finality for the liquid portion of each epoch reward: if a challenge succeeds, the liquid portion can be delayed, reduced, or clawed back before release. The longer 30-day to 12-month lock-up applies to the locked portion after the challenge window and exists to catch late rights disputes, marketplace quality failures, or delayed fraud evidence.

#### Fee Offset Rule

Emissions should decline as marketplace revenue grows.

Recommended rule:

```text
effective_epoch_emission = max(minimum_security_emission, planned_epoch_emission - fee_funded_rewards)
role_total_reward = min(fee_funded_rewards + effective_epoch_emission, role_reward_guardrail)
```

Where:

- `planned_epoch_emission` is the scheduled $PSDN emission for the epoch.
- `fee_funded_rewards` is the amount of marketplace revenue routed to participants.
- `minimum_security_emission` keeps validation, challenge, and red-herring systems funded even when demand fluctuates.
- `role_reward_guardrail` is the maximum reward that should be paid to a role in an epoch after considering utilization, stake at risk, and target APY.

This prevents the network from overpaying with new emissions when real buyer demand can cover participant costs.

#### Revenue, Buying Pressure, and Selling Pressure

Marketplace revenue should be modeled as external demand for $PSDN. Buyers should not be forced to hold crypto for enterprise procurement. The default policy should allow buyers to pay in fiat, stablecoin, or $PSDN, while Poseidon routes a policy-defined share of net marketplace revenue through $PSDN settlement, reward funding, buyback, burn, insurance, or treasury operations.

The default planning denominator is a 70% $PSDN settlement or conversion ratio on net marketplace revenue after refunds, chargebacks, and taxes. This is not an open placeholder: it is the proposed launch policy. Governance can revise it later, but any change materially affects token demand and should trigger an updated buying/selling pressure model.

The core tokenomics question is whether useful subnet demand can eventually exceed the sell pressure created by emissions.

Recommended model:

```text
annual_subnet_revenue = paid_dataset_accesses x average_dataset_price
network_revenue_year_n = active_subnets x annual_subnet_revenue x (1 + revenue_growth_rate)^(n - 1)

buying_pressure_year_n = network_revenue_year_n x psdn_settlement_ratio
modeled_emission_year_n = effective_emission_year_n x reward_utilization_ratio
selling_pressure_year_n = modeled_emission_year_n x emission_sell_through_ratio
net_pressure_year_n = buying_pressure_year_n - selling_pressure_year_n
```

Where:

- `annual_subnet_revenue` is the $PSDN-equivalent revenue generated by one subnet in a year.
- `psdn_settlement_ratio` is the percentage of revenue that must touch $PSDN through buyer payment, conversion, settlement, buyback, burn, insurance, or treasury policy.
- `reward_utilization_ratio` is the portion of the emission cap actually paid after useful work, availability, quality, APY guardrails, and fee offset.
- `emission_sell_through_ratio` is the estimated percentage of emitted rewards sold by recipients. This should be treated conservatively because early participants may sell to cover operating costs.
- `net_pressure_year_n` is not a price prediction. It is a directional health metric: positive means modeled external demand exceeds modeled emission sell pressure.

Recommended beta/mainnet planning assumptions:

| Parameter | Conservative Starting Point | Why |
|---|---:|---|
| Annual revenue per production subnet | 3,000,000 $PSDN-equivalent | Enough to test meaningful buyer demand without assuming immediate market leadership |
| Active mainnet launch subnets | 2 minimum; 4 target | Four-subnet launch depends on signed partners; the model can be rerun for either launch scope |
| Annual revenue growth | 50% | Aggressive but plausible if partner-led subnets compound supply and demand |
| $PSDN settlement or conversion ratio | 70% | Creates token demand while leaving room for fiat abstraction and operating flexibility |
| Reward utilization ratio | 35% | Models the fact that Year 1 emissions are caps, not automatic yield; unused cap returns to reserve by default |
| Emission sell-through ratio | 65% | Conservative assumption that many early recipients sell some rewards to cover costs |

If Year 1 effective emission cap is 45,000,000 $PSDN, reward utilization is 35%, four subnets each generate 3,000,000 $PSDN-equivalent revenue, 70% of revenue touches $PSDN, and 65% of paid emissions are sold, then:

```text
network_revenue_year_1 = 4 x 3,000,000 = 12,000,000 $PSDN-equivalent
buying_pressure_year_1 = 12,000,000 x 70% = 8,400,000 $PSDN
modeled_emission_year_1 = 45,000,000 x 35% = 15,750,000 $PSDN
selling_pressure_year_1 = 15,750,000 x 65% = 10,237,500 $PSDN
net_pressure_year_1 = -1,837,500 $PSDN
```

This is acceptable for bootstrap if emissions are capped, locked, and tied to useful work. The design goal is for revenue growth, fee routing, and reduced emissions to move net pressure positive over time.

#### Revenue Sharing Rules

Marketplace revenue should use the canonical CPVSS allocation table above. Revenue sharing is therefore not a separate schedule; it is the fee-funded version of the same Collection, Parsing, Validation, Score, Search, and Security pools.

Internal sub-allocations can still vary by contract. For example, the 10% Search and Marketplace Demand pool can be split between Poseidon marketplace operations, curators, search partners, and buyer incentives. The 5% Network Security and Challenges pool can be split between challenger rewards, audit programs, red-herring generation, insurance, buyback, or burn policy. Those internal choices should not create new top-level pools unless the emission schedule is also changed.

Revenue can also offset emissions:

```text
fee_offset_eligible_share = collection_share + parsing_share + validation_share + score_share + search_share + security_share
fee_funded_rewards_year_n = network_revenue_year_n x fee_offset_eligible_share
emission_offset_ratio_year_n = min(100%, fee_funded_rewards_year_n / planned_emission_year_n)
```

Under the default gross-pool model, `fee_offset_eligible_share` is 100% because all marketplace revenue is assigned to the same CPVSS pools used by emissions. If Poseidon later takes an off-top platform fee before CPVSS distribution, that fee should be modeled explicitly by reducing `fee_offset_eligible_share` or by updating both the revenue-sharing table and emission schedule.

Fee-funded payouts should reduce same-pool emissions before they are added as extra upside. For example, validation revenue should first offset validation emissions. Otherwise the model can produce excessive combined APY for validation agents and miner agents even when their stake at risk is low.

Governance or Poseidon policy should decide whether the Network Security and Challenges reserve is burned, retained as an insurance pool, used for buybacks, or routed to ecosystem grants. The safest initial design is to keep it as an insurance pool during testnet and decide burn or buyback policy only after real marketplace behavior is visible.

Open questions:

- Should Poseidon marketplace operations be funded entirely from the Search and Marketplace Demand pool, or should there be an explicit off-top platform fee later?
- Should contributors receive recurring royalties forever, or should some datasets use a capped royalty model?
- Should internal revenue sub-splits be dataset-specific, subnet-specific, or network-standard with limited overrides?
- Should burn/buyback policy be automatic, or discretionary during the first year to preserve operational flexibility?

### Bootstrap Phases

| Phase | Goal | $PSDN Use | Emission Posture |
|---|---|---|---|
| Testnet 1 | Prove CPVSS flow with two voice/video subnets | Testnet $PSDN, off-chain points, or capped internal accounting | No meaningful open-ended emissions |
| Beta Testnet | Expand to four launch-candidate subnets, run user campaigns, and test partner operations | Non-transferable points, testnet $PSDN, simulated staking, and anti-abuse accounting | Capped test incentives for verified useful work |
| Mainnet Launch | Activate signed launch-partner subnets, with two production subnets as the decision-ready minimum and four as the conditional target | $PSDN staking, reward vesting, marketplace fee routing, and published reward rules | Targeted emissions with strict epoch caps and fee-offset rules |
| Growth | Expand subnet count and marketplace demand | Buyer-funded rewards, subnet owner staking, marketplace fee routing | Declining emissions with demand-based rewards |
| Mature Network | Preserve token value and quality | Fee-funded payouts, staking, burns or insurance routing | Minimal emissions, mostly market-funded |

### Game-Theory Threats

The tokenomics must assume rational adversarial behavior.

| Threat | Description | Design Response |
|---|---|---|
| Sybil contribution | Many wallets submit duplicate, fake, or low-rights data | Deduplication, rights checks, delayed rewards, contributor reputation, optional bonds |
| Volume farming | Actors optimize for number of uploads or jobs rather than usefulness | Quality-weighted rewards, owner score, marketplace demand weighting |
| Low-quality parsing | Miner agents submit low-cost, low-quality outputs | Validation consensus, spot checks, stake slashing, delayed payout |
| Low-effort validation | Validation agents rubber-stamp outputs | Red-herring tasks, reliability score, slashing, reduced future assignment |
| Collusion | Contributors, miner agents, and validation agents coordinate to approve bad data | Random assignment, hidden tests, reputation decay, owner scoring, challenge windows |
| Score abuse | Subnet owner manipulates scores to favor insiders | Signed score batches, public audit trail, challenge bond, Poseidon-level monitoring |
| Wash demand | Actors create fake marketplace purchases to trigger rewards | Buyer reputation, fee friction, anomaly detection, reward delay, anti-self-dealing rules |

The table above is a design checklist, not a claim that every defense already exists. Beta Testnet should implement the following minimum controls before any meaningful reward conversion:

- Contributor reputation: account age, wallet or account uniqueness, duplicate rate, rights-valid acceptance rate, dispute history, and accepted-data usefulness.
- Random assignment: validation and parsing assignments should use a verifiable random seed or auditable assignment log so subnet owners cannot quietly route work to friendly agents.
- Hidden tests: red-herring tasks and known-answer validation items should be generated by Poseidon or the subnet owner and mixed into normal queues without advance disclosure.
- Reputation decay: old good behavior should not permanently protect an agent from current bad behavior; recent failures should carry heavier weight.
- Anti-self-dealing: buyer, curator, contributor, miner-agent, and validation-agent relationships should be checked for common ownership before demand incentives are finalized.

### Token Sink Options

To reduce unnecessary emissions and support $PSDN value capture, Poseidon can combine several sinks:

1. Stake locks for miner agents, validation agents, subnet owners, and curators.
2. Marketplace fees paid in $PSDN or converted into $PSDN accounting.
3. Slashed stake burned or routed to an insurance pool.
4. Subnet launch deposits.
5. Priority dataset placement fees.
6. Buyer access passes or subscription tiers.

The beta does not need to finalize every sink. It should define the accounting surface so these mechanisms can be introduced without changing the CPVSS architecture.

## CPVSS Overview

### Stage Summary

| Stage | Function | Decentralization Thesis | Why Crypto Matters | Beta Shape |
|---|---|---|---|---|
| Collection | Gather raw voice and video data, metadata, consent, and provenance | Naturally decentralized because contributors are distributed | On-chain contribution records, audit trails, contributor identity, provenance, and reward eligibility | Contributor upload/API, dataset manifest, content hash, wallet-linked contribution ledger |
| Parsing | Convert raw data into structured artifacts such as transcripts, segments, labels, and metadata | Decentralizable because jobs are parallel and do not require real-time execution | On-chain coordination, miner agent assignment, result commitment, staking, and reward accounting | Miner agent framework for voice and video parsing jobs |
| Validation | Check parsing quality and detect invalid or low-effort work | Strong fit for decentralized consensus through redundant validation agents | Validation agent staking, red-herring tasks, slashing, reputation, and proof-of-usefulness | Multi-agent review, consensus threshold, red-herring detection |
| Score | Assign final quality score and determine reward allocation | Should be centralized by the subnet owner | Crypto makes the score auditable and payout-linked, while authority remains with the owner | Owner scoring service, signed score batches, reward distribution output |
| Search | Enable dataset discovery, access, transactions, and monetization | Should be centralized at the Poseidon network level | Payments, revenue splits, contributor royalties, and provenance-backed marketplace access | Poseidon portal with searchable voice and video datasets |

### IP and Licensing Registry Integration

The CPVSS ledger should separate two layers:

1. Operational commitments: content hashes, manifests, parser output hashes, validation records, score batches, and reward accounting.
2. IP and licensing records: contributor rights, usage permissions, license terms, royalty routing, derivative-dataset lineage, and revocation or dispute status.

Story is the preferred candidate for the second layer. The practical integration plan is:

| Phase | Integration Requirement | Fallback if Story Is Not Ready |
|---|---|---|
| Testnet 1 | Keep Story-compatible fields in the dataset manifest: contributor identity reference, content hash, rights statement, license reference, royalty recipient, and derivative lineage field | Store fields in the internal ledger and export a Story-compatible manifest later |
| Beta Testnet | Register a sample set of accepted voice/video assets or dataset manifests through Story or a Story-compatible adapter | Use signed manifest roots and preserve migration metadata |
| Mainnet Launch | Production datasets need a rights registry before marketplace sale: Story integration or a formally approved alternative | Mainnet marketplace launch should block commercial dataset sale until rights registry is live |

This keeps Story from being a loose marketing reference while avoiding a hard dependency that could block the June testnet.

### Collection Stage

#### Function

Collection is the intake layer for raw voice and video data. It captures the asset, contributor identity, metadata, consent status, usage rights, and provenance information.

#### Goal

The goal is to make contribution easy while ensuring every dataset item has a traceable origin. The system should know who contributed what, when they contributed it, what rights are attached, and how it moved through the pipeline.

#### Decentralization

Collection is naturally decentralized. Contributors are distributed across geographies, communities, platforms, and data sources. A centralized data collection operation can work, but it limits scale and weakens contribution attribution, auditability, and incentive alignment.

The beta should allow contributors or trusted operators to submit data through a simple upload/API flow. Every submitted item should produce a durable record that can later be used for audit, scoring, and payout.

#### Why Crypto Matters

Crypto matters in collection because it creates an auditable contribution ledger. A Kled-style on-chain contribution record can preserve who contributed each asset, what metadata and rights were attached, and how that contribution later created value.

For beta, the system does not need to put raw data on-chain. It should put hashes, contribution metadata, and batch commitments on-chain or in a chain-compatible ledger.

#### Beta Requirements

- Contributor identity linked to wallet or account.
- Upload/API flow for voice and video files.
- Content hash for each submitted item.
- Metadata manifest for each submitted item.
- Consent and rights fields in the manifest.
- Contribution ledger that can support later rewards.
- Metadata-based fraud checks for duplicates, suspicious account patterns, unrealistic language coverage, campaign abuse, duration anomalies, and upload timing.
- Client-side or pre-ingestion filtering for obvious spam so the network does not pay bandwidth, storage, or parsing cost for unusable data.
- Clear rejection explanations when possible, so honest contributors understand whether the issue is language, quality, rights, privacy, or task mismatch.

Pre-ingestion filtering is a centralized cost-control step run by Poseidon or the subnet owner before an item becomes reward-eligible. It should not silently bypass accountability: rejected submissions should receive a rejection reason where feasible, rejected-item hashes and aggregate rejection metrics should be logged, and a random sample of rejected items should be auditable during testnet. No slashing should apply at this stage unless the contributor is a bonded campaign operator or the system detects repeated intentional abuse.

#### Incentive Design Options

##### Design A: Quality-Weighted Contribution Rewards

Contributors do not receive meaningful $PSDN rewards at upload time. They receive provisional credit when data enters the system, then final rewards only after parsing, validation, subnet-owner scoring, and potentially marketplace usage.

Mechanism:

- Contributor submits data and receives a contribution record.
- Duplicate, low-rights, or invalid data receives no reward.
- Useful data earns $PSDN based on quality score, uniqueness, demand, and rights clarity.
- Rewards can vest over time or remain clawback-eligible during an audit window.

Pros:

- Reduces emissions because Poseidon pays for useful data, not raw uploads.
- Encourages contributors to submit higher-quality assets.
- Works well for beta because it does not require heavy staking.

Cons:

- Contributors may dislike delayed rewards.
- New contributors may not know what the network values.
- Sybil attacks remain possible if identity creation is low cost and rewards are too high.

##### Design B: Contributor Bond and Curated Campaigns

Contributors or data collection operators stake a small amount of $PSDN to submit into a campaign. Campaigns define the exact data type needed, quality bar, rights requirements, and reward budget.

Mechanism:

- Poseidon or subnet owners create collection campaigns.
- Contributors stake a small $PSDN bond to participate.
- Valid accepted data earns rewards.
- Duplicate, fake, or rights-invalid submissions can lose part of the bond.
- Campaign budgets cap total emissions.

Pros:

- Stronger spam resistance.
- Easier to guide supply toward useful voice and video datasets.
- Emissions are capped by campaign budget.

Cons:

- Bonds may exclude small contributors or contributors unfamiliar with crypto.
- Campaign design becomes operationally important.
- Slashing for rights problems can be contentious if the contributor made a good-faith mistake.

##### Collection Comparison

| Design | Incentive | Slashing/Penalty | Pros | Cons |
|---|---|---|---|---|
| Quality-weighted rewards | Pay only after data is verified as useful | No or low slashing; delayed reward and clawback | Simple, low-friction, emission-aware | Weaker spam deterrence |
| Contributor bond campaigns | Stake to submit into defined campaigns | Bond loss for duplicate, fake, or rights-invalid data | Better game-theory defense, targeted supply | Higher friction, harder contributor onboarding |

##### Open Questions

- Should small individual contributors be required to stake $PSDN, or only professional collection operators?
- How long should contribution rewards remain clawback-eligible?
- Should marketplace demand affect contributor rewards, or should rewards be based only on quality score?
- How should the system distinguish malicious rights fraud from honest metadata mistakes?

### Parsing Stage

#### Function

Parsing converts raw data into structured artifacts that are useful for AI workflows.

For voice data, parsing may include:

- Audio normalization
- Speech-to-text transcription
- Speaker segmentation
- Language detection
- Topic tagging
- Quality flags

For video data, parsing may include:

- Scene segmentation
- Frame sampling
- Speech transcription
- Object or activity labels
- OCR where applicable
- Metadata extraction

#### Goal

The goal is to transform raw, noisy media into structured datasets that are easier to validate, search, package, and commercialize.

#### Decentralization

Parsing is decentralizable, although not mandatory. Its primary decentralization argument is parallelism. Parsing jobs can be split across many independent miner agents, and most parsing jobs do not require real-time execution.

This makes parsing a good fit for distributed compute:

- Jobs are independent.
- Latency tolerance is relatively high.
- Outputs can be committed and later validated.
- Specialized miner agents can compete on speed, cost, and quality.

#### Why Crypto Matters

Crypto matters because decentralized parsing needs coordination:

- Who receives which job?
- What did the miner agent commit to producing?
- How is the output linked to the input?
- How is the miner agent paid?
- How is bad work penalized?
- How does the system verify completed work without placing large artifacts on-chain?

The key design question is how much coordination happens on-chain versus off-chain. The beta should avoid overbuilding. A practical design is to keep job execution off-chain while recording job commitments, output hashes, miner agent identity, and reward events in an auditable ledger.

#### Beta Requirements

- Miner agent interface.
- Job queue for voice and video parsing.
- Parser output schema.
- Output artifact storage.
- Output hash linked to input hash.
- Miner agent identity and job history.
- Basic parser quality metadata.

#### Incentive Design Options

##### Design A: Fixed Bounty With Quality Multiplier

Each parsing job has a posted $PSDN bounty. Miner agents receive the bounty only after the output passes validation. Higher-quality outputs receive a multiplier based on validation result and subnet-owner score.

Mechanism:

- Miner agent stakes $PSDN to accept jobs.
- Job has a base bounty.
- Output must pass validation before payout.
- High score increases payout.
- Failed or fraudulent output can reduce payout or slash stake.

Pros:

- Easy for miner agents to understand.
- Predictable cost for subnet owners.
- Strong beta fit because it is operationally straightforward.

Cons:

- Miner agents may optimize for easy jobs.
- Fixed rewards can overpay easy work and underpay hard work.
- Quality multipliers require a trusted scoring function.

##### Design B: Competitive Miner Agent Market

Multiple miner agents can bid for or compete on parsing jobs. The network selects miner agents based on price, reputation, stake, historical quality, or a commit-reveal process.

Mechanism:

- Miner agents stake $PSDN to enter the market.
- Jobs can be assigned through auction, reputation routing, or random weighted assignment.
- Miner agents commit output hashes before revealing outputs.
- Spot audits and validation agent results determine payout.
- Repeated low-quality work reduces reputation or slashes stake.

Pros:

- Encourages price and quality competition.
- Supports specialized miner agents for different media types.
- Can reduce long-term emissions by letting market pricing replace subsidies.

Cons:

- More complex than fixed bounties.
- Auctions can be gamed by underbidding.
- Commit-reveal adds operational overhead.

##### Parsing Comparison

| Design | Incentive | Slashing/Penalty | Pros | Cons |
|---|---|---|---|---|
| Fixed bounty with quality multiplier | Base reward plus score-based upside | Stake slash or no payout for failed output | Simple, predictable, beta-ready | Risk of volume farming and mispriced jobs |
| Competitive miner agent market | Market-priced jobs and reputation routing | Stake slash, reputation loss, spot-audit penalty | Scales toward efficiency | More mechanism complexity |

##### Open Questions

- Should miner agents stake per job, per epoch, or per subnet?
- Should hard jobs pay more automatically based on file length, media quality, or scarcity?
- How many parser failures should trigger slashing versus only reputation loss?
- Should the beta use permissioned miner agents first, then open participation later?

### Validation Stage

#### Function

Validation checks whether parsing outputs are accurate, complete, and useful. It is the quality-control layer between miner agent work and final scoring.

#### Goal

The goal is to prevent low-quality parsing from entering the marketplace and to create an incentive-compatible mechanism for validation agents to perform real review work.

#### Decentralization

Validation is a particularly strong fit for decentralization in the CPVSS pipeline. Multiple validation agents can independently review parser outputs, and their results can be aggregated through a consensus algorithm.

For beta, validation should focus on practical consensus rather than perfect mechanism design. The first version should demonstrate that redundant validation can detect bad outputs and produce a reliable quality signal.

#### Why Crypto Matters

Crypto matters because validation agents need incentives, accountability, and penalties. Validation agents can stake reputation or tokens. Correct validation earns rewards. Low-effort or dishonest validation can be penalized.

The red-herring mechanism is especially useful. The system can inject known test cases into validation queues. Validation agents who repeatedly fail these hidden checks can be down-weighted or slashed.

#### Consensus Design Space

Open design questions include:

- Number of validation agents per artifact.
- Required agreement threshold.
- Weighting by validation agent reputation.
- Handling disagreement between validation agents.
- Red-herring frequency.
- Slashing severity.
- Appeals or owner override.
- Whether validation produces binary pass/fail, graded scores, or structured comments.

#### Beta Requirements

- Validation agent assignment flow.
- Validation schema.
- Registered validation-agent pool of 16 per subnet, with at least 70% active during Beta Testnet.
- At least three validation agents per selected artifact, sampled from the active pool where feasible.
- Two-stage consensus rule: accept clear 2-of-3 agreement, then escalate uncertain or disputed cases to a larger 5-of-7 review.
- Active-pool shortfalls should reduce validation throughput or epoch-budget utilization; they should not increase per-agent reward caps.
- Red-herring task injection.
- Validation agent reliability score.
- Basic slashing or down-weighting simulation.

#### Incentive Design Options

##### Design A: Majority Consensus With Red Herrings

Each artifact is reviewed by multiple validation agents. Validation agents earn rewards when they complete reviews and align with consensus, but they are penalized when they fail hidden red-herring tasks.

Mechanism:

- Validation agents stake $PSDN to participate.
- Artifacts are randomly assigned.
- Red-herring tasks with known answers are mixed into the queue.
- Validation agents earn rewards for timely, accurate validation.
- Validation agents who fail red herrings lose reliability score and may be slashed.

Pros:

- Operationally clear validation model.
- Red herrings directly target low-effort validation.
- Strong beta fit.

Cons:

- Consensus can reward herding.
- Honest minority validation agents may be punished if the majority is wrong.
- Colluding validation agents can still pass bad outputs if assignment randomness is weak.

##### Design B: Reputation-Weighted Validation With Challenge Window

Validation agent votes are weighted by historical accuracy, stake, and red-herring performance. Disputed results can enter a challenge window where challengers stake $PSDN to request owner or expert adjudication.

Mechanism:

- Validation agents stake $PSDN and build reliability reputation.
- Vote weight depends on accuracy and past behavior.
- Low-confidence consensus triggers additional review.
- Challengers can bond $PSDN to dispute a result.
- Correct challenges earn part of the penalty; incorrect challenges lose the bond.

Pros:

- Better quality over time because good validation agents gain weight.
- Challenge windows reduce damage from bad consensus.
- Creates a path for expert correction.

Cons:

- More complex to explain and implement.
- Reputation can entrench early validation agents.
- Challenge mechanisms can be spammed if the bond is too low.

##### Validation Comparison

| Design | Incentive | Slashing/Penalty | Pros | Cons |
|---|---|---|---|---|
| Majority consensus with red herrings | Reward consensus and hidden-test accuracy | Slash or down-weight validation agents who fail red herrings | Operationally simple defense against low-effort validation | Herding and collusion risk |
| Reputation-weighted validation | More weight and rewards for proven validation agents | Slash for failed tests, wrong challenges, or repeated bad votes | Better long-term quality | Complexity and possible validation-agent oligopoly |

##### Open Questions

- How often should red-herring tasks appear?
- Should validation agents be rewarded for disagreeing with a wrong majority after adjudication?
- Should slashing burn $PSDN, compensate harmed parties, or fund future validation?
- How should the system detect validation-agent collusion beyond red-herring failure?

### Score Stage

#### Function

Scoring is the final quality and usefulness assessment. It determines how much value a contribution, parser output, or validation action should receive.

#### Goal

The goal is to make reward distribution accountable while preserving the subnet owner's authority over final quality.

#### Decentralization

Scoring should be centralized. The subnet owner has the ultimate responsibility to determine quality, usefulness, and reward allocation. This is especially important because the score directly affects token distribution.

Trying to decentralize scoring too early could weaken accountability. For beta, the subnet owner should retain explicit final authority.

#### Why Crypto Matters

Crypto still matters in this centralized stage because the scoring output can be auditable. A subnet owner can publish signed score batches, reward allocation records, and references to the underlying artifacts and validation results.

This creates transparency without pretending that quality judgment is fully objective.

#### Beta Requirements

- Owner scoring interface or admin workflow.
- Score schema.
- Signed or auditable score batch.
- Reward allocation output.
- Linkage from score to contribution, parsing, and validation records.
- Manual override ability.

#### Incentive Design Options

##### Design A: Owner-Signed Scoring With Challenge Bond

The subnet owner signs final score batches. Participants can challenge a score by posting a $PSDN bond during a challenge window.

Mechanism:

- Owner publishes signed score batch.
- Score determines final reward allocation.
- Any affected participant can challenge by bonding $PSDN.
- Valid challenge triggers correction and possibly owner penalty or reputation loss.
- Invalid challenge loses bond.

Adjudication should default to a Poseidon-level review panel during beta and mainnet launch. The panel should include one Poseidon protocol representative, one modality/domain reviewer for the subnet, and one independent reviewer when the disputed reward or penalty exceeds a published threshold. The subnet owner should provide evidence and can defend the score, but should not be the final adjudicator for challenges against its own score batch. Decisions should produce a signed adjudication record that updates the score batch, challenger bond, owner reputation, and any slashing action.

Pros:

- Preserves clear owner authority.
- Gives participants a safety valve against obvious scoring abuse.
- Keeps beta implementation manageable.

Cons:

- Challenge resolution still needs an adjudicator.
- Too many challenges can slow payout.
- If the challenge bond is too high, small contributors cannot contest bad scores.

##### Design B: Model-Assisted Rubric With Owner Veto

Scores are generated from a transparent rubric, optionally assisted by models or evaluators, and the subnet owner has final veto authority.

Mechanism:

- Rubric defines quality dimensions.
- Model or evaluation workflow proposes a score.
- Owner approves, adjusts, or vetoes the score.
- Score batch is signed and published.
- Outlier adjustments are logged for audit.

Pros:

- More consistent than fully manual scoring.
- Easier to explain score differences.
- Creates training data for future scoring automation.

Cons:

- Models can be wrong or biased.
- Participants may over-optimize for the rubric instead of true usefulness.
- Owner veto still creates centralization concerns.

##### Score Comparison

| Design | Incentive | Slashing/Penalty | Pros | Cons |
|---|---|---|---|---|
| Owner-signed scoring with challenge bond | Owner controls final rewards with accountable audit trail | Challenge bond loss; possible owner reputation penalty | Clear authority, beta-ready | Requires fair adjudication |
| Model-assisted rubric with owner veto | Transparent scoring criteria plus owner control | Outlier logging, challenge bond, owner reputation risk | More consistent and scalable | Rubric gaming and model bias |

##### Open Questions

- What challenge-bond size keeps spam low without pricing out small contributors?
- What reward or penalty threshold should trigger an independent reviewer?
- How much scoring transparency is safe before participants start gaming the rubric?

### Search Stage

#### Function

Search is the user-facing discovery and marketplace layer. It lets users find, inspect, request, purchase, or access processed datasets.

#### Goal

The goal is to make Poseidon the central marketplace for AI-ready voice and video datasets.

#### Decentralization

Search should be centralized at the network level. Poseidon should manage the portal, ranking, access flow, transactions, and marketplace rules. This creates a coherent user experience and gives the project a direct revenue engine.

#### Why Crypto Matters

Crypto matters because marketplace transactions can connect back to provenance and contribution history. Revenue can be routed through the same CPVSS pools used by the emission schedule, with transparent records for Collection, Parsing, Validation, Score, Search and Marketplace Demand, and Network Security and Challenges.

The marketplace is where the crypto incentive loop becomes economically meaningful.

#### Beta Requirements

- Searchable dataset portal.
- Dataset detail page.
- Provenance summary.
- Quality score display.
- Voice and video filters.
- Basic access or request flow.
- Marketplace transaction placeholder or testnet payment flow.

#### Incentive Design Options

##### Design A: Marketplace Fee Split

Dataset buyers pay through the Poseidon marketplace. Fees are routed through the CPVSS revenue pools according to the same top-level allocation used by the Year 1 emission schedule, then distributed internally according to dataset contribution, quality, marketplace, and security records.

Mechanism:

- Buyer pays in $PSDN or a payment rail that maps into $PSDN accounting.
- Marketplace fees follow the CPVSS revenue policy unless governance explicitly approves an off-top platform fee.
- Prior CPVSS records determine who receives value inside the Collection, Parsing, Validation, and Score pools.
- The Search and Marketplace Demand pool funds Poseidon marketplace operations, curators/search partners, buyer support, and demand incentives.
- The Network Security and Challenges pool funds challengers, audits, red-herring generation, insurance, buyback, or burn policy.

Pros:

- Rewards are backed by real demand rather than emissions.
- Aligns all actors around commercially useful data.
- Strong long-term model for preserving $PSDN value.

Cons:

- Does not bootstrap supply if early buyer demand is weak.
- Revenue attribution can be hard when many assets compose one dataset.
- Contributors may wait too long for meaningful payouts.

##### Design B: Capped Demand Incentives With Anti-Wash Rules

Poseidon uses capped $PSDN incentives to bootstrap marketplace activity, but rewards only unlock when there is verified demand, quality, and non-self-dealing behavior.

Mechanism:

- Dataset receives eligibility based on score and provenance.
- Early buyer activity can unlock capped incentive rewards.
- Wash-trading signals delay or block rewards.
- Curators or subnet owners may stake $PSDN behind featured datasets.
- Bad curation or fake demand can lose stake or ranking.

Pros:

- Helps bootstrap demand before marketplace fees are large.
- Makes emissions conditional on usage, not just supply.
- Staked curation can improve search quality.

Cons:

- Fake demand is a serious risk.
- Incentive design can become complex.
- Emissions may leak to actors who are good at farming demand signals.

##### Search Comparison

| Design | Incentive | Slashing/Penalty | Pros | Cons |
|---|---|---|---|---|
| Marketplace fee split | Pay from real buyer demand | No direct buyer slashing; bad actors lose ranking or access | Sustainable, emission-light | Slow bootstrap |
| Capped demand incentives | Subsidize early useful marketplace activity | Curator or subnet owner stake can be slashed for fake demand | Accelerates network effects | Wash trading and subsidy farming risk |

##### Open Questions

- Should the 70% $PSDN settlement/conversion policy be raised or lowered after real buyer procurement data is available?
- Within the Search and Marketplace Demand pool, what share should fund Poseidon marketplace operations versus curators, search partners, and buyer-demand incentives?
- Should a portion of revenue be burned, routed to insurance, or used for buyback-style reward pools?
- How should the marketplace detect and penalize self-dealing or fake demand?

### End-to-End Beta Flow

1. Contributor uploads voice or video data.
2. System creates a content hash, metadata manifest, contributor record, and audit trail.
3. Miner agent receives a job.
4. Miner agent produces structured artifacts.
5. Parser output is stored off-chain and committed through an output hash.
6. Validation agents review parser output.
7. Red-herring validation tasks detect low-effort or dishonest validation agents.
8. Consensus produces a validation result.
9. Subnet owner reviews final artifacts and assigns a score.
10. Reward allocation is generated from contribution, parsing, validation, and owner score.
11. Dataset appears in the Poseidon search marketplace.
12. Users discover, preview, and request or purchase access.

### Recommended Testnet Architecture

#### Off-Chain

- Raw voice and video files
- Parsed transcripts and structured artifacts
- Validation agent comments
- Search index
- Marketplace UI
- Admin scoring dashboard

#### On-Chain or Chain-Compatible Ledger

- Contributor identity reference
- Input content hash
- Dataset manifest hash
- Parser job commitment
- Parser output hash
- Validation agent participation record
- Consensus result hash
- Score batch hash
- Reward allocation record
- Marketplace transaction record

For Testnet 1 and Beta Testnet, a chain-compatible ledger or testnet contract is sufficient. The system should be designed so the testnet ledger can later be upgraded to production smart contracts.

## Open Design Decisions

These decisions should remain open during testnet design and be resolved only when real workflow evidence appears:

1. Whether testnet rewards use testnet tokens, off-chain points, or capped token-denominated accounting.
2. Whether contribution records are written individually or batched through Merkle roots.
3. Whether voice and video share one subnet framework or use two separate subnet templates.
4. How validation agents are selected and weighted.
5. How aggressive red-herring slashing should be.
6. Whether miner agents need simulated staking in Testnet 1 and Beta Testnet.
7. Whether search ranking should include quality score, commercial demand, freshness, or subnet owner reputation.
8. Whether score decisions are manually assigned, model-assisted, or hybrid.
9. Whether buyers transact directly with subnet owners or through Poseidon as marketplace operator, while preserving the 70% $PSDN settlement/conversion policy.
10. What minimum $PSDN stake is required for each role without excluding useful early participants.
11. Whether slashed $PSDN should be burned, routed to insurance, or redistributed to honest participants.
12. How quickly emissions should decline as marketplace revenue grows.
13. Whether the 70% $PSDN settlement/conversion ratio should change after testnet buyer data is available.
14. How to prevent early high-stake actors from capturing validation agent or miner agent reputation permanently.

## Milestone Roadmap

The roadmap should be managed by monthly milestone gates, not weekly task lists. Each gate must demonstrate a product capability, a testing level, a points or reward-accounting capability, and a launch-partner readiness level.

The three hard milestone dates are:

| Milestone | Target Date | Subnet Scope | Launch Meaning |
|---|---:|---|---|
| Testnet 1 | June 30, 2026 | 2 subnets: voice and video | Prove the CPVSS loop works end to end with testnet or internal points accounting |
| Beta Testnet | September 30, 2026 | 4 launch-candidate subnets | Run partner-led subnet operations, user campaigns, points system, anti-abuse controls, and marketplace testing |
| Mainnet Launch | December 31, 2026 | 2 signed production subnets minimum; 4 signed launch-partner subnets target | Launch production staking, reward policy, marketplace flow, and partner-backed subnet operations. Four-subnet launch is conditional on signed partners |

### Monthly Milestones

| Month | Product and Protocol Milestone | Testing and Campaign Milestone | Launch-Partner Blocker | Exit Metrics |
|---|---|---|---|---|
| May 2026 | Lock CPVSS architecture, schemas, role-based staking assumptions, point-accounting model, IP registry abstraction, and Testnet 1 scope | Create test plan, seed datasets, red-herring strategy, QA checklist, internal points ledger spec, and Story-compatible manifest fields | Biz team assigns partner owner for Poseidon, Kled, Korea-based data partner, major AI lab track, and a dedicated video-domain track | Architecture approved; voice/video subnet specs drafted; points ledger spec approved; partner pipeline owner named for all launch tracks |
| June 2026 | Launch Testnet 1 with 2 subnets: voice and video | Run invite-only user campaign, internal/testnet points, end-to-end CPVSS QA, parser/validation/scoring dry runs, and marketplace discovery test | Poseidon and Kled technical owners confirmed; external partner pitch pack delivered to Korea partner and AI lab candidates | 2 subnets live; 16 miner-agent slots and 16 validation-agent slots configured per subnet; >=20 full CPVSS runs; >=95% manifest completeness; no open P0/P1 launch bugs |
| July 2026 | Convert Testnet 1 learnings into Beta Testnet architecture for 4 launch-candidate subnets | Expand campaign tooling, anti-Sybil checks, points dashboards, validation-agent red-herring library, Story-compatible export, and load-test plan | At least 2 external launch-candidate partners have signed LOI or equivalent written commitment, including at least 1 video-specific partner or campaign | 4-subnet templates ready; points fraud rules drafted; partner data requirements captured; beta campaign terms drafted |
| August 2026 | Stand up 4 Beta Testnet subnet environments and partner onboarding workflow | Run closed partner pilots, rights review, data-quality QA, security review, economic simulation, and campaign rehearsal | All 4 launch-candidate partners assign business owner, technical owner, data owner, and campaign owner | 4 subnets deployed in staging/testnet; >=64 miner-agent registrations; >=64 validation-agent registrations; partner sample datasets ingested; no unresolved data-rights blocker |
| September 2026 | Launch Beta Testnet with 4 subnets | Run public or partner-led user campaign, points leaderboard, anti-abuse review, marketplace access tests, and partner operating drills | All 4 launch-candidate partners actively participate in Beta Testnet with signed campaign terms and data rights approval | 4 subnets live; >=500 contributor or user accounts; >=5,000 accepted data items or partner-approved equivalent; parser success >=90%; red-herring detection >=90%; no open P0/P1 launch bugs |
| October 2026 | Freeze mainnet architecture, production tokenomics parameters, Story or alternative IP registry decision, and launch-scope decision tree | Run audit prep, incident-response drills, reward replay tests, data deletion/rights workflows, and marketplace transaction QA | Mainnet partner agreement drafts circulated to all candidate launch partners; at least 2 production subnet tracks are identified as minimum launch scope | Mainnet contract or ledger design frozen; reward formula replay passes; slashing/challenge policy approved; marketplace fee split draft approved; IP registry decision approved |
| November 2026 | Complete mainnet release candidate and launch operations plan | Run security review, economic attack simulation, load test, points audit, partner launch rehearsal, and disaster-recovery rehearsal | At least 2 launch partners sign mainnet launch agreement or binding equivalent; 4-subnet launch requires 4 signed partners, including a voice/audio track and a video track | 2-week release candidate stable; audit issues triaged; points-to-reward policy approved if applicable; partner launch runbook signed off; final launch scope declared as 2, 3, or 4 subnets |
| December 2026 | Launch mainnet with signed launch-partner subnets | Run final production readiness review, launch monitoring, post-launch support plan, and marketplace transaction verification | No mainnet launch without at least 2 signed production subnet tracks, approved data rights, operator runbooks, and staking/reward commitments. No four-subnet claim without 4 signed tracks | Signed mainnet subnets live; staking/reward policy active; marketplace access flow live; partner dashboards live; rights registry live; no open P0/P1 launch bugs |

### Mandatory Launch-Partner Blockers

These are milestone blockers, not optional business-development notes. A milestone should not be marked complete if the matching partner dependency is missing.

| Blocker | Required By | Why It Matters | Proof Needed |
|---|---:|---|---|
| Four named launch-candidate tracks | May 31, 2026 | The beta roadmap depends on four candidate tracks, but mainnet scope should be based only on signed partners | Named internal owner, target partner or internal operator, target subnet thesis, commitment status, and next meeting for Poseidon, Kled, Korea-based partner, AI lab track, and video-domain track |
| Poseidon and Kled Testnet 1 participation | June 30, 2026 | Testnet 1 needs at least two credible operators to demonstrate contribution provenance and CPVSS operations | Technical owner, sample data or workflow, testnet account, and feedback loop |
| Two external partner commitments | July 31, 2026 | The September 4-subnet target cannot wait until September for partner discovery | LOI, written intent, pilot scope, or equivalent written approval; at least one should cover video-specific data or a video buyer workflow |
| Four Beta Testnet partner workstreams | August 31, 2026 | Beta Testnet needs data, campaign, legal, and technical owners before launch | Named business owner, technical owner, data rights owner, campaign owner, and launch dataset for each partner |
| Four active Beta Testnet partners | September 30, 2026 | A 4-subnet beta without real partner participation does not test mainnet operations | Partner-led subnet activity, campaign terms, data rights approval, and recurring operating review |
| Minimum signed mainnet launch partners | November 30, 2026 | December launch requires legal, operational, and commercial certainty | At least 2 signed production subnet tracks for limited mainnet; 4 signed tracks required only for the four-subnet mainnet claim. Each signed track needs launch dataset commitment, operating runbook, marketplace terms, data-rights approval, and staking/reward acknowledgment |

### User Campaign and Points System

The testnet campaign should use non-transferable points first. Points should reward verified usefulness, not raw activity, and should not imply guaranteed token conversion unless Poseidon later publishes a formal conversion policy.

| Phase | Campaign Design | Points Design | Abuse Controls |
|---|---|---|---|
| Testnet 1 | Invite-only campaign for contributors, miner agents, validation agents, and early dataset users | Internal points for accepted contribution, completed parsing, correct validation, useful challenges, and marketplace feedback | Wallet/account uniqueness, duplicate detection, manifest completeness checks, red-herring validation, manual review |
| Beta Testnet | Public or partner-led campaign across 4 launch-candidate subnets | Visible points dashboard, role-specific points, quality multipliers, capped referral or campaign boosts, delayed finalization | Sybil scoring, rights review, anomaly detection, challenge window, leaderboard audit, partner data-quality review |
| Mainnet Launch | Points campaign closes or converts into production reward/accounting policy if approved | Published points audit and reward policy; no retroactive ambiguity | Legal review, fraud exclusions, conversion cap if applicable, vesting, clawback window, partner sign-off |

### Milestone Metrics

These metrics are proposed planning targets. They should be tuned as real testnet data arrives, but each milestone needs measurable exit criteria.

| Metric Category | Testnet 1 by June 30, 2026 | Beta Testnet by September 30, 2026 | Mainnet Launch by December 31, 2026 |
|---|---|---|---|
| Subnets | 2 live subnets: voice and video | 4 live Beta Testnet launch-candidate subnets | 2 signed production subnets minimum; 4 signed subnets target |
| Partner Readiness | Poseidon and Kled active; 2 external partner tracks in active BD | 4 launch-candidate partners active in Beta Testnet | At least 2 signed launch partners with data, legal, ops, and campaign commitments; 4 signed partners required for four-subnet launch claim |
| Agent Network | 16 miner-agent slots and 16 validation-agent slots configured per subnet; permissioned agents acceptable | >=64 miner-agent registrations and >=64 validation-agent registrations across 4 subnets; >=70% active during the campaign period, meaning at least 45 active agents network-wide and roughly 11 active agents per subnet on average | Production agent registry active; staking or launch-bond rules enforced; agent reliability history migrated or initialized |
| Data Supply | >=2 curated seed datasets; >=95% accepted items include manifest, content hash, and rights metadata | >=5,000 accepted data items or partner-approved equivalent; >=90% rights metadata completeness | Partner launch datasets committed; data-rights workflow approved; deletion and dispute workflow tested |
| CPVSS Throughput | >=20 full end-to-end CPVSS runs across voice and video | >=200 full CPVSS runs across 4 subnets | Two-week release candidate with stable daily CPVSS processing |
| Quality and Validation | Parser job success >=80%; validation consensus produced for >=90% completed jobs; red-herring detection >=80% | Parser job success >=90%; validation consensus produced for >=95% completed jobs; red-herring detection >=90% | Mainnet quality thresholds approved; challenge and slashing policy active; no unresolved high-risk validation issue |
| Points and Rewards | Points ledger v0 records contribution, parsing, validation, scoring, and search feedback | Points dashboard live; leaderboard audited; fraud review completed before final points settlement | Points audit complete; mainnet reward or conversion policy approved if applicable; vesting and clawback rules active |
| Marketplace | Search portal shows processed datasets with provenance and quality score | 4 subnet marketplace pages live; request/access flow tested with design partners | Marketplace access and transaction flow live; fee split, 70% $PSDN settlement/conversion policy, and revenue accounting verified |
| Reliability | No open P0/P1 bugs at milestone close; observability dashboard live | No open P0/P1 bugs; load test passes 5x Testnet 1 traffic assumptions | No open P0/P1 bugs; launch monitoring, incident response, and rollback plan approved |
| Security and Compliance | Basic threat model and rights checklist complete | Security review, rights review, anti-Sybil review, Story-compatible manifest review, and economic simulation complete | Security review issues triaged; partner legal approvals complete; Story or alternative rights registry live; production readiness review signed off |

## Conclusion

The subnet architecture should be evaluated on operational and economic grounds: whether it can produce higher-quality AI data at acceptable cost, whether it can detect low-quality or fraudulent work, whether participants have appropriate economic exposure, and whether buyer revenue can progressively replace emissions.

The design does not require full decentralization. It uses decentralization where distributed execution and adversarial verification improve the system, and it preserves central authority where quality judgment, marketplace trust, and commercial distribution require accountable ownership. CPVSS is the mechanism that connects these choices into a single production workflow.

### Decision Scorecard

| Area | Status | Decision or Blocker |
|---|---|---|
| CPVSS architecture | Locked for testnet | Collection, Parsing, Validation, Score, and Search remain the operating pipeline |
| Token model | Locked for proposal | Single-token $PSDN model with staking, rewards, settlement, penalties, and access utility |
| Launch scope | Partially locked | Testnet 1 is 2 subnets; Beta Testnet is 4 launch-candidate subnets; mainnet is 2 signed subnets minimum and 4 signed subnets only if partner closure succeeds |
| Staking model | Proposed | Mainnet target stakes are set for miner agents, validation agents, and subnet owners; collection and curator stakes remain campaign-specific |
| Emission model | Proposed | Four-year cap, Year 1 CPVSS allocation, default same allocation for Years 2-4, no-job-no-emission rule, unused weekly emissions return to reserve by default |
| Slashing model | Proposed | Severity ranges are defined; exact thresholds should be tuned during testnet |
| Score adjudication | Locked for beta | Poseidon-level review panel adjudicates score challenges; subnet owners cannot adjudicate challenges against their own score batches |
| Buyer settlement | Proposed launch policy | Buyers can pay fiat, stablecoin, or $PSDN; Poseidon routes 70% of net marketplace revenue through $PSDN settlement/conversion by default |
| IP and rights registry | Mainnet blocker | Story is preferred; a Story-compatible abstraction is required for testnet, and Story or an approved alternative is required before commercial mainnet dataset sale |
| Partner readiness | Mainnet blocker | Four-subnet launch requires four signed tracks, including voice/audio and video coverage. If not signed by November 30, 2026, mainnet scope should be reduced and labeled accordingly |
