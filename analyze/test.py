__author__ = 'GongXingFa'

from bo.bo  import Stocks, Stocks2
from pony.orm import select, db_session, commit
from splinter import Browser

browser = Browser('phantomjs')


@db_session
def get_stocks():
    return select(s for s in Stocks if s.id > 1844)

@db_session
def save_correct_stocks():
    stocks = get_stocks()
    for s in stocks:
        url = s.url
        browser.visit(url)
        r = browser.find_by_id('realprice')
        if not r:
            Stocks2(name=s.name, code=s.code, local=s.local, url=s.url)
            commit()

save_correct_stocks()



