from fastapi import APIRouter, HTTPException
from models import UserNameNew, User, OrderBook, Transaction, Role
from uuid import uuid1
from typing import List
from fake_db import users_history, orderbooks_history, transactions_history, generate_user_id


router = APIRouter(prefix="/public", tags=["public"])


@router.post("/register", response_model=User)
def register(new_user: UserNameNew):
    user_id = generate_user_id()
    api_key = f"{uuid1()}"

    user = User(id=user_id, name=new_user.name, role=Role.USER, api_key=api_key)
    users_history[user_id] = user
    return user

@router.get("/transactions/{ticker}", response_model=List[Transaction])
def get_transaction_history(ticker: str, limit: int = 10):
    if ticker not in transactions_history:
        raise HTTPException(status_code=422, detail="Instrument not found")

    return transactions_history[ticker][:limit]

@router.get("/orderbook/{ticker}", response_model=OrderBook)
def get_orderbook(ticker: str, limit: int = 10):
    if ticker not in orderbooks_history:
        raise HTTPException(status_code=422, detail="Instrument not found")

    orderbook = orderbooks_history[ticker]

    return OrderBook(
        buy_levels=orderbook.buy_levels[:limit],
        sell_levels=orderbook.sell_levels[:limit],
    )
