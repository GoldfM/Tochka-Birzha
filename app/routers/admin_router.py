from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models_DB.instruments import Instrument_db
from app.models_DB.users import User_db
from app.models import Instrument as InstrumentSchema, Ok
from app.db_manager import get_db
from app.tools import validate_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/instrument", response_model=Ok)
async def add_instrument(
    instrument: InstrumentSchema,
    user: User_db = Depends(validate_admin),
    db: AsyncSession = Depends(get_db)
):
    instrument_find = await db.execute(
        select(Instrument_db).where(Instrument_db.ticker == instrument.ticker)
    )
    instrument_find = instrument_find.scalar_one_or_none()

    if instrument_find:
        raise HTTPException(status_code=400, detail="Instrument already exists")

    instrument_create = Instrument_db(
        name=instrument.name,
        ticker=instrument.ticker
    )
    db.add(instrument_create)

    await db.commit()
    return Ok()

@router.delete("/instrument/{ticker}", response_model=Ok)
async def delete_instrument(
    ticker: str,
    user: User_db = Depends(validate_admin),
    db: AsyncSession = Depends(get_db)
):
    instrument_delete = await db.execute(
        select(Instrument_db).where(Instrument_db.ticker == ticker)
    )
    instrument_delete = instrument_delete.scalar_one_or_none()

    if not instrument_delete:
        raise HTTPException(status_code=404, detail="Instrument not found")

    await db.execute(
        delete(Instrument_db).where(Instrument_db.ticker == ticker)
    )

    await db.commit()
    return Ok()
