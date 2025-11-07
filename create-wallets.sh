#!/bin/bash

# Create and fund Solana devnet wallets
# Usage: ./create-wallets.sh [count]
# Example: ./create-wallets.sh 10

WALLET_COUNT=${1:-10}
AIRDROP_AMOUNT=2
OUTPUT_DIR="wallets"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Creating $WALLET_COUNT wallets on Solana devnet"
echo "Output directory: $OUTPUT_DIR"
echo "Airdrop amount: $AIRDROP_AMOUNT SOL per wallet"
echo ""

SUCCESS_COUNT=0
FAIL_COUNT=0

# Track all addresses
> "$OUTPUT_DIR/addresses.txt"
> "$OUTPUT_DIR/summary.txt"

for i in $(seq 1 $WALLET_COUNT); do
    echo "[$i/$WALLET_COUNT] Creating wallet..."

    # Generate new keypair
    KEYPAIR_FILE="$OUTPUT_DIR/wallet-$i.json"
    solana-keygen new --no-bip39-passphrase --silent --outfile "$KEYPAIR_FILE" 2>&1

    if [ $? -ne 0 ]; then
        echo -e "${RED}  ✗ Failed to generate keypair${NC}"
        ((FAIL_COUNT++))
        continue
    fi

    # Get public key
    PUBKEY=$(solana-keygen pubkey "$KEYPAIR_FILE")
    echo "  Public Key: $PUBKEY"
    echo "$PUBKEY" >> "$OUTPUT_DIR/addresses.txt"

    # Request airdrop
    echo "  Requesting airdrop..."
    AIRDROP_OUTPUT=$(solana airdrop $AIRDROP_AMOUNT "$PUBKEY" --url devnet 2>&1)

    if echo "$AIRDROP_OUTPUT" | grep -q "Signature"; then
        # Wait for confirmation
        sleep 2

        # Check balance
        BALANCE=$(solana balance "$PUBKEY" --url devnet 2>/dev/null | awk '{print $1}')
        echo -e "  Balance: $BALANCE SOL"
        echo -e "${GREEN}  ✓ Wallet created and funded${NC}"
        echo "✓ wallet-$i: $PUBKEY ($BALANCE SOL)" >> "$OUTPUT_DIR/summary.txt"
        ((SUCCESS_COUNT++))
    else
        echo -e "${RED}  ✗ Airdrop failed${NC}"
        echo "  Error: $AIRDROP_OUTPUT"
        echo "✗ wallet-$i: $PUBKEY (airdrop failed)" >> "$OUTPUT_DIR/summary.txt"
        ((FAIL_COUNT++))
    fi

    # Delay between requests to avoid rate limiting
    if [ $i -lt $WALLET_COUNT ]; then
        echo ""
        echo "Waiting 5s before creating next wallet..."
        sleep 5
        echo ""
    fi
done

# Summary
echo ""
echo "============================================================"
echo "SUMMARY"
echo "============================================================"
echo ""
echo "Total wallets: $WALLET_COUNT"
echo -e "${GREEN}Successfully funded: $SUCCESS_COUNT${NC}"
echo -e "${RED}Failed: $FAIL_COUNT${NC}"
echo ""
echo "Keypairs saved to: $OUTPUT_DIR/wallet-*.json"
echo "Addresses saved to: $OUTPUT_DIR/addresses.txt"
echo "Summary saved to: $OUTPUT_DIR/summary.txt"
echo ""
echo "============================================================"
echo "DONE"
echo "============================================================"
