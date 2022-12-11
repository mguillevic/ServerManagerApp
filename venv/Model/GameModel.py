from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
Base = declarative_base()
from sqlalchemy.orm import relationship
class GameModel(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    cpu_usage = Column(Float)
    ram = Column(Float)

