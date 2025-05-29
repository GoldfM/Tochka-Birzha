from fake_db import balances_history, users_history
from models import BalanceUp, BalanceDown, StatusMessage
from fastapi import APIRouter, HTTPException, Query, Header
from typing import Dict, Optional

balance_router = APIRouter(prefix="/balance", tags=["balance"])

def get_key_token(authorization: Optional[str]) -> str:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization is required")
    
    return f"{authorization}"

@balance_router.get("/", response_model=Dict[str, int])
def get_balances(authorization: Optional[str] = Query(None)):
    api_key = get_key_token(authorization)
    user_id = next((user.id for user in users_history.values() if user.api_key == api_key), None)

    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    return balances_history.get(user_id, {})



@balance_router.post("/withdraw", response_model=StatusMessage)
def withdraw(request: BalanceDown, authorization: Optional[str] = Query(None)):
    api_key = get_key_token(authorization)
    user_id = next((user.id for user in users_history.values() if user.api_key == api_key), None)

    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    if user_id not in balances_history or balances_history[user_id].get(request.ticker, 0) < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    balances_history[user_id][request.ticker] -= request.amount
    return StatusMessage(status=True)
@balance_router.post("/deposit", response_model=StatusMessage)
def deposit(request: BalanceUp, authorization: Optional[str] = Query(None)):
    api_key = get_key_token(authorization)
    user_id = next((user.id for user in users_history.values() if user.api_key == api_key), None)

    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    if user_id not in balances_history:
        balances_history[user_id] = {}

    balances_history[user_id][request.ticker] = balances_history[user_id].get(request.ticker, 0) + request.amount

    return StatusMessage(status=True)