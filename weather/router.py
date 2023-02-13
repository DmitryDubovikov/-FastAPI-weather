from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy import select, insert
from database import get_async_session
from weather.models import city, weather
from weather.schemas import CitySchema, WeatherSchema

router = APIRouter(prefix="", tags=["Weather"])


@router.post("/weather/")
async def add_city(
    new_city: CitySchema, session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(city).values(**new_city.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/last_weather/")
async def get_last_weather(session: AsyncSession = Depends(get_async_session)):
    query = select(weather)
    result = await session.execute(query)
    res = result.all()
    return {"result": res}


@router.get("/city_stats/")
async def get_city_stats(
    city_name: str, session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(
            weather.c.id,
            city.c.id,
            city.c.name,
            weather.c.time,
            weather.c.temperature,
            weather.c.pressure,
            weather.c.wind,
            func.avg(weather.c.temperature).over(partition_by=city.c.id),
            func.avg(weather.c.pressure).over(partition_by=city.c.id),
            func.avg(weather.c.wind).over(partition_by=city.c.id),
        )
        .join(city)
        .where(city.c.name == city_name)
    )
    result = await session.execute(query)
    print(city_name)
    print(query)
    # print(result.all())
    return {"result": result.all()}
