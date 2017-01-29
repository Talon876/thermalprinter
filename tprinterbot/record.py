#!/usr/bin/python
# coding=utf-8

import peewee as pw
import datetime

db = pw.SqliteDatabase(None)


class BaseModel(pw.Model):
    class Meta:
        database = db


class ChatMessageLog(BaseModel):
    timestamp = pw.DateTimeField(default=datetime.datetime.utcnow, index=True)
    username = pw.TextField()
    message = pw.TextField()


def init_db(dbname='chatlog.db'):
    db.init(dbname)
    db.connect()
    db.create_tables([ChatMessageLog], safe=True)


def log_message(name, msg):
    msg_model = ChatMessageLog(username=name, message=msg)
    msg_model.save()


def test():
    init_db('test.db')
    log_message('bro', u'abc (ง ͠° ل͜ °)ง ')


if __name__ == '__main__':
    test()
