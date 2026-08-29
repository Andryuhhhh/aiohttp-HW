import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as client:

        response = await client.post(
            'http://localhost:8080/adverts',
            json={"title": "hello", "description": "world", "owner": "user_1"},
        )
        print(response.status)
        print(await response.json())

        # response = await client.post(
        #     'http://localhost:8080/adverts',
        #     json={"title": "hello2", "description": "world2", "owner": "user_2"},
        # )
        # print(response.status)
        # print(await response.json())
        #
        # # response = await client.get(
        # #     'http://127.0.0.1:8080/adverts/1',
        # # )
        # # print(response.status)
        # # print(await response.json())
        #
        # response = await client.patch(
        #     'http://127.0.0.1:8080/adverts/1',
        #     json={
        #         "title": "title_text",
        #         "description": "description_text",
        #         "owner": "owner_text"
        #           }
        # )
        # print(response.status)
        # print(await response.json())





asyncio.run(main())
