import uvicorn
from fastapi import FastAPI
from public_routers import router


app = FastAPI()

app.include_router(router)


#TODO: маршруты

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)