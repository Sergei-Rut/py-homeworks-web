from datetime import datetime

import gino
from aiohttp import web

db = gino.Gino()


class NotFound(Exception):
    pass


@web.middleware
async def not_found_handler(request, handler):
    try:
        response = await handler(request)
    except NotFound:
        response = web.json_response({'error': ' Not found'}, status=404)
    return response


class Advertisement(db.Model):
    __tablename__ = 'advertisement'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    owner = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'Advertisement:{self.title}, date: {self.created_at}'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'owner': self.owner
        }


