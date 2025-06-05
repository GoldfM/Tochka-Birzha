import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers.public_router import router as public_router
from app.routers.balance_router import router as balance_router
from app.routers.order_router import router as order_router
from app.routers.admin_router import admin_router as admin_router
from app.routers.admin_router import balance_router as admin_balance_router
from app.routers.user_router import router as user_router

# ToDo
# orderbook
app = FastAPI()

app.include_router(public_router,prefix='/api/v1')
app.include_router(admin_balance_router,prefix='/api/v1')
app.include_router(user_router,prefix='/api/v1')
app.include_router(order_router,prefix='/api/v1')
app.include_router(balance_router,prefix='/api/v1')
app.include_router(admin_router,prefix='/api/v1')


'''
def get_model_schema(model):
    inspector = inspect(model)
    schema = {}
    for column in inspector.columns:
        schema[column.name] = {
            "type": str(column.type),
            "primary_key": column.primary_key,
            "nullable": column.nullable,
            "unique": column.unique,
        }
    return schema
from app.models_DB import (User, Balance, Instrument,
    LimitOrder, MarketOrder, OrderReq,
    OrderBook, Withdraw, Transaction
)

all_models = [User, Balance, Instrument, LimitOrder,
              MarketOrder, OrderReq, OrderBook, Withdraw, Transaction]

db_schemas = {}
for model in all_models:
    db_schemas[model.__tablename__] = get_model_schema(model)

for k,v in db_schemas.items():
    print(k,v)'''
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
