from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import relationship
engine = create_engine("mysql+pymysql://user:RdsDb120922@cloud-gaming.cvdwrd5aphyd.us-east-2.rds.amazonaws.com:3306/cloudgaming",echo = True)
Base = declarative_base(bind=engine)

class ServerModel(Base):
    __tablename__ = 'server_node'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    cpu_usage = Column(Float)
    available_ram = Column(Float)
    latency = Column(Float)
    down = Column(Boolean)

    client_list = relationship('ClientModel', secondary='server_client_link', back_populates='server_list')

class ClientModel(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)

    server_list = relationship("ServerModel",secondary="server_client_link",back_populates='client_list')

class ServerClientLink(Base):
   __tablename__ = 'server_client_link'

   server_id = Column(
      Integer,
      ForeignKey('server_node.id'),
      primary_key = True)

   client_id = Column(
      Integer,
      ForeignKey('client.id'),
      primary_key=True)

   distance = Column(
      Float
   )

Base.metadata.create_all()