/**
 * Create and fund multiple Solana devnet wallets
 *
 * Usage: node create-wallets.js [count]
 * Example: node create-wallets.js 10
 */

const solanaWeb3 = require('@solana/web3.js');
const { Keypair, Connection, LAMPORTS_PER_SOL } = solanaWeb3;
const fs = require('fs');
const path = require('path');

// Configuration
const WALLET_COUNT = parseInt(process.argv[2]) || 10;
const AIRDROP_AMOUNT = 2; // SOL per wallet
const DEVNET_RPC = 'https://api.devnet.solana.com';
const OUTPUT_DIR = path.join(__dirname, 'wallets');

// Create output directory
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

const connection = new Connection(DEVNET_RPC, 'confirmed');

/**
 * Sleep helper
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Request airdrop with retry logic
 */
async function requestAirdropWithRetry(publicKey, amount, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            console.log(`  Requesting airdrop (attempt ${i + 1}/${maxRetries})...`);
            const signature = await connection.requestAirdrop(
                publicKey,
                amount * LAMPORTS_PER_SOL
            );

            console.log(`  Confirming airdrop...`);
            await connection.confirmTransaction(signature, 'confirmed');

            // Verify balance
            const balance = await connection.getBalance(publicKey);
            console.log(`  Balance: ${balance / LAMPORTS_PER_SOL} SOL`);

            return signature;
        } catch (error) {
            console.log(`  Airdrop failed: ${error.message}`);
            if (i < maxRetries - 1) {
                console.log(`  Waiting 10s before retry...`);
                await sleep(10000);
            } else {
                throw error;
            }
        }
    }
}

/**
 * Create and fund a single wallet
 */
async function createAndFundWallet(index) {
    console.log(`\n[${index + 1}/${WALLET_COUNT}] Creating wallet...`);

    // Generate keypair
    const keypair = Keypair.generate();
    const publicKey = keypair.publicKey.toString();

    console.log(`  Public Key: ${publicKey}`);

    // Save keypair to file
    const filename = `wallet-${index + 1}.json`;
    const filepath = path.join(OUTPUT_DIR, filename);
    fs.writeFileSync(
        filepath,
        JSON.stringify(Array.from(keypair.secretKey))
    );
    console.log(`  Saved to: ${filename}`);

    // Request airdrop
    try {
        await requestAirdropWithRetry(keypair.publicKey, AIRDROP_AMOUNT);
        console.log(`  ✓ Wallet created and funded`);

        return {
            index: index + 1,
            publicKey: publicKey,
            filepath: filename,
            balance: AIRDROP_AMOUNT,
            success: true
        };
    } catch (error) {
        console.log(`  ✗ Failed to fund wallet: ${error.message}`);
        return {
            index: index + 1,
            publicKey: publicKey,
            filepath: filename,
            balance: 0,
            success: false,
            error: error.message
        };
    }
}

/**
 * Main execution
 */
async function main() {
    console.log(`Creating ${WALLET_COUNT} wallets on Solana devnet`);
    console.log(`Output directory: ${OUTPUT_DIR}`);
    console.log(`Airdrop amount: ${AIRDROP_AMOUNT} SOL per wallet\n`);

    const results = [];

    // Create wallets sequentially to avoid rate limiting
    for (let i = 0; i < WALLET_COUNT; i++) {
        const result = await createAndFundWallet(i);
        results.push(result);

        // Add delay between wallet creations to avoid rate limiting
        if (i < WALLET_COUNT - 1) {
            console.log(`\nWaiting 5s before creating next wallet...`);
            await sleep(5000);
        }
    }

    // Generate summary
    console.log('\n' + '='.repeat(60));
    console.log('SUMMARY');
    console.log('='.repeat(60));

    const successful = results.filter(r => r.success);
    const failed = results.filter(r => !r.success);

    console.log(`\nTotal wallets: ${WALLET_COUNT}`);
    console.log(`Successfully funded: ${successful.length}`);
    console.log(`Failed: ${failed.length}`);

    if (successful.length > 0) {
        console.log('\n✓ Successfully funded wallets:');
        successful.forEach(w => {
            console.log(`  ${w.index}. ${w.publicKey} (${w.balance} SOL)`);
        });
    }

    if (failed.length > 0) {
        console.log('\n✗ Failed wallets:');
        failed.forEach(w => {
            console.log(`  ${w.index}. ${w.publicKey} - ${w.error}`);
        });
    }

    // Save summary to file
    const summaryFile = path.join(OUTPUT_DIR, 'summary.json');
    fs.writeFileSync(summaryFile, JSON.stringify(results, null, 2));
    console.log(`\nSummary saved to: wallets/summary.json`);

    // Generate addresses list
    const addressesFile = path.join(OUTPUT_DIR, 'addresses.txt');
    fs.writeFileSync(
        addressesFile,
        results.map(w => w.publicKey).join('\n')
    );
    console.log(`Addresses saved to: wallets/addresses.txt`);

    console.log('\n' + '='.repeat(60));
    console.log('DONE');
    console.log('='.repeat(60));
}

// Run
main().catch(error => {
    console.error('\nFatal error:', error);
    process.exit(1);
});
