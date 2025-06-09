from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4
from typing import List
from app.models import NewUser, User, Instrument, L2OrderBook, Transaction, Level
from app.models_DB.users import User_db
from app.models_DB.instruments import Instrument_db
from app.models_DB.transactions import Transaction_db
from app.models_DB.orderbook import OrderBook_db
from app.db_manager import get_db

router = APIRouter(prefix="/public", tags=["public"])


async def _check_instrument_exists(ticker: str, db: AsyncSession):
    query = select(Instrument_db).where(Instrument_db.ticker == ticker)
    result = await db.execute(query)
    return result.first()


@router.post("/register", response_model=User)
async def user_registration(new_user_data: NewUser, db_session: AsyncSession = Depends(get_db)):
    user_query = select(User_db).where(User_db.name == new_user_data.name)
    existing = (await db_session.execute(user_query)).first()

    if existing:
        return existing

    new_user = User_db(
        id=uuid4(),
        name=new_user_data.name,
        role="USER",
        api_key='key-' + str(uuid4())
    )

    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    return new_user


@router.get("/instrument", response_model=List[Instrument])
async def fetch_all_instruments(database: AsyncSession = Depends(get_db)):
    query_result = await database.execute(select(Instrument_db))
    return query_result.scalars().all()


@router.get("/orderbook/{ticker}", response_model=L2OrderBook)
async def fetch_orderbook_data(
        ticker: str,
        depth: int = 10,
        db_connection: AsyncSession = Depends(get_db)
):
    if not await _check_instrument_exists(ticker, db_connection):
        raise HTTPException(status_code=422, detail="Instrument not found")

    orderbook_query = select(OrderBook_db).where(OrderBook_db.ticker == ticker)
    orderbook_data = (await db_connection.scalars(orderbook_query)).first()

    if orderbook_data:
        return L2OrderBook(
            bid_levels=[Level(**l) for l in orderbook_data.bid_levels][:depth],
            ask_levels=[Level(**l) for l in orderbook_data.ask_levels][:depth]
        )
    else:
        raise HTTPException(status_code=404, detail="Orderbook not found")

@router.get("/transactions/{ticker}", response_model=List[Transaction])
async def retrieve_transaction_history(
        ticker: str,
        max_results: int = 10,
        db: AsyncSession = Depends(get_db)
):
    if not await _check_instrument_exists(ticker, db):
        raise HTTPException(status_code=422, detail="Instrument not found")

    history_query = (
        select(Transaction_db)
        .where(Transaction_db.ticker == ticker)
        .order_by(Transaction_db.timestamp.desc())
        .limit(max_results)
    )

    transactions = (await db.execute(history_query)).scalars().all()

    return [
        Transaction(
            ticker=t.ticker,
            amount=t.amount,
            price=t.price,
            timestamp=t.timestamp.isoformat()
        )
        for t in transactions
    ]