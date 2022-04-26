from aiohttp import web

from models import NotFound, Advertisement


class AdvertisementView(web.View):

    async def get(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv = await Advertisement.get(adv_id)
        if adv is None:
            raise NotFound
        return web.json_response(adv.to_dict())

    async def post(self):
        adv_data = await self.request.json()
        new_adv = await Advertisement.create(**adv_data)
        response = new_adv.to_dict()
        return web.json_response(response)

    async def delete(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv = await Advertisement.get(adv_id)
        if adv is None:
            raise NotFound
        else:
            await adv.delete()
        return web.json_response({'Advertisement': 'Advertisement delete'})

    async def patch(self):
        new_adv = await self.request.json()
        adv_id = int(self.request.match_info['adv_id'])
        adv = await Advertisement.get(adv_id)
        if adv is None:
            raise NotFound
        else:
            await adv.update(title=new_adv.get('title')).apply()
            await adv.update(description=new_adv.get('description')).apply()
        return web.json_response({'Advertisement': 'Advertisement patched'})
