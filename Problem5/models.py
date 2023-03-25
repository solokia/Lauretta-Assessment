""" This file contains ORM structure and metadata """

from datetime import datetime
from sqlalchemy import  Column, Integer, String, DateTime
from database import Base
from passlib.context import CryptContext

class User(Base):
    """ creates table in the database when the app boots """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username: str = Column(String,unique=True) # this should prevent users with the same username
    hashed_password: str = Column(String)

    date_created: datetime = Column(DateTime, default=datetime.now)
    date_modified: datetime = Column(DateTime, default=datetime.now)

    def verify_password(self, password: str):
        hash_helper = CryptContext(schemes=["bcrypt"])
        return hash_helper.verify(password, self.hashed_password)