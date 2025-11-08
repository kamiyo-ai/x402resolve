#!/bin/bash

# Script to aggregate devnet SOL from multiple temporary wallets
# This works around rate limits by creating multiple wallets

set -e

export PATH="/home/vscode/.local/share/solana/install/active_release/bin:$PATH"

# Target wallet (our main wallet)
TARGET_WALLET="7xw1vBFvkUK3YMi8dULQHCbZgtNaRXAaSD8ttSvWdnCv"

# Number of temporary wallets to create
NUM_WALLETS=5

# Directory for temporary wallets
TEMP_DIR="/tmp/solana_temp_wallets"
mkdir -p "$TEMP_DIR"

echo "========================================="
echo "Devnet SOL Aggregator"
echo "========================================="
echo "Target wallet: $TARGET_WALLET"
echo "Creating $NUM_WALLETS temporary wallets..."
echo ""

solana config set --url devnet > /dev/null 2>&1

total_collected=0

for i in $(seq 1 $NUM_WALLETS); do
    echo "--- Wallet $i/$NUM_WALLETS ---"

    # Create temporary wallet
    TEMP_WALLET="$TEMP_DIR/temp_wallet_$i.json"
    solana-keygen new -o "$TEMP_WALLET" --no-bip39-passphrase --force > /dev/null 2>&1

    TEMP_ADDRESS=$(solana-keygen pubkey "$TEMP_WALLET")
    echo "Temporary wallet: $TEMP_ADDRESS"

    # Try to get airdrop
    echo "Requesting airdrop..."
    if solana airdrop 1 "$TEMP_ADDRESS" --keypair "$TEMP_WALLET" 2>&1 | grep -q "Error"; then
        echo "  ⚠️  Airdrop failed (rate limited), waiting 15 seconds..."
        sleep 15

        # Retry once
        if solana airdrop 1 "$TEMP_ADDRESS" --keypair "$TEMP_WALLET" 2>&1 | grep -q "Error"; then
            echo "  ❌ Airdrop failed again, skipping this wallet"
            continue
        fi
    fi

    echo "  ✓ Airdrop successful!"

    # Wait for confirmation
    sleep 3

    # Check balance
    BALANCE=$(solana balance "$TEMP_ADDRESS" --keypair "$TEMP_WALLET" | awk '{print $1}')
    echo "  Balance: $BALANCE SOL"

    if (( $(echo "$BALANCE > 0.01" | bc -l) )); then
        # Transfer to main wallet (keeping 0.01 SOL for fees)
        TRANSFER_AMOUNT=$(echo "$BALANCE - 0.01" | bc)
        echo "  Transferring $TRANSFER_AMOUNT SOL to target wallet..."

        if solana transfer "$TARGET_WALLET" "$TRANSFER_AMOUNT" --from "$TEMP_WALLET" --allow-unfunded-recipient --fee-payer "$TEMP_WALLET" 2>&1; then
            echo "  ✓ Transfer successful!"
            total_collected=$(echo "$total_collected + $TRANSFER_AMOUNT" | bc)
        else
            echo "  ❌ Transfer failed"
        fi
    else
        echo "  ⚠️  Insufficient balance to transfer"
    fi

    echo ""

    # Wait between wallets to avoid rate limiting
    if [ $i -lt $NUM_WALLETS ]; then
        echo "Waiting 20 seconds before next wallet..."
        sleep 20
    fi
done

echo "========================================="
echo "Summary"
echo "========================================="
echo "Total SOL collected: $total_collected"
echo ""
echo "Checking target wallet balance..."
FINAL_BALANCE=$(solana balance "$TARGET_WALLET")
echo "Target wallet balance: $FINAL_BALANCE"
echo ""
echo "========================================="

# Cleanup
echo "Cleaning up temporary wallets..."
rm -rf "$TEMP_DIR"
echo "Done!"
