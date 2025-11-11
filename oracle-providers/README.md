# Independent Oracle Providers

**Status**: ✅ 5 Oracle Providers Generated and Ready for Registration

---

## Overview

This directory contains the keypairs and configuration for 5 independent oracle providers that will participate in multi-oracle consensus for x402-escrow dispute resolution.

## Oracle Providers

### 1. Kamiyo AI
- **ID**: `kamiyo`
- **Public Key**: `5dVGmgzMBdjcKoNoTwxKxbvgVwJsnMmyTx9ezxFxiW4f`
- **Methodology**: Claude/GPT-4 analysis with custom scoring model
- **Description**: Proprietary AI-powered quality assessment
- **Weight**: 1
- **Active**: true

### 2. QualityMetrics Inc
- **ID**: `auditor`
- **Public Key**: `4trZFvYAkBrwSmZNfh8hjU7zpEUu6JXuy51wjZNaeSFU`
- **Methodology**: Human experts + automated validation tools
- **Description**: Independent auditor with manual expert review
- **Weight**: 1
- **Active**: true

### 3. DataVerify DAO
- **ID**: `community`
- **Public Key**: `7cxSyvZoKoVXedehWTKfYB3dmymUnMViN8NsawMj6zMX`
- **Methodology**: Token-weighted community voting mechanism
- **Description**: Community-driven verification via governance
- **Weight**: 1
- **Active**: true

### 4. DataQuality.ai
- **ID**: `ai-service`
- **Public Key**: `AMyUMcqy7FGTgWPhz99pruNSAPq2jeeVKSYN3WVH8cWC`
- **Methodology**: Different AI model (GPT-4 vs Claude for diversity)
- **Description**: Alternative AI service provider
- **Weight**: 1
- **Active**: true

### 5. University Research Lab
- **ID**: `academic`
- **Public Key**: `FqTZhXzQmntbywsqVhZPKcuhwPzKbFpFvA5dLSwUFz13`
- **Methodology**: Peer-reviewed quality assessment framework
- **Description**: Academic institution with research-based metrics
- **Weight**: 1
- **Active**: true

---

## Files

### Generated Files
- `providers-info.json` - Public information about all providers
- `kamiyo-keypair.json` - Kamiyo AI keypair (gitignored)
- `auditor-keypair.json` - QualityMetrics Inc keypair (gitignored)
- `community-keypair.json` - DataVerify DAO keypair (gitignored)
- `ai-service-keypair.json` - DataQuality.ai keypair (gitignored)
- `academic-keypair.json` - University Research Lab keypair (gitignored)
- `oracle-registry.json` - Complete registry data (gitignored)

### Scripts
- `generate-oracles.js` - Generate new oracle provider keypairs
- `register-oracles.js` - Register oracles on-chain (requires local validator)

---

## Usage

### 1. Generate Oracles (Already Done)

```bash
node generate-oracles.js
```

This creates 5 independent oracle provider keypairs.

### 2. Register Oracles On-Chain

**Option A: Using demo-integration.html (Recommended)**

1. Open `demo-integration.html` in browser
2. Connect to local validator (http://localhost:8899)
3. Connect Phantom wallet
4. Click "Initialize Oracle Registry"
   - Min Consensus: 2
   - Max Deviation: 15
5. For each oracle in `providers-info.json`:
   - Enter oracle public key
   - Select Oracle Type: Ed25519
   - Weight: 1
   - Click "Add to Registry"

**Option B: Using register-oracles.js (Work in Progress)**

```bash
# Set admin keypair (must be funded)
export ADMIN_KEYPAIR=/path/to/admin-keypair.json

# Set RPC URL
export RPC_URL=http://localhost:8899

# Run registration
node register-oracles.js
```

---

## Oracle Provider Responsibilities

Each oracle provider must:

1. **Secure Key Management**
   - Store private keys in HSM or secure enclave
   - Never share private keys
   - Implement key rotation policies

2. **Quality Assessment Service**
   - Implement independent quality assessment methodology
   - Maintain consistency and accuracy
   - Document assessment criteria

3. **Signature Generation**
   ```javascript
   // When dispute is filed, each oracle independently:
   const message = `${transactionId}:${qualityScore}`;
   const messageBytes = new TextEncoder().encode(message);
   const signature = nacl.sign.detached(messageBytes, oracleSecretKey);
   ```

4. **Operational Excellence**
   - High uptime (>99%)
   - Low latency (<5 seconds per assessment)
   - Monitoring and alerting
   - DDoS protection

---

## Security

⚠️ **IMPORTANT**: Keypair files are gitignored and MUST NOT be committed to version control

**For Production**:
- Distribute keypairs to respective providers via secure channel
- Each provider stores only their own keypair
- Admin wallet maintains registry management rights
- Use multi-sig for admin wallet in production

---

## Multi-Oracle Consensus Example

When a dispute is filed:

1. **5 Independent Assessments**:
   - Kamiyo AI: 85 (AI analysis)
   - QualityMetrics: 82 (human expert review)
   - DataVerify DAO: 88 (community vote)
   - DataQuality.ai: 84 (different AI model)
   - University Lab: 86 (academic metrics)

2. **On-Chain Consensus**:
   - Scores: [85, 82, 88, 84, 86]
   - Sorted: [82, 84, 85, 86, 88]
   - **Median: 85**
   - Deviation: 6% (within 15% limit ✅)

3. **Result**:
   - Consensus Score: 85
   - Quality Tier: Excellent (80-100)
   - Refund to Agent: 0%
   - Payment to API: 100%

---

## Registry Configuration

**Current Settings**:
- Min Consensus: 2 (need at least 2 oracles to agree)
- Max Deviation: 15% (max difference between scores)
- Total Oracles: 5
- Equal Weight: All oracles have weight = 1

**Why These Settings**:
- **Min 2**: Ensures liveness even if some oracles are offline
- **Max 15%**: Allows for reasonable disagreement while detecting outliers
- **5 Oracles**: Balances decentralization with efficiency
- **Equal Weight**: Prevents single oracle dominance

---

## Testing Checklist

- [ ] Initialize oracle registry on local validator
- [ ] Register all 5 oracle providers
- [ ] Verify registry state (5 active oracles)
- [ ] Create test escrow
- [ ] Mark escrow as disputed
- [ ] Generate 5 independent quality assessments
- [ ] Submit multi-oracle resolution
- [ ] Verify median calculation
- [ ] Verify consensus reached
- [ ] Verify refund distribution

---

## Next Steps

1. **Local Testing**:
   - Start local validator: `solana-test-validator -r`
   - Deploy program
   - Register all oracles
   - Test multi-oracle resolution

2. **Devnet Deployment**:
   - Deploy program to devnet
   - Initialize registry
   - Register production oracles
   - Integration testing

3. **Production**:
   - Onboard real oracle providers
   - Distribute keypairs securely
   - Monitor oracle performance
   - Implement SLAs and incentives

---

**Generated**: 2025-11-11
**Status**: Ready for On-Chain Registration
**Network**: Local Validator / Devnet
