from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    category = Column(String(20), nullable=False, default=True)
    @property
    def serialize(self):
        return {
            'id'  : self.id,
            'name' : self.name,
            'category' : self.category
        }


class Rooms(Base):
    __tablename__ = 'parties'

    id = Column(Integer, primary_key=True)
    category = Column(String(250))
    count = Column(Integer, default=5)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'category' : self.category,
            'count' : self.count,
        }

engine = create_engine('sqlite:///resortbooking.db')


Base.metadata.create_all(engine)
