import asyncio
import aiohttp


async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8080') as resp:
            print(resp.status)
        async with session.get('http://127.0.0.1:8080/health') as resp:
            print(await resp.json())
        # async with session.post('http://127.0.0.1:8080/advertisement', json={
        #     "title": "3 adv",
        #     "description": "3 adv",
        #     "owner": "3 owner"
        # }) as resp:
        #     print(await resp.json())
        async with session.get('http://127.0.0.1:8080/advertisement/1') as resp:
            print(await resp.json())
        async with session.patch('http://127.0.0.1:8080/advertisement/2', json={
            "title": "22 adv"
        }) as resp:
            print(await resp.json())
        async with session.delete('http://127.0.0.1:8080/advertisement/1') as resp:
            print(await resp.json())


asyncio.run(main())