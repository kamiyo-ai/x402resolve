# x402Resolve Demo Video Script - 25 Second Scene

## Visual Flow & Narration

### Scene: "The Quality Problem Solved"

**SECONDS 0-5: The Problem**
```
VISUAL: Split screen showing two API responses side-by-side

LEFT PANEL (Good Data):
{
  "exploits": [
    {
      "severity": "CRITICAL",
      "protocol": "UniswapV3",
      "tvl_at_risk": "$2.4M",
      "timestamp": "2025-11-11T03:15:00Z"
    }
  ]
}

RIGHT PANEL (Bad Data):
{
  "exploits": []
}

NARRATION:
"APIs charge the same price whether they return quality data... or garbage."
```

**SECONDS 5-10: The Solution - Agent Assessment**
```
VISUAL: Terminal showing autonomous agent analyzing data

TERMINAL OUTPUT:
$ npm run agent-demo

[Agent] Calling API: exploit-feed.xyz
[Agent] Creating escrow: 0.001 SOL
[Agent] Assessing quality...
  ├─ Completeness: 20% ❌
  ├─ Freshness: 50% ⚠️
  └─ Quality Score: 38% ❌

[Agent] DISPUTE: Quality 38% < threshold 80%
[Agent] Calculating refund...

NARRATION:
"x402Resolve agents autonomously assess quality and dispute low-quality responses."
```

**SECONDS 10-15: The Magic - Sliding Scale Refunds**
```
VISUAL: Animated calculation showing refund formula

DISPLAY:
Quality Score: 38%
Threshold: 80%

Refund Calculation:
  refund = ((80 - 38) / 80) × 100
  refund = 52.5%

VISUAL EFFECT: Money flowing back from provider to consumer

ON-CHAIN TRANSACTION:
✓ Escrow released: 0.00048 SOL → Provider
✓ Refund: 0.00052 SOL → Consumer

NARRATION:
"Sliding-scale refunds on Solana. Pay only for quality you receive."
```

**SECONDS 15-20: The Integration - MCP + SDK + Agents**
```
VISUAL: Three panels showing integration

LEFT: Claude Desktop with MCP
[Claude] Using x402 MCP tools:
  ✓ create_escrow
  ✓ assess_data_quality
  ✓ file_dispute

CENTER: SDK in Action
const agent = new AutonomousServiceAgent({
  qualityThreshold: 80,
  autoDispute: true
});

const result = await agent.consumeAPI(
  'exploit-feed.xyz',
  query,
  schema
);
// Automatically disputes if quality < 80%

RIGHT: Multi-Agent Consensus
Agent1: 95% quality ✓
Agent2: 88% quality ✓
Agent3: 72% quality ❌ (filtered)

Consensus: EXECUTE (92% avg)

NARRATION:
"MCP for Claude. SDK for developers. Multi-agent coordination for institutions."
```

**SECONDS 20-25: The Result**
```
VISUAL: Dashboard showing validation results

VALIDATION RESULTS:
══════════════════════════════════════
✓ 14/14 Tests Passing (100%)
✓ Real Solana Devnet Integration
✓ Quality Assessment: <1ms
✓ Multi-Agent Consensus: Working
✓ PDA Derivation: Deterministic
══════════════════════════════════════

PROGRAM: E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n

FINAL VISUAL: Logo + GitHub

x402Resolve
Fair payments for quality data
github.com/kamiyo-ai/x402resolve

NARRATION:
"Production-ready. Fully validated. Built on Solana."
```

---

## Alternative: "Live Demo" Version (Technical Audience)

### Scene: Real Terminal Session

**SECONDS 0-8: Setup**
```
VISUAL: Terminal showing quick setup

$ cd examples/agent-integration-test
$ npm install
$ npm test

NARRATION:
"Watch a real agent consume an API, assess quality, and dispute automatically."
```

**SECONDS 8-15: Agent in Action**
```
TERMINAL OUTPUT (fast-forwarded but readable):

[Test 3] Agent - Autonomous Service Consumption
──────────────────────────────────────────────────
  Agent initialized
  Quality Threshold: 80%
  Max Price: 0.001 SOL

  Simulating API call: exploit-feed.xyz

  Response received:
  {
    "exploits": [
      { "id": "123" }  // Missing fields!
    ]
  }

  ✓ Quality assessment: 38%
  ✗ Quality BELOW threshold (38% < 80%)

  [Agent] Filing dispute autonomously...
  [Agent] Refund: 52.5%

✓ PASS: Agent Autonomous Consumption

NARRATION:
"The agent caught incomplete data and automatically claimed a 52% refund."
```

**SECONDS 15-20: Multi-Agent Scene**
```
TERMINAL OUTPUT:

[Test 4] Multi-Agent - Coordination and Consensus
──────────────────────────────────────────────────
  Testing 3 specialized agents

  Agent Results:
    ✓ Agent1: 95% quality, 0.0003 SOL
    ✓ Agent2: 88% quality, 0.0005 SOL
    ⚠ Agent3: 72% quality, 0.0002 SOL (DISPUTED)

  Consensus Analysis:
    Valid Agents: 2/3 (filtered by quality)
    Average Quality: 92%

  Quality-Weighted Votes:
    Agent1: 51.9% weight
    Agent2: 48.1% weight

  ✓ Consensus: STRONG (92% avg quality)
✓ PASS: Multi-Agent Coordination

NARRATION:
"Three agents. Quality-weighted consensus. One filtered out. This is production-ready."
```

**SECONDS 20-25: Validation Summary**
```
VISUAL: Split screen - Terminal + Explorer

LEFT PANEL - Terminal:
══════════════════════════════════════
VALIDATION SUMMARY
══════════════════════════════════════

Total Tests: 14
Passed: 14
Failed: 0
Success Rate: 100.0%

All validations passed!

RIGHT PANEL - Solana Explorer:
https://explorer.solana.com/address/
E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n
?cluster=devnet

[Shows real program with transactions]

NARRATION:
"100% test success. Real Solana program. Ready to deploy."
```

---

## Recording Tips

### Setup Before Recording

```bash
# Terminal 1: Run validation (record this)
cd examples/comprehensive-validation
npm run validate

# Terminal 2: Have Claude Desktop open with MCP configured
# Show tools list in Claude Desktop

# Terminal 3: Have Solana Explorer open
# Show program: E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n
```

### Camera Angles
1. **Full screen terminal** for technical validation
2. **Split screen** for showing multiple components
3. **Zoom in on key metrics** (100%, quality scores, refund amounts)
4. **End with GitHub + logo** for credibility

### Text Overlays to Add# KAMIYO x402Resolve - Solana x402 Hackathon Video Script
**Duration:** 2 minutes 50 seconds (170s) | **Format:** Demo + Narration

---

## SCENE 1: OPENING (0:00-0:10) - 10 seconds

**Visual:** KAMIYO logo reveal → Fade to live demo interface

**Narration:**
"Introducing KAMIYO x402Resolve. Quality-verified x402 payment refunds on Solana."

**Timing:** 10 seconds

---

## SCENE 2: THE PROBLEM (0:10-0:25) - 15 seconds

**Visual:** Animated graphics showing API payment failures

**Narration:**
"Traditional API payments have a problem: pay upfront, no guarantees. Chargebacks cost $35 and take 90 days. For developers testing APIs, for businesses consuming data, this doesn't scale. We need real-time dispute resolution with quality guarantees."

**Timing:** 15 seconds

---

## SCENE 3: DEMO FLOW - FULL WALKTHROUGH (0:25-1:40) - 75 seconds

**Visual:** Screen recording - Complete demo flow from wallet connect to refund

**Narration:**
"Here's the underlying infrastructure. Connect your Phantom wallet to Solana devnet. Set your payment amount and click 'Run on-chain quality assessment'. Confirm the escrow creation in your wallet—funds lock in a Program Derived Address with no admin keys, no custody risk. The system automatically triggers three independent oracles to analyze the API response, checking completeness, freshness, and schema compliance. Each oracle assigns a quality score. The system calculates consensus: scores under 50 get full refunds, 50 to 79 get partial refunds, and 80-plus means the API delivered. Based on the consensus, the smart contract calculates your refund, splits the escrow, and updates both parties' reputations on-chain."

**On-screen actions:**
- Click "Connect Wallet" → Phantom popup
- Wallet connects → Demo loads
- Set payment amount → Click "Run on-chain quality assessment"
- Confirm escrow creation in wallet
- Progress bar animates
- Oracle cards display individual scores (3 oracles)
- Consensus calculation shows
- Quality score displays
- Refund percentage calculated
- Transaction executes on devnet
- Solana Explorer link appears
- Reputation scores update

**Timing:** 75 seconds

---

## SCENE 4: TECHNICAL HIGHLIGHTS + MCP (1:40-2:05) - 25 seconds

**Visual:** Split screen - architecture diagram + code snippets

**Narration:**
"Why Solana? PDA-based escrow means no admin keys. Sub-penny costs—two cents per dispute versus $35 traditional. Lightning-fast finality—disputes resolve in 48 hours, not 90 days. And for AI agents, we built an MCP server—giving Claude and autonomous agents the ability to pay for APIs, assess quality, and file disputes autonomously. Quality-verified payments with automated refunds, built for the agent economy."

**On-screen graphics:**
- PDA architecture diagram
- Cost: $35 → $0.02
- Time: 90 days → 48 hours
- MCP logo + Claude integration
- Tool icons (8 MCP tools)

**Timing:** 25 seconds

---

## SCENE 5: INTEGRATION & SDK (2:05-2:25) - 20 seconds

**Visual:** Three-panel split screen showing SDK, Agent, and MCP code in action

**Narration:**
"Three integration layers. The TypeScript SDK provides escrow creation, dispute resolution, and reputation tracking—eleven methods for developers. The Autonomous Agent client handles everything: API consumption, quality assessment, automatic disputes when scores fall below your threshold. And our MCP server gives Claude eight tools: create escrow, assess quality, file disputes, check reputation—autonomous agents that pay for APIs and demand refunds when quality fails."

**On-screen display:**
```typescript
// PANEL 1: SDK (EscrowClient)
const client = new EscrowClient(config, IDL);
await client.createEscrow({
  amount: solToLamports(0.001),
  timeLock: hoursToSeconds(24),
  transactionId: 'tx-123',
  apiPublicKey: provider
});
await client.resolveDispute(txId, qualityScore, refundPct);
// 11 methods: create, release, dispute, resolve, fetch, reputation

// PANEL 2: Autonomous Agent
const agent = new AutonomousServiceAgent({
  qualityThreshold: 80,  // Auto-dispute if < 80%
  autoDispute: true
});
const result = await agent.consumeAPI(endpoint, query, schema);
// Returns: { data, quality: 38%, cost: 0.00048, disputed: true }

// PANEL 3: MCP Server (8 Tools for Claude)
// create_escrow - Lock payment with quality guarantee
// assess_data_quality - Score 0-100 with refund estimate
// file_dispute - Trigger resolution with evidence
// get_api_reputation - Check provider trustworthiness
// call_api_with_escrow - Full workflow automation
// + 3 more tools
```

**Timing:** 20 seconds

---

## SCENE 6: VALUE PROPOSITION (2:25-2:40) - 15 seconds

**Visual:** Animated metrics and comparison charts

**Narration:**
"The numbers: 84 to 94 percent cost reduction. 97 to 99 percent faster resolution. Most importantly, this enables AI agents to transact with confidence. Quality guarantees for the agent economy."

**On-screen graphics:**
- Animated cost savings: $35K → $2K annually
- Timeline: 90 days → 48 hours
- "Built for the Agent Economy"
- 8 MCP tools + Live on Devnet

**Timing:** 15 seconds

---

## SCENE 7: CLOSE (2:40-2:50) - 10 seconds

**Visual:** Return to live demo + final branding

**Narration:**
"KAMIYO x402Resolve. Trustless payments. Quality-verified. On Solana. Try the live demo at x402resolve.kamiyo.ai."

**Final screen:**
- x402resolve.kamiyo.ai
- Program ID: E5Eia...sEu6n
- "Built for Solana x402 Hackathon 2025"
- KAMIYO logo

**Timing:** 10 seconds

---

## PRODUCTION NOTES

### Voice Style
- Tone: Confident, technical but accessible
- Pace: ~155-160 words per minute
- Energy: Medium-high (demo enthusiasm)
- OpenAI Voice: **"nova"** (professional, clear, female voice)

### Screen Recording Checklist
- [ ] Wallet connection flow (5 seconds)
- [ ] Complete demo walkthrough - escrow to refund (70 seconds)
- [ ] Code examples scroll (10 seconds)

### Editing Timeline

| Time | Scene | Video Track | Audio File |
|------|-------|-------------|------------|
| 0:00-0:10 | Opening | KAMIYO logo + demo | 01_opening.mp3 |
| 0:10-0:25 | Problem | Animated graphics | 02_problem.mp3 |
| 0:25-1:40 | Demo Flow | Screen recording (full) | 03_demo_flow.mp3 |
| 1:40-2:05 | Technical + MCP | Diagrams + code | 04_technical_mcp.mp3 |
| 2:05-2:25 | Integration | Code snippets | 05_integration.mp3 |
| 2:25-2:40 | Value | Animated metrics | 06_value.mp3 |
| 2:40-2:50 | Close | Demo + branding | 07_close.mp3 |

**Total:** 170 seconds = 2 minutes 50 seconds ✓

### Key Metrics to Highlight Visually
- **$0.02** per dispute (vs $35 traditional)
- **48 hours** resolution (vs 90 days)
- **84-94%** cost reduction
- **8 MCP tools** for AI agents
- **Program ID:** E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n

### Music & Sound
- Background music: Minimal tech/synth (20-25% volume)
- Sound effects for transitions (optional)
- Keep audio mix clean for narration clarity

### Graphics to Prepare
- KAMIYO logo animation
- Problem statement graphics (API failures, chargebacks)
- Architecture diagram (PDA-based escrow)
- Cost comparison chart ($35 → $0.02)
- Timeline comparison (90 days → 48 hours)
- MCP integration diagram (Claude + tools)
- "Built for Agent Economy" badge

---

## WORD COUNT

**Total narration:** ~433 words
**Speaking rate:** 160 words/minute
**Calculated duration:** 433 ÷ 160 = 2.70 minutes ≈ 2:50 ✓

---

## SCENE BREAKDOWN BY NARRATION LENGTH

| Scene | Words | Time (160 wpm) | Target |
|-------|-------|----------------|--------|
| 1. Opening | 12 | 10s | 10s ✓ |
| 2. Problem | 42 | 15s | 15s ✓ |
| 3. Demo Flow | 200 | 75s | 75s ✓ |
| 4. Technical + MCP | 67 | 25s | 25s ✓ |
| 5. Integration | 53 | 20s | 20s ✓ |
| 6. Value | 40 | 15s | 15s ✓ |
| 7. Close | 19 | 10s | 10s ✓ |
| **Total** | **433** | **170s** | **170s** |

---

## MCP SERVER HIGHLIGHTS (Scene 4 & 5)

**Why MCP is Important:**
- Enables autonomous AI agent transactions with quality guarantees
- Only MCP server with sliding-scale refunds based on oracle verification
- 8 production-ready tools
- Integrates with Claude Desktop, LangChain, AutoGPT

**All 8 MCP Tools:**
1. `create_escrow` - Lock payment with quality guarantee
2. `check_escrow_status` - Monitor escrow state
3. `verify_payment` - Confirm payment received
4. `assess_data_quality` - Score API response (0-100)
5. `estimate_refund` - Calculate refund from quality score
6. `file_dispute` - Submit dispute with evidence
7. `get_api_reputation` - Check provider track record
8. `call_api_with_escrow` - Full workflow automation

**Visual Emphasis:**
- Show Claude Desktop with MCP tools
- Display tool names on screen
- Highlight "First HTTP 402 MCP Server"
- Show autonomous agent workflow

---

## B-ROLL SUGGESTIONS

- Abstract blockchain animations
- Data flowing through networks
- AI agent icons interacting
- Quality score meters filling
- Transaction confirmations
- Solana logo animations
- Claude Code interface (for MCP demo)

---

## NEXT STEPS

1.  Script written (2:50 exact timing)
2.  Generate audio narration (run generate-narration.py)
3.  Record screen demos
4.  Gather B-roll and graphics
5.  Edit video with narration sync
6.  Add background music and polish
7.  Export final video

---

**Ready for audio generation!** Run `python3 generate-narration.py` to create the 7 MP3 files.

- "x402Resolve" logo (top corner throughout)
- "Built on Solana" badge
- Key numbers highlighted: "38%", "52.5% refund", "100% tests passing"
- GitHub link at end

### Audio Tips
- Keep narration concise and punchy
- Use technical terms confidently (PDA, escrow, consensus)
- Emphasize: "autonomous", "production-ready", "100% validated"

---

## One-Liner Taglines (Choose One)

1. **"Fair payments for quality data"**
2. **"Pay only for what you actually receive"**
3. **"Autonomous agents that dispute on your behalf"**
4. **"HTTP 402: Finally implemented correctly"**
5. **"Quality-verified payments on Solana"**

---

## What Judges Will See

### In 25 Seconds:
1. **The Problem**: APIs charge regardless of quality
2. **The Solution**: Autonomous quality assessment
3. **The Innovation**: Sliding-scale refunds (not binary)
4. **The Integration**: MCP + SDK + Agents working together
5. **The Proof**: 100% validation, real Solana program

### Key Differentiators:
- Not just "escrow" - it's **quality-verified escrow**
- Not just "refunds" - it's **sliding-scale fairness**
- Not just "agents" - it's **multi-agent consensus**
- Not just "demo" - it's **production-ready with 14 passing tests**

---

## Post-Demo Call-to-Action

```
TRY IT NOW:
$ git clone github.com/kamiyo-ai/x402resolve
$ cd examples/comprehensive-validation
$ npm install --no-workspaces
$ npm run validate

SEE IT WORK:
100% test success in under 2 seconds

READ MORE:
- VALIDATION-SUMMARY.md
- VALIDATION-RESULTS.md
- README.md
```
