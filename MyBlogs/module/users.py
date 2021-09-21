from sqlalchemy import Table
from common.database import dbconnect

dbsession,DBase,md = dbconnect()
class Users(DBase):
    __table__ = Table('users', md, autoload=True)   #autoload=True,自动提交事务

    def find_all(self):
        result = dbsession.query(Users).all()


