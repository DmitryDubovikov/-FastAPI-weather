import uvicorn
from fastapi import FastAPI

from weather.router import router as router_weather

app = FastAPI(title="Weather")


@app.get("/")
async def hello():
    return {"message": "Hello World!"}


app.include_router(router_weather)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
