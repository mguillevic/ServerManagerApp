from Controller.ClientServerController import create_client, create_server, get_all_clients, \
insert_client_server_link, update_cpu_ram_from_server_ip, get_all_servers, get_servers_by_client_id, get_client_by_ip
from Controller.GameController import get_game_by_name
from Model.ServerManagerModel import ServerManagerModel
from Model.ClientServerModels import ServerModel,ClientModel,ServerClientLink
from Remote.ClientThread import ClientThread
from json import load
from urllib.request import urlopen
import hashlib
import socket
from sqlalchemy import select, exists

#multithread to get cpu and ram
threads = []

def create_server_manager_model(session,port):
    url = 'https://ipinfo.io/json'
    res = urlopen(url)
    # response from url(if res==None then check connection)
    data = load(res)
    ip = data['ip']
    server_manager = ServerManagerModel(ip=ip, port=port)
    try:
        session.add(server_manager)
        session.commit()
    except:
        session.rollback()
        print("An exception occurred")
    return server_manager


def get_server_manager_model_by_ip(session,ip):
    stmt = select(ServerManagerModel).where(ServerManagerModel.ip==ip)
    return session.execute(stmt).scalars()

def add_server(request,session):
    server_model = create_server(session,request['ip'])
    clients = get_all_clients(session)
    url = 'https://ipinfo.io/json'
    res = urlopen(url)
    # response from url(if res==None then check connection)
    data = load(res)
    ip = data['ip']
    server_manager = get_server_manager_model_by_ip(session,ip)
    begin_thread_for_server_node(server_model.ip,session)
    for client in clients:
        lat_dist = abs(server_model.latitude - client.latitude)
        long_dist = abs(server_model.longitude - client.longitude)
        distance = (lat_dist+long_dist)/2
        insert_client_server_link(session,client.id,server_model.id,distance)


def change_server_properties(ip,cpu,ram,latence,session):
    update_cpu_ram_from_server_id(session,ip,cpu,ram,latence)


def handle_client_connection(session,request):
    #if new client create client
    ip = request['ip']
    exist = session.query(exists(ClientModel).where(ClientModel.ip==ip)).scalar()
    if not exist :
        new_client = create_client(ip,session)
        servers = get_all_servers(session)
        distances = []
        for server in servers:
            lat_dist = abs(server.latitude - new_client.latitude)
            long_dist = abs(server.longitude - new_client.longitude)
            distance= (lat_dist+long_dist)/2;
            insert_client_server_link(session, new_client.id, server.id, distance)
    else:
        new_client = get_client_by_ip(session,ip)
    #for the client
    game = get_game_by_name(session,request['game'])
    links_client = get_servers_by_client_id(session,new_client.id)
    for serv in links_client:
        #add latency criteria
        if serv.cpu_usage<game.cpu_usage and serv.available_ram > game.ram and serv.latency<0.15 and not serv.down:
            return serv.ip

    #if no server works
    return -1

def begin_thread_for_server_node(server_ip,session):
    newthread = ClientThread(server_ip,session)
    newthread.start()
    threads.append(newthread)

