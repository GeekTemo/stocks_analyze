# -*- coding:utf-8 -*-
__author__ = 'gongxingfa'

from pony.orm import db_session
from bo.sqlite_bo import Simple_Sessions
import json
from pony.orm import db_session, commit


def new_obj_from_dict(cls, d):
    obj = cls()
    for key, value in items(d):
        setattr(obj, key, value)
    return obj

@db_session
def write_simple_sessions(simple_sessions):
    data = json.loads(simple_sessions)
    ss = new_obj_from_dict(Simple_Sessions, data)
    commit()


def writer(ch, method, properties, body):
    write_simple_sessions(str(body))
    print(" [x] Received %s" % (str(body),))

def start_writer():
    import pika
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='simple_sessions')
    channel.basic_consume(writer,
                      queue='simple_sessions',
                      no_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    start_writer()