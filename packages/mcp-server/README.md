# KAMIYO MCP Server

MCP server providing crypto exploit intelligence and automated dispute resolution for AI agents.

## Quick Start

```bash
# 1. Install dependencies
cd packages/mcp-server
pip install -r requirements.txt

# 2. Configure Claude Desktop
# Edit ~/Library/Application Support/Claude/claude_desktop_config.json:
{
  "mcpServers": {
    "kamiyo": {
      "command": "python3",
      "args": ["/path/to/x402resolve/packages/mcp-server/server.py"]
    }
  }
}

# 3. Restart Claude Desktop
# Tools appear automatically in Claude
```

## Overview

AI agent access to KAMIYO exploit database ($2.1B+ tracked) with x402Resolve automated dispute resolution.

**Features**:
- 5 MCP tools
- Automated dispute filing
- Tiered access: Free/Personal/Team/Enterprise
- stdio/SSE transport
- JWT authentication
- Rate limiting

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL or SQLite database
- KAMIYO API access

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Configuration

Create `.env` file:

```bash
# Required
KAMIYO_API_URL=https://api.kamiyo.ai
MCP_JWT_SECRET=your_jwt_secret
DATABASE_URL=postgresql://user:pass@localhost/kamiyo

# Optional
STRIPE_SECRET_KEY=your_stripe_key
LOG_LEVEL=INFO
ENABLE_CACHE=true
```

## Running the Server

### Local Development

```bash
python server.py
```

### Claude Desktop Integration

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "kamiyo-security": {
      "command": "python3",
      "args": ["/absolute/path/to/packages/mcp-server/server.py"],
      "env": {
        "KAMIYO_API_URL": "https://api.kamiyo.ai",
        "MCP_JWT_SECRET": "your_jwt_secret",
        "DATABASE_URL": "postgresql://user:pass@localhost/kamiyo"
      }
    }
  }
}
```

Restart Claude Desktop to load the server.

## Available Tools

### 1. health_check

Check server status and connectivity.

**Parameters**: None

**Returns**: Server version, database status, API status

**Example**:
```
Use the health_check tool
```

### 2. search_crypto_exploits

Query KAMIYO exploit database by protocol, chain, date range, or impact.

**Parameters**:
- `protocol` (optional): Protocol name (e.g., "Uniswap")
- `chain` (optional): Blockchain (e.g., "Ethereum")
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)
- `min_amount_usd` (optional): Minimum loss amount

**Returns**: List of exploits with transaction hashes, amounts, timestamps

**Example**:
```
Search for Uniswap exploits on Ethereum with minimum $1M loss
```

### 3. assess_defi_protocol_risk

Analyze security risk of a DeFi protocol.

**Parameters**:
- `protocol`: Protocol name
- `chain` (optional): Blockchain network

**Returns**: Risk score (0-100), exploit history, security analysis

**Example**:
```
Assess risk for Curve Finance on Ethereum
```

### 4. monitor_wallet

Check if wallet has exposure to compromised protocols.

**Parameters**:
- `wallet_address`: Wallet address to check
- `chain` (optional): Blockchain network

**Returns**: Exposed protocols, risk level, recommended actions

**Example**:
```
Monitor wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
```

### 5. file_dispute

Submit quality dispute for API response with x402Resolve integration.

**Parameters**:
- `transaction_id`: Solana transaction ID
- `original_query`: Expected data query
- `data_received`: Actual API response
- `issue_type`: Quality issue (incomplete/inaccurate/outdated)
- `expected_criteria`: Quality requirements

**Returns**: Dispute ID, quality score, refund percentage

**Example**:
```
File dispute for transaction tx_abc123 due to incomplete data
```

## Subscription Tiers

### Free Tier
- 10 requests/hour
- 100 requests/day
- Basic exploit search
- No dispute filing

### Personal ($49/month)
- 100 requests/hour
- 10,000 requests/day
- All tools enabled
- Automated dispute filing
- Email support

### Team ($299/month)
- 500 requests/hour
- 100,000 requests/day
- Priority API access
- Dedicated support channel
- Custom integrations

### Enterprise (Custom)
- Unlimited requests
- SLA guarantees
- On-premise deployment
- Custom tools
- 24/7 support

## Rate Limiting

Enforced per subscription tier:

```python
RATE_LIMITS = {
    "free": {"per_hour": 10, "per_day": 100},
    "personal": {"per_hour": 100, "per_day": 10000},
    "team": {"per_hour": 500, "per_day": 100000},
    "enterprise": {"per_hour": None, "per_day": None}
}
```

## Authentication

JWT-based authentication for tool access (except health_check).

**Token Structure**:
```json
{
  "sub": "user_id",
  "tier": "personal",
  "exp": 1234567890
}
```

## Error Handling

All tools return structured errors:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {}
}
```

**Common Error Codes**:
- `auth_required`: Missing or invalid JWT token
- `rate_limit_exceeded`: Tier rate limit reached
- `invalid_params`: Invalid tool parameters
- `api_error`: KAMIYO API error
- `database_error`: Database connection issue

## Development

### Project Structure

```
packages/mcp-server/
├── server.py                 # Main MCP server
├── config.py                 # Configuration management
├── tools/
│   ├── exploits.py          # Exploit search tool
│   ├── risk.py              # Risk assessment tool
│   ├── monitoring.py        # Wallet monitoring tool
│   └── dispute.py           # Dispute filing tool
├── auth/
│   ├── jwt_handler.py       # JWT auth
│   └── subscription.py      # Subscription management
├── requirements.txt         # Dependencies
└── README.md               # This file
```

### Adding New Tools

1. Create tool implementation in `tools/`
2. Define parameters using Pydantic models
3. Implement tool logic with error handling
4. Register tool in `server.py`
5. Add tests
6. Update documentation

**Example**:
```python
from fastmcp import FastMCP

mcp = FastMCP("kamiyo-security")

@mcp.tool()
async def my_new_tool(param: str) -> dict:
    """Tool description"""
    # Implementation
    return {"result": "data"}
```

### Testing

```bash
# Run server locally
python server.py

# Test with MCP inspector
npx @modelcontextprotocol/inspector python server.py

# Integration tests
pytest tests/
```

## Security

### Best Practices

- Store JWT secrets in environment variables (never commit)
- Use HTTPS in production
- Rotate JWT secrets regularly
- Implement request logging for auditing
- Validate all user inputs
- Rate limit by IP for DoS protection

### Reporting Security Issues

Email: security@kamiyo.ai

Do not create public GitHub issues for security vulnerabilities.

## Deployment

### Production Checklist

- [ ] Set strong JWT secret (min 32 characters)
- [ ] Configure production database
- [ ] Enable HTTPS
- [ ] Set up monitoring/alerting
- [ ] Configure log aggregation
- [ ] Enable rate limiting
- [ ] Set up backup strategy
- [ ] Test failover scenarios

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "server.py"]
```

### Systemd Service

```ini
[Unit]
Description=KAMIYO MCP Server
After=network.target

[Service]
Type=simple
User=kamiyo
WorkingDirectory=/opt/kamiyo/mcp-server
EnvironmentFile=/opt/kamiyo/.env
ExecStart=/usr/bin/python3 /opt/kamiyo/mcp-server/server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Monitoring

### Health Check Endpoint

```bash
# Check server health
curl http://localhost:3000/health
```

### Metrics

Server exposes metrics for:
- Request count per tool
- Error rates
- Response times
- Active connections
- Rate limit hits

### Logging

Structured JSON logging with configurable levels:

```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "INFO",
  "tool": "search_crypto_exploits",
  "user_id": "user_123",
  "duration_ms": 245,
  "status": "success"
}
```

## Troubleshooting

### Server Won't Start

1. Check Python version (3.9+ required)
2. Verify all environment variables set
3. Test database connectivity
4. Check log files for errors

### Tools Not Appearing in Claude

1. Verify server running (`ps aux | grep server.py`)
2. Check Claude Desktop config path
3. Restart Claude Desktop completely
4. Review MCP server logs

### Rate Limit Issues

1. Check current tier: `health_check` tool shows tier info
2. Upgrade subscription if needed
3. Implement client-side caching
4. Review API usage patterns

## Performance

### Optimization Tips

- Enable response caching for frequently accessed data
- Use connection pooling for database
- Implement request batching where possible
- Monitor and optimize slow queries
- Set appropriate timeout values

### Benchmarks

Typical response times (P95):
- `health_check`: <50ms
- `search_crypto_exploits`: <200ms
- `assess_defi_protocol_risk`: <500ms
- `monitor_wallet`: <300ms
- `file_dispute`: <1000ms

## License

MIT

## Links

- KAMIYO Website: https://kamiyo.ai
- MCP Specification: https://modelcontextprotocol.io
- x402Resolve: https://github.com/x402kamiyo/x402resolve
- Support: hello@kamiyo.ai
