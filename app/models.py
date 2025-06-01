from pydantic import BaseModel
from typing import List
from uuid import UUID
from enum import Enum

class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class OrderState(str, Enum):
    CREATED = "CREATED"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELED = "CANCELED"

class TradeDirection(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class UserNameNew(BaseModel):
    name: str

class User(BaseModel):
    id: UUID
    name: str
    role: Role = Role.USER
    api_key: str

class Level(BaseModel):
    price: int
    qty: int

class OrderBook(BaseModel):
    buy_levels: List[Level]
    sell_levels: List[Level]
class Instrument(BaseModel):
    name: str
    ticker: str


class StatusMessage(BaseModel):
    status: bool = True
class Transaction(BaseModel):
    ticker: str
    amount: int
    price: int
    timestamp: str

class BalanceDown(BaseModel):
    user_id: UUID
    ticker: str
    amount: int

class BalanceUp(BaseModel):
    user_id: UUID
    ticker: str
    amount: int



class LimitOrderRequest(BaseModel):
    direction: TradeDirection
    symbol: str
    quantity: int
    limit_price: int

class MarketOrderRequest(BaseModel):
    direction: TradeDirection
    symbol: str
    quantity: int


class CreateOrder(BaseModel):
    success: bool = True
    order_id: UUID

class LimitOrder(BaseModel):
    order_id: UUID
    status: OrderState
    trader_id: UUID
    created_at: str
    details: LimitOrderRequest
    executed_qty: int = 0

class MarketOrder(BaseModel):
    order_id: UUID
    status: OrderState
    trader_id: UUID
    created_at: str
    details: MarketOrderRequest

