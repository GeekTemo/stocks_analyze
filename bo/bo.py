__author__ = 'gongxingfa'

from pony.orm import *

db = Database("sqlite", "database.sqlite", create_db=True)


class Simple_Sessions(db.Entity):
    _table_ = "simple_sessions"
    id = PrimaryKey(int, auto=True)
    open = Optional(str)
    prev_close = Optional(str)
    highest_price = Optional(str)
    lowest_price = Optional(str)
    limit_up = Optional(str)
    limit_down = Optional(str)
    close = Optional(str)
    grains = Optional(str)
    gains_drop = Optional(float)


sql_debug(True)
db.generate_mapping(create_tables=True)
