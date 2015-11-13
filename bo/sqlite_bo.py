__author__ = 'gongxingfa'

from datetime import datetime
from pony.orm import *
import os, sys
import inspect

file_path = inspect.getfile(inspect.currentframe())
current_dir_path = file_path[0:file_path.rindex('/')]

db = Database("sqlite", os.path.join(current_dir_path, 'stocks_analyze.db'))


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


sql_debug(True)
db.generate_mapping(create_tables=False)
