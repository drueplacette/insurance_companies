from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from Base import Base

class SearchOption(Base):
    '''ORM model for records in the 'search_options' table'''
    __tablename__ = 'search_options'

    id = Column(Integer)
    company_id = Column(Integer, ForeignKey('companies.id'))
    option_number = Column(Integer)
    field1 = Column(String)
    field2 = Column(String)
    field3 = Column(String)
    field4 = Column(String)
    field5 = Column(String)
    field6 = Column(String)

    company = relationship('Company', backref=backref('search_options', order_by=id))

    def __init__(self, company_id, option_number, field1='', field2='', field3=''
                                                  field4='', field5='', field6=''):
        self.company_id = company_id
        self.option_number = option_number
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3
        self.field4 = field4
        self.field5 = field5
        self.field6 = field6

    def __repr__(self):
        return '< SearchOption: ({}, {}, {}, {}, {}, {}, {}, {} )>'.format(
               self.company_id, self.option_number,
               self.field1, self.field2, self.field3,
               self.field4, self.field5, self.field6)
