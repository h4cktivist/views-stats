from sqlalchemy import Column, String, Integer
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)
