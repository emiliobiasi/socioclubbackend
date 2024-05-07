from typing import List, Optional
from models.Club import Club
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
import base64

projeto_raiz = os.getcwd()
caminho_env = os.path.join(projeto_raiz, '.env')
env_vars = dotenv_values(caminho_env)

if load_dotenv(caminho_env):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
else:
   raise Exception('Não foi possível achar o arquivo .env: ' + caminho_env)

class ClubService:

    @staticmethod
    def get_clubs() -> List[Club]:
        connection = connect_to_db()
        
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Club;")
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            clubs_list = []
            for club in data:
                clubs_list.append(
                    Club(
                        id = club[0],
                        name = club[1],
                        password = club[2],
                        description = club[3],
                        address = club[4],
                        logo = club[5],
                        email = club[6],
                        cnpj = club[7],
                        background = club[8],
                        titles_color = club[9],
                        subtitles_color = club[10],
                        buttons_color = club[11],
                        palette_1 = club[12],
                        palette_2 = club[13],
                        palette_3 = club[14],
                        club_category= club[15]
                    )
                )
            return clubs_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
        
    @staticmethod
    def find_by_id(client_id: int) -> Optional[Club]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM Club WHERE id={client_id};")
            club = cursor.fetchone()
            cursor.close()
            connection.close()
            if club:
                return Club(
                        id = club[0],
                        name = club[1],
                        password = club[2],
                        description = club[3],
                        address = club[4],
                        logo = club[5],
                        email = club[6],
                        cnpj = club[7],
                        background = club[8],
                        titles_color = club[9],
                        subtitles_color = club[10],
                        buttons_color = club[11],
                        palette_1 = club[12],
                        palette_2 = club[13],
                        palette_3 = club[14],
                        club_category= club[15]
                    )
            else:
                return None
        else:
            raise Exception("Falha na conexão ao PostgreSQL")