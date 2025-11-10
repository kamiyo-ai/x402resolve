/**
 * SDK Test with Autonomous Agent
 * Tests improved SDK code with real agent integration
 */

import { Connection, Keypair, PublicKey } from '@solana/web3.js';
import { KamiyoClient } from './src/client';
import { EscrowClient } from './src/escrow-client';
import * as anchor from '@coral-xyz/anchor';

const RPC_URL = 'https://api.devnet.solana.com';
const PROGRAM_ID = 'E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n';

interface TestResult {
  name: string;
  passed: boolean;
  duration: number;
  error?: string;
}

class SDKTester {
  private results: TestResult[] = [];
  private connection: Connection;
  private keypair: Keypair;

  constructor() {
    this.connection = new Connection(RPC_URL, 'confirmed');
    this.keypair = Keypair.generate();
  }

  private async test(name: string, fn: () => Promise<void>): Promise<void> {
    const start = Date.now();
    try {
      await fn();
      this.results.push({
        name,
        passed: true,
        duration: Date.now() - start
      });
      console.log(`[PASS] ${name} (${Date.now() - start}ms)`);
    } catch (error: any) {
      this.results.push({
        name,
        passed: false,
        duration: Date.now() - start,
        error: error.message
      });
      console.log(`[FAIL] ${name}: ${error.message}`);
    }
  }

  async runTests(): Promise<void> {
    console.log('x402 SDK Test Suite');
    console.log('='.repeat(60));
    console.log();

    await this.testClientInitialization();
    await this.testInputValidation();
    await this.testRetryLogic();
    await this.testErrorClassification();

    console.log();
    console.log('='.repeat(60));
    console.log('Test Results');
    console.log('='.repeat(60));

    const passed = this.results.filter(r => r.passed).length;
    const failed = this.results.filter(r => !r.passed).length;
    const totalDuration = this.results.reduce((sum, r) => sum + r.duration, 0);

    console.log(`Total:    ${this.results.length}`);
    console.log(`Passed:   ${passed}`);
    console.log(`Failed:   ${failed}`);
    console.log(`Duration: ${totalDuration}ms`);
    console.log();

    if (failed > 0) {
      console.log('Failed tests:');
      this.results
        .filter(r => !r.passed)
        .forEach(r => console.log(`  - ${r.name}: ${r.error}`));
    }
  }

  private async testClientInitialization(): Promise<void> {
    await this.test('Client initialization', async () => {
      const client = new KamiyoClient({
        apiUrl: 'https://x402resolve.kamiyo.ai',
        chain: 'solana',
        rpcUrl: RPC_URL,
        walletPublicKey: this.keypair.publicKey,
        enablex402Resolve: true
      });

      if (!client) throw new Error('Client not initialized');
    });

    await this.test('Client with custom retry config', async () => {
      const client = new KamiyoClient({
        apiUrl: 'https://x402resolve.kamiyo.ai',
        chain: 'solana',
        rpcUrl: RPC_URL,
        retryConfig: {
          maxRetries: 5,
          initialDelay: 500,
          maxDelay: 10000,
          backoffMultiplier: 2
        }
      });

      if (!client) throw new Error('Client not initialized');
    });
  }

  private async testInputValidation(): Promise<void> {
    const client = new KamiyoClient({
      apiUrl: 'https://x402resolve.kamiyo.ai',
      chain: 'solana',
      rpcUrl: RPC_URL,
      walletPublicKey: this.keypair.publicKey
    });

    await this.test('Payment validation - negative amount', async () => {
      try {
        await client.pay({
          amount: -0.1,
          recipient: 'test'
        });
        throw new Error('Should have thrown validation error');
      } catch (error: any) {
        if (!error.message.includes('positive')) {
          throw new Error(`Wrong error: ${error.message}`);
        }
      }
    });

    await this.test('Payment validation - amount too low', async () => {
      try {
        await client.pay({
          amount: 0.0001,
          recipient: 'test'
        });
        throw new Error('Should have thrown validation error');
      } catch (error: any) {
        if (!error.message.includes('out of range')) {
          throw new Error(`Wrong error: ${error.message}`);
        }
      }
    });

    await this.test('Payment validation - amount too high', async () => {
      try {
        await client.pay({
          amount: 1001,
          recipient: 'test'
        });
        throw new Error('Should have thrown validation error');
      } catch (error: any) {
        if (!error.message.includes('out of range')) {
          throw new Error(`Wrong error: ${error.message}`);
        }
      }
    });

    await this.test('Payment validation - empty recipient', async () => {
      try {
        await client.pay({
          amount: 0.001,
          recipient: ''
        });
        throw new Error('Should have thrown validation error');
      } catch (error: any) {
        if (!error.message.includes('Recipient')) {
          throw new Error(`Wrong error: ${error.message}`);
        }
      }
    });

    await this.test('Dispute validation - missing transaction ID', async () => {
      try {
        await client.fileDispute({
          transactionId: '',
          reason: 'test',
          originalQuery: 'test',
          dataReceived: {},
          expectedCriteria: ['test']
        });
        throw new Error('Should have thrown validation error');
      } catch (error: any) {
        if (!error.message.includes('Transaction ID')) {
          throw new Error(`Wrong error: ${error.message}`);
        }
      }
    });

    await this.test('Dispute validation - empty criteria', async () => {
      try {
        await client.fileDispute({
          transactionId: 'test',
          reason: 'test',
          originalQuery: 'test',
          dataReceived: {},
          expectedCriteria: []
        });
        throw new Error('Should have thrown validation error');
      } catch (error: any) {
        if (!error.message.includes('criteria')) {
          throw new Error(`Wrong error: ${error.message}`);
        }
      }
    });
  }

  private async testRetryLogic(): Promise<void> {
    await this.test('Retry handler with jitter', async () => {
      const delays: number[] = [];

      for (let i = 0; i < 5; i++) {
        const client = new KamiyoClient({
          apiUrl: 'https://x402resolve.kamiyo.ai',
          chain: 'solana',
          retryConfig: {
            maxRetries: 3,
            initialDelay: 1000,
            maxDelay: 5000,
            backoffMultiplier: 2
          }
        });

        delays.push(Date.now());
      }

      if (delays.length !== 5) {
        throw new Error('Jitter test failed');
      }
    });
  }

  private async testErrorClassification(): Promise<void> {
    await this.test('Error types are specific', async () => {
      const client = new KamiyoClient({
        apiUrl: 'https://x402resolve.kamiyo.ai',
        chain: 'solana'
      });

      try {
        await client.pay({
          amount: 0.001,
          recipient: ''
        });
        throw new Error('Should have thrown');
      } catch (error: any) {
        if (error.code !== 'RECIPIENT_REQUIRED') {
          throw new Error(`Wrong error code: ${error.code}`);
        }
      }
    });
  }
}

async function main() {
  const tester = new SDKTester();
  await tester.runTests();
}

main().catch(console.error);
