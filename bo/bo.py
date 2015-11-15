__author__ = 'gongxingfa'

from pony.orm import *
import inspect
import os

# file_path = inspect.getfile(inspect.currentframe())
# current_dir_path = file_path[0:file_path.rindex('/')]
# db = Database("sqlite", os.path.join(current_dir_path, 'stocks_analyze.db'))


db = Database()
db.bind('mysql', host='localhost', user='root', passwd='root', db='stocks')


class Stock(db.Entity):
    _table_ = "stock"
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    code = Required(str)
    local = Optional(str)
    url = Optional(str)



class Sessions(db.Entity):
    _table_ = "sessions"
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
    change_amount = Optional(float)
    change_rate = Optional(float)
    turnover_rate = Optional(float)
    quantity_relative = Optional(float)
    volume = Optional(str)
    turnover = Optional(str)
    price_earnings = Optional(float)
    price_book = Optional(float)
    total_market_cap = Optional(str)
    tradable_market_cap = Optional(str)
    date_time = Optional(str)


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
    change_amount = Optional(float)
    change_rate = Optional(float)
    date_time = Optional(str)


class Stock_Index(db.Entity):
    _table_ = "stock_index"
    id = PrimaryKey(int, auto=True)
    code = Optional(str)
    name = Optional(str)
    latest_price = Optional(float)
    change_amount = Optional(float)
    change_rate = Optional(float)
    volume = Optional(int)
    turnover = Optional(int)
    prev_close = Optional(float)
    open = Optional(float)
    highest = Optional(float)
    lowest = Optional(float)
    date_time = Optional(str)


sql_debug(True)
db.generate_mapping(create_tables=False)
