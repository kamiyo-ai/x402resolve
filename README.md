# x402 MCP Server

Model Context Protocol server for Solana escrow-based API payments with quality guarantees and dispute resolution.

## Features

- Solana/Anchor program integration for x402Resolve escrow system
- Quality assessment and automatic dispute filing
- Reputation tracking for API providers
- Full transaction lifecycle management

## Installation

```bash
npm install
npm run build
```

## Configuration

Create `.env`:

```env
SOLANA_RPC_URL=https://api.devnet.solana.com
X402_PROGRAM_ID=E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n
AGENT_PRIVATE_KEY=<base58_private_key>
```

Generate keypair:

```bash
solana-keygen new --no-bip39-passphrase -o keypair.json
```

Fund devnet wallet:

```bash
solana airdrop 2 <address> --url devnet
```

## Usage

Start server:

```bash
npm start
```

Configure in Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "x402": {
      "command": "node",
      "args": ["/path/to/kamiyo-mcp/dist/index.js"],
      "env": {
        "SOLANA_RPC_URL": "https://api.devnet.solana.com",
        "X402_PROGRAM_ID": "E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n",
        "AGENT_PRIVATE_KEY": "<your_key>"
      }
    }
  }
}
```

## Available Tools

- `create_escrow` - Create payment escrow with quality guarantee
- `check_escrow_status` - Query escrow account status
- `verify_payment` - Confirm payment was received
- `assess_data_quality` - Evaluate API response quality
- `estimate_refund` - Calculate refund based on quality score
- `file_dispute` - File dispute for poor quality data
- `get_api_reputation` - Query provider reputation
- `call_api_with_escrow` - Unified workflow with automatic dispute handling

## Testing

Run integration tests:

```bash
node tests/test-integration.ts
```

## Architecture

```
src/
├── index.ts              # MCP server entry point
├── solana/
│   ├── client.ts         # Solana RPC client
│   ├── anchor.ts         # Anchor program wrapper
│   ├── pdas.ts           # PDA derivation
│   └── transactions.ts   # Transaction utilities
└── tools/
    ├── escrow.ts         # Escrow management
    ├── dispute.ts        # Dispute handling
    ├── quality.ts        # Quality assessment
    ├── reputation.ts     # Reputation queries
    └── unified.ts        # Unified workflow
```

## License

MIT
