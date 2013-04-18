from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from .Base import Base

class Company(Base):
    '''ORM model for records in the 'companies' table'''
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    payer_id = Column(String)

    search_options = relationship("SearchOption", order_by="SearchOption.option_number", backref="company")

    def __init__(self, name, payerid=''):
        self.name = name
        self.payer_id = payerid

    def __repr__(self):
        return '< Company ({}, {}) >'.format(self.name, self.payerid)
