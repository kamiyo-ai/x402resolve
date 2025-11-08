# x402Resolve

![x402Resolve Dashboard](./docs/media/switchboard-dashboard.png)

[![Solana](https://img.shields.io/badge/Solana-Devnet-9945FF?logo=solana)](https://explorer.solana.com/address/ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY?cluster=devnet)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Anchor](https://img.shields.io/badge/Anchor-0.31.1-663399)](https://www.anchor-lang.com/)

**Live Demo**: https://x402kamiyo.github.io/x402resolve
**Program ID**: `ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY` (Devnet)

Trustless escrow protocol for HTTP 402 APIs with oracle-verified quality assessment and sliding-scale refunds. Implements RFC 9110 Section 15.5.3 with PDA-secured payments released only after cryptographic quality verification.

## Problem

Traditional API monetization lacks quality guarantees. Consumers pay upfront with no recourse for poor responses. Chargebacks cost $35+ and take 30-90 days. Payment processors cannot evaluate API quality, creating trust asymmetry favoring providers.

## Solution

On-chain escrow with oracle quality scoring. Payments locked in PDAs until quality verified. Refunds automatically calculated on sliding scale (0-100%) based on response quality metrics. No intermediaries, no admin keys, no custody risk.

## Technical Architecture

```
┌─────────┐          ┌──────────┐          ┌─────────┐          ┌────────────┐
│ Agent   │─────────▶│  Escrow  │─────────▶│   API   │◀────────▶│  Oracle    │
│ Wallet  │  0.1 SOL │    PDA   │  Request │ Provider│  Quality │ (Ed25519 / │
└─────────┘          └──────────┘          └─────────┘  Score   │Switchboard)│
                           │                     │                └────────────┘
                           │                     │                      │
                           │◀────────────────────┴──────────────────────┘
                           │         Quality Score: 0-100
                           │         Refund %: Calculated
                           ▼
                     ┌──────────────┐
                     │ Distribute   │
                     │ Agent: 35%   │
                     │ API:   65%   │
                     └──────────────┘
```

### State Machine

```
initialize_escrow
       │
       ▼
    ACTIVE ────────────────┬──────────────┐
       │                   │              │
       │ timeout           │ release      │ mark_disputed
       ▼                   ▼              ▼
   EXPIRED            RELEASED        DISPUTED
                                          │
                                          │ resolve_dispute
                                          │ (oracle signature)
                                          ▼
                                      RESOLVED
                                    (refund split)
```

### PDA Structure

**Escrow Account**: `["escrow", transaction_id]`
```rust
pub struct Escrow {
    pub agent: Pubkey,              // Consumer wallet
    pub api: Pubkey,                // Provider wallet
    pub amount: u64,                // Lamports escrowed
    pub status: EscrowStatus,       // Active/Disputed/Released/Resolved
    pub created_at: i64,            // Unix timestamp
    pub expires_at: i64,            // Expiry (1h-30d)
    pub transaction_id: String,     // Unique identifier
    pub quality_score: Option<u8>,  // 0-100
    pub refund_percentage: Option<u8>, // 0-100
    pub bump: u8,
}
```

**Reputation Account**: `["reputation", pubkey]`
```rust
pub struct Reputation {
    pub total_transactions: u64,
    pub disputes_filed: u64,
    pub disputes_won: u64,
    pub disputes_partial: u64,
    pub disputes_lost: u64,
    pub average_quality_received: u8,
    pub reputation_score: u16,      // 0-1000
    pub bump: u8,
}
```

## Oracle Integration

### Centralized Oracle (Python ML)

Ed25519 signature verification on-chain. Oracle signs `(transaction_id || quality_score || refund_percentage)` payload. Signature verified via `Ed25519Program` precompile before fund distribution.

```rust
let ix_sysvar = Sysvar::from_account_info(&ctx.accounts.instruction_sysvar)?;
let current_ix = solana_program::sysvar::instructions::get_instruction_relative(0, &ix_sysvar)?;
require!(current_ix.program_id == solana_program::ed25519_program::ID, InvalidOracle);
```

### Decentralized Oracle (Switchboard On-Demand)

Pull-based oracle feeds with cryptographic attestation. 300-second freshness window enforced on-chain.

```rust
let feed = PullFeedAccountData::parse(feed_info.data.borrow())?;
let age = clock.unix_timestamp - feed.last_update_timestamp;
require!(age >= 0 && age <= 300, StaleAttestation);
```

## Quality Scoring

Multi-factor weighted algorithm:

```
Quality = (Completeness × 0.4) + (Accuracy × 0.3) + (Timeliness × 0.3)
Refund  = max(0, 100 - Quality)  for Quality < 80
        = 0                       for Quality ≥ 80
```

**Example Distributions**:
- Quality 95: Agent 0%, API 100%
- Quality 65: Agent 35%, API 65%
- Quality 30: Agent 70%, API 30%
- Quality 0:  Agent 100%, API 0%

## Security

- **No Admin Keys**: PDAs enforce deterministic authority
- **Checked Arithmetic**: All operations use `checked_add/sub/mul`
- **Bounds Validation**: Timelock (3600s-2592000s), Amount (0.001-1000 SOL)
- **Rent Exemption**: All accounts validated for minimum balance
- **Signature Verification**: Ed25519 precompile validation
- **Timestamp Validation**: Switchboard feeds require <300s staleness

See [SECURITY.md](./SECURITY.md) for full audit report.

## Repository Structure

```
x402resolve/
├── packages/
│   ├── x402-escrow/          # Anchor program (Rust)
│   ├── x402-sdk/             # TypeScript client library
│   ├── x402-middleware/      # Express/FastAPI middleware
│   ├── agent-client/         # Autonomous agent implementation
│   ├── switchboard-function/ # Decentralized oracle
│   └── mcp-server/           # Model Context Protocol server
├── docs/
│   ├── markdown/API_REFERENCE.md
│   ├── security/SECURITY_AUDIT_REPORT.md
│   └── ARCHITECTURE_DIAGRAMS.md
├── examples/
│   ├── autonomous-agent-demo/
│   ├── x402-api-server/
│   └── exploit-prevention/
└── tests/                    # Integration tests
```

## Quick Start

### Deploy Program

```bash
cd packages/x402-escrow
anchor build
anchor deploy --provider.cluster devnet --program-id <KEYPAIR>
```

### Initialize Escrow (TypeScript)

```typescript
import { X402Client } from '@x402resolve/sdk';

const client = new X402Client(connection, wallet);

const tx = await client.initializeEscrow({
  api: apiPubkey,
  amount: 0.1 * LAMPORTS_PER_SOL,
  expiresIn: 3600,
  transactionId: 'tx_unique_id',
});
```

### Resolve Dispute

```typescript
// With centralized oracle (Ed25519)
const signature = oracle.sign(message); // Off-chain
await client.resolveDispute({
  transactionId,
  qualityScore: 75,
  refundPercentage: 25,
  signature,
});

// With Switchboard
await client.resolveDisputeSwitchboard({
  transactionId,
  feedAccount: switchboardFeedPubkey,
});
```

## Economics

At 1% dispute rate on $5,000 monthly API spend:

| Metric           | Traditional | x402Resolve | Reduction  |
|------------------|-------------|-------------|------------|
| Cost/Dispute     | $35.00      | $0.005      | 99.98%     |
| Resolution Time  | 30-90 days  | 48 hours    | 98%        |
| Monthly Cost     | $3,500      | $0.50       | 99.98%     |
| Annual Savings   | -           | $41,994     | -          |

## Performance Metrics

| Metric                  | Value              |
|-------------------------|-------------------|
| Program Size            | 275 KB            |
| Compute Units (Init)    | ~15,000           |
| Compute Units (Resolve) | ~25,000           |
| Transaction Cost        | ~0.00001 SOL      |
| Account Rent            | 0.002 SOL/escrow  |

## Development

```bash
# Install dependencies
npm install

# Build all packages
npm run build

# Run tests
anchor test

# Deploy to devnet
cd packages/x402-escrow
anchor deploy --provider.cluster devnet
```

## Documentation

- [API Reference](./docs/markdown/API_REFERENCE.md)
- [Architecture Details](./docs/ARCHITECTURE_DIAGRAMS.md)
- [Security Audit](./docs/security/SECURITY_AUDIT_REPORT.md)
- [Switchboard Integration](./packages/x402-escrow/SWITCHBOARD_INTEGRATION.md)

## License

MIT | KAMIYO
