import json
import socket
from threading import Thread
from socketserver import ThreadingMixIn
from ClientRest.ServerManagerClient import get_cpu_and_ram_from_server
from Controller.ClientServerController import update_cpu_ram_from_server_ip, get_server_down, update_down_status
import time
# Multithreaded Python server : TCP Server Socket Thread Pool

class ClientThread(Thread):

    def __init__(self, ip,session):
        Thread.__init__(self)
        self.ip = ip
        self.prev_time = time.time()
        self.session = session
        self.count_down = 0
        self.down = False

    def run(self):
        print("start")
        while True:
            current_time = time.time()
            if current_time-self.prev_time >= 5:

                try:
                    response = get_cpu_and_ram_from_server(self.ip)
                    if str(response) == "<Response [404]>":
                        print("error")
                        self.count_down = self.count_down+1
                        if self.count_down == 300:
                            self.down = True
                            update_down_status(self.session,self.ip,True)
                    else :
                        if get_server_down(self.session,self.ip):
                            self.down = False
                            update_down_status(self.session, self.ip, False)
                            self.count_down = 0
                        json_resp = response.json()
                        cpu = json_resp['cpu_usage']
                        ram = json_resp['available_ram']
                        latence = response.elapsed.total_seconds()
                        self.server_update_cpu_ram_from_server_ip(cpu,ram,latence)
                except Exception as e:    # This is the correct syntax
                    print(e)
                    self.count_down = self.count_down + 1
                    if self.count_down == 300:
                        self.down = True
                        update_down_status(self.session, self.ip, True)

                self.prev_time = time.time()

    def server_update_cpu_ram_from_server_ip(self,cpu,ram,latence):
        update_cpu_ram_from_server_ip(self.session,self.ip,cpu,ram,latence)