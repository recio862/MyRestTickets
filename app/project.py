__author__ = 'rjr862'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()
'''
Class representing the MySQL table for Projects
Note: Not currently being used, I mainly put it
here to outline the structure of the table in the database
'''
class Project(Base):
    __tablename__ = 'projects'
    p_id = Column(Integer , primary_key=True)
    project_name = Column(String)
    project_category = Column(String)
    project_description = Column(String)
    date_created = Column(DateTime)
    created_by = Column(String)

    def __repr__(self):
        return "<User(p_id='%s', project_name='%s', project_category='%s', project_description='%s', date_created='%s', created_by='%s')>" % (self.p_id, self.project_name, self.project_category, self.project_description, self.date_created, self.created_by)

