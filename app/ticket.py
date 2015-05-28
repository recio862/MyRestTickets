__author__ = 'rjr862'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()
'''
Class representing the MySQL table for Tickets
'''
class Ticket(Base):
    __tablename__ = 'tickets'
    t_id = Column(Integer , primary_key=True)
    p_id = Column(Integer)
    ticket_name = Column(String)
    ticket_description = Column(String)
    date_created = Column(DateTime)

    def __repr__(self):
        return "<User(t_id='%s', p_id='%s', ticket_name='%s', ticket_description='%s', date_created='%s')>" % (self.t_id, self.p_id, self.ticket_name, self.ticket_description, self.date_created)

