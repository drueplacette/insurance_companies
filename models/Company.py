from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship, backref
from .Base import Base

class Company(Base):
    '''ORM model for records in the 'companies' table'''
    __tablename__ = 'companies'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String)
    payer_id = Column(String)

    search_options = relationship("SearchOption", order_by="SearchOption.option_number", backref="company")

    def __init__(self, name, payer_id=''):
        self.name = name
        self.payer_id = payer_id

    def __repr__(self):
        return '< Company ({}, {}) >'.format(self.name, self.payer_id)

    def jsonify(self):
        '''Convert model to dictionary for the API server to serve'''
        return { "name":self.name, "payer_id":self.payer_id }
