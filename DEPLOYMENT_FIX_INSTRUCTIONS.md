# Deployment Instructions for Sonnet 4.5 Agent

## Current Status
The program has been deployed to address `E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n` on Solana devnet.

All source code and configuration files have been updated to use this program ID.

## Solution
Build and deploy the program with the correct program ID.

## Prerequisites
- Linux environment (GitHub Codespace, Ubuntu, or Docker)
- Solana CLI tools
- Anchor CLI 0.31.1
- Deployer wallet keypair (program keypair is included in repository)

## Step-by-Step Instructions

### 1. Set up environment (if not already done)

```bash
# Install Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/v1.18.22/install)"
export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"

# Install Rust (if needed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# Install Anchor
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force
avm install 0.31.1
avm use 0.31.1
```

### 2. Configure Solana CLI

```bash
# Set to devnet
solana config set --url devnet

# Set deployer keypair (YOU MUST PROVIDE THE ACTUAL KEYPAIR)
# The keypair should be saved to ~/.config/solana/id.json
mkdir -p ~/.config/solana
# Copy your deployer keypair to ~/.config/solana/id.json
solana config set --keypair ~/.config/solana/id.json

# Verify wallet has SOL for deployment
solana balance
# If balance is low, airdrop some SOL:
# solana airdrop 2
```

### 3. Clone and navigate to repository

```bash
git clone https://github.com/kamiyo-ai/x402resolve.git
cd x402resolve/packages/x402-escrow
```

### 4. Verify the program ID is correct

```bash
# Should output: declare_id!("E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n");
grep "declare_id" programs/x402-escrow/src/lib.rs

# Should output: x402_escrow = "E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n"
grep "x402_escrow" Anchor.toml
```

### 5. Build the program

```bash
anchor build
```

Expected output:
- Binary will be at: `target/deploy/x402_escrow.so`
- IDL will be at: `target/idl/x402_escrow.json`

### 6. Deploy the program

```bash
anchor deploy --provider.cluster devnet
```

### 7. Verify deployment

```bash
# Check program details
solana program show E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n

# View on Solana Explorer
echo "https://explorer.solana.com/address/E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n?cluster=devnet"
```

### 8. Test the deployment

Try running the demo at https://x402resolve.kamiyo.ai/ - the error 4100 should be resolved.

## Troubleshooting

### "Insufficient funds"
```bash
solana airdrop 2
```

### "Invalid upgrade authority"
The wallet you're using must be the upgrade authority. Check with:
```bash
solana program show E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n
```

### Build fails
Make sure you're using:
- Anchor 0.31.1
- Rust stable toolchain
- Solana CLI 1.18.x

### Program ID mismatch
1. Ensure `packages/x402-escrow/programs/x402-escrow/src/lib.rs` contains:
   ```rust
   declare_id!("E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n");
   ```
2. Clean build and try again:
   ```bash
   anchor clean
   anchor build
   ```

## Expected Result

After successful deployment:
- Demo site should work without errors
- Transaction logs should show: `Program E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n invoke [1]` followed by successful execution

## Files Modified (Already Done)

These files have already been updated with the correct program ID:
- ✅ `packages/x402-escrow/programs/x402-escrow/src/lib.rs`
- ✅ `packages/x402-escrow/Anchor.toml`
- ✅ `packages/x402-sdk/types/x402_escrow.json`
- ✅ `README.md`
- ✅ `tests/production-e2e-test.js`
- ✅ `tests/test-production-oracle.ts`
- ✅ `tests/test-production-oracle.js`
- ✅ `docs/oracle-transactions.js`

The program is ready to be built and deployed.

## Alternative: Using GitHub Codespaces

If you have access to GitHub Codespaces:

1. Go to https://github.com/kamiyo-ai/x402resolve
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Wait for environment to load
4. Follow steps 2-7 above

## Notes for Agent

- **DO NOT** change the program ID - it has been correctly set to `E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n`
- The program keypair is included in the repository at `packages/x402-escrow/target/deploy/x402_escrow-keypair.json`
- The deployer wallet keypair must be provided by the user for funding the deployment
