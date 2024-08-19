from typing import List, Optional
from models.Club import Club
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
import base64
import bcrypt

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
    
    
    @staticmethod
    def get_following_clubs(client_id: str) -> List[Club]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()

            cursor.execute(
                'SELECT c.* FROM Club c JOIN Follow f ON c.id = f.fk_Club_id WHERE f.fk_Client_id = %s',
                (client_id)
            )

            data = cursor.fetchall()
            clubs = []
            
            for club in data:
                clubs.append(
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
            cursor.close()
            connection.close()
            return clubs
        else:
            raise Exception('Falha na conexão ao PostgreSQL')

    @staticmethod
    def create_club(club: Club):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                '''
                    INSERT INTO Club (
                        name,
                        password,
                        description,
                        address,
                        logo,
                        email,
                        cnpj,
                        background,
                        titles_color,
                        subtitles_color,
                        buttons_color,
                        palette_1,
                        palette_2,
                        palette_3,
                        fk_ClubCategory_id
                    ) values (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                ''',
                (
                    club.name,
                    ClubService.create_hash_password(club.password),
                    club.description,
                    club.address,
                    club.logo,
                    club.email,
                    club.cnpj,
                    club.background,
                    club.titles_color,
                    club.subtitles_color,
                    club.buttons_color,
                    club.palette_1,
                    club.palette_2,
                    club.palette_3,
                    club.club_category,
                )
            )
    
    def create_hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password.decode('utf-8')