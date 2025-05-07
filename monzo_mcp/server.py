from typing import List, Optional
from fastmcp import FastMCP
from dotenv import load_dotenv
import os

from .client import (
    Account,
    AccountType,
    MonzoClient,
    GetBalanceResponse,
    Transaction,
)

# Load environment variables from .env file
load_dotenv()

MONZO_API_BASE = "https://api.monzo.com"

# Get access token from environment variable
MONZO_ACCESS_TOKEN = os.getenv("MONZO_ACCESS_TOKEN")
if not MONZO_ACCESS_TOKEN:
    raise ValueError("MONZO_ACCESS_TOKEN environment variable is not set")

mcp = FastMCP()

monzo_client = MonzoClient(MONZO_API_BASE)


@mcp.tool()
async def get_balance(ctx, account_id: str) -> GetBalanceResponse:
    response = await monzo_client.get_balance(account_id)
    return response


@mcp.tool()
async def list_accounts(
    ctx, account_type: Optional[AccountType] = None
) -> List[Account]:
    response = await monzo_client.list_accounts(account_type)
    return response.accounts


@mcp.tool()
async def list_transactions(
    ctx, account_id: str, since: Optional[str] = None, before: Optional[str] = None
) -> List[Transaction]:
    response = await monzo_client.list_transactions(account_id, since, before)
    return response.transactions
