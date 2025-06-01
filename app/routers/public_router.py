from fastapi import APIRouter, HTTPException, Depends
from app.models import UserNameNew, User, Instrument, OrderBook, Transaction, Level
from app.models_DB.users import User_db
from app.models_DB.instruments import Instrument_db
from app.models_DB.transactions import Transaction_db
from app.models_DB.orderbook import OrderBook_db
from app.db_manager import get_db
from sqlalchemy import select
from uuid import uuid4
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/public", tags=["public"])

@router.post("/register", response_model=User)
async def register(new_user: UserNameNew, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User_db).where(User_db.name == new_user.name))
    existing_user = existing_user.scalar_one_or_none()

    if existing_user:
        return existing_user

    user_id = uuid4()
    api_key = f"{uuid4()}"

    user = User_db(id=user_id, name=new_user.name, role="USER", api_key=api_key)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

@router.get("/instrument", response_model=List[Instrument])
async def list_instruments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Instrument_db))
    instruments = result.scalars().all()   

    return instruments

@router.get("/orderbook/{ticker}", response_model=OrderBook)
async def get_orderbook(ticker: str, limit: int = 10, db: AsyncSession = Depends(get_db)):
    instrument_result = await db.execute(
        select(Instrument_db).where(Instrument_db.ticker == ticker)
    )

    instrument = instrument_result.scalar_one_or_none()
    if not instrument:
        raise HTTPException(status_code=422, detail="Instrument not found")

    orderbook_result = await db.execute(
        select(OrderBook_db).where(OrderBook_db.ticker == ticker)
    )

    orderbook = orderbook_result.scalar_one_or_none()
    if not orderbook:
        raise HTTPException(status_code=404, detail="Orderbook not found")

    return OrderBook(
        buy_levels=[Level(**level) for level in orderbook.buy_levels][:limit],
        sell_levels=[Level(**level) for level in orderbook.sell_levels][:limit],
    )

@router.get("/transactions/{ticker}", response_model=List[Transaction])
async def get_transaction_history(ticker: str, limit: int = 10, db: AsyncSession = Depends(get_db)):
    instrument_result = await db.execute(
        select(Instrument_db).where(Instrument_db.ticker == ticker)
    )

    instrument = instrument_result.scalar_one_or_none()
    if not instrument:
        raise HTTPException(status_code=422, detail="Instrument not found")

    transactions_result = await db.execute(
        select(Transaction_db)
        .where(Transaction_db.ticker == ticker)
        .order_by(Transaction_db.timestamp.desc())
        .limit(limit)
    )
    transactions = transactions_result.scalars().all()

    response = [
        Transaction(
            ticker=transaction.ticker,
            amount=transaction.amount,
            price=transaction.price,
            timestamp=transaction.timestamp.isoformat()
        )
        for transaction in transactions
    ]

    return response
