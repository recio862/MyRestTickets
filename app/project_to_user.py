__author__ = 'rjr862'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()
'''
Class representing the many-to-many MySQL table for projects_to_users
Note: Not currently being used, I mainly put it
here to outline the structure of the table in the database
'''
class Project(Base):
    __tablename__ = 'projects_to_users'
    p_id = Column(Integer , primary_key=True)
    username = Column(String)

    def __repr__(self):
        return "<User(p_id='%s', username='%s')>" % (self.p_id, self.username)

