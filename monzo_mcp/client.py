from typing import List, Optional, Literal
from pydantic import BaseModel
import httpx


class Account(BaseModel):
    id: str
    description: str
    created: str

AccountType = Literal["uk_retail", "uk_retail_joint"]

class ListAccountsRequest(BaseModel):
    account_type_filter: Optional[AccountType] = None


class ListAccountsResponse(BaseModel):
    accounts: List[Account]


class GetBalanceResponse(BaseModel):
    balance: int
    total_balance: int
    currency: str
    spend_today: int



class MonzoClient:
    def __init__(self, base_url: str, access_token: str):
        self.base_url = base_url
        self.access_token = access_token

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}
    
    async def read_balance(self) -> GetBalanceResponse:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/balance",
                headers=self._get_headers(),
            )
            return GetBalanceResponse(**resp.json())

    async def list_accounts(
        self, account_type_filter: Optional[str] = None
    ) -> ListAccountsResponse:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/accounts",
                params={"account_type": account_type_filter},
                headers=self._get_headers(),
            )
            return ListAccountsResponse(**resp.json())
