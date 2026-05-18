# Poseidon Subnet CPVSS Design and Beta Roadmap

Date: May 15, 2026  
Beta target: June 30, 2026  
Scope: Two production beta subnets for voice and video data

## Executive Summary

The subnet design should use crypto where crypto creates a real advantage: coordinating distributed labor, preserving contribution history, proving provenance, creating auditable reward trails, and enabling a marketplace for AI data.

The design should not claim that every part of the system must be decentralized. A stronger and more credible architecture is hybrid:

- Collection, parsing, and validation benefit directly from decentralization.
- Scoring should remain controlled by the subnet owner.
- Search and marketplace distribution should remain centrally managed by Poseidon at the network level.

This gives Poseidon a clear thesis:

> Crypto is not here to decentralize everything. Crypto is here to coordinate distributed AI data work, make contribution and quality auditable, and create programmable ownership and payout rails for useful AI datasets.

The CPVSS pipeline is:

1. Collection
2. Parsing
3. Validation
4. Score
5. Search

By the end of June 2026, the beta should demonstrate an end-to-end working flow for both voice and video data: contribution, provenance tracking, miner parsing, decentralized validation, subnet-owner scoring, reward allocation, and dataset discovery through a Poseidon search portal.

## Design Principles

1. Decentralize where distributed work creates real value.
2. Centralize where authority, quality control, or commercial distribution needs a clear owner.
3. Keep raw data and large artifacts off-chain, but make provenance, commitments, scores, and reward history auditable.
4. Treat the beta as a working system, not just a protocol demo.
5. Leave room for design decisions in consensus, scoring, slashing, and marketplace economics.
6. Use one token, $PSDN, for the full network. Avoid creating subnet-specific tokens unless there is an overwhelming reason later.
7. Reduce long-term emissions to protect token value, but reserve enough targeted incentives to bootstrap contributors, miners, validators, and early buyers.
8. Design every reward around game theory: pay for useful verified work, not raw activity.

## $PSDN Single Token Model

Poseidon should use $PSDN as the single network token for staking, rewards, marketplace settlement, fee routing, and penalty accounting.

The design goal is not maximum token emissions. The design goal is a useful network where $PSDN captures value because participants need it to access work, stake behind claims, buy data, and receive rewards from real marketplace demand.

### Token Utility

$PSDN should support five core utilities:

1. Staking: miners, validators, subnet owners, and possibly curators stake $PSDN to participate in roles where bad behavior creates cost.
2. Rewards: contributors, parsers, validators, and subnet owners receive $PSDN or $PSDN-denominated credits for useful verified work.
3. Settlement: buyers can pay in $PSDN, or fiat payments can be converted into $PSDN-denominated marketplace accounting.
4. Penalties: slashed $PSDN can be burned, routed to an insurance pool, or redistributed to honest participants.
5. Access: advanced marketplace placement, priority jobs, or subnet launch rights can require $PSDN staking or payment.

### Role-Based Staking Model

> **Skin in the game principle:** any actor who can impose cost on the network should have enough $PSDN at risk that honest behavior is economically better than spam, laziness, collusion, or fraud.

The role-based staking model is one of the most important pieces of the tokenomics design because it makes participation economically accountable.

Not every actor should stake the same way. Staking should be required where the actor can impose real cost on the network, and optional or lightweight where high friction would block useful growth.

Assumption for the baseline estimate:

- Total $PSDN supply: 1,000,000,000 tokens.
- Proposed stake amount = total supply x role stake rate.
- These are starting-point numbers for design discussion, not final launch parameters.
- Mainnet values should be adjusted by observed token price, participant cost, marketplace revenue, and attack frequency.

| Role | Stake Requirement | Proposed Stake With 1B $PSDN Supply | Why Stake Exists | Slash or Penalty Condition | Game-Theory Purpose |
|---|---|---:|---|---|---|
| Contributor | Optional for individuals; required for large operators or campaign participants | Individual: 0-1,000 $PSDN; campaign operator: 50,000 $PSDN, or 0.005% of supply | Discourage spam, duplicates, and rights fraud | Duplicate data, fake data, fraudulent rights claims, repeated bad metadata | Prevent low-cost Sybil supply while keeping casual contribution possible |
| Parser Miner | Required per subnet, per epoch, or per job batch | 250,000 $PSDN per active subnet, or 0.025% of supply | Make low-quality parsing costly | Fraudulent output, repeated failed validation, refusal to reveal committed output | Stop miners from farming bounties with cheap invalid work |
| Validator | Required per epoch or assignment pool | 100,000 $PSDN per validation pool, or 0.01% of supply | Ensure validators take review work seriously | Failed red herrings, provably lazy validation, collusion, bad challenge behavior | Make honest validation more profitable than rubber-stamping |
| Subnet Owner | Required launch bond or quality bond | 5,000,000 $PSDN per subnet launch, or 0.5% of supply | Hold owners accountable for scoring and subnet quality | Repeated scoring abuse, unresolved fraud, marketplace delisting event | Prevent owners from extracting rewards while degrading network trust |
| Curator/Search Participant | Required only for promoted listings or curation markets | 100,000 $PSDN per promoted dataset or curation pool, or 0.01% of supply | Align discovery influence with quality | Promoting fake demand, low-quality datasets, or self-dealing | Prevent marketplace ranking from becoming pay-to-spam |
| Buyer | Usually no stake; optional anti-abuse deposit for incentive programs | 0 $PSDN for normal buyers; 25,000 $PSDN only for subsidized buyer programs, or 0.0025% of supply | Buyers should face low friction while incentive programs need anti-wash protection | Fraudulent payment, chargeback abuse, self-dealing for incentives | Keep demand easy while preventing reward farming |

The beta should probably use simulated or capped staking for most roles. Mainnet can harden staking once the actual attack patterns are visible. A practical beta approach is to record the required stake in the ledger and enforce only lightweight penalties until the team has enough data to tune slashing severity.

#### Staking Amount Formula

For each role:

```text
role_stake_tokens = total_psdn_supply x role_stake_rate
```

Using the 1,000,000,000 $PSDN supply assumption:

```text
validator_stake = 1,000,000,000 x 0.0001 = 100,000 $PSDN
parser_miner_stake = 1,000,000,000 x 0.00025 = 250,000 $PSDN
subnet_owner_stake = 1,000,000,000 x 0.005 = 5,000,000 $PSDN
```

The stake should be high enough to make malicious behavior expensive, but not so high that only whales can participate. If the market price of $PSDN rises sharply, the token-denominated stake can be reduced while preserving the same economic security in dollar terms.

### Emission Philosophy

The network should minimize emissions by default and use them only where they create durable supply-side or demand-side liquidity.

Recommended principles:

- Emit against verified usefulness, not activity volume.
- Cap emissions per epoch and per subnet.
- Increase rewards when a subnet is supply-constrained and reduce them when marketplace demand can fund the work.
- Prefer delayed rewards, vesting, or clawback windows for work that may later be found low quality.
- Move from emission-funded rewards to fee-funded rewards as soon as a subnet has real buyer demand.
- Use staking locks to reduce circulating supply while forcing participants to internalize the cost of bad behavior.

### Bootstrap Phases

| Phase | Goal | $PSDN Use | Emission Posture |
|---|---|---|---|
| Beta | Prove CPVSS flow with voice and video subnets | Testnet $PSDN, points, or capped internal accounting | No meaningful open-ended emissions |
| Early Mainnet | Recruit contributors, miners, validators, and first buyers | Capped $PSDN rewards, role staking, reward vesting | Targeted emissions for verified useful work |
| Growth | Expand subnet count and marketplace demand | Buyer-funded rewards, subnet owner staking, marketplace fee routing | Declining emissions with demand-based rewards |
| Mature Network | Preserve token value and quality | Fee-funded payouts, staking, burns or insurance routing | Minimal emissions, mostly market-funded |

### Game-Theory Threats

The tokenomics must assume rational adversarial behavior.

| Threat | Description | Design Response |
|---|---|---|
| Sybil contribution | Many wallets submit duplicate, fake, or low-rights data | Deduplication, rights checks, delayed rewards, contributor reputation, optional bonds |
| Volume farming | Actors optimize for number of uploads or jobs rather than usefulness | Quality-weighted rewards, owner score, marketplace demand weighting |
| Lazy parsing | Miners submit cheap low-quality outputs | Validation consensus, spot checks, stake slashing, delayed payout |
| Lazy validation | Validators rubber-stamp outputs | Red-herring tasks, reliability score, slashing, reduced future assignment |
| Collusion | Contributors, parsers, and validators coordinate to approve bad data | Random assignment, hidden tests, reputation decay, owner scoring, challenge windows |
| Score abuse | Subnet owner manipulates scores to favor insiders | Signed score batches, public audit trail, challenge bond, Poseidon-level monitoring |
| Wash demand | Actors create fake marketplace purchases to trigger rewards | Buyer reputation, fee friction, anomaly detection, reward delay, anti-self-dealing rules |

### Token Sink Options

To reduce unnecessary emissions and support $PSDN value capture, Poseidon can combine several sinks:

1. Stake locks for miners, validators, subnet owners, and curators.
2. Marketplace fees paid in $PSDN or converted into $PSDN accounting.
3. Slashed stake burned or routed to an insurance pool.
4. Subnet launch deposits.
5. Priority dataset placement fees.
6. Buyer access passes or subscription tiers.

The beta does not need to finalize every sink. It should define the accounting surface so these mechanisms can be introduced without changing the CPVSS architecture.

## CPVSS Overview

| Stage | Function | Decentralization Thesis | Why Crypto Matters | Beta Shape |
|---|---|---|---|---|
| Collection | Gather raw voice and video data, metadata, consent, and provenance | Naturally decentralized because contributors are distributed | On-chain contribution records, audit trails, contributor identity, provenance, and reward eligibility | Contributor upload/API, dataset manifest, content hash, wallet-linked contribution ledger |
| Parsing | Convert raw data into structured artifacts such as transcripts, segments, labels, and metadata | Decentralizable because jobs are parallel and do not require real-time execution | On-chain coordination, miner assignment, result commitment, staking, and reward accounting | Miner agent framework for voice and video parsing jobs |
| Validation | Check parsing quality and detect bad or lazy work | Strong fit for decentralized consensus through redundant validators | Validator staking, red-herring tasks, slashing, reputation, and proof-of-usefulness | Multi-validator review, consensus threshold, red-herring detection |
| Score | Assign final quality score and determine reward allocation | Should be centralized by the subnet owner | Crypto makes the score auditable and payout-linked, while authority remains with the owner | Owner scoring service, signed score batches, reward distribution output |
| Search | Enable dataset discovery, access, transactions, and monetization | Should be centralized at the Poseidon network level | Payments, revenue splits, contributor royalties, and provenance-backed marketplace access | Poseidon portal with searchable voice and video datasets |

## Incentive Design Summary

Every CPVSS stage touches incentives, but each stage has a different failure mode. The beta should not overfit to one perfect mechanism. It should launch with a simple mechanism, measure behavior, and keep a decision log for when incentives need to evolve.

| Stage | Main Incentive Problem | Conservative Beta Design | More Advanced Design |
|---|---|---|---|
| Collection | Prevent spam, duplicates, and unclear rights while attracting useful supply | Quality-weighted rewards after validation and owner score | Contributor bond plus curated campaigns |
| Parsing | Pay miners for useful work without rewarding low-quality volume | Fixed bounty with quality multiplier and slashable stake | Competitive miner market with commit-reveal and spot audits |
| Validation | Stop lazy validators and collusion | Majority consensus with red-herring tasks | Reputation-weighted consensus with adjudication and challenge windows |
| Score | Preserve owner authority while avoiding opaque favoritism | Owner-signed score batches with audit trail | Score committee or model-assisted rubric with owner veto |
| Search | Bootstrap demand without wasting emissions | Marketplace fee split funded by real transactions | Capped demand incentives with anti-wash safeguards |

## C: Collection

### Function

Collection is the intake layer for raw voice and video data. It captures the asset, contributor identity, metadata, consent status, usage rights, and provenance information.

### Goal

The goal is to make contribution easy while ensuring every dataset item has a traceable origin. The system should know who contributed what, when they contributed it, what rights are attached, and how it moved through the pipeline.

### Decentralization

Collection is naturally decentralized. Contributors are distributed across geographies, communities, platforms, and data sources. A centralized data collection operation can work, but it limits scale and weakens the crypto-native incentive story.

The beta should allow contributors or trusted operators to submit data through a simple upload/API flow. Every submitted item should produce a durable record that can later be used for audit, scoring, and payout.

### Why Crypto Matters

Crypto matters in collection because it creates an auditable contribution ledger. Similar to systems like Kled using on-chain records for contribution tracking and audit trails, Poseidon can use crypto rails to preserve who contributed which asset and how that contribution later created value.

For beta, the system does not need to put raw data on-chain. It should put hashes, contribution metadata, and batch commitments on-chain or in a chain-compatible ledger.

### Beta Requirements

- Contributor identity linked to wallet or account.
- Upload/API flow for voice and video files.
- Content hash for each submitted item.
- Metadata manifest for each submitted item.
- Consent and rights fields in the manifest.
- Contribution ledger that can support later rewards.

### Incentive Design Options

#### Design A: Quality-Weighted Contribution Rewards

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
- Sybil attacks are still possible if identities are cheap and rewards are too high.

#### Design B: Contributor Bond and Curated Campaigns

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

- Bonds may exclude small or non-crypto-native contributors.
- Campaign design becomes operationally important.
- Slashing for rights problems can be contentious if the contributor made a good-faith mistake.

#### Collection Comparison

| Design | Incentive | Slashing/Penalty | Pros | Cons |
|---|---|---|---|---|
| Quality-weighted rewards | Pay only after data proves useful | No or low slashing; delayed reward and clawback | Simple, low-friction, emission-aware | Weaker spam deterrence |
| Contributor bond campaigns | Stake to submit into defined campaigns | Bond loss for duplicate, fake, or rights-invalid data | Better game-theory defense, targeted supply | Higher friction, harder contributor onboarding |

#### Open Questions

- Should small individual contributors be required to stake $PSDN, or only professional collection operators?
- How long should contribution rewards remain clawback-eligible?
- Should marketplace demand affect contributor rewards, or should rewards be based only on quality score?
- How should the system distinguish malicious rights fraud from honest metadata mistakes?

## P: Parsing

### Function

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

### Goal

The goal is to transform raw, messy media into structured datasets that are easier to validate, search, package, and sell.

### Decentralization

Parsing is decentralizable, although not mandatory. Its strongest decentralization argument is parallelism. Parsing jobs can be split across many independent miner agents, and most parsing jobs do not require real-time execution.

This makes parsing a good fit for distributed compute:

- Jobs are independent.
- Latency tolerance is relatively high.
- Outputs can be committed and later validated.
- Specialized miners can compete on speed, cost, and quality.

### Why Crypto Matters

Crypto matters because decentralized parsing needs coordination:

- Who receives which job?
- What did the miner commit to producing?
- How is the output linked to the input?
- How is the miner paid?
- How is bad work penalized?
- How can the system prove that work was done?

The key design question is how much coordination happens on-chain versus off-chain. The beta should avoid overbuilding. A practical design is to keep job execution off-chain while recording job commitments, output hashes, miner identity, and reward events in an auditable ledger.

### Beta Requirements

- Miner agent interface.
- Job queue for voice and video parsing.
- Parser output schema.
- Output artifact storage.
- Output hash linked to input hash.
- Miner identity and job history.
- Basic parser quality metadata.

### Incentive Design Options

#### Design A: Fixed Bounty With Quality Multiplier

Each parsing job has a posted $PSDN bounty. Miners receive the bounty only after the output passes validation. Higher-quality outputs receive a multiplier based on validation result and subnet-owner score.

Mechanism:

- Miner stakes $PSDN to accept jobs.
- Job has a base bounty.
- Output must pass validation before payout.
- High score increases payout.
- Failed or fraudulent output can reduce payout or slash stake.

Pros:

- Easy for miners to understand.
- Predictable cost for subnet owners.
- Strong beta fit because it is operationally simple.

Cons:

- Miners may optimize for easy jobs.
- Fixed rewards can overpay easy work and underpay hard work.
- Quality multipliers require a trusted scoring function.

#### Design B: Competitive Miner Market

Multiple miners can bid for or compete on parsing jobs. The network selects miners based on price, reputation, stake, historical quality, or a commit-reveal process.

Mechanism:

- Miners stake $PSDN to enter the market.
- Jobs can be assigned through auction, reputation routing, or random weighted assignment.
- Miners commit output hashes before revealing outputs.
- Spot audits and validator results determine payout.
- Repeated low-quality work reduces reputation or slashes stake.

Pros:

- Encourages price and quality competition.
- Supports specialized miners for different media types.
- Can reduce long-term emissions by letting market pricing replace subsidies.

Cons:

- More complex than fixed bounties.
- Auctions can be gamed by underbidding.
- Commit-reveal adds operational overhead.

#### Parsing Comparison

| Design | Incentive | Slashing/Penalty | Pros | Cons |
|---|---|---|---|---|
| Fixed bounty with quality multiplier | Base reward plus score-based upside | Stake slash or no payout for failed output | Simple, predictable, beta-ready | Risk of volume farming and mispriced jobs |
| Competitive miner market | Market-priced jobs and reputation routing | Stake slash, reputation loss, spot-audit penalty | Scales toward efficiency | More mechanism complexity |

#### Open Questions

- Should miners stake per job, per epoch, or per subnet?
- Should hard jobs pay more automatically based on file length, media quality, or scarcity?
- How many parser failures should trigger slashing versus only reputation loss?
- Should the beta use permissioned miners first, then open participation later?

## V: Validation

### Function

Validation checks whether parsing outputs are accurate, complete, and useful. It is the quality-control layer between miner work and final scoring.

### Goal

The goal is to prevent low-quality parsing from entering the marketplace and to create an incentive-compatible mechanism for validators to perform real review work.

### Decentralization

Validation is one of the strongest decentralization fits in the CPVSS pipeline. Multiple validators can independently review parser outputs, and their results can be aggregated through a consensus algorithm.

For beta, validation should focus on practical consensus rather than perfect mechanism design. The first version should prove that redundant validation can detect bad outputs and produce a reliable quality signal.

### Why Crypto Matters

Crypto matters because validators need incentives, accountability, and penalties. Validators can stake reputation or tokens. Correct validation earns rewards. Lazy or dishonest validation can be penalized.

The red-herring mechanism is especially useful. The system can inject known test cases into validator queues. Validators who repeatedly fail these hidden checks can be down-weighted or slashed.

### Consensus Design Space

Open design questions include:

- Number of validators per artifact.
- Required agreement threshold.
- Weighting by validator reputation.
- Handling disagreement between validators.
- Red-herring frequency.
- Slashing severity.
- Appeals or owner override.
- Whether validation produces binary pass/fail, graded scores, or structured comments.

### Beta Requirements

- Validator assignment flow.
- Validation schema.
- At least three validators per selected artifact, where feasible.
- Consensus rule for pass/fail or quality tier.
- Red-herring task injection.
- Validator reliability score.
- Basic slashing or down-weighting simulation.

### Incentive Design Options

#### Design A: Majority Consensus With Red Herrings

Each artifact is reviewed by multiple validators. Validators earn rewards when they complete reviews and align with consensus, but they are penalized when they fail hidden red-herring tasks.

Mechanism:

- Validators stake $PSDN to participate.
- Artifacts are randomly assigned.
- Red-herring tasks with known answers are mixed into the queue.
- Validators earn rewards for timely, accurate validation.
- Validators who fail red herrings lose reliability score and may be slashed.

Pros:

- Clear and simple validation model.
- Red herrings directly target lazy validation.
- Strong beta fit.

Cons:

- Consensus can reward herding.
- Honest minority validators may be punished if the majority is wrong.
- Colluding validators can still pass bad outputs if assignment randomness is weak.

#### Design B: Reputation-Weighted Validation With Challenge Window

Validator votes are weighted by historical accuracy, stake, and red-herring performance. Disputed results can enter a challenge window where challengers stake $PSDN to request owner or expert adjudication.

Mechanism:

- Validators stake $PSDN and build reliability reputation.
- Vote weight depends on accuracy and past behavior.
- Low-confidence consensus triggers additional review.
- Challengers can bond $PSDN to dispute a result.
- Correct challenges earn part of the penalty; incorrect challenges lose the bond.

Pros:

- Better quality over time because good validators gain weight.
- Challenge windows reduce damage from bad consensus.
- Creates a path for expert correction.

Cons:

- More complex to explain and implement.
- Reputation can entrench early validators.
- Challenge mechanisms can be spammed if the bond is too low.

#### Validation Comparison

| Design | Incentive | Slashing/Penalty | Pros | Cons |
|---|---|---|---|---|
| Majority consensus with red herrings | Reward consensus and hidden-test accuracy | Slash or down-weight validators who fail red herrings | Simple, strong lazy-validator defense | Herding and collusion risk |
| Reputation-weighted validation | More weight and rewards for proven validators | Slash for failed tests, wrong challenges, or repeated bad votes | Better long-term quality | Complexity and possible validator oligopoly |

#### Open Questions

- How often should red-herring tasks appear?
- Should validators be rewarded for disagreeing with a wrong majority after adjudication?
- Should slashing burn $PSDN, compensate harmed parties, or fund future validation?
- How should the system detect validator collusion beyond red-herring failure?

## S: Score

### Function

Scoring is the final quality and usefulness assessment. It determines how much value a contribution, parser output, or validation action should receive.

### Goal

The goal is to make reward distribution accountable while preserving the subnet owner's authority over final quality.

### Decentralization

Scoring should be centralized. The subnet owner has the ultimate responsibility to determine quality, usefulness, and reward allocation. This is especially important because the score directly affects token distribution.

Trying to decentralize scoring too early could weaken accountability. For beta, the subnet owner should retain explicit final authority.

### Why Crypto Matters

Crypto still matters in this centralized stage because the scoring output can be auditable. A subnet owner can publish signed score batches, reward allocation records, and references to the underlying artifacts and validation results.

This creates transparency without pretending that quality judgment is fully objective.

### Beta Requirements

- Owner scoring interface or admin workflow.
- Score schema.
- Signed or auditable score batch.
- Reward allocation output.
- Linkage from score to contribution, parsing, and validation records.
- Manual override ability.

### Incentive Design Options

#### Design A: Owner-Signed Scoring With Challenge Bond

The subnet owner signs final score batches. Participants can challenge a score by posting a $PSDN bond during a challenge window.

Mechanism:

- Owner publishes signed score batch.
- Score determines final reward allocation.
- Any affected participant can challenge by bonding $PSDN.
- Valid challenge triggers correction and possibly owner penalty or reputation loss.
- Invalid challenge loses bond.

Pros:

- Preserves clear owner authority.
- Gives participants a safety valve against obvious scoring abuse.
- Keeps beta implementation manageable.

Cons:

- Challenge resolution still needs an adjudicator.
- Too many challenges can slow payout.
- If the challenge bond is too high, small contributors cannot contest bad scores.

#### Design B: Model-Assisted Rubric With Owner Veto

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

#### Score Comparison

| Design | Incentive | Slashing/Penalty | Pros | Cons |
|---|---|---|---|---|
| Owner-signed scoring with challenge bond | Owner controls final rewards with accountable audit trail | Challenge bond loss; possible owner reputation penalty | Clear authority, beta-ready | Requires fair adjudication |
| Model-assisted rubric with owner veto | Transparent scoring criteria plus owner control | Outlier logging, challenge bond, owner reputation risk | More consistent and scalable | Rubric gaming and model bias |

#### Open Questions

- Should subnet owners stake $PSDN against scoring integrity?
- Who adjudicates challenges: Poseidon, expert panel, or subnet owner with public explanation?
- Should owner penalties be financial, reputational, or marketplace-ranking based?
- How much scoring transparency is safe before participants start gaming the rubric?

## S: Search

### Function

Search is the user-facing discovery and marketplace layer. It lets users find, inspect, request, purchase, or access processed datasets.

### Goal

The goal is to make Poseidon the central marketplace for AI-ready voice and video datasets.

### Decentralization

Search should be centralized at the network level. Poseidon should manage the portal, ranking, access flow, transactions, and marketplace rules. This creates a coherent user experience and gives the project a direct revenue engine.

### Why Crypto Matters

Crypto matters because marketplace transactions can connect back to provenance and contribution history. Revenue can be split between contributors, miners, validators, subnet owners, and Poseidon according to transparent rules.

The marketplace is where the crypto incentive loop becomes economically meaningful.

### Beta Requirements

- Searchable dataset portal.
- Dataset detail page.
- Provenance summary.
- Quality score display.
- Voice and video filters.
- Basic access or request flow.
- Marketplace transaction placeholder or testnet payment flow.

### Incentive Design Options

#### Design A: Marketplace Fee Split

Dataset buyers pay through the Poseidon marketplace. Fees are split among contributors, parser miners, validators, subnet owners, and Poseidon according to the dataset's contribution and quality records.

Mechanism:

- Buyer pays in $PSDN or a payment rail that maps into $PSDN accounting.
- Marketplace fee is split by policy.
- Prior CPVSS records determine who receives value.
- A portion of fees can go to Poseidon, subnet owner, contributors, miners, validators, and possibly a burn or insurance pool.

Pros:

- Rewards are backed by real demand rather than emissions.
- Aligns all actors around commercially useful data.
- Strong long-term model for preserving $PSDN value.

Cons:

- Does not bootstrap supply if early buyer demand is weak.
- Revenue attribution can be hard when many assets compose one dataset.
- Contributors may wait too long for meaningful payouts.

#### Design B: Capped Demand Incentives With Anti-Wash Rules

Poseidon uses capped $PSDN incentives to bootstrap marketplace activity, but rewards only unlock when there is credible demand, quality, and non-self-dealing behavior.

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

#### Search Comparison

| Design | Incentive | Slashing/Penalty | Pros | Cons |
|---|---|---|---|---|
| Marketplace fee split | Pay from real buyer demand | No direct buyer slashing; bad actors lose ranking or access | Sustainable, emission-light | Slow bootstrap |
| Capped demand incentives | Subsidize early useful marketplace activity | Curator or subnet owner stake can be slashed for fake demand | Accelerates network effects | Wash trading and subsidy farming risk |

#### Open Questions

- Should marketplace fees be paid only in $PSDN, or can fiat payments be converted into $PSDN accounting?
- What percentage of marketplace fees should go to Poseidon versus contributors and subnet operators?
- Should a portion of revenue be burned, routed to insurance, or used for buyback-style reward pools?
- How should the marketplace detect and penalize self-dealing or fake demand?

## End-to-End Beta Flow

1. Contributor uploads voice or video data.
2. System creates a content hash, metadata manifest, contributor record, and audit trail.
3. Parser miner receives a job.
4. Parser miner produces structured artifacts.
5. Parser output is stored off-chain and committed through an output hash.
6. Validators review parser output.
7. Red-herring validation tasks detect lazy or dishonest validators.
8. Consensus produces a validation result.
9. Subnet owner reviews final artifacts and assigns a score.
10. Reward allocation is generated from contribution, parsing, validation, and owner score.
11. Dataset appears in the Poseidon search marketplace.
12. Users discover, preview, and request or purchase access.

## Recommended Beta Architecture

### Off-Chain

- Raw voice and video files
- Parsed transcripts and structured artifacts
- Validator comments
- Search index
- Marketplace UI
- Admin scoring dashboard

### On-Chain or Chain-Compatible Ledger

- Contributor identity reference
- Input content hash
- Dataset manifest hash
- Parser job commitment
- Parser output hash
- Validator participation record
- Consensus result hash
- Score batch hash
- Reward allocation record
- Marketplace transaction record

For beta, a chain-compatible ledger or testnet contract is sufficient. The system should be designed so the beta ledger can later be upgraded to production smart contracts.

## Open Design Decisions

These decisions should remain open during beta design and be resolved only when real workflow evidence appears:

1. Whether beta rewards use real tokens, testnet tokens, or off-chain points.
2. Whether contribution records are written individually or batched through Merkle roots.
3. Whether voice and video share one subnet framework or use two separate subnet templates.
4. How validators are selected and weighted.
5. How aggressive red-herring slashing should be.
6. Whether parser miners need staking in beta.
7. Whether search ranking should include quality score, commercial demand, freshness, or subnet owner reputation.
8. Whether score decisions are manually assigned, model-assisted, or hybrid.
9. Whether buyers transact directly with subnet owners or through Poseidon as marketplace operator.
10. What minimum $PSDN stake is required for each role without excluding useful early participants.
11. Whether slashed $PSDN should be burned, routed to insurance, or redistributed to honest participants.
12. How quickly emissions should decline as marketplace revenue grows.
13. Whether fiat buyer payments should be converted into $PSDN, abstracted behind credits, or kept separate in beta.
14. How to prevent early high-stake actors from capturing validator or miner reputation permanently.

## Beta Success Criteria

By June 30, 2026, beta should prove:

- A contributor can submit voice and video data.
- The system records provenance and contribution history.
- Miner agents can parse real data.
- Validators can verify outputs through consensus.
- Red-herring tasks can detect lazy validation.
- Subnet owner can assign final quality scores.
- Rewards can be calculated transparently.
- Users can find processed datasets through a central Poseidon marketplace.
- Two production beta subnets are running: one for voice data and one for video data.

## Weekly Roadmap

| Week | Dates | Goal | Concrete Output |
|---|---|---|---|
| Week 0 | May 15-17, 2026 | Lock beta scope | CPVSS spec, two subnet definitions, voice and video beta acceptance criteria |
| Week 1 | May 18-22, 2026 | Architecture and schemas | Subnet config, data manifest schema, parser job schema, validation schema, reward model draft |
| Week 2 | May 25-29, 2026 | Collection layer | Upload/API flow, contributor wallet identity, content hashing, metadata manifest, contribution ledger |
| Week 3 | June 1-5, 2026 | Parsing miner framework | Job queue, miner agent interface, voice parser working, video parser skeleton, output schema |
| Week 4 | June 8-12, 2026 | Validation layer | Validator assignment, consensus rule, red-herring tasks, validator reliability score |
| Week 5 | June 15-19, 2026 | Scoring and search MVP | Owner scoring workflow, reward batch output, searchable dataset portal, dataset detail page |
| Week 6 | June 22-26, 2026 | Production pilot | End-to-end runs for voice and video, observability, QA, beta docs, pilot datasets |
| Release | June 29-30, 2026 | Beta launch | Two production beta subnets live, demo datasets processed end to end, beta users onboarded |

## Week-by-Week Detail

### Week 0: May 15-17, 2026

Goal: Lock the beta scope.

Deliverables:

- CPVSS design document.
- Voice subnet definition.
- Video subnet definition.
- Beta success criteria.
- Decision log template.

Key decision:

- Confirm whether beta rewards are testnet, points-based, or real token-denominated.

### Week 1: May 18-22, 2026

Goal: Define the architecture and schemas.

Deliverables:

- Dataset manifest schema.
- Contributor record schema.
- Parser job schema.
- Parser output schema.
- Validation schema.
- Score schema.
- Reward allocation model.
- System architecture diagram.

Key decision:

- Choose beta ledger design: direct testnet contract, internal ledger with hash commitments, or hybrid.

### Week 2: May 25-29, 2026

Goal: Build the collection layer.

Deliverables:

- Contributor upload/API.
- Wallet or account identity linkage.
- Content hash generation.
- Metadata and rights capture.
- Contribution ledger.
- Basic audit trail.

Key decision:

- Decide minimum consent and rights metadata required before data can enter parsing.

### Week 3: June 1-5, 2026

Goal: Build the parser miner framework.

Deliverables:

- Miner agent interface.
- Job queue.
- Voice parsing pipeline.
- Video parsing pipeline skeleton.
- Parser output artifact storage.
- Output hash commitment.
- Miner job history.

Key decision:

- Decide whether parser miners are permissioned for beta or open to external operators.

### Week 4: June 8-12, 2026

Goal: Build the validation layer.

Deliverables:

- Validator assignment workflow.
- Validation UI or API.
- Consensus threshold.
- Red-herring task injection.
- Validator reliability score.
- Slashing or down-weighting simulation.

Key decision:

- Choose the initial consensus algorithm for beta and define failure handling.

### Week 5: June 15-19, 2026

Goal: Build scoring and search MVP.

Deliverables:

- Subnet owner scoring workflow.
- Score batch output.
- Reward allocation output.
- Dataset search index.
- Dataset detail page.
- Voice and video filters.
- Marketplace access placeholder.

Key decision:

- Decide what marketplace transaction flow is required for beta: request access, testnet payment, or manual approval.

### Week 6: June 22-26, 2026

Goal: Run production pilot.

Deliverables:

- End-to-end voice subnet run.
- End-to-end video subnet run.
- QA report.
- Observability dashboard.
- Failure recovery checklist.
- Beta onboarding guide.
- Initial pilot datasets in search portal.

Key decision:

- Decide what qualifies as production beta readiness.

### Release Window: June 29-30, 2026

Goal: Launch beta.

Deliverables:

- Two beta subnets live in production.
- Voice dataset processed end to end.
- Video dataset processed end to end.
- Contributor, miner, validator, owner, and user flows demonstrated.
- Beta users onboarded.
- Known limitations documented.
- Post-beta design backlog created.

## Immediate Next Steps

1. Approve the CPVSS stage ownership model.
2. Define the voice and video subnet schemas.
3. Choose the beta ledger approach.
4. Create the first end-to-end demo dataset.
5. Assign owners for collection, parsing, validation, scoring, and search.

## Final Positioning

Poseidon should position the subnet as a pragmatic crypto-AI infrastructure layer.

The strongest argument is not that every step is decentralized. The strongest argument is that AI data creation involves many distributed actors, and crypto provides the rails to coordinate them, verify their work, preserve provenance, and distribute value when the data becomes commercially useful.

Collection, parsing, and validation show why decentralization matters. Scoring and search show why central authority still matters. The full CPVSS system shows how the two can work together.
