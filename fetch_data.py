import asyncio
import json
from datetime import datetime

import aiohttp


API_KEY = "368662db261f1e3f7461aa0ecdae097b"


def write_to_file(data):
    with open("fetched_data.json", "w") as jf:
        # json.dump(data, jf)
        print(*data, datetime.utcnow(), sep="\n")


async def fetch(session, url, city):
    async with session.get(url) as response:
        data = await response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "pressure": data["main"]["pressure"],
            "wind": data["wind"]["speed"],
        }


async def main(city_names):
    async with aiohttp.ClientSession() as session:
        for _ in range(3):
            data = await asyncio.gather(
                *[
                    fetch(
                        session,
                        f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid="
                        + API_KEY,
                        city,
                    )
                    for city in city_names
                ]
            )
            write_to_file(data)
            await asyncio.sleep(5)


city_names = ["London", "Paris", "Moscow"]

asyncio.run(main(city_names))
