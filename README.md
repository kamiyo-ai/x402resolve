# x402Resolve

![x402resolve](https://github.com/user-attachments/assets/7c7783d6-2055-400b-a1e5-cb4c2ce7a76c)

Trustless payment escrow for HTTP 402 APIs with oracle-verified quality assessment on Solana.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Solana](https://img.shields.io/badge/Solana-Devnet-14F195?logo=solana)](https://solana.com)
[![Anchor](https://img.shields.io/badge/Anchor-0.31.1-663399)](https://www.anchor-lang.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![Rust](https://img.shields.io/badge/Rust-1.75-orange?logo=rust)](https://www.rust-lang.org/)
[![Tests](https://img.shields.io/badge/tests-unit%20%7C%20integration%20%7C%20e2e%20%7C%20security-success)](TESTING.md)
[![Coverage](https://img.shields.io/badge/coverage-program%20%7C%20SDK%20%7C%20oracle-brightgreen)](TESTING.md)
[![Docs](https://img.shields.io/badge/docs-API%20examples-success)](docs/API_EXAMPLES.md)
[![MCP](https://img.shields.io/badge/MCP-8%20tools-purple?logo=anthropic)](packages/mcp-server/README.md)

## Overview

PDA-based escrow implementing RFC 9110 Section 15.5.3 (HTTP 402) with sliding-scale refunds based on oracle quality assessment. No admin keys, no custody. Quality verified before payment release.

**Program ID**: `E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n` (Devnet)

**Live Demo**: [https://x402resolve.kamiyo.ai/](https://x402resolve.kamiyo.ai/)

**Demo Video**: [https://x402resolve.kamiyo.ai/demo-video.mp4](https://x402resolve.kamiyo.ai/demo-video.mp4)

## Problem

HTTP 402 APIs lack trustless quality assurance. Clients pay upfront with no recourse for poor data. Traditional chargebacks take 30-90 days and cost $35-50 per dispute. Providers face fraud risk and admin overhead.

**x402Resolve fixes this:** Oracle-verified quality assessment triggers automatic sliding-scale refunds (0-100%) on-chain. Payment released only after quality validation. 2-48 hour resolution at $2-8 per dispute.

## Market Opportunity

The AI agents market reached **$7.6B in 2025** (41% YoY growth) while payment disputes hit **$41.69B**. As agents make autonomous purchases, traditional chargebacks (30-90 days, $35-50/dispute) break automation. Industry experts predict: *"AI agent transactions will trigger new payment disputes... It's going to be messy for the next five years."*

**x402Resolve advantage:** 15-45x faster resolution, 5-25x cheaper, sliding-scale refunds vs binary (all-or-nothing). First and only MCP server for payments—MCP adopted by OpenAI, Google DeepMind in 2025.

**Go-to-Market:** Phase 1: MCP ecosystem (Claude, LangChain). Phase 2: Developer platforms (Replit, Zed). Phase 3: Enterprise (Fortune 500, Stripe, Visa). Phase 4: Protocol standardization (RFC, industry adoption). 6-12 month first-mover lead, network effects via reputation data.

**Full strategy:** [Market Analysis & GTM](docs/MARKET_STRATEGY.md)

## Quick Integration

Build x402-compliant APIs or agents in **minutes**, not weeks. No custom escrow logic, refund math, or reputation tracking needed.

### API Provider

```typescript
import { x402PaymentMiddleware } from '@x402resolve/middleware';

app.use('/api/*', x402PaymentMiddleware({
  programId: new PublicKey('E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n'),
  connection, price: 0.001, qualityGuarantee: true
}));
```

### AI Agent

```typescript
const escrow = await client.createEscrow({ api: provider, amount: 0.001 });
const data = await fetch(apiUrl, { headers: { 'X-Payment-Proof': escrow } });
if (quality < 80) await client.markDisputed(escrow); // Auto-refund
```

**What you get:** Automatic escrows, quality-based refunds, dispute resolution, reputation tracking, rate limiting—all handled on-chain.

## MCP Server (AI Agent Integration)

**MCP server for HTTP 402 payments with quality-verified refunds** - enabling Claude and autonomous agents to autonomously create escrows, assess data quality, and file disputes on Solana.

### What is MCP?

[Model Context Protocol (MCP)](https://modelcontextprotocol.io) is Anthropic's open standard for connecting AI systems to external tools and data sources. Our MCP server gives Claude Desktop, LangChain, AutoGPT, and other AI agents the ability to:

- Create payment escrows with quality guarantees
- Assess API response quality
- File disputes for poor data
- Check escrow status
- Verify API provider reputation
- Estimate refunds based on quality scores

**8 production-ready tools** for trustless agent-to-API transactions.

### Quick Start (Claude Desktop)

1. **Install dependencies:**
```bash
cd packages/mcp-server
pip3 install -r requirements.txt
```

2. **Configure Claude Desktop:**
```json
{
  "mcpServers": {
    "x402resolve": {
      "command": "python3",
      "args": ["/absolute/path/to/packages/mcp-server/server.py"],
      "env": {
        "SOLANA_RPC_URL": "https://api.devnet.solana.com",
        "X402_PROGRAM_ID": "E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n"
      }
    }
  }
}
```

3. **Use in Claude:**
```
User: "Create a 0.1 SOL escrow for the weather API"
Claude: I'll use the create_escrow tool...
Escrow created: EscrowABC123...
  Amount: 0.1 SOL
  Quality guarantee: Enabled
```

### Available Tools

| Tool | Description |
|------|-------------|
| `create_escrow` | Lock payment with quality guarantee |
| `call_api_with_escrow` | Unified flow: create + call + assess |
| `assess_data_quality` | Evaluate completeness, freshness, schema compliance |
| `file_dispute` | Submit dispute for poor quality data |
| `check_escrow_status` | Monitor escrow state |
| `get_api_reputation` | Check provider trust score |
| `verify_payment` | Confirm payment received |
| `estimate_refund` | Calculate refund by quality score |

**Full Documentation:** [packages/mcp-server/README.md](packages/mcp-server/README.md)

## Why Solana?

**High TPS** → Real-time refunds (2-48 hours vs 30-90 days). No waiting for traditional payment processors.

**PDAs (Program Derived Addresses)** → Keyless escrow security. No admin keys to compromise, no custody risk. Funds locked by cryptographic derivation.

**Switchboard On-Demand** → Decentralized oracle verification. Quality assessment verified on-chain with 300s freshness guarantee. No single point of failure.

**Sub-penny costs** → $0.02/dispute (even with ML inference + infrastructure). Traditional methods cost $35-50.

## Use Cases

| Use Case | Features | Example |
|----------|----------|---------|
| **AI Agent Marketplaces** | Auto-pay with quality guarantees, threshold enforcement (85%+ quality) | Agent calls Twitter API → pays 0.001 SOL → auto-refund if data incomplete |
| **Data Marketplaces** | Oracle-verified freshness, completeness and schema validation | Financial API → oracle checks timestamp → refund if stale |
| **Compute Marketplaces** | SLA enforcement, response time and accuracy verification | Image generation → quality score based on resolution + inference time |
| **ML Model Endpoints** | Pay-per-inference, confidence thresholds, schema validation | Sentiment analysis → refund if confidence <90% |

## Ecosystem

| Category | Description | Integrations |
|----------|-------------|--------------|
| **Agent Frameworks** | Drop-in payment layer for autonomous agents | LangChain tool calling, AutoGPT flows, any HTTP client (axios, fetch) |
| **Solana DeFi** | Composable with existing protocols | SPL tokens (planned), Solana Pay format, Jupiter/Orca swaps (planned) |
| **Oracle Networks** | Multi-oracle quality verification | Switchboard On-Demand (live), Pyth feeds (planned), custom endpoints |
| **API Standards** | RFC-compliant design | HTTP 402 (RFC 9110), OpenAPI 3.0, Express/FastAPI/Next.js |

## Economics

Cost comparison at 1% dispute rate (100 disputes/month on $5,000 API spend):

| Method | Cost/Dispute | Total/Month | Resolution Time | Annual Cost |
|--------|--------------|-------------|-----------------|-------------|
| Traditional (Stripe/PayPal) | $35-50 | $3,500-5,000 | 30-90 days | $42,000-60,000 |
| x402Resolve (All-in) | $2-8 | $200-800 | 2-48 hours | $2,400-9,600 |
| **Savings** | **$27-48 (84-94%)** | **$2,700-4,800 (84-94%)** | **97-99% faster** | **$32,400-57,600 (84-94%)** |

- **Traditional:** $35-50/dispute (chargeback + processing + admin)
- **x402Resolve:** $2-8/dispute (ML inference $0.5-2 + agent compute $0.3-1.5 + infrastructure $1-3 + on-chain $0.02)
- **84-94% cost reduction**

## Features

- PDA-secured escrow without admin keys
- Ed25519 signature verification for centralized oracle
- Switchboard On-Demand integration for decentralized oracle
- Sliding-scale refunds (0-100%) based on quality metrics
- Timestamp validation (300s freshness window)
- Reputation tracking for agents and APIs
- Rate limiting with verification tiers

## Architecture

### High-Level Flow

```
┌──────────┐    ┌────────┐    ┌─────┐    ┌────────┐
│  Client  │───▶│ Escrow │───▶│ API │◀──▶│ Oracle │
└──────────┘    └────────┘    └─────┘    └────────┘
                     │            │           │
                     │            │           │
                     │◀───────────┴───────────┘
                     │  Quality Assessment
                     │
                     ▼
              Sliding-Scale Refund
```

### Dispute Resolution Flow

```
1. Payment          2. API Call         3. Quality Check      4. Settlement
┌─────────┐        ┌─────────┐         ┌──────────┐         ┌──────────┐
│ Client  │        │   API   │         │  Oracle  │         │  Escrow  │
│ creates │───────▶│ returns │────────▶│ assesses │────────▶│ executes │
│ escrow  │  SOL   │  data   │  JSON   │ quality  │  score  │  refund  │
└─────────┘        └─────────┘         └──────────┘         └──────────┘
   0.01 SOL          Response            Score: 65            0.0035 SOL
   locked            received            (35% refund)         returned
```

### State Machine

```
initialize_escrow → Active → [release_funds | mark_disputed]
                      ↓                           ↓
                   Released                   Disputed
                                                 ↓
                                         resolve_dispute
                                                 ↓
                                             Resolved
                                         (split by refund %)
```

### Account Structure

**Escrow PDA**
```rust
seeds = [b"escrow", transaction_id.as_bytes()]

agent: Pubkey                              // 32 bytes - Client/consumer
api: Pubkey                                // 32 bytes - API provider
amount: u64                                // 8 bytes  - Escrowed amount in lamports
status: EscrowStatus                       // 2 bytes  - Active | Released | Disputed | Resolved
created_at: i64                            // 8 bytes  - Unix timestamp
expires_at: i64                            // 8 bytes  - Time-lock expiration
transaction_id: String                     // 68 bytes - 4 (length) + 64 (max_len)
bump: u8                                   // 1 byte   - PDA bump seed
quality_score: Option<u8>                  // 2 bytes  - Oracle quality assessment (0-100)
refund_percentage: Option<u8>              // 2 bytes  - Refund percentage (0-100)
```

**EntityReputation PDA**
```rust
seeds = [b"reputation", entity.key().as_ref()]

entity: Pubkey                             // 32 bytes - Agent or API provider
entity_type: EntityType                    // 2 bytes  - Agent | Provider
total_transactions: u64                    // 8 bytes  - Total completed transactions
disputes_filed: u64                        // 8 bytes  - Total disputes initiated
disputes_won: u64                          // 8 bytes  - Full refunds (quality <50)
disputes_partial: u64                      // 8 bytes  - Partial refunds (quality 50-79)
disputes_lost: u64                         // 8 bytes  - No refund (quality ≥80)
average_quality_received: u8               // 1 byte   - Running average quality score
reputation_score: u16                      // 2 bytes  - Calculated score (0-1000)
created_at: i64                            // 8 bytes  - Account creation timestamp
last_updated: i64                          // 8 bytes  - Last reputation update
bump: u8                                   // 1 byte   - PDA bump seed
```

## Oracle Integration

### Centralized (Python)
Ed25519-signed quality assessment with on-chain signature verification.

### Decentralized (Switchboard)
On-Demand pull feed with cryptographic attestation. Timestamp validation enforces 300-second freshness window.

```rust
let feed_data = PullFeedAccountData::parse(feed_account_info.data.borrow())?;
let age = clock.unix_timestamp - feed_data.last_update_timestamp;
require!(age >= 0 && age <= 300, StaleAttestation);
```

## Quality Scoring

Oracle outputs:
1. **quality_score** (0-100): Weighted assessment
2. **refund_percentage** (0-100): Refund amount

Refund logic determined by oracle. Typical mapping:
- Score < 50 → Full refund
- Score 50-79 → Partial refund
- Score ≥ 80 → No refund

## Getting Started

### 1. Install SDK/Middleware

**For API Providers:**
```bash
npm install @x402resolve/middleware @solana/web3.js
```

**For AI Agents:**
```bash
npm install @kamiyo/x402-sdk @solana/web3.js
```

### 2. API Provider Setup

```typescript
import express from 'express';
import { Connection, PublicKey } from '@solana/web3.js';
import { x402PaymentMiddleware } from '@x402resolve/middleware';

const app = express();
const connection = new Connection('https://api.devnet.solana.com');

app.use('/api/premium/*', x402PaymentMiddleware({
  programId: new PublicKey('E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n'),
  connection,
  price: 0.001,
  qualityGuarantee: true
}));

app.get('/api/premium/data', (req, res) => {
  res.json({ data: 'protected content', quality_score: 95 });
});
```

### 3. AI Agent Setup

```typescript
import { KamiyoClient } from '@kamiyo/x402-sdk';
import { Connection, Keypair } from '@solana/web3.js';

const connection = new Connection('https://api.devnet.solana.com');
const wallet = Keypair.fromSecretKey(/* your key */);

const client = new KamiyoClient({
  apiUrl: 'https://api.example.com',
  chain: 'solana',
  rpcUrl: 'https://api.devnet.solana.com',
  walletPublicKey: wallet.publicKey
});

// Pay with escrow
const payment = await client.pay({
  amount: 0.001,
  recipient: new PublicKey('API_PROVIDER'),
  enableEscrow: true
});

// Call API
const response = await fetch('https://api.example.com/data', {
  headers: { 'X-Payment-Proof': payment.escrowAddress }
});

// Auto-dispute if low quality
if (response.quality_score < 80) {
  await client.fileDispute({
    transactionId: payment.transactionId,
    reason: 'Quality below threshold',
    originalQuery: 'data request',
    dataReceived: response,
    expectedCriteria: ['complete_data', 'valid_format']
  });
}
```

### 4. Local Development (Build from Source)

```bash
git clone https://github.com/kamiyo-ai/x402resolve
cd x402resolve
npm install
cd packages/x402-escrow && anchor build
anchor deploy --provider.cluster devnet
```

## Packages

- `x402-escrow`: Solana program (Anchor)
- `x402-sdk`: TypeScript client library
- `x402-middleware`: HTTP 402 middleware (Express/FastAPI)
- `mcp-server`: Model Context Protocol server for AI agents (Claude, LangChain)
- `agent-client`: Autonomous agent implementation
- `switchboard-function`: Decentralized oracle function

## Security

- Checked arithmetic for all calculations
- PDA authority isolation
- Time-lock bounds (1h - 30d)
- Amount limits (0.001 - 1000 SOL)
- Rent-exempt validation
- Rate limiting by verification tier

See [SECURITY.md](./SECURITY.md) for details.

## API Reference

### SDK Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `client.pay()` | `{ amount, recipient, enableEscrow }` | `{ token, escrowAddress, transactionId }` | Create payment with optional escrow |
| `client.fileDispute()` | `{ transactionId, qualityScore, evidence }` | `Promise<void>` | File dispute for poor quality |
| `client.getDisputeStatus()` | `transactionId: string` | `{ status, refundPercentage }` | Get dispute resolution status |
| `escrow.createEscrow()` | `{ api, amount, timeLock }` | `PublicKey` | Create escrow account |
| `escrow.markDisputed()` | `escrowPDA: PublicKey` | `Transaction` | Mark escrow as disputed |
| `escrow.releaseFunds()` | `escrowPDA: PublicKey` | `Transaction` | Release funds to API provider |

### Middleware Configuration

```typescript
x402PaymentMiddleware({
  programId: PublicKey,      // Escrow program ID
  connection: Connection,    // Solana RPC connection
  price: number,            // Price in SOL
  realm: string,            // API identifier
  qualityGuarantee: boolean // Enable quality refunds (default: false)
})
```

### Error Handling

| Error Code | Message | Solution |
|------------|---------|----------|
| `PAYMENT_REQUIRED` | No payment proof provided | Include `X-Payment-Proof` header with escrow address |
| `INVALID_ESCROW` | Escrow account not found | Verify escrow creation succeeded |
| `ESCROW_EXPIRED` | Time lock expired | Create new escrow |
| `QUALITY_TOO_LOW` | Quality below threshold | Review quality scoring logic |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait or upgrade verification tier |

Full examples: [API_EXAMPLES.md](docs/API_EXAMPLES.md)

## Documentation

- [API Reference](./docs/markdown/API_REFERENCE.md)
- [Switchboard Integration](./packages/x402-escrow/SWITCHBOARD_INTEGRATION.md)
- [Troubleshooting](./TROUBLESHOOTING.md)

## Roadmap

| Timeline | Status | Features |
|----------|--------|----------|
| **Nov 2025 (Hackathon)** | Live | Solana escrow program (devnet), MCP server (Claude integration), TypeScript SDK, HTTP 402 middleware (Express), Switchboard On-Demand oracle, Quality-based sliding-scale refunds, Reputation tracking |
| **Dec 2025 - Feb 2026** | Phase 1 | MCP ecosystem launch, LangChain/AutoGPT integrations, 10+ API provider onboarding, Security audit for mainnet, Multi-oracle consensus (3+ verifiers) |
| **Mar - May 2026** | Phase 2 | Developer platform integrations (Replit, Zed), Framework middleware (FastAPI, Next.js), SPL token escrows (USDC/USDT), Enhanced ML quality scoring, Dispute resolution UI |
| **Jun - Nov 2026** | Phase 3 | Enterprise white-label deployments, Cross-chain support (Base, Ethereum via Wormhole), Pyth price feeds, Governance token launch, SOC2/GDPR compliance packages |
| **2027+** | Phase 4 | Protocol standardization (RFC submission), Multi-chain expansion, Chainlink CCIP integration, DAO governance, NFT-gated API access, Jupiter aggregator |

**See full strategy:** [Market Analysis & GTM](docs/MARKET_STRATEGY.md)

## License

MIT | KAMIYO
