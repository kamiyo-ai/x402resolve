# Scene 5 Visual Guide - Three Integration Layers

## Screen Layout (20 seconds)

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCENE 5: Integration & SDK                    │
├──────────────────┬──────────────────┬──────────────────────────┤
│   PANEL 1: SDK   │  PANEL 2: Agent  │   PANEL 3: MCP Server   │
│                  │                  │                          │
│  EscrowClient    │  AutonomousAgent │   8 Tools for Claude    │
│  11 Methods      │  Auto-Dispute    │   Quality-Verified      │
│                  │                  │                          │
└──────────────────┴──────────────────┴──────────────────────────┘
```

---

## Panel 1: TypeScript SDK (Left)

**Title Overlay:** "TypeScript SDK"
**Subtitle:** "11 Methods for Developers"

**Code Display:**
```typescript
// packages/x402-sdk
import { EscrowClient, EscrowUtils } from '@x402resolve/sdk';

const client = new EscrowClient(config, IDL);

// Create escrow with quality guarantee
await client.createEscrow({
  amount: EscrowUtils.solToLamports(0.001),
  timeLock: EscrowUtils.hoursToSeconds(24),
  transactionId: 'exploit-api-call-123',
  apiPublicKey: providerWallet
});

// Resolve dispute with sliding-scale refund
await client.resolveDispute(
  txId,
  qualityScore,    // 38% quality
  refundPercentage // 52.5% refund
);

// Check reputation before payment
const rep = await client.getReputation(provider);
```

**Animated Highlights:**
- Line-by-line code reveal (0-7 seconds)
- Highlight `qualityScore: 38%` in red
- Highlight `refundPercentage: 52.5%` in green
- Show "11 methods available" badge

**Key Methods List (bottom of panel):**
```
✓ createEscrow       ✓ resolveDispute
✓ releaseFunds       ✓ getEscrow
✓ markDisputed       ✓ getStatus
✓ getReputation      ✓ isExpired
✓ getTimeRemaining   ✓ escrowExists
✓ getAgentEscrows
```

---

## Panel 2: Autonomous Agent (Center)

**Title Overlay:** "Autonomous Service Agent"
**Subtitle:** "Auto-Dispute on Low Quality"

**Code Display:**
```typescript
// packages/agent-client
import { AutonomousServiceAgent } from '@x402resolve/agent';

const agent = new AutonomousServiceAgent({
  keypair: agentWallet,
  connection: solanaRPC,
  qualityThreshold: 80,  // Dispute if < 80%
  maxPrice: 0.001,
  autoDispute: true      // Automatic refunds
});

// Consume API with quality protection
const result = await agent.consumeAPI(
  'https://exploit-feed.xyz/api/alerts',
  { severity: 'high', chain: 'ethereum' },
  { id: '', severity: '', protocol: '', tvl: '' }
);

console.log(result);
// {
//   data: { ... },
//   quality: 38%,          ← Low quality detected
//   cost: 0.00048 SOL,     ← Only paid 48%
//   disputed: true         ← Auto-disputed
// }
```

**Animated Flow:**
1. Agent config appears (0-3 seconds)
2. `consumeAPI` call executes (3-8 seconds)
3. Result object appears with animated values:
   - `quality: 38%` (red, pulsing)
   - `cost: 0.00048 SOL` (green)
   - `disputed: true` (yellow warning icon)
4. Show calculation overlay: "Original: 0.001 SOL → Refund: 52.5% → Paid: 0.00048 SOL"

**Bottom Badge:**
```
⚡ Autonomous Quality Enforcement
✓ HTTP 402 Detection
✓ Escrow Creation
✓ Quality Assessment (3 dimensions)
✓ Auto-Dispute Filing
✓ Reputation Updates
```

---

## Panel 3: MCP Server for Claude (Right)

**Title Overlay:** "MCP Server"
**Subtitle:** "8 Tools for AI Agents"

**Visual: Claude Desktop Interface**
```
┌─────────────────────────────────────┐
│  Claude Desktop - MCP Tools         │
├─────────────────────────────────────┤
│                                     │
│  Available Tools:                   │
│                                     │
│  🔒 create_escrow                   │
│     Lock payment with guarantee     │
│                                     │
│  📊 assess_data_quality             │
│     Score 0-100, estimate refund    │
│                                     │
│  ⚖️ file_dispute                     │
│     Submit with evidence            │
│                                     │
│  ⭐ get_api_reputation               │
│     Check provider track record     │
│                                     │
│  🔄 call_api_with_escrow            │
│     Full workflow automation        │
│                                     │
│  + 3 more tools                     │
│                                     │
└─────────────────────────────────────┘
```

**Animated Tool Cards (sliding in from right):**

Each tool card appears with icon and description:

```
┌──────────────────────────────────────┐
│ 1. create_escrow                     │
│ Lock payment with quality guarantee  │
│ Input: api, amount, timeLock         │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ 2. check_escrow_status               │
│ Monitor escrow state                 │
│ Returns: Active|Disputed|Released    │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ 3. verify_payment                    │
│ Confirm payment received             │
│ Used by API providers                │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ 4. assess_data_quality               │
│ Score API response (0-100)           │
│ Returns: score + refund estimate     │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ 5. estimate_refund                   │
│ Calculate refund from quality        │
│ Sliding scale: 50-80% quality        │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ 6. file_dispute                      │
│ Submit dispute with evidence         │
│ Triggers on-chain resolution         │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ 7. get_api_reputation                │
│ Check provider trustworthiness       │
│ Returns: score + tx history          │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ 8. call_api_with_escrow              │
│ Full workflow automation             │
│ Create → Call → Assess → Dispute    │
└──────────────────────────────────────┘
```

**Bottom Section:**
```
┌─────────────────────────────────────┐
│  Example Claude Interaction:         │
├─────────────────────────────────────┤
│  User: "Call the exploit API and    │
│         only pay if quality is good" │
│                                     │
│  Claude: Using call_api_with_escrow │
│          ✓ Escrow created           │
│          ✓ API called               │
│          ✓ Quality: 38% ❌          │
│          ✓ Dispute filed            │
│          ✓ Refund: 52.5%            │
│                                     │
│  Result: Paid 0.00048 SOL instead   │
│          of 0.001 SOL               │
└─────────────────────────────────────┘
```

---

## Narration Timing Breakdown

**0-5 seconds:**
"Three integration layers."

- All three panels fade in
- Titles appear: "SDK", "Agent", "MCP Server"

**5-10 seconds:**
"The TypeScript SDK provides escrow creation, dispute resolution, and reputation tracking—eleven methods for developers."

- Panel 1 highlights
- Code lines appear sequentially
- "11 methods" badge pulses

**10-15 seconds:**
"The Autonomous Agent client handles everything: API consumption, quality assessment, automatic disputes when scores fall below your threshold."

- Panel 2 highlights
- Agent config appears
- Result object animates in with values
- Quality: 38% in red, disputed: true

**15-20 seconds:**
"And our MCP server gives Claude eight tools: create escrow, assess quality, file disputes, check reputation—autonomous agents that pay for APIs and demand refunds when quality fails."

- Panel 3 highlights
- Tool cards slide in (2 per second)
- Show Claude interaction example
- End with "8 Tools for AI Agents" badge

---

## Technical Specifications for Video Editor

### Font Choices
- Code: JetBrains Mono, 14pt
- Titles: Inter Bold, 24pt
- Subtitles: Inter Regular, 16pt
- Narration text: Inter Regular, 14pt

### Color Scheme
```
Panel 1 (SDK):        Blue accent   #3B82F6
Panel 2 (Agent):      Purple accent #A855F7
Panel 3 (MCP):        Green accent  #10B981

Background:           Dark gray     #1F2937
Text:                 White         #FFFFFF
Code background:      Darker gray   #111827
Error/Low quality:    Red           #EF4444
Success/Refund:       Green         #22C55E
Warning:              Yellow        #F59E0B
```

### Animations
- Panel transitions: 0.3s ease-in-out
- Code reveal: 0.1s per line
- Tool cards: 0.2s slide-in from right
- Value highlights: 0.5s pulse effect
- Quality score: Color change with bounce

### Key Frames
- 0:00 - Three panels appear
- 0:05 - Panel 1 spotlight
- 0:10 - Panel 2 spotlight
- 0:15 - Panel 3 spotlight
- 0:20 - All panels visible, fade to Scene 6

---

## What Judges Will See

In this 20-second scene, judges see:

1. **SDK Completeness**: 11 methods covering full escrow lifecycle
2. **Agent Autonomy**: Automatic quality checks and disputes
3. **MCP Integration**: 8 tools enabling Claude to transact autonomously
4. **Real Numbers**: 38% quality → 52.5% refund → 0.00048 SOL paid
5. **Production Ready**: Not concept code, actual TypeScript implementation

**Key Differentiator:**
Not just "we built an SDK" - we built THREE integration layers:
- Developers get a full-featured SDK
- Autonomous agents get quality enforcement
- AI assistants get MCP tools for natural language transactions

This is the **complete stack** for the agent economy.
