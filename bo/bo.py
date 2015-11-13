__author__ = 'gongxingfa'

from peewee import *

file_path = inspect.getfile(inspect.currentframe())
current_dir_path = file_path[0:file_path.rindex('/')]
db = SqliteDatabase(os.path.join(current_dir_path, 'stocks_analyze.db'))


class BaseModel(Model):
    class Meta:
        database = db

class Stocks(BaseModel):
    pass
