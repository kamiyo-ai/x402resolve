# Troubleshooting

## Installation Issues

### `npm install` fails

Symptoms: `ERESOLVE unable to resolve dependency tree`

Solutions:
```bash
# Verify Node 18+
node --version
nvm install 18 && nvm use 18

# Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Use legacy peer deps if needed
npm install --legacy-peer-deps
```

### Anchor build fails

Symptoms: `package solana-program v1.14.0 cannot be built`

Solutions:
```bash
# Verify Anchor 0.28.0+
anchor --version

# Install Solana CLI 1.14.0+
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"
solana --version

# Configure devnet
solana config set --url devnet
```

### Issue: Python dependencies fail

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement sentence-transformers
```

**Solutions:**

1. **Use Python 3.9+:**
```bash
python --version  # Should be 3.9 or higher
```

2. **Create virtual environment:**
```bash
cd packages/x402-verifier
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Install specific versions:**
```bash
pip install sentence-transformers==2.2.2
pip install fastapi==0.104.1
```

---

## Wallet & Connection Issues

### Issue: Phantom wallet connection fails

**Symptoms:**
```
Wallet connection failed: Unexpected error
```

**Solutions:**

1. **Check wallet is installed:**
   - Visit https://phantom.app/
   - Install browser extension
   - Create or import wallet

2. **Refresh the page:**
   - Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
   - Clear browser cache
   - Try incognito/private mode

3. **Check Phantom permissions:**
   - Open Phantom settings
   - Go to "Trusted Apps"
   - Make sure site is not blocked

4. **Update Phantom:**
   - Check for extension updates
   - Restart browser after update

### Issue: Insufficient funds error

**Symptoms:**
```
Error: failed to send transaction: insufficient funds for rent
```

**Solutions:**

1. **Get devnet SOL:**
```bash
solana airdrop 2 YOUR_WALLET_ADDRESS --url devnet
```

2. **Use faucet:**
   - Visit https://faucet.solana.com/
   - Enter your wallet address
   - Request devnet SOL

3. **Check balance:**
```bash
solana balance YOUR_WALLET_ADDRESS --url devnet
```

### Issue: RPC connection timeout

**Symptoms:**
```
FetchError: request to https://api.devnet.solana.com failed
```

**Solutions:**

1. **Try different RPC:**
```typescript
const connection = new Connection('https://api.devnet.solana.com');
// OR
const connection = new Connection('https://rpc.ankr.com/solana_devnet');
```

2. **Increase timeout:**
```typescript
const connection = new Connection(rpcUrl, {
  commitment: 'confirmed',
  confirmTransactionInitialTimeout: 60000
});
```

3. **Check network status:**
   - Visit https://status.solana.com/
   - Verify devnet is operational

---

## Payment & Escrow Issues

### Issue: Escrow creation fails

**Symptoms:**
```
Error: Escrow account already exists
```

**Solutions:**

1. **Use unique transaction ID:**
```typescript
const transactionId = `tx_${Date.now()}_${Math.random()}`;
```

2. **Check escrow doesn't exist:**
```typescript
const [escrowPda] = await PublicKey.findProgramAddress(
  [Buffer.from('escrow'), Buffer.from(transactionId)],
  programId
);

const accountInfo = await connection.getAccountInfo(escrowPda);
if (accountInfo) {
  console.log('Escrow already exists');
}
```

3. **Use different wallet:**
   - Generate new wallet for testing
   - Or use different transaction ID

### Issue: Funds not released

**Symptoms:**
```
Error: dispute window not expired
```

**Solutions:**

1. **Wait for dispute window:**
   - Default: 24 hours (86400 seconds)
   - Check escrow data for exact time

2. **Check escrow status:**
```typescript
const escrowData = await escrowClient.getEscrowData(escrowPda);
console.log('Created at:', new Date(escrowData.createdAt * 1000));
console.log('Can release at:', new Date((escrowData.createdAt + 86400) * 1000));
```

3. **For testing, use shorter window:**
```typescript
await escrowClient.initializeEscrow({
  // ...
  disputeWindowSeconds: 60  // 1 minute for testing
});
```

### Issue: Refund calculation wrong

**Symptoms:**
```
Expected 35% refund, got 0%
```

**Solutions:**

1. **Check quality score:**
```typescript
// Refund only if score < 80
if (qualityScore >= 80) refund = 0%;
else if (qualityScore >= 50) refund = variable;
else refund = 100%;
```

2. **Verify oracle signature:**
   - Signature must be valid Ed25519
   - Must match verifier public key

3. **Check escrow amount:**
```bash
solana account ESCROW_PDA --url devnet
```

---

## Oracle & Verification Issues

### Issue: Verifier not starting

**Symptoms:**
```
ModuleNotFoundError: No module named 'sentence_transformers'
```

**Solutions:**

1. **Install dependencies:**
```bash
cd packages/x402-verifier
pip install -r requirements.txt
```

2. **Download models:**
```python
# First run downloads ~500MB model
python verifier.py
# Wait for "Model loaded successfully"
```

3. **Check port availability:**
```bash
lsof -i :8000  # Check if port 8000 is in use
# If in use, kill process or use different port
python verifier.py --port 8001
```

### Issue: Quality score always 0

**Symptoms:**
```json
{
  "quality_score": 0,
  "breakdown": {
    "semantic_similarity": 0.0,
    "completeness_score": 0.0,
    "freshness_score": 0.0
  }
}
```

**Solutions:**

1. **Check input data format:**
```python
# Data should be array of objects
data = [
  {"tx_hash": "0x123...", "amount_usd": 1000000},
  {"tx_hash": "0x456...", "amount_usd": 500000}
]
```

2. **Verify expected criteria:**
```python
expected_criteria = {
  "min_records": 5,
  "required_fields": ["tx_hash", "amount_usd"],
  "max_age_days": 30
}
```

3. **Check model loading:**
```bash
# Look for this in logs:
# "Model loaded successfully: sentence-transformers/all-MiniLM-L6-V2"
```

### Issue: Signature verification fails

**Symptoms:**
```
Error: Ed25519 signature verification failed
```

**Solutions:**

1. **Check verifier key exists:**
```bash
ls packages/x402-verifier/.verifier_key
```

2. **Regenerate key if missing:**
```bash
cd packages/x402-verifier
rm .verifier_key
python verifier.py  # Will generate new key
```

3. **Verify public key matches:**
```typescript
const verifierPubkey = new PublicKey('YOUR_VERIFIER_PUBKEY');
// Must match verifier's public key
```

---

## Example Code Issues

### Issue: Example not found

**Symptoms:**
```
bash: cd: examples/basic-payment: No such file or directory
```

**Solutions:**

1. **Clone repository:**
```bash
git clone https://github.com/x402kamiyo/x402resolve
cd x402resolve
```

2. **List available examples:**
```bash
ls examples/
# Should show: basic-payment, with-dispute, complete-flow, etc.
```

3. **Check you're in right directory:**
```bash
pwd  # Should end with /x402resolve
```

### Issue: TypeScript compilation errors

**Symptoms:**
```
error TS2307: Cannot find module '@kamiyo/x402-sdk'
```

**Solutions:**

1. **Build SDK first:**
```bash
cd packages/x402-sdk
npm install
npm run build
```

2. **Link SDK locally:**
```bash
cd packages/x402-sdk
npm link

cd ../../examples/basic-payment
npm link @kamiyo/x402-sdk
```

3. **Or install directly:**
```bash
cd examples/basic-payment
npm install ../../packages/x402-sdk
```

### Issue: Environment variables not loaded

**Symptoms:**
```
Error: VERIFIER_URL is not defined
```

**Solutions:**

1. **Create .env file:**
```bash
cd examples/with-dispute
cp .env.example .env
```

2. **Edit .env with your values:**
```env
VERIFIER_URL=http://localhost:8000
API_URL=https://api.kamiyo.ai
SOLANA_RPC_URL=https://api.devnet.solana.com
```

3. **Load .env in code:**
```typescript
import dotenv from 'dotenv';
dotenv.config();

const verifierUrl = process.env.VERIFIER_URL;
```

---

## MCP Server Issues

### Issue: Claude Desktop doesn't see tools

**Symptoms:**
- MCP server starts but Claude shows no tools
- "No tools available" message

**Solutions:**

1. **Check MCP config:**
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json (Mac)
// %APPDATA%\Claude\claude_desktop_config.json (Windows)
{
  "mcpServers": {
    "x402resolve": {
      "command": "python",
      "args": ["/absolute/path/to/packages/mcp-server/server.py"]
    }
  }
}
```

2. **Use absolute paths:**
```json
{
  "mcpServers": {
    "x402resolve": {
      "command": "/usr/local/bin/python3",
      "args": ["/Users/you/x402resolve/packages/mcp-server/server.py"]
    }
  }
}
```

3. **Restart Claude Desktop:**
   - Completely quit Claude Desktop
   - Restart application
   - Check server logs

4. **Check server logs:**
```bash
# Mac
tail -f ~/Library/Logs/Claude/mcp-server-x402resolve.log

# Windows
type %APPDATA%\Claude\Logs\mcp-server-x402resolve.log
```

### Issue: MCP tools fail with errors

**Symptoms:**
```
Error: Connection refused to http://localhost:8000
```

**Solutions:**

1. **Start verifier oracle:**
```bash
cd packages/x402-verifier
python verifier.py
```

2. **Check verifier is running:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

3. **Update MCP server config:**
```python
# In server.py
VERIFIER_URL = os.getenv('VERIFIER_URL', 'http://localhost:8000')
```

---

## General Debugging

### Enable Debug Logging

**SDK:**
```typescript
import { KamiyoClient } from '@kamiyo/x402-sdk';

const client = new KamiyoClient({
  apiUrl: 'https://api.kamiyo.ai',
  debug: true  // Enables console logging
});
```

**Verifier:**
```bash
python verifier.py --log-level DEBUG
```

**Solana:**
```bash
export RUST_LOG=debug
anchor test
```

### Check Transaction on Explorer

```typescript
console.log(`View transaction: https://explorer.solana.com/tx/${txSignature}?cluster=devnet`);
```

### Inspect Account Data

```bash
solana account ACCOUNT_ADDRESS --url devnet --output json
```

### Test Individual Components

**1. Test SDK:**
```bash
cd packages/x402-sdk
npm test
```

**2. Test Verifier:**
```bash
cd packages/x402-verifier
pytest test_verifier.py -v
```

**3. Test Smart Contract:**
```bash
cd packages/x402-escrow
anchor test
```

---

## Getting Help

If you're still stuck:

1. **Check existing issues:**
   - https://github.com/x402kamiyo/x402resolve/issues

2. **Create new issue:**
   - Include error messages
   - Include your environment (OS, Node version, etc.)
   - Include steps to reproduce

3. **Contact support:**
   - Email: support@kamiyo.ai
   - Include transaction IDs and account addresses

---

## Quick Diagnostic Commands

Run these to diagnose issues:

```bash
# Check all versions
node --version
npm --version
python --version
anchor --version
solana --version

# Check Solana connection
solana config get
solana balance --url devnet

# Check if services are running
curl http://localhost:8000/health  # Verifier
lsof -i :8000  # Check port

# Verify project structure
ls -la packages/
ls -la examples/

# Run all tests
cd packages/x402-sdk && npm test
cd ../x402-verifier && pytest
cd ../x402-escrow && anchor test
```

---

## Common Fixes Checklist

Before creating an issue, try these:

- [ ] Run `npm install` in all package directories
- [ ] Rebuild SDK: `cd packages/x402-sdk && npm run build`
- [ ] Get fresh devnet SOL: `solana airdrop 2`
- [ ] Restart verifier: `python packages/x402-verifier/verifier.py`
- [ ] Clear browser cache and retry
- [ ] Check you're on devnet: `solana config get`
- [ ] Verify all services are running (verifier, MCP server)
- [ ] Use absolute paths in config files
- [ ] Restart Claude Desktop (for MCP issues)
- [ ] Check firewall isn't blocking ports 8000, 8080
