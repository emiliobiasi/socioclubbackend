import json
from typing import List, Optional
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
from models.Game import Game


projeto_raiz = os.getcwd()
caminho_env = os.path.join(projeto_raiz, '.env')
env_vars = dotenv_values(caminho_env)

if load_dotenv(caminho_env):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
else:
    raise Exception('Não foi possível achar o arquivo .env: ' + caminho_env)

class GameService:
    @staticmethod
    def get_games() -> List[Game]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Game;")
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            game_list = []
            for game in data:
                game_list.append(
                    Game(
                        id=game[0],
                        awayTeam=game[1],
                        fullPrice=game[2],
                        gameDate=game[3],
                        ticketsAway=game[4],
                        ticketsHome=game[5],
                        fkClubId=game[6],
                        description=game[7]
                    )
                )
            return game_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")

    @staticmethod
    def find_by_id(id: int) -> Optional[Game]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM Game WHERE id={id};")
            game = cursor.fetchone()
            cursor.close()
            connection.close()
            if game:
                return Game(
                    id=game[0],
                    awayTeam=game[1],
                    fullPrice=game[2],
                    gameDate=game[3],
                    ticketsAway=game[4],
                    ticketsHome=game[5],
                    fkClubId=game[6],
                    description=game[7]
                )
            else:
                return None
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
