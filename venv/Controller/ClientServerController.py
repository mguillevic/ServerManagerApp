from json import load
from urllib.request import urlopen
from Model.ClientServerModels import ClientModel,ServerModel,ServerClientLink
from sqlalchemy import select, exc


def create_client(ip,session):
    url = 'https://ipinfo.io/' + ip + '/json'
    res = urlopen(url)
    # response from url(if res==None then check connection)
    data = load(res)
    loc = data['loc'].split(',')
    client_model = ClientModel(ip=ip, latitude=float(loc[0]), longitude=float(loc[1]))
    try:
        session.add(client_model)
        session.commit()
    except:
        session.rollback()
        print("An exception occurred")
    return client_model

def get_all_clients(session):
    stmt = select(ClientModel)
    return session.execute(stmt).scalars()

def create_server(session,ip):
    url = 'https://ipinfo.io/' + ip + '/json'
    res = urlopen(url)
    # response from url(if res==None then check connection)
    data = load(res)
    loc = [37.7725,-122.415]
    if "loc" in data:
        loc = data['loc'].split(',')
    server_model = ServerModel(ip=ip, latitude=float(loc[0]), longitude=float(loc[1]),down = False)
    try:
        session.add(server_model)
        session.commit()
    except exc.SQLAlchemyError as e:
        session.rollback()
        print(str(e.orig))
    return server_model

def update_down_status(session,ip,down):
    try:
        server = session.query(ServerModel).filter(ServerModel.ip==ip).update({'down':down})
        session.commit()
    except:
        session.rollback()
        print("An exception occurred")

def get_server_down(session,ip):
    return session.query(ServerModel.down).filter(ServerModel.ip == ip).scalar()

def update_cpu_ram_from_server_ip(session, ip, cpu, ram,latence):
    server=None
    try:
        server = session.query(ServerModel).filter(ServerModel.ip==ip)\
            .update({'cpu_usage':cpu})\
            .update({'available_ram':ram})\
            .update({'latency':latence})
        session.commit()
    except:
        session.rollback()
        print("An exception occurred")
    return server

def insert_client_server_link(session,client_id,server_id,distance):
    link = ServerClientLink(client_id=client_id, server_id=server_id, distance=distance)
    try:
        print(link.server_id)
        session.add(link)
        session.commit()
    except:
        session.rollback()
        print("An exception occurred")
    return link

def get_all_servers(session):
    stmt = select(ServerModel)
    return session.execute(stmt).scalars()

def get_client_by_ip(session,ip):
    stmt = select(ClientModel).where(ClientModel.ip==ip)
    return session.execute(stmt).scalar()

def get_server_by_id(session,id):
    return session.query(ServerModel).get(id).scalar()


def get_client_by_id(session,id):
    return session.query(ClientModel).get(id).scalar()


def get_servers_by_client_id(session,client_id):
    stmt = select(ServerModel).join(ServerClientLink).where(ServerClientLink.client_id == client_id).where(ServerModel.id==ServerClientLink.server_id).order_by(ServerClientLink.distance)
    return session.execute(stmt).scalars()