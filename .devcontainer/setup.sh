#!/bin/bash
set -e

echo "Setting up Solana development environment..."

# Update system packages
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    pkg-config \
    libudev-dev \
    llvm \
    libclang-dev \
    protobuf-compiler \
    libssl-dev

# Source cargo environment (works for both /usr/local/cargo and ~/.cargo)
if [ -f "$HOME/.cargo/env" ]; then
    source "$HOME/.cargo/env"
elif [ -f "/usr/local/cargo/env" ]; then
    source "/usr/local/cargo/env"
fi

# Ensure Rust 1.79.0 is installed
if ! rustc --version | grep -q "1.79.0"; then
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain 1.79.0
    source "$HOME/.cargo/env" 2>/dev/null || source "/usr/local/cargo/env"
fi

# Install Solana CLI (v1.18.26) with retry logic
echo "Installing Solana CLI v1.18.26..."
for i in {1..3}; do
    if sh -c "$(curl -sSfL https://release.solana.com/v1.18.26/install)"; then
        break
    else
        echo "Attempt $i failed, retrying in 5 seconds..."
        sleep 5
    fi
done

export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"

# Add to bashrc (avoid duplicates)
grep -qxF 'export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"' ~/.bashrc || \
    echo 'export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"' >> ~/.bashrc
grep -qxF 'export PATH="$HOME/.cargo/bin:$PATH"' ~/.bashrc || \
    echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
grep -qxF 'export PATH="$HOME/.avm/bin:$PATH"' ~/.bashrc || \
    echo 'export PATH="$HOME/.avm/bin:$PATH"' >> ~/.bashrc

# Install Anchor Version Manager
echo "Installing Anchor Version Manager..."
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force

# Add avm to PATH for this session
export PATH="$HOME/.cargo/bin:$PATH"

# Install Anchor CLI 0.29.0 (compatible with anchor-lang 0.29.0 in the project)
echo "Installing Anchor CLI 0.29.0..."
avm install 0.29.0
avm use 0.29.0

# Configure Solana for devnet
echo "Configuring Solana for devnet..."
solana config set --url devnet

# Generate keypair if it doesn't exist
if [ ! -f "$HOME/.config/solana/id.json" ]; then
    echo "Generating new Solana keypair..."
    solana-keygen new --no-bip39-passphrase
fi

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
cd /workspaces/x402resolve/packages/x402-escrow
yarn install || npm install

echo ""
echo "✓ Solana development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Fund your devnet wallet: solana airdrop 2"
echo "2. Build the program: cd packages/x402-escrow && anchor build"
echo "3. Deploy to devnet: anchor deploy --provider.cluster devnet"
echo ""
echo "Your wallet address:"
solana address
