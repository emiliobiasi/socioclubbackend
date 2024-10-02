from typing import List
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
from models.events.CreateEvent import CreateEvent
from models.events.Event import Event


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
            cursor.execute("SELECT id, event_name, description, image, full_price, event_date, tickets_away, tickets_home, fk_Club_id FROM Event;")
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
            cursor.execute(f"SELECT id, event_name, description, image, full_price, event_date, tickets_away, tickets_home, fk_Club_id FROM Event WHERE fk_Club_id = {club_id};")
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
        
    @staticmethod
    def create_event(new_event: CreateEvent):
        query = f'''
                    INSERT INTO Event(event_name, full_price, tickets_away, tickets_home, event_date, image, description, fk_Club_id)
                    VALUES (
                        '{new_event.eventName}', 
                        {new_event.fullPrice}, 
                        {new_event.ticketsAway}, 
                        {new_event.ticketsHome}, 
                        '{new_event.eventDate}', 
                        '{new_event.image}', 
                        '{new_event.description}',
                        {new_event.fkClubId}
                    ) 
                '''
        print(query)
        EventService._execute_query(query)
    
    @staticmethod
    def delete_event(event_id: str):
        delete_query = "delete from event where id = %s"
        delete_tuple = (event_id)

        EventService._execute_query(delete_query, delete_tuple)

        
    @staticmethod
    def _execute_query(query:str):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
