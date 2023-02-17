from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy import select, text
from database import get_async_session
from weather.models import city, weather
from weather.schemas import CitySchema, WeatherSchema

router = APIRouter(prefix="", tags=["Weather"])


@router.post("/weather/{city_name}")
async def add_city(city_name: str, session: AsyncSession = Depends(get_async_session)):
    # TODO: добавить проверку, что город есть в openweathermap
    stmt = city.insert().values({"name": city_name})
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/last_weather/")
async def get_last_weather(
    search: str = "", session: AsyncSession = Depends(get_async_session)
):
    qstr = """
    SELECT *
    FROM
    (SELECT weather.id,
            city_id,
            city.name,
            TIME,
            temperature,
            pressure,
            wind,
            Row_number() OVER (PARTITION BY city_id
                                ORDER BY TIME DESC) AS r_num
    FROM public.weather
    INNER JOIN city ON city.id = weather.city_id
    AND TRUE) AS decorated
    WHERE r_num = 1
    """
    if search:
        qstr = qstr.replace("AND TRUE", f"AND city.name like '%{search}%'")
    else:
        qstr = qstr.replace("AND TRUE", "")
    result = await session.execute(text(qstr))
    # res = result.all()
    # print(res, type(res))
    # return {"result": res}
    print(result.all())
    return result.all()


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
    # print(city_name)
    # print(query)
    # print(result.all())
    # return {"result": result.all()}
    return result.all()
