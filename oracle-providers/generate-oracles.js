/**
 * Generate Independent Oracle Provider Keypairs
 * Creates 5 distinct oracle providers for multi-oracle consensus
 */

const { Keypair } = require('@solana/web3.js');
const fs = require('fs');
const path = require('path');

const ORACLE_PROVIDERS = [
    {
        name: 'Kamiyo AI',
        id: 'kamiyo',
        description: 'Proprietary AI-powered quality assessment',
        methodology: 'Claude/GPT-4 analysis with custom scoring model'
    },
    {
        name: 'QualityMetrics Inc',
        id: 'auditor',
        description: 'Independent auditor with manual expert review',
        methodology: 'Human experts + automated validation tools'
    },
    {
        name: 'DataVerify DAO',
        id: 'community',
        description: 'Community-driven verification via governance',
        methodology: 'Token-weighted community voting mechanism'
    },
    {
        name: 'DataQuality.ai',
        id: 'ai-service',
        description: 'Alternative AI service provider',
        methodology: 'Different AI model (GPT-4 vs Claude for diversity)'
    },
    {
        name: 'University Research Lab',
        id: 'academic',
        description: 'Academic institution with research-based metrics',
        methodology: 'Peer-reviewed quality assessment framework'
    }
];

console.log('🔐 Generating Independent Oracle Provider Keypairs...\n');

const oracles = {};

ORACLE_PROVIDERS.forEach((provider, index) => {
    const keypair = Keypair.generate();

    const oracleData = {
        ...provider,
        publicKey: keypair.publicKey.toBase58(),
        secretKey: Array.from(keypair.secretKey),
        weight: 1,
        active: true
    };

    oracles[provider.id] = oracleData;

    // Save individual keypair
    const filename = provider.id + '-keypair.json';
    fs.writeFileSync(
        path.join(__dirname, filename),
        JSON.stringify({
            publicKey: oracleData.publicKey,
            secretKey: oracleData.secretKey
        }, null, 2)
    );

    console.log('✅ Oracle ' + (index + 1) + ': ' + provider.name);
    console.log('   ID: ' + provider.id);
    console.log('   Public Key: ' + oracleData.publicKey);
    console.log('   Methodology: ' + provider.methodology);
    console.log('   Keypair saved: ' + filename + '\n');
});

// Save consolidated oracle registry
fs.writeFileSync(
    path.join(__dirname, 'oracle-registry.json'),
    JSON.stringify(oracles, null, 2)
);

// Create provider info file
const providerInfo = ORACLE_PROVIDERS.map((p, i) => ({
    index: i + 1,
    name: p.name,
    id: p.id,
    publicKey: oracles[p.id].publicKey,
    description: p.description,
    methodology: p.methodology,
    weight: 1,
    active: true
}));

fs.writeFileSync(
    path.join(__dirname, 'providers-info.json'),
    JSON.stringify(providerInfo, null, 2)
);

console.log('📋 Registry Summary:');
console.log('   Total Oracles: ' + ORACLE_PROVIDERS.length);
console.log('   Registry File: oracle-registry.json');
console.log('   Info File: providers-info.json');
console.log('\n✨ Oracle provider keypairs generated successfully!');
console.log('\n⚠️  IMPORTANT: Keep these keypairs secure!');
console.log('   - Never commit to git');
console.log('   - Each provider should receive only their own keypair');
console.log('   - Store in secure key management system for production\n');

// Create .gitignore for keypairs
fs.writeFileSync(
    path.join(__dirname, '.gitignore'),
    '*-keypair.json\noracle-registry.json\n'
);

console.log('🔒 Created .gitignore to protect keypairs');
