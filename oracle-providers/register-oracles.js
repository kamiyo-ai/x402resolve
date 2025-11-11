/**
 * Register Independent Oracle Providers to Oracle Registry
 * Requires: Local validator running, admin wallet funded
 */

const anchor = require('@project-serum/anchor');
const { Connection, Keypair, PublicKey, SystemProgram } = require('@solana/web3.js');
const fs = require('fs');
const path = require('path');

// Configuration
const PROGRAM_ID = new PublicKey('4x8i1j1Xy9wTPCLELtXuBt6nMwCmfzF9BK47BG8MWWf7');
const RPC_URL = process.env.RPC_URL || 'http://localhost:8899';
const MIN_CONSENSUS = 2;  // Need at least 2 oracles to agree
const MAX_DEVIATION = 15; // Maximum 15% difference between scores

async function main() {
    console.log('🏛️  Oracle Provider Registration System\n');
    console.log('Network: ' + RPC_URL);
    console.log('Program ID: ' + PROGRAM_ID.toString());
    console.log('\n=====================================\n');

    // Connect to network
    const connection = new Connection(RPC_URL, 'confirmed');

    // Load admin wallet (you'll need to have this funded)
    let adminKeypair;
    try {
        const adminPath = process.env.ADMIN_KEYPAIR || path.join(require('os').homedir(), '.config/solana/id.json');
        const adminKeyData = JSON.parse(fs.readFileSync(adminPath, 'utf-8'));
        adminKeypair = Keypair.fromSecretKey(new Uint8Array(adminKeyData));
        console.log('✅ Admin Wallet: ' + adminKeypair.publicKey.toString());

        // Check balance
        const balance = await connection.getBalance(adminKeypair.publicKey);
        console.log('   Balance: ' + (balance / 1e9).toFixed(4) + ' SOL');

        if (balance < 0.1 * 1e9) {
            console.log('\n⚠️  Warning: Low balance. Need at least 0.1 SOL for registration');
            console.log('   Run: solana airdrop 1 ' + adminKeypair.publicKey.toString());
            return;
        }
    } catch (err) {
        console.log('❌ Could not load admin keypair');
        console.log('   Set ADMIN_KEYPAIR environment variable or ensure ~/.config/solana/id.json exists');
        console.log('   Error: ' + err.message);
        return;
    }

    // Derive oracle registry PDA
    const [registryPDA, registryBump] = await PublicKey.findProgramAddress(
        [Buffer.from('oracle-registry')],
        PROGRAM_ID
    );

    console.log('   Registry PDA: ' + registryPDA.toString());
    console.log('\n');

    // Check if registry already exists
    const registryAccount = await connection.getAccountInfo(registryPDA);
    let registryExists = registryAccount !== null;

    if (!registryExists) {
        console.log('📝 Step 1: Initialize Oracle Registry\n');
        console.log('   Min Consensus: ' + MIN_CONSENSUS);
        console.log('   Max Deviation: ' + MAX_DEVIATION + '%');

        // Build initialize instruction (you'll need the IDL here)
        // For now, showing the structure
        console.log('\n   ⚠️  Registry not found. Need to initialize first.');
        console.log('   Use demo-integration.html to initialize, or implement anchor program call here.\n');
    } else {
        console.log('✅ Oracle Registry already initialized\n');
    }

    // Load oracle providers
    const oraclesData = JSON.parse(
        fs.readFileSync(path.join(__dirname, 'oracle-registry.json'), 'utf-8')
    );

    console.log('📋 Step 2: Register Independent Oracle Providers\n');
    console.log('   Found ' + Object.keys(oraclesData).length + ' oracle providers\n');

    let registered = 0;
    for (const [id, oracle] of Object.entries(oraclesData)) {
        console.log('Oracle: ' + oracle.name);
        console.log('  ID: ' + id);
        console.log('  Public Key: ' + oracle.publicKey);
        console.log('  Methodology: ' + oracle.methodology);

        // For demo purposes, we'll show the structure
        // In practice, you'd call the add_oracle instruction here
        console.log('  Status: ⏳ Ready to register (implement anchor call)');
        console.log('');
        registered++;
    }

    console.log('=====================================\n');
    console.log('📊 Registration Summary:');
    console.log('   Total Providers: ' + registered);
    console.log('   Registry PDA: ' + registryPDA.toString());
    console.log('   Admin: ' + adminKeypair.publicKey.toString());
    console.log('\n✅ Oracle providers ready for registration!');
    console.log('\n💡 Next Steps:');
    console.log('   1. Use demo-integration.html to initialize registry');
    console.log('   2. Use demo to register each oracle provider');
    console.log('   3. Or implement full anchor integration in this script\n');
}

main().catch(err => {
    console.error('❌ Error:', err);
    process.exit(1);
});
