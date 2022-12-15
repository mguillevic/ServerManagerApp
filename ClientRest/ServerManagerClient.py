import requests

def get_cpu_and_ram_from_server(server_ip):
    url = "http://" + server_ip + ":5000/get/cpu/and/ram"
    req = requests.get(url=url)
    return req