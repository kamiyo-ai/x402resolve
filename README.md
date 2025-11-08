# x402Resolve

![x402Resolve Header](./media/x402resolve-header.gif)

Trustless payment escrow for HTTP 402 APIs with oracle-verified quality assessment on Solana.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Anchor](https://img.shields.io/badge/Anchor-0.31.1-663399)](https://www.anchor-lang.com/)

## Overview

PDA-based escrow implementing RFC 9110 Section 15.5.3 (HTTP 402) with sliding-scale refunds based on oracle quality assessment. No admin keys, no custody. Quality verified before payment release.

**Program ID**: `E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n` (Devnet)

**Live Demo**: [https://x402resolve.kamiyo.ai/](https://x402resolve.kamiyo.ai/)

## Features

- PDA-secured escrow without admin keys
- Ed25519 signature verification for centralized oracle
- Switchboard On-Demand integration for decentralized oracle
- Sliding-scale refunds (0-100%) based on quality metrics
- Timestamp validation (300s freshness window)
- Reputation tracking for agents and APIs
- Rate limiting with verification tiers

## Quick Start

### API Provider

```typescript
import { x402PaymentMiddleware } from '@x402resolve/middleware';

app.use('/api/*', x402PaymentMiddleware({
  programId: ESCROW_PROGRAM_ID,
  connection,
  price: 0.001,
}));
```

### Agent/Consumer

```typescript
import { AutonomousServiceAgent } from '@x402resolve/agent-client';

const agent = new AutonomousServiceAgent({
  keypair,
  connection,
  programId: ESCROW_PROGRAM_ID,
  qualityThreshold: 85,
});

const result = await agent.consumeAPI(url, params, { expectedSchema });
```

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

**Escrow PDA**: `seeds = ["escrow", transaction_id.as_bytes()]`
- agent: Pubkey (32 bytes) - Client/consumer
- api: Pubkey (32 bytes) - API provider
- amount: u64 (8 bytes) - Escrowed amount in lamports
- status: EscrowStatus (2 bytes) - Active | Released | Disputed | Resolved
- created_at: i64 (8 bytes) - Unix timestamp
- expires_at: i64 (8 bytes) - Time-lock expiration
- transaction_id: String (4 + 64 bytes) - Unique transaction identifier
- bump: u8 (1 byte) - PDA bump seed
- quality_score: Option\<u8\> (2 bytes) - Oracle quality assessment (0-100)
- refund_percentage: Option\<u8\> (2 bytes) - Refund percentage (0-100)

**Reputation PDA**: `seeds = ["reputation", entity_pubkey.as_ref()]`
- entity: Pubkey (32 bytes) - Agent or API provider
- total_transactions: u64 (8 bytes)
- disputes_filed: u64 (8 bytes)
- disputes_won: u64 (8 bytes)
- disputes_partial: u64 (8 bytes)
- disputes_lost: u64 (8 bytes)
- average_quality_received: u8 (1 byte) - For agents
- reputation_score: u16 (2 bytes) - Calculated score (0-1000)
- bump: u8 (1 byte)

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

## Installation

```bash
git clone https://github.com/kamiyo-ai/x402resolve
cd x402resolve
npm install
```

### Build Program

```bash
cd packages/x402-escrow
anchor build
anchor deploy --provider.cluster devnet
```

## Packages

- `x402-escrow`: Solana program (Anchor)
- `x402-sdk`: TypeScript client library
- `x402-middleware`: HTTP 402 middleware (Express/FastAPI)
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

## Documentation

- [API Reference](./docs/markdown/API_REFERENCE.md)
- [Switchboard Integration](./packages/x402-escrow/SWITCHBOARD_INTEGRATION.md)
- [Troubleshooting](./TROUBLESHOOTING.md)

## License

MIT | KAMIYO
