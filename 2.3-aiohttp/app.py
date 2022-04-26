from aiohttp import web

from models import db, not_found_handler
from view import AdvertisementView

import config


async def init_orm(app):
    print('start')
    await db.set_bind(config.POSTGRE_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
    print('stop')


async def health(request: web.Request):
    return web.json_response({'status': 'OK'})


app = web.Application(middlewares=[not_found_handler])
app.add_routes([web.get('/health', health)])
app.add_routes([web.get('/advertisement/{adv_id:\d+}', AdvertisementView)])
app.add_routes([web.delete('/advertisement/{adv_id:\d+}', AdvertisementView)])
app.add_routes([web.patch('/advertisement/{adv_id:\d+}', AdvertisementView)])
app.add_routes([web.post('/advertisement', AdvertisementView)])
app.cleanup_ctx.append(init_orm)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
