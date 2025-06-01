import datetime
from typing import List, Union
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models_DB.users import User_db
from app.models_DB.limit_orders import LimitOrder_db
from app.models_DB.market_orders import MarketOrder_db
from app.models import LimitOrderRequest, LimitOrder, MarketOrder, MarketOrderRequest, CreateOrder, TradeDirection, OrderState, StatusMessage
from app.db_manager import get_db
from uuid import uuid4, UUID
from app.tools import verify_auth_token

router = APIRouter(prefix="/order", tags=["order"])

@router.post("/", response_model=CreateOrder)
async def create_order(
    order_body: LimitOrderRequest | MarketOrderRequest,
    api_key: str = Depends(verify_auth_token),
    db: AsyncSession = Depends(get_db)
):
    user_result = await db.execute(
        select(User_db).where(User_db.api_key == api_key)
    )

    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order_id = uuid4()
    if isinstance(order_body, LimitOrderRequest):
        order = LimitOrder_db(
            id=order_id,
            status="NEW",
            user_id=user.id,
            timestamp=datetime.datetime.now(),
            direction=order_body.direction,
            ticker=order_body.ticker,
            qty=order_body.qty,
            price=order_body.price,
            filled=0
        )
    else:
        order = MarketOrder_db(
            id=order_id,
            status="NEW",
            user_id=user.id,
            timestamp=datetime.datetime.now(),
            direction=order_body.direction,
            ticker=order_body.ticker,
            qty=order_body.qty
        )

    db.add(order)
    await db.commit()

    return CreateOrder(success=True, order_id=order_id)

@router.get("/", response_model=List[Union[LimitOrder, MarketOrder]])
async def list_orders(
    api_key: str = Depends(verify_auth_token),
    db: AsyncSession = Depends(get_db)
):
    user_result = await db.execute(
        select(User_db).where(User_db.api_key == api_key)
    )

    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    limit_orders_result = await db.execute(
        select(LimitOrder_db).where(LimitOrder_db.user_id == user.id)
    )
    limit_orders = limit_orders_result.scalars().all()

    market_orders_result = await db.execute(
        select(MarketOrder_db).where(MarketOrder_db.user_id == user.id)
    )
    market_orders = market_orders_result.scalars().all()

    orders = []
    for order in limit_orders:
        orders.append(LimitOrder(
            id=order.id,
            status=OrderState(order.status),
            user_id=order.user_id,
            timestamp=order.timestamp.isoformat() + "Z",
            body=LimitOrderRequest(
                direction=TradeDirection(order.direction),
                ticker=order.ticker,
                qty=order.qty,
                price=order.price
            ),
            filled=order.filled
        ))

    for order in market_orders:
        orders.append(MarketOrder(
            id=order.id,
            status=OrderState(order.status),
            user_id=order.user_id,
            timestamp=order.timestamp.isoformat() + "Z",
            body=MarketOrderRequest(
                direction=TradeDirection(order.direction),
                ticker=order.ticker,
                qty=order.qty
            )
        ))

    return orders

@router.delete("/{order_id}", response_model=StatusMessage)
async def cancel_order(
    order_id: UUID,
    api_key: str = Depends(verify_auth_token),
    db: AsyncSession = Depends(get_db)
):
    user_result = await db.execute(
        select(User_db).where(User_db.api_key == api_key)
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    limit_order_result = await db.execute(
        select(LimitOrder_db).where(LimitOrder_db.id == order_id)
    )
    limit_order = limit_order_result.scalar_one_or_none()

    market_order_result = await db.execute(
        select(MarketOrder_db).where(MarketOrder_db.id == order_id)
    )
    market_order = market_order_result.scalar_one_or_none()

    if limit_order:
        if user.id != limit_order.user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        limit_order.status = "CANCELLED"

    elif market_order:
        if user.id != market_order.user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        market_order.status = "CANCELLED"

    else:
        raise HTTPException(status_code=404, detail="Order not found")

    await db.commit()

    return StatusMessage()


@router.get("/{order_id}", response_model=Union[LimitOrder, MarketOrder])
async def get_order(
    order_id: UUID,
    api_key: str = Depends(verify_auth_token),
    db: AsyncSession = Depends(get_db)
):
    user_result = await db.execute(
        select(User_db).where(User_db.api_key == api_key)
    )

    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    limit_order_result = await db.execute(
        select(LimitOrder_db).where(LimitOrder_db.id == order_id)
    )
    limit_order = limit_order_result.scalar_one_or_none()

    market_order_result = await db.execute(
        select(MarketOrder_db).where(MarketOrder_db.id == order_id)
    )
    market_order = market_order_result.scalar_one_or_none()

    if limit_order:
        if limit_order.user_id != user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        return LimitOrder(
            id=limit_order.id,
            status=OrderState(limit_order.status),
            user_id=limit_order.user_id,
            timestamp=limit_order.timestamp.isoformat() + "Z",
            body=LimitOrderRequest(
                direction=TradeDirection(limit_order.direction),
                ticker=limit_order.ticker,
                qty=limit_order.qty,
                price=limit_order.price
            ),
            filled=limit_order.filled
        )
    elif market_order:
        if market_order.user_id != user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        return MarketOrder(
            id=market_order.id,
            status=OrderState(market_order.status),
            user_id=market_order.user_id,
            timestamp=market_order.timestamp.isoformat() + "Z",
            body=MarketOrderRequest(
                direction=TradeDirection(market_order.direction),
                ticker=market_order.ticker,
                qty=market_order.qty
            )
        )
    else:
        raise HTTPException(status_code=404, detail="Order not found")
