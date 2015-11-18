__author__ = 'gongxingfa'

import rows
from path import Path
from pony.orm import db_session, commit
from bo.bo import Stock, Sessions_History
import logging
logging.basicConfig(level=logging.WARNING, datefmt='%a, %d %b %Y %H:%M:%S')

STOCK_NAME_CODES = {}

with db_session:
    stocks = Stock.select_by_sql('select * from stock')[:]
    for s in stocks:
        STOCK_NAME_CODES[s.code] = s.name


def csv_files(data_dir):
    d = Path(data_dir)
    return d.files('*.csv')


def sessions_history(row):
    code = row.code[2:]
    name = STOCK_NAME_CODES.get(code, '*')
    open_price = row.open
    highest_price = row.high
    lowest_price = row.low
    close = row.close
    change_amount = close - open_price
    change_rate = row.change
    volume = row.volume
    turnover = row.turnover
    total_market_cap = row.market_value
    tradable_market_cap = row.traded_market_value
    price_earnings = row.ps_ttm
    price_book = row.pb
    date_time = str(row.date)
    return dict(name=name, code=code, open=open_price, highest_price=highest_price, lowest_price=lowest_price,
                close=close, change_amount=change_amount, change_rate=change_rate, volume=volume, turnover=turnover,
                total_market_cap=total_market_cap, tradable_market_cap=tradable_market_cap,
                price_earnings=price_earnings,
                price_book=price_book, date_time=date_time)


@db_session
def import_data(data_dir):
    for f in csv_files(data_dir):
        csv = rows.import_from_csv(str(f.realpath()))
        logging.warning('Import file:' + str(f.realpath()))
        csv = csv[::-1]
        s = sessions_history(csv[0])
        s['prev_close'] = csv[0].open
        sh = Sessions_History()
        sh.set(**s)
        commit()
        size = len(csv)
        for i in range(1, size):
            s = sessions_history(csv[i])
            s['prev_close'] = csv[i - 1].close
            sh = Sessions_History()
            sh.set(**s)
            commit()


if __name__ == '__main__':
    import_data('/Users/gongxingfa/Downloads/s_d')
