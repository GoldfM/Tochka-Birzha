from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models import BalanceUp, BalanceDown, StatusMessage
from app.models_DB.balances import Balance_db
from app.models_DB.users import User_db
from typing import Dict
from app.tools import validate_admin, verify_auth_token
from app.db_manager import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter(prefix="/balance", tags=["balance"])
admin_router = APIRouter(prefix="/admin/balance", tags=["admin", "balance"])

@router.get("/", response_model=Dict[str, float])
async def get_balances(api_key: str = Depends(verify_auth_token), db: AsyncSession = Depends(get_db)):
    user_result = await db.execute(
        select(User_db).where(User_db.api_key == api_key)
    )
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    balances_result = await db.execute(
        select(Balance_db).where(Balance_db.user_id == user.id)
    )
    balances = balances_result.scalars().all()
    response = {balance.ticker: balance.amount for balance in balances}
    return response

@admin_router.post("/deposit", response_model=StatusMessage)
async def deposit(
    request: BalanceUp,
    api_key: str = Depends(verify_auth_token),
    user: User_db = Depends(validate_admin),
    db: AsyncSession = Depends(get_db)
):

    user_result = await db.execute(
        select(User_db).where(User_db.id == request.user_id)
    )

    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    balance_result = await db.execute(
        select(Balance_db)
        .where(Balance_db.user_id == request.user_id, Balance_db.ticker == request.ticker)
    )
    balance = balance_result.scalar_one_or_none()

    if balance:
        balance.amount += request.amount
    else:
        balance = Balance_db(
            user_id=request.user_id,
            ticker=request.ticker,
            amount=request.amount
            )
        db.add(balance)

    await db.commit()

    return StatusMessage()

@admin_router.post("/withdraw", response_model=StatusMessage)
async def withdraw(
    request: BalanceDown,
    api_key: str = Depends(verify_auth_token),
    user: User_db = Depends(validate_admin),
    db: AsyncSession = Depends(get_db)
):
    user_result = await db.execute(
        select(User_db).where(User_db.id == request.user_id)
    )
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    balance_result = await db.execute(
        select(Balance_db)
        .where(Balance_db.user_id == request.user_id, Balance_db.ticker == request.ticker)
    )
    balance = balance_result.scalar_one_or_none()

    if not balance or balance.amount < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    balance.amount -= request.amount
    await db.commit()

    return StatusMessage()
