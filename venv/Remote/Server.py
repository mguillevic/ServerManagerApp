from .ClientThread import ClientThread
from Controller.ServerManagerController import get_ip_and_port
import socket
from threading import Thread
from socketserver import ThreadingMixIn


def run(manager):
    # Multithreaded Python server : TCP Server Socket Program Stub
    print(manager.port)
    print(manager.ip)
    TCP_IP = manager.ip
    TCP_PORT = manager.port
    BUFFER_SIZE = 20  # Usually 1024, but we need quick response

    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((TCP_IP, TCP_PORT))
    threads = []

    while True:
        tcpServer.listen(4)
        print("Multithreaded Python server : Waiting for connections from TCP clients...")
        (conn, (ip, port)) = tcpServer.accept()
        newthread = ClientThread(ip, port,conn)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()