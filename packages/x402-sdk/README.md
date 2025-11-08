# @kamiyo/x402-sdk

TypeScript SDK for x402Resolve - Automated payment and dispute resolution for AI agents.

## What is x402Resolve?

HTTP 402 implementation with automated conflict resolution. Agents dispute poor quality data programmatically and receive refunds based on objective quality metrics.

Automated resolution in seconds with no manual intervention.

## Features

- Escrow payments with quality verification
- Programmatic dispute filing
- AI-powered quality scoring
- Instant proportional refunds (0-100%)
- Solana native (low cost, high speed)
- Full TypeScript type safety

## Installation

```bash
npm install @kamiyo/x402-sdk
```

## Quick Start

### 1. Basic Payment (No Escrow)

```typescript
import { KamiyoClient } from '@kamiyo/x402-sdk';

const client = new KamiyoClient({
  apiUrl: 'https://api.kamiyo.ai',
  chain: 'solana',
  enablex402Resolve: false  // Disable escrow
});

// Pay for API access
const accessToken = await client.pay({
  amount: 0.01,  // SOL
  recipient: 'API_WALLET_ADDRESS'
});

// Use access token
client.setAccessToken(accessToken.token);

// Query API
const data = await client.query('/exploits/recent');
```

### 2. Payment with x402Resolve (Escrow + Dispute Support)

```typescript
import { KamiyoClient } from '@kamiyo/x402-sdk';
import { PublicKey } from '@solana/web3.js';

const client = new KamiyoClient({
  apiUrl: 'https://api.kamiyo.ai',
  chain: 'solana',
  verifierUrl: 'http://localhost:8000',
  enablex402Resolve: true,  // Enable escrow + disputes
  walletPublicKey: 'YOUR_AGENT_WALLET_PUBLIC_KEY',
  rpcUrl: 'https://api.devnet.solana.com'
});

// Pay to escrow
const payment = await client.pay({
  amount: 0.01,
  recipient: 'API_WALLET_ADDRESS',
  enableEscrow: true
});

console.log('Payment held in escrow:', payment.escrowAddress);
console.log('Transaction ID:', payment.transactionId);

// Use access token
client.setAccessToken(payment.token);

// Query API
const data = await client.query('/exploits/comprehensive', {
  protocol: 'uniswap',
  chain: 'ethereum'
});
```

### 3. Filing a Dispute

```typescript
// Agent evaluates data quality
const isQualityAcceptable = evaluateData(data);

if (!isQualityAcceptable) {
  // File dispute with x402 Verifier Oracle
  const dispute = await client.dispute({
    transactionId: payment.transactionId,
    reason: 'Incomplete data: received 3 exploits, expected 10+',
    originalQuery: 'Get comprehensive Uniswap V3 exploit history',
    dataReceived: data,
    expectedCriteria: ['comprehensive', 'uniswap', 'ethereum', 'verified'],
    expectedRecordCount: 10
  });

  console.log('Dispute filed:', dispute.disputeId);
  console.log('Quality score:', dispute.qualityScore);  // e.g., 65/100
  console.log('Refund:', dispute.refundPercentage + '%');  // e.g., 35%
  console.log('Reasoning:', dispute.reasoning);
}
```

### 4. Checking Dispute Status

```typescript
const status = await client.getDisputeStatus(dispute.disputeId);

console.log('Status:', status.status);  // 'resolved'
console.log('Refund amount:', status.refundAmount);  // 0.0035 SOL
console.log('Resolved at:', new Date(status.resolvedAt));
```

## API Reference

### `new KamiyoClient(config)`

Creates a new KAMIYO client instance.

**Config:**
```typescript
{
  apiUrl: string;                    // KAMIYO API URL
  chain: 'solana' | 'ethereum' | 'base';
  verifierUrl?: string;              // x402 Verifier Oracle URL (default: localhost:8000)
  enablex402Resolve?: boolean;       // Enable escrow + disputes (default: true)
  walletPublicKey?: string | PublicKey;  // Agent's wallet (required for escrow)
  rpcUrl?: string;                   // Solana RPC URL
}
```

### `client.pay(params): Promise<AccessToken>`

Pay for API access.

**Params:**
```typescript
{
  amount: number;           // Payment amount (SOL)
  recipient: string;        // API wallet address
  metadata?: object;        // Optional metadata
  enableEscrow?: boolean;   // Override global enablex402Resolve
}
```

**Returns:**
```typescript
{
  token: string;            // JWT access token
  expiresAt: number;        // Token expiration (unix timestamp)
  transactionId: string;    // Unique transaction ID
  escrowAddress?: string;   // Escrow address (if escrow enabled)
}
```

### `client.dispute(params): Promise<DisputeResult>`

File a dispute for poor data quality.

**Params:**
```typescript
{
  transactionId: string;         // Transaction to dispute
  reason: string;                // Human-readable reason
  originalQuery: string;         // What agent requested
  dataReceived: any;             // What agent received
  expectedCriteria: string[];    // Expected quality criteria
  expectedRecordCount?: number;  // Expected number of records
}
```

**Returns:**
```typescript
{
  disputeId: string;
  status: 'pending' | 'resolved' | 'rejected';
  qualityScore: number;          // 0-100
  recommendation: 'release' | 'partial_refund' | 'full_refund';
  refundPercentage: number;      // 0-100
  reasoning: string;             // Explanation
  signature: string;             // Verifier signature
}
```

### `client.getDisputeStatus(disputeId): Promise<DisputeStatus>`

Get current status of a dispute.

**Returns:**
```typescript
{
  disputeId: string;
  transactionId: string;
  status: 'pending' | 'verifying' | 'resolved' | 'rejected';
  qualityScore?: number;
  refundPercentage?: number;
  refundAmount?: number;         // Actual SOL refunded
  createdAt: number;
  resolvedAt?: number;
  reasoning?: string;
}
```

### `client.getEscrowDetails(escrowAddress): Promise<EscrowDetails>`

Get details of an escrow account.

**Returns:**
```typescript
{
  escrowAddress: string;
  agent: string;                 // Agent wallet
  api: string;                   // API wallet
  amount: number;                // Escrowed amount (SOL)
  status: 'active' | 'released' | 'disputed' | 'resolved';
  createdAt: number;
  expiresAt: number;             // Auto-release time
}
```

### `client.query(endpoint, params?): Promise<any>`

Query KAMIYO API with authenticated access.

**Example:**
```typescript
const exploits = await client.query('/exploits/search', {
  protocol: 'uniswap',
  minAmount: 1000000
});
```

### `client.setAccessToken(token: string): void`

Set JWT access token manually.

### `client.clearAccessToken(): void`

Clear stored access token.

## Quality Scoring Algorithm

The x402 Verifier Oracle uses a multi-factor algorithm:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Semantic Similarity** | 40% | Cosine similarity between query and data (embeddings) |
| **Completeness** | 40% | Coverage of expected criteria + record count |
| **Freshness** | 20% | Data recency validation |

**Refund Calculation:**
- **80-100**: Full release (0% refund) - Quality acceptable
- **50-79**: Sliding scale partial refund
- **0-49**: Full refund (100%) - Quality unacceptable

**Example:**
```
Quality Score: 65/100
├─ Semantic: 0.72 (40% × 0.72 = 28.8)
├─ Completeness: 0.40 (40% × 0.40 = 16.0)
└─ Freshness: 1.00 (20% × 1.00 = 20.0)
Total: 64.8 → Refund: 33.6%
```

## Error Handling

All SDK methods can throw `X402Error`:

```typescript
import { X402Error } from '@kamiyo/x402-sdk';

try {
  await client.pay({ amount: 0.01, recipient: 'WALLET' });
} catch (error) {
  if (error instanceof X402Error) {
    console.error('Code:', error.code);
    console.error('Message:', error.message);
    console.error('Status:', error.statusCode);
  }
}
```

**Error Codes:**
- `PAYMENT_REQUIRED` - API requires payment
- `PAYMENT_FAILED` - Payment transaction failed
- `ESCROW_PAYMENT_FAILED` - Escrow creation failed
- `WALLET_NOT_CONFIGURED` - Solana wallet not set
- `X402_RESOLVE_DISABLED` - x402Resolve not enabled
- `VERIFIER_UNAVAILABLE` - Cannot connect to verifier
- `DISPUTE_FAILED` - Dispute filing failed
- `DISPUTE_STATUS_FAILED` - Cannot fetch dispute status
- `ESCROW_DETAILS_FAILED` - Cannot fetch escrow details
- `QUERY_FAILED` - API query failed

## Examples

See `/examples` directory for complete examples:
- [`basic-payment/`](../../examples/basic-payment/) - Simple payment without escrow
- [`agent-dispute/`](../../examples/agent-dispute/) - Complete dispute resolution flow

## Requirements

- Node.js 18+
- TypeScript 5+
- Solana wallet (for escrow payments)
- Running x402 Verifier Oracle (for disputes)

## Development

```bash
# Install dependencies
npm install

# Build
npm run build

# Watch mode
npm run dev

# Run tests
npm test

# Lint
npm run lint
```

## License

MIT
