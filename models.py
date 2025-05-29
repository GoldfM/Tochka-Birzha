from pydantic import BaseModel
from typing import List
from uuid import UUID
from enum import Enum

class Role(Enum):
    USER = "user"
    ADMIN = "admin"

class OrderState(str, Enum):
    CREATED = "CREATED"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELED = "CANCELED"

class TradeDirection(str, Enum):
    BUY = "buy"
    SELL = "sell"

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



class Transaction(BaseModel):
    ticker: str
    amount: int
    price: int
    timestamp: str

class BalanceDown(BaseModel):
    id: UUID
    ticker: str
    amount: int

class BalanceUp(BaseModel):
    id: UUID
    ticker: str
    amount: int



class LimitOrderRequest(BaseModel):
    side: TradeDirection
    symbol: str
    quantity: int
    limit_price: int

class MarketOrderRequest(BaseModel):
    side: TradeDirection
    symbol: str
    quantity: int

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