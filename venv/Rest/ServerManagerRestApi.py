from Rest import app

from Controller import ServerManagerController, GameController
from Controller.ClientServerController import create_client,get_all_clients
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker

import json
from flask import Flask, request,Response, jsonify

# sql connection
engine = create_engine("mysql+pymysql://user:RdsDb120922@cloud-gaming.cvdwrd5aphyd.us-east-2.rds.amazonaws.com:3306/cloudgaming",echo = True)
metadata = MetaData(engine)
metadata.reflect()
engine.connect()
Session  = sessionmaker(bind=engine)
session=Session()

@app.route('/server/manager/add',methods=['POST'])
def add_server_manager():
    ServerManagerController.create_server_manager_model(session,request.json['port'])
    return Response(status=201, mimetype='application/json')

@app.route('/server/add',methods=['POST'])
def add_server():
    ServerManagerController.add_server({
        'ip': request.json['ip']
    },
    session)
    return Response(status=201, mimetype='application/json')


@app.route("/games", methods=["GET"])
def get_games():
    games = GameController.get_games(session)
    return jsonify(games)

@app.route("/games", methods=["POST"])
def create_game():
    GameController.create_game(session,request.json['name'],request.json['cpu'],request.json['ram'])
    return Response(status=201, mimetype='application/json')

@app.route("/game/<name>", methods=["GET"])
def get_game(name):
    result = GameController.get_game_by_name(session,name)
    game = json.dumps({
        'name':result.name,
        'cpu': result.cpu_usage,
        'ram': result.ram
    })
    return jsonify(game)

@app.route("/play", methods=["Get"])
def play():
    server_ip = ServerManagerController.handle_client_connection(session,request.json)
    return jsonify(server_ip)

# curl http://localhost:5000/games

