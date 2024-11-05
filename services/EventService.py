from typing import List
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
from models.events.CreateEvent import CreateEvent
from models.events.Event import Event
from models.events.event_stripe import EventStripe


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
        query = '''
                    INSERT INTO Event(event_name, full_price, tickets_away, tickets_home, event_date, image, description, fk_Club_id)
                    VALUES (
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s,
                        %s
                    ) 
                '''
        create_tuple = (
            new_event.eventName,
            new_event.fullPrice,
            new_event.ticketsAway,
            new_event.ticketsHome,
            new_event.eventDate,
            new_event.image,
            new_event.description,
            new_event.fkClubId
        )
        EventService._execute_query(query, create_tuple)

    
    @staticmethod
    def get_stripe_events_by_club_id(club_id: str):
        print(club_id)
        select_query = '''
            select e.id, e.event_name, e.description, e.image, e.full_price,  e.event_date, e.tickets_away, e.tickets_home, s.stripe_id, s.price_id
            from event e 
            join stripe s on e.id = s.fk_Event_id
            where e.fk_Club_id = %s
        '''
        select_tuple = (club_id,)

        data = EventService._execute_select_all_query(query=select_query, t=select_tuple)

        ret = []

        for plan in data:
            ret.append(
                EventStripe(
                    id=plan[0],
                    eventName=plan[1],
                    description=plan[2],
                    image=plan[3],
                    fullPrice=plan[4],
                    eventDate=plan[5],
                    ticketsAway=plan[6],
                    ticketsHome=plan[7],
                    stripe_id=plan[8],
                    price_id=plan[9],
                    club_id=int(club_id)
                )
            )

        return ret
    
    @staticmethod
    def delete_event(event_id: str):
        delete_query = "delete from event where id = %s"
        delete_tuple = (event_id,)

        EventService._execute_query(delete_query, delete_tuple)

        
    @staticmethod
    def _execute_query(query:str , t: tuple):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query, t)
            connection.commit()
            cursor.close()
            connection.close()
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
    
    @staticmethod
    def _execute_select_all_query(query: str, t: tuple):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query, t)
            data = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()

            return data
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
