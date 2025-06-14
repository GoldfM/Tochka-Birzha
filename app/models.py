from pydantic import BaseModel
from typing import List
from uuid import UUID
from enum import Enum

class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class OrderState(str, Enum):
    NEW = "NEW"
    EXECUTED = "EXECUTED"
    PARTIALLY_EXECUTED = "PARTIALLY_EXECUTED"
    CANCELLED = "CANCELLED"

class Direction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class NewUser(BaseModel):
    name: str

class User(BaseModel):
    id: UUID
    name: str
    role: Role = Role.USER
    api_key: str

class Level(BaseModel):
    price: int
    qty: int

class L2OrderBook(BaseModel):
    bid_levels: List[Level]
    ask_levels: List[Level]
class Instrument(BaseModel):
    name: str
    ticker: str


class Ok(BaseModel):
    status: bool = True

from pydantic import AwareDatetime
class Transaction(BaseModel):
    ticker: str
    amount: int
    price: int
    timestamp: AwareDatetime

class Body_withdraw_api_v1_admin_balance_withdraw_post(BaseModel):
    user_id: UUID
    ticker: str
    amount: int

class Body_deposit_api_v1_admin_balance_deposit_post(BaseModel):
    user_id: UUID
    ticker: str
    amount: int



class LimitOrderRequest(BaseModel):
    direction: Direction
    ticker: str
    qty: int
    price: int

class MarketOrderRequest(BaseModel):
    direction: Direction
    ticker: str
    qty: int


class CreateOrderResponse(BaseModel):
    success: bool = True
    order_id: UUID

class LimitOrder(BaseModel):
    id: UUID
    status: OrderState
    user_id: UUID
    timestamp: str
    body: LimitOrderRequest
    filled: int = 0

class MarketOrder(BaseModel):
    id: UUID
    status: OrderState
    user_id: UUID
    timestamp: str
    body: MarketOrderRequest

