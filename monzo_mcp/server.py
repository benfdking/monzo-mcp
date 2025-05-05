from typing import List, Optional
from fastmcp import FastMCP
from dotenv import load_dotenv
import os

from monzo_mcp.client import Account, AccountType, MonzoClient
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

MONZO_API_BASE = "https://api.monzo.com"

# Get access token from environment variable
MONZO_ACCESS_TOKEN = os.getenv("MONZO_ACCESS_TOKEN")
if not MONZO_ACCESS_TOKEN:
    raise ValueError("MONZO_ACCESS_TOKEN environment variable is not set")

mcp = FastMCP()

monzo_client = MonzoClient(MONZO_API_BASE)


class Balance(BaseModel):
    balance: int


# @mcp.tool()
# async def get_balance(ctx):
#     async with httpx.AsyncClient() as client:
#         resp = await client.get(
#             f"{MONZO_API_BASE}/balance",
#             headers={"Authorization": f"Bearer {MONZO_ACCESS_TOKEN}"},
#         )
#         resp.raise_for_status()
#         return resp.json()
#     return Balance(balance=100)

# class Transaction(BaseModel):
#     amount: int
#     date: str


@mcp.tool()
async def list_accounts(
    ctx, account_type: Optional[AccountType] = None
) -> List[Account]:
    response = await monzo_client.list_accounts(account_type)
    return response.accounts
