__author__ = 'gongxingfa'

from pony.orm import *

db = Database()


class Stocks(db.Entity):
    _table_ = "stocks"
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    code = Optional(str)
    local = Optional(str)
    url = Optional(str)


class Simple_Sessions(db.Entity):
    _table_ = "simple_sessions"
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    code = Optional(str)
    open = Optional(float)
    prev_close = Optional(float)
    highest_price = Optional(float)
    lowest_price = Optional(float)
    limit_up = Optional(float)
    limit_down = Optional(float)
    close = Optional(float)
    grains = Optional(float)
    gains_drop = Optional(float)
    date_time = Optional(str)


db.bind('mysql', host='localhost', user='root', passwd='root', db='stocks')
sql_debug(True)
db.generate_mapping(create_tables=False)
