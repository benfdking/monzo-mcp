from typing import List, Optional
import httpx
from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import logging

from .client import (
    Account,
    AccountType,
    MonzoClient,
    GetBalanceResponse,
    Transaction,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

MONZO_API_BASE = "https://api.monzo.com"

# Get access token from environment variable
MONZO_ACCESS_TOKEN = os.getenv("MONZO_ACCESS_TOKEN")
if not MONZO_ACCESS_TOKEN:
    raise ValueError("MONZO_ACCESS_TOKEN environment variable is not set")

try:
    mcp = FastMCP()
    monzo_client = MonzoClient(MONZO_API_BASE, MONZO_ACCESS_TOKEN)
    logger.info("Initialized FastMCP and MonzoClient successfully")
except Exception as e:
    logger.error(f"Failed to initialize MCP or MonzoClient: {e}")
    raise


@mcp.tool()
async def get_balance(ctx, account_id: str) -> GetBalanceResponse:
    try:
        response = await monzo_client.get_balance(account_id)
        return response
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error accessing Monzo API: {e}")
        raise
    except Exception as e:
        logger.error(f"Error getting balance: {e}")
        raise


@mcp.tool()
async def list_accounts(
    ctx, account_type: Optional[AccountType] = None
) -> List[Account]:
    try:
        response = await monzo_client.list_accounts(account_type)
        return response.accounts
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error accessing Monzo API: {e}")
        raise
    except Exception as e:
        logger.error(f"Error listing accounts: {e}")
        raise


@mcp.tool()
async def list_transactions(
    ctx, account_id: str, since: Optional[str] = None, before: Optional[str] = None
) -> List[Transaction]:
    try:
        response = await monzo_client.list_transactions(account_id, since, before)
        return response.transactions
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error accessing Monzo API: {e}")
        raise
    except Exception as e:
        logger.error(f"Error listing transactions: {e}")
        raise
