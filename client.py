import asyncio

import aiohttp


BASE_URL = "http://127.0.0.1:8080"


async def print_response(name: str, response: aiohttp.ClientResponse):
    print(f"\n{name}")
    print("Статус:", response.status)
    print("Ответ:", await response.json())


async def main():
    async with aiohttp.ClientSession() as client:
        # 1. Нет title — ожидается 400
        response = await client.post(
            f"{BASE_URL}/adverts",
            json={
                "description": "Описание объявления",
                "owner": "user_1",
            },
        )
        await print_response("POST без title", response)

        # 2. Пустой title — ожидается 400
        response = await client.post(
            f"{BASE_URL}/adverts",
            json={
                "title": "   ",
                "description": "Описание объявления",
                "owner": "user_1",
            },
        )
        await print_response("POST с пустым title", response)

        # 3. Корректное объявление — ожидается 200
        response = await client.post(
            f"{BASE_URL}/adverts",
            json={
                "title": "Продам велосипед",
                "description": "Почти новый велосипед в хорошем состоянии",
                "owner": "user_1",
            },
        )
        await print_response("Корректный POST", response)

        # Подставьте сюда id из ответа предыдущего запроса.
        advert_id = 1

        # 4. PATCH без description — ожидается 400
        response = await client.patch(
            f"{BASE_URL}/adverts/{advert_id}",
            json={
                "title": "Новое название",
            },
        )
        await print_response("PATCH без description", response)

        # 5. PATCH с пустым description — ожидается 400
        response = await client.patch(
            f"{BASE_URL}/adverts/{advert_id}",
            json={
                "title": "Новое название",
                "description": "   ",
            },
        )
        await print_response("PATCH с пустым description", response)

        # 6. Корректное изменение — ожидается 200
        response = await client.patch(
            f"{BASE_URL}/adverts/{advert_id}",
            json={
                "title": "Велосипед со скидкой",
                "description": "Состояние отличное, возможен торг",
            },
        )
        await print_response("Корректный PATCH", response)


asyncio.run(main())