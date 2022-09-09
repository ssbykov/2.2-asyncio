import asyncio
import datetime

import aiohttp
from models import People, engine, Base, async_session_maker

URL = 'https://swapi.dev/api/people/'

CHUNK_SIZE = 10

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def get_people(session, people_id):
    result = await session.get(f'{URL}{people_id}')
    return await result.json()

async def incert_people(people):
    people_list = [People(
        name=item['name'],
        birth_year=item['birth_year'],
        eye_color=item['eye_color'],
        films=', '.join(item['films']),
        gender=item['gender'],
        hair_color=item['hair_color'],
        height=item['height'],
        homeworld=item['homeworld'],
        mass=item['mass'],
        skin_color=item['skin_color'],
        species=', '.join(item['species']),
        vehicles=', '.join(item['vehicles']),
        starships=', '.join(item['starships'])
    ) for item in people]

    async with async_session_maker() as orm_session:
        orm_session.add_all(people_list)
        await orm_session.commit()


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    async with aiohttp.ClientSession() as web_session:
        n = 1
        while True:
            coros = [get_people(web_session, i) for i in range(n, n + CHUNK_SIZE)]
            people = await asyncio.gather(*coros)
            people = [item for item in people if not item.get('detail')]
            if not people:
                break
            in_p = incert_people(people)
            task = asyncio.create_task(in_p)
            await task
            n += CHUNK_SIZE

start = datetime.datetime.now()
asyncio.run(main())
print(f'Время выполнения: {datetime.datetime.now() - start}')
