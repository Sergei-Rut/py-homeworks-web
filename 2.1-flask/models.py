from app import db
from datetime import datetime


class BaseModelMixin:

    def add(self):
        db.session.add(self)
        db.session.commit()

    def commit(self):
        db.session.commit()


class Advertisement(db.Model, BaseModelMixin):
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
