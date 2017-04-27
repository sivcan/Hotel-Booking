from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Users, Rooms

engine = create_engine('sqlite:///resortbooking.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

RoomType1 = Rooms(id=1, category='Delux ₹5000', count=5)
session.add(RoomType1)
session.commit()

RoomType2 = Rooms(id=2, category='Delux Two Bedroom Suite ₹9000', count=5)
session.add(RoomType2)
session.commit()

RoomType3 = Rooms(id=3, category='The Studio - 2 Queens Bed ₹16000', count=5)
session.add(RoomType3)
session.commit()
