# Deployment Fix Instructions for Sonnet 4.5 Agent

## Problem
The deployed Solana program at address `ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY` has a **DeclaredProgramIdMismatch** error (error 4100).

The on-chain program binary was compiled with `declare_id!("AubiRw1L6seTBKEZfkK2gE1TRY9kpV7J3VnEfZpL4Xta")` but deployed to address `ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY`.

The source code has been updated to use the correct program ID, but the on-chain program needs to be rebuilt and upgraded.

## Solution
Rebuild and upgrade the program with the correct program ID.

## Prerequisites
- Linux environment (GitHub Codespace, Ubuntu, or Docker)
- Solana CLI tools
- Anchor CLI 0.31.1
- Deployer wallet keypair with upgrade authority for program `ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY`

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
# Should output: declare_id!("ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY");
grep "declare_id" programs/x402-escrow/src/lib.rs

# Should output: x402_escrow = "ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY"
grep "x402_escrow" Anchor.toml
```

### 5. Build the program

```bash
anchor build
```

Expected output:
- Binary will be at: `target/deploy/x402_escrow.so`
- IDL will be at: `target/idl/x402_escrow.json`

### 6. Verify the upgrade authority

```bash
solana program show ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY
```

Look for "Upgrade Authority" - it should match your deployer wallet address.

### 7. Upgrade the program

```bash
anchor upgrade target/deploy/x402_escrow.so --program-id ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY
```

### 8. Verify deployment

```bash
# Check program details
solana program show ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY

# View on Solana Explorer
echo "https://explorer.solana.com/address/ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY?cluster=devnet"
```

### 9. Test the deployment

Try running the demo at https://x402resolve.kamiyo.ai/ - the error 4100 should be resolved.

## Troubleshooting

### "Insufficient funds"
```bash
solana airdrop 2
```

### "Invalid upgrade authority"
The wallet you're using must be the upgrade authority. Check with:
```bash
solana program show ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY
```

### Build fails
Make sure you're using:
- Anchor 0.31.1
- Rust stable toolchain
- Solana CLI 1.18.x

### Program ID mismatch persists
1. Ensure `packages/x402-escrow/programs/x402-escrow/src/lib.rs` contains:
   ```rust
   declare_id!("ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY");
   ```
2. Clean build and try again:
   ```bash
   anchor clean
   anchor build
   ```

## Expected Result

After successful upgrade:
- Demo site should work without error 4100
- Transaction logs should show: `Program ERjFnw8BMLo4aRx82itMogcPPrUzXh6Kd6pwWt6dgBbY invoke [1]` followed by successful execution
- No more "DeclaredProgramIdMismatch" errors

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

All that's needed is to rebuild and upgrade the on-chain program.

## Alternative: Using GitHub Codespaces

If you have access to GitHub Codespaces:

1. Go to https://github.com/kamiyo-ai/x402resolve
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Wait for environment to load
4. Follow steps 2-8 above

## Notes for Agent

- **DO NOT** change the program ID back to the old one
- **DO NOT** deploy to a new address - use `anchor upgrade` to update the existing program
- The deployer wallet keypair must be provided by the user
- This is a one-time fix - once upgraded, the issue will be resolved permanently
