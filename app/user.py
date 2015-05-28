__author__ = 'rjr862'
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(String , primary_key=True)
    password = Column(String)
    email = Column(String)
    sessionid = Column(String)
    sessionstate = Column(String)

    def __repr__(self):
        return "<User(username='%s', password='%s', email='%s', sessionid='%s', sessionstate='%s')>" % (self.username, self.password, self.email, self.sessionid, self.sessionstate)

