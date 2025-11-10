"""
x402Resolve MCP Tools

Tools for AI agents to interact with x402Resolve escrow system:
- create_escrow: Create payment escrow with quality guarantee
- call_api_with_escrow: Create escrow + call API + assess quality
- assess_data_quality: Evaluate API response quality
- file_dispute: Submit dispute for poor quality data
- check_escrow_status: Monitor escrow state
- get_api_reputation: Check provider trust score
- verify_payment: Confirm payment received
- estimate_refund: Calculate refund by quality score
"""

import logging
from typing import Dict, Any, Optional
import httpx

from utils.quality_assessment import get_quality_assessor
from utils.solana_client import get_solana_client

logger = logging.getLogger(__name__)

# Validation constants
MIN_AMOUNT_SOL = 0.001
MAX_AMOUNT_SOL = 1000.0
MIN_QUALITY_THRESHOLD = 0
MAX_QUALITY_THRESHOLD = 100
MIN_TIME_LOCK_HOURS = 1
MAX_TIME_LOCK_HOURS = 720
HTTP_TIMEOUT = 30.0


async def create_escrow(
    api_provider: str,
    amount_sol: float,
    api_endpoint: str,
    quality_threshold: int = 80,
    time_lock_hours: int = 24
) -> Dict[str, Any]:
    """
    Create escrow payment for HTTP 402 API call with quality guarantee

    Args:
        api_provider: API provider wallet address
        amount_sol: Payment amount in SOL
        api_endpoint: API endpoint URL
        quality_threshold: Minimum quality score (0-100)
        time_lock_hours: Escrow expiry (1-720 hours)

    Returns:
        {
            "escrow_address": str,
            "transaction_id": str,
            "payment_proof": str,
            "expires_at": str,
            "status": str
        }
    """
    try:
        logger.info(
            f"Creating escrow: {amount_sol} SOL for {api_endpoint} "
            f"(threshold: {quality_threshold})"
        )

        # Validate inputs
        if not isinstance(amount_sol, (int, float)) or amount_sol <= 0:
            raise ValueError(f"Amount must be a positive number, got: {amount_sol}")

        if not (MIN_AMOUNT_SOL <= amount_sol <= MAX_AMOUNT_SOL):
            raise ValueError(
                f"Amount must be between {MIN_AMOUNT_SOL} and {MAX_AMOUNT_SOL} SOL, got: {amount_sol}"
            )

        if not isinstance(quality_threshold, int):
            raise ValueError(f"Quality threshold must be an integer, got: {type(quality_threshold).__name__}")

        if not (MIN_QUALITY_THRESHOLD <= quality_threshold <= MAX_QUALITY_THRESHOLD):
            raise ValueError(
                f"Quality threshold must be between {MIN_QUALITY_THRESHOLD} and {MAX_QUALITY_THRESHOLD}, got: {quality_threshold}"
            )

        if not isinstance(time_lock_hours, int):
            raise ValueError(f"Time lock must be an integer, got: {type(time_lock_hours).__name__}")

        if not (MIN_TIME_LOCK_HOURS <= time_lock_hours <= MAX_TIME_LOCK_HOURS):
            raise ValueError(
                f"Time lock must be between {MIN_TIME_LOCK_HOURS} and {MAX_TIME_LOCK_HOURS} hours, got: {time_lock_hours}"
            )

        # Create escrow on-chain
        solana_client = get_solana_client()
        result = await solana_client.create_escrow(
            api_provider=api_provider,
            amount_sol=amount_sol,
            api_endpoint=api_endpoint,
            quality_threshold=quality_threshold,
            time_lock_hours=time_lock_hours
        )

        logger.info(f"Escrow created: {result['escrow_address']}")
        return result

    except Exception as e:
        logger.error(f"Error creating escrow: {e}")
        raise


async def call_api_with_escrow(
    api_provider: str,
    amount_sol: float,
    api_endpoint: str,
    request_body: Optional[Dict[str, Any]] = None,
    quality_criteria: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Simplified flow: create escrow + call API + auto-assess quality

    Args:
        api_provider: API provider wallet address
        amount_sol: Payment amount in SOL
        api_endpoint: API endpoint URL
        request_body: Optional POST body
        quality_criteria: Quality requirements
            - min_records: Minimum number of records
            - required_fields: List of required fields
            - max_age_days: Maximum data age in days
            - schema: Expected JSON schema

    Returns:
        {
            "escrow_address": str,
            "api_response": dict,
            "quality_score": float,
            "refund_percentage": int,
            "recommendation": str
        }
    """
    try:
        # Step 1: Create escrow
        escrow = await create_escrow(
            api_provider=api_provider,
            amount_sol=amount_sol,
            api_endpoint=api_endpoint,
            quality_threshold=quality_criteria.get("quality_threshold", 80) if quality_criteria else 80
        )

        # Step 2: Call API with payment proof
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            headers = {
                "X-Payment-Proof": escrow["payment_proof"],
                "Content-Type": "application/json"
            }

            if request_body:
                response = await client.post(
                    api_endpoint,
                    json=request_body,
                    headers=headers
                )
            else:
                response = await client.get(
                    api_endpoint,
                    headers=headers
                )

            response.raise_for_status()
            api_data = response.json()

        # Step 3: Assess quality
        if quality_criteria:
            assessment = await assess_data_quality(
                data=api_data,
                expected_criteria=quality_criteria
            )
        else:
            # Basic assessment if no criteria provided
            assessment = {
                "quality_score": 100,
                "issues_found": [],
                "refund_percentage": 0,
                "assessment_details": {}
            }

        # Step 4: Determine recommendation
        quality_score = assessment["quality_score"]
        if quality_score >= 80:
            recommendation = "release"
        elif quality_score >= 50:
            recommendation = "partial"
        else:
            recommendation = "dispute"

        return {
            "escrow_address": escrow["escrow_address"],
            "api_response": api_data,
            "quality_score": quality_score,
            "refund_percentage": assessment["refund_percentage"],
            "recommendation": recommendation,
            "issues_found": assessment.get("issues_found", []),
            "assessment_details": assessment.get("assessment_details", {})
        }

    except httpx.HTTPError as e:
        logger.error(f"API call failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Error in call_api_with_escrow: {e}")
        raise


async def assess_data_quality(
    data: Any,
    expected_criteria: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Assess quality of API response against expected criteria

    Args:
        data: API response data
        expected_criteria: Quality requirements
            - min_records: Minimum number of records expected
            - required_fields: List of required field names
            - max_age_days: Maximum age of data in days
            - schema: Expected JSON schema
            - custom_validation: Natural language rules

    Returns:
        {
            "quality_score": float (0-100),
            "issues_found": list[str],
            "refund_percentage": int (0-100),
            "assessment_details": {
                "completeness": float,
                "freshness": float,
                "schema_compliance": float
            }
        }
    """
    try:
        logger.info("Assessing data quality")

        assessor = get_quality_assessor()
        result = assessor.assess(data, expected_criteria)

        logger.info(
            f"Quality assessment complete: score={result['quality_score']}, "
            f"refund={result['refund_percentage']}%"
        )

        return result

    except Exception as e:
        logger.error(f"Error assessing quality: {e}")
        raise


async def file_dispute(
    escrow_address: str,
    quality_score: int,
    evidence: Dict[str, Any],
    refund_percentage: int
) -> Dict[str, Any]:
    """
    File dispute for escrow due to poor quality data

    Args:
        escrow_address: Escrow account address
        quality_score: Assessed quality (0-100)
        evidence: Dispute evidence
            - original_query: What was expected
            - data_received: What was actually received
            - issues: List of quality issues
        refund_percentage: Requested refund (0-100%)

    Returns:
        {
            "dispute_id": str,
            "status": str,
            "oracle_assessment_eta": str,
            "transaction_id": str
        }
    """
    try:
        logger.info(
            f"Filing dispute for escrow {escrow_address}: "
            f"quality={quality_score}, refund={refund_percentage}%"
        )

        # Validate inputs
        if not isinstance(quality_score, int):
            raise ValueError(f"Quality score must be an integer, got: {type(quality_score).__name__}")

        if not (MIN_QUALITY_THRESHOLD <= quality_score <= MAX_QUALITY_THRESHOLD):
            raise ValueError(
                f"Quality score must be between {MIN_QUALITY_THRESHOLD} and {MAX_QUALITY_THRESHOLD}, got: {quality_score}"
            )

        if not isinstance(refund_percentage, int):
            raise ValueError(f"Refund percentage must be an integer, got: {type(refund_percentage).__name__}")

        if not (0 <= refund_percentage <= 100):
            raise ValueError(f"Refund percentage must be between 0 and 100, got: {refund_percentage}")

        # File dispute on-chain
        solana_client = get_solana_client()
        result = await solana_client.file_dispute(
            escrow_address=escrow_address,
            quality_score=quality_score,
            evidence=evidence,
            refund_percentage=refund_percentage
        )

        logger.info(f"Dispute filed: {result['dispute_id']}")
        return result

    except Exception as e:
        logger.error(f"Error filing dispute: {e}")
        raise


async def check_escrow_status(
    escrow_address: str
) -> Dict[str, Any]:
    """
    Check status of an escrow payment

    Args:
        escrow_address: Escrow account address

    Returns:
        {
            "status": str,
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
        logger.info(f"Checking escrow status: {escrow_address}")

        solana_client = get_solana_client()
        result = await solana_client.check_escrow_status(escrow_address)

        logger.info(f"Escrow status: {result['status']}")
        return result

    except Exception as e:
        logger.error(f"Error checking escrow status: {e}")
        raise


async def get_api_reputation(
    api_provider: str
) -> Dict[str, Any]:
    """
    Check on-chain reputation of an API provider

    Args:
        api_provider: API provider wallet address

    Returns:
        {
            "reputation_score": int (0-1000),
            "total_transactions": int,
            "disputes_filed": int,
            "disputes_won": int,
            "disputes_lost": int,
            "average_quality_provided": float,
            "recommendation": str
        }
    """
    try:
        logger.info(f"Checking reputation for: {api_provider}")

        solana_client = get_solana_client()
        result = await solana_client.get_api_reputation(api_provider)

        # Determine recommendation
        score = result["reputation_score"]
        if score >= 900:
            result["recommendation"] = "trusted"
        elif score >= 700:
            result["recommendation"] = "reliable"
        elif score >= 500:
            result["recommendation"] = "caution"
        else:
            result["recommendation"] = "avoid"

        logger.info(
            f"Reputation: {score}/1000 ({result['recommendation']})"
        )
        return result

    except Exception as e:
        logger.error(f"Error getting reputation: {e}")
        raise


async def verify_payment(
    transaction_hash: str,
    expected_amount: Optional[float] = None,
    expected_recipient: Optional[str] = None
) -> Dict[str, Any]:
    """
    Verify that a payment was received (integrates with x402 Infrastructure)

    Args:
        transaction_hash: Solana transaction hash
        expected_amount: Optional amount verification
        expected_recipient: Optional recipient verification

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
        logger.info(f"Verifying payment: {transaction_hash}")

        solana_client = get_solana_client()
        result = await solana_client.verify_payment(
            transaction_hash=transaction_hash,
            expected_amount=expected_amount,
            expected_recipient=expected_recipient
        )

        logger.info(f"Payment verified: {result['verified']}")
        return result

    except Exception as e:
        logger.error(f"Error verifying payment: {e}")
        raise


def estimate_refund(
    amount_sol: float,
    quality_score: int
) -> Dict[str, Any]:
    """
    Estimate refund amount based on quality score

    Args:
        amount_sol: Payment amount in SOL
        quality_score: Quality score (0-100)

    Returns:
        {
            "refund_sol": float,
            "payment_sol": float,
            "refund_percentage": int,
            "rationale": str
        }
    """
    try:
        logger.info(
            f"Estimating refund: {amount_sol} SOL, quality={quality_score}"
        )

        solana_client = get_solana_client()
        result = solana_client.estimate_refund(amount_sol, quality_score)

        logger.info(
            f"Refund estimate: {result['refund_sol']} SOL "
            f"({result['refund_percentage']}%)"
        )
        return result

    except Exception as e:
        logger.error(f"Error estimating refund: {e}")
        raise
