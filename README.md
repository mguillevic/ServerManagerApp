# ServerManagerApp

## Load balancer configuration
To distribute the work load between the different manager server, we used  the "azure for students" subscription.
Here are the different configurations : 
- Nom : LB1
- Nom configuration IP frontale : frontIP_LB1
- Nom adresse IP publique : publicIP_LB1
- IP publique : 20.242.152.92
- Type : public
- Pool principaux : PoolBackEnd_ServerManager

If a manager server is added to the architecture you need to add it to the main pool.
To distribute the workload, we need to add some rules so the load balancer can make the right redirections.
Here we want to be able to :
- Ask for html ressources on managers : Rule for port 80
- Make requests on managers' API exposed on port 9090

Here are the configurations : 
- Name : Rule_LB1 et Rule_LB1_9090
- Adresse IP front-end : publicIP_LB1
- Pool principal : PoolBackEnd_ServerManager
- Protocole : TCP
- Persistance de session : Adresse IP cliente pour port 80 (le traffic en provenance d'un client est traîté par un même serveur tout au long d'une session) et Adresse IP cliente et protocole pour 9090.
- Port : 80 or 9090
- Port principal : 80 or 9090
- TCP rest : disabled
- Sonde d'intégrité : IntegrityProbe_LB1, protocole HTTP pour port 80 et TCP pour port 9090, intervalle toutes les 5 secondes.
- IP flottante : DESACTIVER.

To make a request to a server manager's API through the load balancer we use the following url structure:
- http://20.242.152.92:9090/endpoint

Play the game:
- http://20.242.152.92:9090/play/game_name/ip_client

Add a game: 
- http://20.242.152.92:9090/games
It's a post request. You can use postman to do it.
You need to pass the following json body
{
  'name':game_name,
  'cpu" : cpu_max,
  'ram' : min_ram,
  'port' : game_port
}


## Server manager configuration
Server managers are Azure VMs. For our student subscription, the VMs are in the ressource group CloudGaming_ServerManager.
VM's names are based on Debian 11 "Bullsey" image:
ServerManager1
ServerManager2
Subscription : Standard B1s (soit 1 vCPU, 1 CiB de mémoire, 1 GiB en SSD local, 100% de perfomance maximale de la VM)

"ServerManager1" configurations :
Type d'authentification : mot de passe
Nom utilisateur : ServerManager1
Mot de passe : ServerManager1!

"ServerManager2" configurations :
Type d'authentification : mot de passe
Nom utilisateur : ServerManager2
Mot de passe : ServerManager2!

Exposed ports : HTTP (80) et SHH (22) + 9090 for the rest API

OS disk : SSD Premium (conseillé pour charge de travail en production et sensible à la performance)

Daily automatic VM stop at midnight.

To connect to the VM which needs to be running, use ssh:
ssh -p 22 ServerManager1@20.25.75.224
Then enter the corresponding password.

ssh -p 22 ServerManager2@24.246.197.210
Then enter the corresponding password.

### Start API
To start the api you need to go in the following folder : /var/www/html/ServerManagerApp/
Since we are using python env you need to enter the command, it will activate the virtual environnement: 

source env/bin/activate

Then to start the api, execut:

uwsgi dev.ini

- Now you need to add the server nodes so that the manager can begin in a thread to get the server node data (cpu,ram,latency...)
To do so:
In postman or equivalent run the following post request for each server node:
http://ip_server_manager:9090/server/add
with json body:
{
  'ip': public_node_ip
  'private_ip': private_node_ip
}
This step is to be improved by automating it.

You are all done!

### Add a manager
When adding a manager you need to configure its environement so it can run our API.

Run following commands:

- sudo apt-get update
- python3 --version (to check if installed)
- sudo apt-get install python3.6 (if not installed)
- sudo apt-get install git-all (to install git if not installed)
- cd /var/www/html/
- git clone https://github.com/mguillevic/ServerManagerApp.git
- cd ServerManagerApp/
- sudo apt install python3-venv
- sudo apt-get install python3-pip
- python3 -m venv env
- pip install Flask
- pip install sqlalchemy
- pip install pymysql
- pip install psutil
- pip install requests
- pip install uwsgi
And you should be able to start the api

### API's content
 - Configurations file
 dev.ini will allow to indicate which port to use when requesting endpoints
 config.py allow to add configurations specific to the environment
 run.py Used by .ini files to run the api
 
 - REST
 __init__.py calling the different configuration according to the environnement
 ServerManagerRestApi contains the api endpoints
 
 - Controller
 All files contain the controllers for each model
 They allow to make all the logic algorithms as server node selection or add new client/server_node and make the transactions using to the database.
 
 - Model
 All database model objects such as ServerManager or game tables
 
 - Remote
 ClientThread to request server nodes data
 
 - ClientRest
 Methods to make the requests to the server nodes' apis.

 










