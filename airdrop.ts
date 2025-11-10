import { Connection, PublicKey, LAMPORTS_PER_SOL } from '@solana/web3.js';

async function main() {
  const connection = new Connection('https://api.devnet.solana.com', 'confirmed');
  const pubkey = new PublicKey('EJaMMwwZpXdCyNMa5Kf1a95J1tmJyYtqDQPhuABgWf9h');

  console.log('Requesting airdrop of 1 SOL...');
  const signature = await connection.requestAirdrop(pubkey, 1 * LAMPORTS_PER_SOL);

  console.log('Airdrop requested. Signature:', signature);
  console.log('Waiting for confirmation...');

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  await connection.confirmTransaction({ signature, blockhash, lastValidBlockHeight });

  console.log('✅ Airdrop confirmed!');

  const balance = await connection.getBalance(pubkey);
  console.log('Balance:', balance / LAMPORTS_PER_SOL, 'SOL');
}

main().catch(console.error);
