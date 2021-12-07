from __future__ import annotations

from peewee import *

db = SqliteDatabase('local-storage.db')


class BaseModel(Model):
    class Meta:
        database = db


class Study(BaseModel):
    id = AutoField()
    title = CharField()
    abstract = TextField()
    eid = CharField(null=True)


def create_tables():
    db.create_tables([Study])
