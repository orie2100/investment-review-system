from pydantic import BaseModel, ConfigDict
from typing import Optional

class AccountCreate(BaseModel):
    name: str
    account_type: str = "基金账户"
    institution: Optional[str] = None
    currency: str = "CNY"


class AccountOut(AccountCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PositionCreate(BaseModel):
    account_id: int
    name: str
    code: Optional[str] = None
    asset_type: str = "基金"
    quantity: Optional[float] = None
    cost_price: Optional[float] = None
    current_price: Optional[float] = None
    category: Optional[str] = None
    currency: str = "CNY"
    note: Optional[str] = None


class PositionOut(PositionCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)