import json

from Model.GameModel import GameModel
from sqlalchemy import select

def create_game(session,name, cpu,ram):
    game_model = GameModel(name=name, cpu_usage=cpu, ram=ram)
    try:
        session.add(game_model)
        session.commit()
    except:
        session.rollback()
        print("An exception occurred")
    return game_model

def get_game_by_name(session,name):
    stmt = select(GameModel).where(GameModel.name == name)
    result = session.execute(stmt).scalar()
    return result

def get_games(session):
    stmt = select(GameModel)
    res = session.execute(stmt).scalars()
    obj = []
    for game in res:
        ob = json.dumps({
            'name':game.name
        })
        obj.append(ob)
    return obj