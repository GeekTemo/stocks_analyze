__author__ = 'gongxingfa'

from bo.bo import Simple_Sessions, Stock_Index
from pony.orm import db_session, commit

@db_session
def simple_sessions_handler(data):
    simple_sessions = Simple_Sessions()
    simple_sessions.set(**data)
    commit()


@db_session
def stock_index_handler(data):
    stock_indexs = data
    for si in stock_indexs:
        stock_index = Stock_Index()
        stock_index.set(**si)
        commit()