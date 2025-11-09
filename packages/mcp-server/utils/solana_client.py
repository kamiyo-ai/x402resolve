"""
Solana Client for x402Resolve Program Integration

Handles:
- Escrow creation (initialize_escrow instruction)
- Escrow status checks
- Dispute filing (mark_disputed instruction)
- Reputation queries
- Payment verification
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import base58

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import transfer, TransferParams
from solders.pubkey import Pubkey as SoldersPubkey
from solders.system_program import ID as SYS_PROGRAM_ID

logger = logging.getLogger(__name__)


class X402ResolveClient:
    """Client for interacting with x402Resolve Solana program"""

    def __init__(
        self,
        rpc_url: Optional[str] = None,
        program_id: Optional[str] = None,
        agent_keypair: Optional[Keypair] = None
    ):
        self.rpc_url = rpc_url or os.getenv(
            "SOLANA_RPC_URL",
            "https://api.devnet.solana.com"
        )
        self.program_id = PublicKey(
            program_id or os.getenv(
                "X402_PROGRAM_ID",
                "E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n"
            )
        )
        self.client = AsyncClient(self.rpc_url, commitment=Confirmed)
        self.agent_keypair = agent_keypair or self._load_agent_keypair()

    def _load_agent_keypair(self) -> Optional[Keypair]:
        """Load agent wallet from environment"""
        try:
            # Try to load from AGENT_PRIVATE_KEY env var
            private_key_b58 = os.getenv("AGENT_PRIVATE_KEY")
            if private_key_b58:
                private_key_bytes = base58.b58decode(private_key_b58)
                return Keypair.from_secret_key(private_key_bytes)

            # Try to load from AGENT_WALLET_PATH
            wallet_path = os.getenv("AGENT_WALLET_PATH")
            if wallet_path and os.path.exists(wallet_path):
                import json
                with open(wallet_path, 'r') as f:
                    keypair_data = json.load(f)
                    return Keypair.from_secret_key(bytes(keypair_data))

            logger.warning("No agent keypair found - read-only mode")
            return None

        except Exception as e:
            logger.error(f"Failed to load agent keypair: {e}")
            return None

    async def create_escrow(
        self,
        api_provider: str,
        amount_sol: float,
        api_endpoint: str,
        quality_threshold: int = 80,
        time_lock_hours: int = 24
    ) -> Dict[str, Any]:
        """
        Create escrow payment for HTTP 402 API call

        Args:
            api_provider: API provider wallet address
            amount_sol: Payment amount in SOL
            api_endpoint: API endpoint URL
            quality_threshold: Minimum quality score (0-100)
            time_lock_hours: Escrow expiry in hours

        Returns:
            {
                "escrow_address": str,
                "transaction_id": str,
                "payment_proof": str,
                "expires_at": str (ISO 8601)
            }
        """
        if not self.agent_keypair:
            raise ValueError("Agent keypair required to create escrow")

        try:
            # Generate transaction ID
            transaction_id = self._generate_transaction_id()

            # Derive PDA for escrow
            escrow_pda, bump = self._derive_escrow_pda(transaction_id)

            # TODO: Build actual Anchor instruction for initialize_escrow
            # For now, this is a placeholder that shows the structure

            logger.info(
                f"Creating escrow: {amount_sol} SOL to {api_provider} "
                f"for {api_endpoint} (threshold: {quality_threshold})"
            )

            # In production, you would:
            # 1. Build initialize_escrow instruction with Anchor
            # 2. Add instruction to transaction
            # 3. Sign and send transaction
            # 4. Wait for confirmation

            # Placeholder response
            expires_at = datetime.now() + timedelta(hours=time_lock_hours)

            return {
                "escrow_address": str(escrow_pda),
                "transaction_id": transaction_id,
                "payment_proof": str(escrow_pda),
                "expires_at": expires_at.isoformat(),
                "api_endpoint": api_endpoint,
                "amount_sol": amount_sol,
                "quality_threshold": quality_threshold,
                "status": "simulated"  # Remove in production
            }

        except Exception as e:
            logger.error(f"Failed to create escrow: {e}")
            raise

    async def check_escrow_status(
        self,
        escrow_address: str
    ) -> Dict[str, Any]:
        """
        Check status of an escrow payment

        Returns:
            {
                "status": "active" | "disputed" | "resolved" | "released",
                "agent": str,
                "api_provider": str,
                "amount_sol": float,
                "created_at": str,
                "expires_at": str,
                "quality_score": int (optional),
                "refund_percentage": int (optional)
            }
        """
        try:
            escrow_pubkey = PublicKey(escrow_address)

            # Fetch account data
            response = await self.client.get_account_info(escrow_pubkey)

            if not response.value:
                raise ValueError(f"Escrow account not found: {escrow_address}")

            # TODO: Deserialize Anchor account data
            # For now, return placeholder

            return {
                "status": "active",
                "agent": str(self.agent_keypair.public_key) if self.agent_keypair else "unknown",
                "api_provider": "placeholder",
                "amount_sol": 0.001,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
                "escrow_address": escrow_address
            }

        except Exception as e:
            logger.error(f"Failed to check escrow status: {e}")
            raise

    async def file_dispute(
        self,
        escrow_address: str,
        quality_score: int,
        evidence: Dict[str, Any],
        refund_percentage: int
    ) -> Dict[str, Any]:
        """
        File dispute for escrow due to poor quality data

        Returns:
            {
                "dispute_id": str,
                "status": "pending_oracle",
                "oracle_assessment_eta": str,
                "transaction_id": str
            }
        """
        if not self.agent_keypair:
            raise ValueError("Agent keypair required to file dispute")

        try:
            logger.info(
                f"Filing dispute for escrow {escrow_address}: "
                f"quality={quality_score}, refund={refund_percentage}%"
            )

            # TODO: Build mark_disputed instruction
            # In production, this would call the on-chain program

            dispute_id = self._generate_transaction_id()

            return {
                "dispute_id": dispute_id,
                "status": "pending_oracle",
                "oracle_assessment_eta": (datetime.now() + timedelta(hours=24)).isoformat(),
                "transaction_id": dispute_id,
                "escrow_address": escrow_address,
                "quality_score": quality_score,
                "refund_percentage": refund_percentage
            }

        except Exception as e:
            logger.error(f"Failed to file dispute: {e}")
            raise

    async def get_api_reputation(
        self,
        api_provider: str
    ) -> Dict[str, Any]:
        """
        Check on-chain reputation of an API provider

        Returns:
            {
                "reputation_score": int (0-1000),
                "total_transactions": int,
                "disputes_filed": int,
                "disputes_won": int,
                "disputes_lost": int,
                "average_quality_provided": float (0-100),
                "recommendation": "trusted" | "caution" | "avoid"
            }
        """
        try:
            provider_pubkey = PublicKey(api_provider)

            # Derive reputation PDA
            reputation_pda, _ = self._derive_reputation_pda(provider_pubkey)

            # Fetch reputation account
            response = await self.client.get_account_info(reputation_pda)

            if not response.value:
                # No reputation data yet (new provider)
                return {
                    "reputation_score": 0,
                    "total_transactions": 0,
                    "disputes_filed": 0,
                    "disputes_won": 0,
                    "disputes_lost": 0,
                    "average_quality_provided": 0,
                    "recommendation": "caution",
                    "note": "New provider - no reputation data"
                }

            # TODO: Deserialize reputation account
            # Placeholder data
            return {
                "reputation_score": 750,
                "total_transactions": 100,
                "disputes_filed": 5,
                "disputes_won": 3,
                "disputes_lost": 2,
                "average_quality_provided": 85.5,
                "recommendation": "trusted"
            }

        except Exception as e:
            logger.error(f"Failed to get reputation: {e}")
            raise

    async def verify_payment(
        self,
        transaction_hash: str,
        expected_amount: Optional[float] = None,
        expected_recipient: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Verify that a payment was received

        Returns:
            {
                "verified": bool,
                "amount_sol": float,
                "sender": str,
                "recipient": str,
                "timestamp": str,
                "confirmations": int
            }
        """
        try:
            # Get transaction details
            response = await self.client.get_transaction(transaction_hash)

            if not response.value:
                return {
                    "verified": False,
                    "error": "Transaction not found"
                }

            # TODO: Parse transaction and verify details
            # Placeholder verification
            return {
                "verified": True,
                "amount_sol": expected_amount or 0.001,
                "sender": "placeholder_sender",
                "recipient": expected_recipient or "placeholder_recipient",
                "timestamp": datetime.now().isoformat(),
                "confirmations": 32,
                "transaction_hash": transaction_hash
            }

        except Exception as e:
            logger.error(f"Failed to verify payment: {e}")
            raise

    def estimate_refund(
        self,
        amount_sol: float,
        quality_score: int
    ) -> Dict[str, Any]:
        """
        Estimate refund amount based on quality score

        Returns:
            {
                "refund_sol": float,
                "payment_sol": float,
                "refund_percentage": int,
                "rationale": str
            }
        """
        # Calculate refund percentage
        if quality_score >= 80:
            refund_pct = 0
            rationale = "Quality meets threshold - no refund"
        elif quality_score >= 50:
            refund_pct = int((80 - quality_score) / 30 * 100)
            rationale = f"Partial refund - quality score {quality_score}/100"
        else:
            refund_pct = 100
            rationale = f"Full refund - quality score {quality_score}/100 below threshold"

        refund_sol = amount_sol * (refund_pct / 100)
        payment_sol = amount_sol - refund_sol

        return {
            "refund_sol": round(refund_sol, 6),
            "payment_sol": round(payment_sol, 6),
            "refund_percentage": refund_pct,
            "rationale": rationale
        }

    def _derive_escrow_pda(self, transaction_id: str) -> tuple[PublicKey, int]:
        """Derive PDA for escrow account"""
        seeds = [b"escrow", transaction_id.encode()]
        return PublicKey.find_program_address(seeds, self.program_id)

    def _derive_reputation_pda(self, entity_pubkey: PublicKey) -> tuple[PublicKey, int]:
        """Derive PDA for reputation account"""
        seeds = [b"reputation", bytes(entity_pubkey)]
        return PublicKey.find_program_address(seeds, self.program_id)

    def _generate_transaction_id(self) -> str:
        """Generate unique transaction ID"""
        import uuid
        return str(uuid.uuid4())[:16]

    async def close(self):
        """Close the RPC client connection"""
        await self.client.close()


# Singleton instance
_solana_client = None


def get_solana_client() -> X402ResolveClient:
    """Get singleton Solana client instance"""
    global _solana_client
    if _solana_client is None:
        _solana_client = X402ResolveClient()
    return _solana_client
