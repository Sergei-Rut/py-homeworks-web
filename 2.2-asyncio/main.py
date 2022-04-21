import asyncio
import aiohttp
from more_itertools import chunked
import asyncpg
import config
from typing import Iterable

import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

URL = "https://swapi.dev/api/people/"
LIST_PARAM = (
    'name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender', 'homeworld', 'films',
    'species', 'vehicles', 'starships')
BOTTLE_NECK = 10


async def get_person(session: aiohttp.client.ClientSession, person_id: int) -> dict:
    async with session.get(f"{URL}{person_id}") as resp:
        return await resp.json()


async def get_persons(session: aiohttp.client.ClientSession, range_person_id: Iterable[int]):
    for person_id_chunk in chunked(range_person_id, BOTTLE_NECK):
        get_person_tasks = [asyncio.create_task(get_person(session, person_id)) for person_id in person_id_chunk]
        persons = await asyncio.gather(*get_person_tasks)
        for person in persons:
            yield person


async def insert_people(pool: asyncpg.Pool, user_list):
    query = 'INSERT INTO people_swapi (name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, homeworld, films, species, vehicles, starships) ' \
            'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)'
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(query, user_list)


async def main():
    pool = await asyncpg.create_pool(config.PG_DSN, min_size=20, max_size=20)
    data = {}
    async with aiohttp.ClientSession() as session:
        async for person in get_persons(session, range(1, 100)):
            for key, value in person.items():
                if key in LIST_PARAM:
                    data[key] = value
            # print(len(data))
            await insert_people(pool, data.values())
    await pool.close()


if __name__ == '__main__':
    asyncio.run(main())
