import uvicorn
from fastapi import FastAPI
from routers.public_routers import public_router
from routers.balance_routers import balance_router


app = FastAPI()

app.include_router(public_router)
app.include_router(balance_router)

#TODO: маршруты, users api key в бд

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)