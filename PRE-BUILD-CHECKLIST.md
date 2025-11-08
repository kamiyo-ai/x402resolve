# Pre-Build Checklist for Codespace Agent

**CRITICAL**: Verify these before running `anchor build` and `anchor deploy`

## 1. Program ID Consistency

All files MUST have program ID: `E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n`

### Check these files:

```bash
# 1. Source code (lib.rs)
grep "declare_id" packages/x402-escrow/programs/x402-escrow/src/lib.rs
# Should show: declare_id!("E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n");

# 2. Anchor configuration
grep "x402_escrow" packages/x402-escrow/Anchor.toml
# Should show: x402_escrow = "E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n"

# 3. Program keypair matches
solana-keygen pubkey packages/x402-escrow/target/deploy/x402_escrow-keypair.json
# Should output: E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n
```

## 2. Deployer Wallet

```bash
# Check deployer wallet has sufficient SOL
solana balance
# Need at least 2 SOL on devnet

# Verify connected to devnet
solana config get
# Should show: RPC URL: https://api.devnet.solana.com
```

## 3. Demo Site Configuration

The demo at https://x402resolve.kamiyo.ai/ MUST use the same program ID.

**After deployment**, update the demo's configuration to point to:
- Program ID: `E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n`
- Cluster: `devnet`

## 4. Common Mistakes to Avoid

❌ **DO NOT** change the program ID in any file
❌ **DO NOT** generate a new program keypair
❌ **DO NOT** deploy to mainnet (use devnet only)
❌ **DO NOT** deploy if any program ID mismatches exist

✅ **DO** verify all program IDs match before building
✅ **DO** ensure deployer wallet has enough SOL
✅ **DO** deploy to devnet cluster
✅ **DO** update demo site after deployment

## 5. Build & Deploy Commands

```bash
cd packages/x402-escrow

# Clean previous builds
anchor clean

# Build the program
anchor build

# Verify the build
ls -lh target/deploy/x402_escrow.so

# Deploy to devnet
anchor deploy --provider.cluster devnet

# Verify deployment
solana program show E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n --url devnet
```

## 6. Post-Deployment Verification

```bash
# Check program is deployed and executable
solana program show E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n --url devnet

# View on explorer
echo "https://explorer.solana.com/address/E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n?cluster=devnet"

# Test the demo site
echo "Test at: https://x402resolve.kamiyo.ai/"
```

## Quick Verification Script

Run this to verify everything is correct:

```bash
#!/bin/bash
EXPECTED_ID="E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n"

echo "Checking program ID consistency..."

# Check lib.rs
if grep -q "declare_id!(\"$EXPECTED_ID\")" packages/x402-escrow/programs/x402-escrow/src/lib.rs; then
  echo "✓ lib.rs correct"
else
  echo "✗ lib.rs WRONG - DO NOT BUILD"
  exit 1
fi

# Check Anchor.toml
if grep -q "x402_escrow = \"$EXPECTED_ID\"" packages/x402-escrow/Anchor.toml; then
  echo "✓ Anchor.toml correct"
else
  echo "✗ Anchor.toml WRONG - DO NOT BUILD"
  exit 1
fi

# Check keypair
KEYPAIR_ADDR=$(solana-keygen pubkey packages/x402-escrow/target/deploy/x402_escrow-keypair.json)
if [ "$KEYPAIR_ADDR" = "$EXPECTED_ID" ]; then
  echo "✓ Keypair correct"
else
  echo "✗ Keypair WRONG - DO NOT BUILD"
  exit 1
fi

echo ""
echo "✓✓✓ ALL CHECKS PASSED - SAFE TO BUILD ✓✓✓"
```
