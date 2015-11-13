__author__ = 'GongXingFa'

from bo.bo  import Simple_Sessions
from pony.orm import select, db_session, commit
from splinter import Browser


with db_session:
    ss = select(ss for ss in Simple_Sessions if ss.change_rate>0)[:]
    print(len(ss))



