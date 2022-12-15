from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import relationship

class ServerManagerModel(Base):
    __tablename__ = 'server_manager'

    id = Column(Integer, primary_key=True)
    ip = Column(String(20))
    port = Column(Integer)



