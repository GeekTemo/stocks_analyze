__author__ = 'gongxingfa'

from datetime import datetime
from pony.orm import *

db = Database("sqlite", r'C:\Users\GongXingFa\PycharmProjects\stocks_analyze\bo\stocks_analyze.db')


class Stocks(db.Entity):
    _table_ = "stocks"
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    code = Required(str)
    local = Optional(str)
    url = Optional(str)

class Stocks2(db.Entity):
    _table_ = "stocks2"
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    code = Required(str)
    local = Optional(str)
    url = Optional(str)

class Simple_Sessions(db.Entity):
    _table_ = "simple_sessions"
    id = PrimaryKey(int, auto=True)
    open = Required(float)
    prev_close = Required(float)
    highest_price = Required(float)
    lowest_price = Required(float)
    limit_up = Required(float)
    limit_down = Required(float)
    close = Required(float)
    grains = Required(float)
    gains_drop = Required(float)
    date_time = Required(datetime)


sql_debug(True)
db.generate_mapping(create_tables=False)
