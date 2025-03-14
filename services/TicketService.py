import os
from dotenv import load_dotenv, dotenv_values
from datetime import datetime
from database.connection.Connection import connect_to_db
import random, string
from models.events.Event import Event

projeto_raiz = os.getcwd()
caminho_env = os.path.join(projeto_raiz, '.env')
env_vars = dotenv_values(caminho_env)

if load_dotenv(caminho_env):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
else:
   raise Exception('Não foi possível achar o arquivo .env: ' + caminho_env)


class TicketService:

    @staticmethod
    def create_ticket(event_id: int, club_id: int, client_id: int):
        connection = connect_to_db()

        if connection:
            try:
                cursor = connection.cursor()

                cursor.execute(
                    'SELECT fk_Club_id, tickets_home, tickets_away FROM Event WHERE id = %s',
                    (str(event_id))
                )
                data = cursor.fetchone()

                if data:
                    club_event_id = data[0]
                    tickets = 0
                    string_tickets = ''
                    if club_event_id == club_id:
                        tickets = data[1]
                        string_tickets = 'tickets_home'
                    else:
                        tickets = data[2]
                        string_tickets = 'tickets_away'
                else:
                    raise Exception('Erro ao buscar evento com id ', event_id)

                
                if tickets > 0:
                    tickets -= 1
                else:
                    raise Exception('Não tem mais ingressos disponíveis')
                
                caracteres = string.ascii_letters + string.digits
                qr_code = ''.join(random.choice(caracteres) for _ in range(16))

                cursor.execute(
                    'INSERT INTO Ticket(qr_code, fk_Event_id, fk_Client_id) VALUES (%s,%s, %s)',
                    (qr_code, event_id, client_id)
                )

                cursor.execute(
                    f'UPDATE Event SET {string_tickets} = %s WHERE id = %s',
                    (tickets, event_id)
                )

                connection.commit()
                cursor.close()
                connection.close()
            except Exception as e:
                raise e
        else:
            raise Exception('Falha na conexão ao PostgreSQL')
    
    @staticmethod
    def get_all_tickets(client_id: str):
        connection = connect_to_db()

        if connection:
            try:
                cursor = connection.cursor()

                cursor.execute(
                    '''
                        SELECT e.id, e.event_name, e.description, e.image, e.full_price, e.event_date, e.tickets_away, e.tickets_home, e.fk_Club_id 
                        FROM Event e
                        INNER JOIN Ticket t ON t.fk_Event_id = e.id
                        WHERE t.fk_Client_id = %s
                    ''',
                    (client_id,)
                )

                data = cursor.fetchall()
                events = []

                if data:
                    for event in data:
                        events.append(
                            Event(
                                id=event[0],
                                eventName=event[1],
                                description=event[2],
                                image=event[3],
                                fullPrice=event[4],
                                eventDate=event[5],
                                ticketsAway=event[6],
                                ticketsHome=event[7],
                                fkClubId=event[8]
                            )
                        )
                
                return events
            except Exception as e:
                print(f'Erro ao retornar eventos comprados: {str(e)}')
        else:
            raise Exception('Falha na conexão ao PostgreSQL')
    
    @staticmethod
    def get_valid_tickets_by_client_id(client_id: str):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()

            now = datetime.now()

            cursor.execute(
                '''
                    SELECT e.event_name, e.image, e.event_date, e.description, e.full_price, t.qr_code
                    FROM Event e
                    INNER JOIN Ticket t ON t.fk_Event_id = e.id
                    WHERE t.fk_Client_id = %s AND e.event_date > %s
                ''',
                (client_id, now.strftime('%Y-%m-%d %H:%M:%S'))
            )

            data = cursor.fetchall()
            event_and_ticket = []

            if data:
                for dt in data:
                    event_and_ticket.append(
                        {
                            'eventName': dt[0],
                            'image': dt[1],
                            'eventDate': dt[2].strftime("%Y-%m-%d %H:%M:%S"),
                            'description': dt[3],
                            'fullPrice': dt[4],
                            'qr_code': dt[5]
                        }
                    )

            return event_and_ticket

            
            

