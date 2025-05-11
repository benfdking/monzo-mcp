from typing import List, Optional, Literal, Union, Dict, Any
from pydantic import BaseModel, Field
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


class Pot(BaseModel):
    id: str
    name: str
    style: str
    balance: int
    currency: str
    created: str
    updated: str
    deleted: bool


class ListPotsResponse(BaseModel):
    pots: List[Pot]


class Address(BaseModel):
    address: str
    city: str
    country: str
    latitude: float
    longitude: float
    postcode: str
    region: str


class Merchant(BaseModel):
    address: Address
    created: str
    group_id: str
    id: str
    logo: str
    emoji: str
    name: str
    category: str


class Transaction(BaseModel):
    amount: int
    created: str
    currency: str
    description: str
    id: str
    merchant: Union[Merchant, str]
    metadata: Dict[str, Any]
    notes: str
    is_load: bool
    settled: str


class GetTransactionResponse(BaseModel):
    transaction: Transaction


class ListTransactionsResponse(BaseModel):
    transactions: List[Transaction]


class ReceiptMerchant(BaseModel):
    """
    The merchant gives us more information about where the purchase was made,
    to help us decide what to show at the top of the receipt.
    """

    name: str = Field(..., description="The merchant name")
    online: bool = Field(
        ...,
        description="true for Ecommerce merchants like Amazon; false for offline merchants like Pret or Starbucks",
    )
    phone: Optional[str] = Field(None, description="The phone number of the store")
    email: Optional[str] = Field(None, description="The merchant's email address")
    store_name: Optional[str] = Field(
        None, description="The name of that particular store, e.g. Old Street"
    )
    store_address: Optional[str] = Field(None, description="The store's address")
    store_postcode: Optional[str] = Field(None, description="The store's postcode")


class ReceiptTax(BaseModel):
    """
    Represents a tax entry on a receipt, such as VAT.
    """

    description: str = Field(..., description="e.g. 'VAT'")
    amount: int = Field(..., description="Total amount of the tax, in pennies")
    currency: str = Field(..., description="e.g. GBP")
    tax_number: Optional[str] = Field(None, description="e.g. '945719291'")


class MonzoClient:
    def __init__(self, base_url: str, access_token: str):
        self.base_url = base_url
        self.access_token = access_token

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    async def get_balance(self, account_id: str) -> GetBalanceResponse:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/balance",
                headers=self._get_headers(),
                params={"account_id": account_id},
            )
            resp.raise_for_status()  # Raise exception for 4XX/5XX responses
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
            resp.raise_for_status()  # Raise exception for 4XX/5XX responses
            return ListAccountsResponse(**resp.json())

    async def list_pots(self) -> ListPotsResponse:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/pots",
                headers=self._get_headers(),
            )
            resp.raise_for_status()  # Raise exception for 4XX/5XX responses
            return ListPotsResponse(**resp.json())

    async def get_transaction(self, transaction_id: str) -> GetTransactionResponse:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/transactions/{transaction_id}",
                headers=self._get_headers(),
                params={"expand[]": "merchant"},
            )
            resp.raise_for_status()  # Raise exception for 4XX/5XX responses
            return GetTransactionResponse(**resp.json())

    async def list_transactions(
        self, account_id: str, since: Optional[str] = None, before: Optional[str] = None
    ) -> ListTransactionsResponse:
        async with httpx.AsyncClient() as client:
            params = {"account_id": account_id}
            if since:
                params["since"] = since
            if before:
                params["before"] = before
            resp = await client.get(
                f"{self.base_url}/transactions",
                headers=self._get_headers(),
                params=params,
            )
            resp.raise_for_status()  # Raise exception for 4XX/5XX responses
            return ListTransactionsResponse(**resp.json())
