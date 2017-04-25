from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    aadhar = Column(String(13), nullable=False)
    voted = Column(Boolean, nullable=False, default=False)
    @property
    def serialize(self):
        return {
            'aadhar'  : self.aadhar,
            'id' : self.id,
            'voted' : self.voted
        }


class Parties(Base):
    __tablename__ = 'parties'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    imageUrl = Column(String(250))
    count = Column(Integer, default=0)
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'imageUrl' : self.imageUrl,
            'count' : self.count,
        }

engine = create_engine('sqlite:///votingsystem.db')


Base.metadata.create_all(engine)