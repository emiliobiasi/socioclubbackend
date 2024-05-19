import json
from typing import List, Optional
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
from models.Event import Event


projeto_raiz = os.getcwd()
caminho_env = os.path.join(projeto_raiz, '.env')
env_vars = dotenv_values(caminho_env)

if load_dotenv(caminho_env):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
else:
    raise Exception('Não foi possível achar o arquivo .env: ' + caminho_env)

class EventService:
    @staticmethod
    def get_events() -> List[Event]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Event;")
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            event_list = []
            for event in data:
                event_list.append(
                    Event(
                        id=event[0],
                        eventName=event[1],
                        description=event[2],
                        image=event[3],
                        fullPrice=event[4],
                        eventDate=event[5],
                        ticketsAway=event[6],
                        ticketsHome=event[7],
                        fkClubId=event[8],
                    )
                )
            return event_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")

    @staticmethod
    def get_events_by_club_id(club_id: int) -> List[Event]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM Event WHERE fk_Club_id = {club_id};")
            data = cursor.fetchall()
            cursor.close
            event_list = []
            for event in data:
                event_list.append(
                    Event(
                        id=event[0],
                        eventName=event[1],
                        description=event[2],
                        image=event[3],
                        fullPrice=event[4],
                        eventDate=event[5],
                        ticketsAway=event[6],
                        ticketsHome=event[7],
                        fkClubId=event[8],
                    )
                )
            return event_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
