from datetime import datetime, timedelta
from typing import List, Optional
from jose import jwt
from fastapi import HTTPException, status
from models.clubs.Club import Club
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
import bcrypt

from models.clubs.ColorSchemeClub import ColorSchemeClub
from models.clubs.RegisterClub import RegisterClub
from models.clubs.LoginClub import LoginClub

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
                        club_category= club[15],
                        stripe_id = club[16]
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
            cursor.execute(f'''
                SELECT id,
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
                fk_ClubCategory_id,                
                stripe_id 
                FROM Club WHERE id={client_id};'''
            )
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
                        club_category = club[15],
                        stripe_id = club[16]
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
                        club_category= club[15],
                        stripe_id = club[16]
                    )
                )
            cursor.close()
            connection.close()
            return clubs
        else:
            raise Exception('Falha na conexão ao PostgreSQL')

    @staticmethod
    def create_club(club: RegisterClub):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                '''
                    INSERT INTO Club (
                        name,
                        password,
                        address,
                        email,
                        cnpj
                    ) values (
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
                    club.address,
                    club.email,
                    club.cnpj,
                )
            )

            connection.commit()
            cursor.close()
            connection.close()

    @staticmethod
    def login(club: LoginClub , expires_at=30):
        
        club_on_db = ClubService.find_club_by_email(club.email)

        if club_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Email ou senha incorretos',
            )
        
        if not ClubService.verify_password(club.password, club_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Email ou senha incorretos',
            )

        exp = datetime.utcnow() + timedelta(minutes=expires_at)

        payload = {
            'sub': club.email,
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'expires_at': exp.strftime("%Y-%m-%d %H:%M:%S"),
            'club': club_on_db.to_json()
        }
    
    @staticmethod
    def find_club_by_email(email: str) -> Optional[Club]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Club WHERE email = %s;", (email,))
            data = cursor.fetchone()
            cursor.close()
            connection.close()
            if data:
                return Club(
                        id = data[0],
                        name = data[1],
                        password = data[2],
                        description = data[3],
                        address = data[4],
                        logo = data[5],
                        email = data[6],
                        cnpj = data[7],
                        background = data[8],
                        titles_color = data[9],
                        subtitles_color = data[10],
                        buttons_color = data[11],
                        palette_1 = data[12],
                        palette_2 = data[13],
                        palette_3 = data[14],
                        club_category= data[15],
                        stripe_id = data[16]
                    )
            else:
                return None
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
        
    @staticmethod
    def update_color_scheme(colors: ColorSchemeClub, club_id: int):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute('''
                    UPDATE Club
                    SET titles_color = %s,
                    subtitles_color = %s,
                    buttons_color = %s,
                    palette_1 = %s,
                    palette_2 = %s,
                    palette_3 = %s
                    WHERE id = %s
                ''', 
                (
                    colors.titles_color,
                    colors.subtitles_color,
                    colors.buttons_color,
                    colors.palette_1,
                    colors.palette_2,
                    colors.palette_3,
                    club_id
                ),
            )
            connection.commit()
            cursor.close()
            connection.close()
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
    
    def create_hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password.decode('utf-8')
    
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def update_stripe_id(stripe_id: str, club_id: int):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute('''
                    UPDATE Club
                    SET stripe_id = %s
                    WHERE id = %s
                ''', 
                (
                    stripe_id,
                    club_id
                ),
            )
            connection.commit()
            cursor.close()
            connection.close()

            return ClubService.find_by_id(club_id)
        else:
            raise Exception("Falha na conexão ao PostgreSQL")

