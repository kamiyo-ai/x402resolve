#!/usr/bin/env python3
"""
x402Resolve MCP Server

MCP server enabling AI agents to pay for APIs with automatic quality guarantees,
escrow protection, and trustless dispute resolution on Solana.

This server provides 8 MCP tools for autonomous agent transactions:
- create_escrow: Lock payment before API call
- call_api_with_escrow: Pay + call + assess in one step
- assess_data_quality: Evaluate API response quality
- file_dispute: Trigger oracle verification
- check_escrow_status: Monitor escrow state
- get_api_reputation: Check provider trust score
- verify_payment: Confirm payment received
- estimate_refund: Calculate refund by quality score
"""

import sys
import os
import asyncio
import logging
from datetime import datetime
from typing import Any, Dict

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("Error: mcp not installed. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

# Import x402resolve tools
from tools.x402resolve import (
    create_escrow,
    call_api_with_escrow,
    assess_data_quality,
    file_dispute,
    check_escrow_status,
    get_api_reputation,
    verify_payment,
    estimate_refund
)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("x402resolve")

# Global state
server_start_time: datetime | None = None


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="create_escrow",
            description="Create escrow payment for HTTP 402 API call with quality guarantee",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_provider": {
                        "type": "string",
                        "description": "API provider wallet address"
                    },
                    "amount_sol": {
                        "type": "number",
                        "description": "Payment amount in SOL (0.001-1000)"
                    },
                    "api_endpoint": {
                        "type": "string",
                        "description": "API endpoint URL"
                    },
                    "quality_threshold": {
                        "type": "integer",
                        "description": "Minimum quality score 0-100 (default: 80)",
                        "default": 80
                    },
                    "time_lock_hours": {
                        "type": "integer",
                        "description": "Escrow expiry in hours (default: 24)",
                        "default": 24
                    }
                },
                "required": ["api_provider", "amount_sol", "api_endpoint"]
            }
        ),
        Tool(
            name="call_api_with_escrow",
            description="Create escrow + call API + auto-assess quality in one step",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_provider": {
                        "type": "string",
                        "description": "API provider wallet address"
                    },
                    "amount_sol": {
                        "type": "number",
                        "description": "Payment amount in SOL"
                    },
                    "api_endpoint": {
                        "type": "string",
                        "description": "API endpoint URL"
                    },
                    "request_body": {
                        "type": "object",
                        "description": "Optional POST body for API request"
                    },
                    "quality_criteria": {
                        "type": "object",
                        "description": "Quality requirements",
                        "properties": {
                            "min_records": {"type": "integer"},
                            "required_fields": {"type": "array", "items": {"type": "string"}},
                            "max_age_days": {"type": "integer"},
                            "schema": {"type": "object"}
                        }
                    }
                },
                "required": ["api_provider", "amount_sol", "api_endpoint"]
            }
        ),
        Tool(
            name="assess_data_quality",
            description="Assess quality of API response against expected criteria",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "API response data to assess"
                    },
                    "expected_criteria": {
                        "type": "object",
                        "description": "Quality requirements",
                        "properties": {
                            "min_records": {"type": "integer", "description": "Minimum number of records"},
                            "required_fields": {"type": "array", "items": {"type": "string"}},
                            "max_age_days": {"type": "integer", "description": "Maximum data age"},
                            "schema": {"type": "object", "description": "Expected JSON schema"}
                        }
                    }
                },
                "required": ["data", "expected_criteria"]
            }
        ),
        Tool(
            name="file_dispute",
            description="File dispute for escrow due to poor quality data",
            inputSchema={
                "type": "object",
                "properties": {
                    "escrow_address": {
                        "type": "string",
                        "description": "Escrow account address"
                    },
                    "quality_score": {
                        "type": "integer",
                        "description": "Assessed quality score (0-100)"
                    },
                    "evidence": {
                        "type": "object",
                        "description": "Dispute evidence",
                        "properties": {
                            "original_query": {"type": "string"},
                            "data_received": {"type": "object"},
                            "issues": {"type": "array", "items": {"type": "string"}}
                        }
                    },
                    "refund_percentage": {
                        "type": "integer",
                        "description": "Requested refund percentage (0-100)"
                    }
                },
                "required": ["escrow_address", "quality_score", "evidence", "refund_percentage"]
            }
        ),
        Tool(
            name="check_escrow_status",
            description="Check status of an escrow payment",
            inputSchema={
                "type": "object",
                "properties": {
                    "escrow_address": {
                        "type": "string",
                        "description": "Escrow account address"
                    }
                },
                "required": ["escrow_address"]
            }
        ),
        Tool(
            name="get_api_reputation",
            description="Check on-chain reputation of an API provider",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_provider": {
                        "type": "string",
                        "description": "API provider wallet address"
                    }
                },
                "required": ["api_provider"]
            }
        ),
        Tool(
            name="verify_payment",
            description="Verify that a payment was received",
            inputSchema={
                "type": "object",
                "properties": {
                    "transaction_hash": {
                        "type": "string",
                        "description": "Solana transaction hash"
                    },
                    "expected_amount": {
                        "type": "number",
                        "description": "Optional expected amount in SOL"
                    },
                    "expected_recipient": {
                        "type": "string",
                        "description": "Optional expected recipient address"
                    }
                },
                "required": ["transaction_hash"]
            }
        ),
        Tool(
            name="estimate_refund",
            description="Estimate refund amount based on quality score",
            inputSchema={
                "type": "object",
                "properties": {
                    "amount_sol": {
                        "type": "number",
                        "description": "Payment amount in SOL"
                    },
                    "quality_score": {
                        "type": "integer",
                        "description": "Quality score (0-100)"
                    }
                },
                "required": ["amount_sol", "quality_score"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """Handle tool calls from MCP clients"""
    global server_start_time

    logger.info(f"Tool called: {name} with args: {arguments}")

    try:
        # Route to appropriate tool handler
        if name == "create_escrow":
            result = await create_escrow(**arguments)

        elif name == "call_api_with_escrow":
            result = await call_api_with_escrow(**arguments)

        elif name == "assess_data_quality":
            result = await assess_data_quality(**arguments)

        elif name == "file_dispute":
            result = await file_dispute(**arguments)

        elif name == "check_escrow_status":
            result = await check_escrow_status(**arguments)

        elif name == "get_api_reputation":
            result = await get_api_reputation(**arguments)

        elif name == "verify_payment":
            result = await verify_payment(**arguments)

        elif name == "estimate_refund":
            result = estimate_refund(**arguments)

        else:
            raise ValueError(f"Unknown tool: {name}")

        # Format result as JSON
        import json
        result_text = json.dumps(result, indent=2)

        logger.info(f"Tool {name} completed successfully")
        return [TextContent(type="text", text=result_text)]

    except Exception as e:
        logger.error(f"Error in tool {name}: {e}", exc_info=True)
        error_result = {
            "error": str(type(e).__name__),
            "message": str(e),
            "tool": name
        }
        import json
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]


async def main():
    """Run the MCP server"""
    global server_start_time
    server_start_time = datetime.now()

    logger.info("="*60)
    logger.info("x402Resolve MCP Server Starting")
    logger.info("="*60)
    logger.info(f"Solana RPC: {os.getenv('SOLANA_RPC_URL', 'https://api.devnet.solana.com')}")
    logger.info(f"Program ID: {os.getenv('X402_PROGRAM_ID', 'E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n')}")
    logger.info(f"Log Level: {os.getenv('LOG_LEVEL', 'INFO')}")
    logger.info("="*60)
    logger.info("Available tools:")
    logger.info("  1. create_escrow - Create payment escrow")
    logger.info("  2. call_api_with_escrow - Pay + call + assess")
    logger.info("  3. assess_data_quality - Evaluate API response")
    logger.info("  4. file_dispute - Submit quality dispute")
    logger.info("  5. check_escrow_status - Monitor escrow")
    logger.info("  6. get_api_reputation - Check provider trust")
    logger.info("  7. verify_payment - Confirm payment")
    logger.info("  8. estimate_refund - Calculate refund")
    logger.info("="*60)

    async with stdio_server() as (read_stream, write_stream):
        logger.info("MCP server ready - waiting for connections...")
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nShutting down MCP server...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
