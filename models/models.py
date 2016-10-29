from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from configure.database import Base
print('testtesttest')
class Test(Base):
	__tablename__ = 'test'
	id = Column(Integer, primary_key= True, autoincrement=True)
	test = Column(Integer)
	test1 = Column(Integer)
	test2 = Column(String)
	test3 = Column(String)


	def __init__(self, id, test, test1, test2, test3):
		self.id = id
		self.test = test
		self.test1 = test1
		self.test2 = test2
		self.test3 = test3


	def __repr__(self):
		return (self.id, self.test, self.test1, self.test2, self.test3)
