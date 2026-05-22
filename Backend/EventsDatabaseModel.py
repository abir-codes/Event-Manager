from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True)
    password = Column(String)
    events = relationship("Eventdb", back_populates="owner")

class Eventdb(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    category = Column(String)
    due_date = Column(String)
    priority = Column(String)
    status = Column(String)
    notes = Column(String)
    owner_id = Column(Integer,ForeignKey("users.id"))
    owner = relationship("User",back_populates="events")