from aiohttp import web
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import json

from db import Session, Advert, init_orm, close_orm
from advert_schemas import AdvertCreate, AdvertUpdate

app = web.Application()

#================ORM================
async def orm_context(app: web.Application):
    print("START ORM")
    await init_orm()
    yield
    await close_orm()
    print("END ORM")

#===================Session================
@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request["session"] = session
        return await handler(request)

#===================Регистрация================
app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)

#===================HTTP-errors================

def get_http_error(err_cls: type[web.HTTPClientError],
                   err_msg: dict | list | str):
    return err_cls(
        text=json.dumps(err_msg),
        content_type="application/json"
    )


async def validate_request(request: web.Request, schema: type) -> dict:
    try:
        json_data = await request.json()
        return schema.model_validate(json_data).model_dump(exclude_none=True)
    except ValidationError as error:
        raise get_http_error(
            web.HTTPBadRequest,
            {"errors": json.loads(error.json())},
        )


#===================HTTP-методы================

class AdvertView(web.View):
    @property
    def session(self) -> AsyncSession:
        return self.request["session"]

    @property
    def advert_id(self) -> int:
        return int(self.request.match_info["advert_id"])

    async def get_advert(self) -> Advert:
        advert = await self.session.get(Advert, self.advert_id)
        if advert is None:
            raise get_http_error(web.HTTPNotFound, {"error": "Advert not found"})
        return advert

    async def add_advert(self, advert: Advert):
        self.session.add(advert)
        try:
            await self.session.commit()
        except IntegrityError:
            raise get_http_error(web.HTTPConflict, {"error": "Advert already exists"})


    async def get(self):
        advert = await self.get_advert()
        return web.json_response(advert.dict)


    async def post(self):
        json_data = await validate_request(self.request, AdvertCreate)
        advert = Advert(
            title=json_data["title"],
            description=json_data["description"],
            owner=json_data["owner"]
        )
        await self.add_advert(advert)
        return web.json_response(advert.id_dict)

    async def patch(self):
        json_data = await validate_request(self.request, AdvertUpdate)
        advert = await self.get_advert()
        advert.title = json_data["title"]
        advert.description = json_data["description"]
        if "owner" in json_data:
            advert.owner = json_data["owner"]
        await self.add_advert(advert)
        return web.json_response(advert.id_dict)

    async def delete(self):
        advert = await self.get_advert()
        await self.session.delete(advert)
        await self.session.commit()
        return web.json_response({"message": "Advert deleted"})

app.add_routes([
    web.get(r"/adverts/{advert_id:\d+}", AdvertView),
    web.post("/adverts", AdvertView),
    web.patch(r"/adverts/{advert_id:\d+}", AdvertView),
    web.delete(r"/adverts/{advert_id:\d+}", AdvertView),
])

web.run_app(app)
