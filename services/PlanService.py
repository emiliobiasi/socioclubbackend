from typing import List
from models.Plan import Plan
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
from datetime import datetime
from dateutil.relativedelta import relativedelta

projeto_raiz = os.getcwd()
caminho_env = os.path.join(projeto_raiz, '.env')
env_vars = dotenv_values(caminho_env)

if load_dotenv(caminho_env):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
else:
   raise Exception('Não foi possível achar o arquivo .env: ' + caminho_env)

class PlanService:

    @staticmethod
    def get_plans() -> List[Plan]:
        connection = connect_to_db()

        if connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Plan')
            data = cursor.fetchall()
            cursor.close
            plan_list = []
            
            for plan in data:
                plan_list.append(
                    Plan(
                        id = plan[0],
                        price=plan[1],
                        discount=plan[2],
                        priority=plan[3],
                        club_id=plan[4],
                        name=plan[5],
                        description=plan[7],
                        image=plan[6]
                    )
                )
            return plan_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
        
    @staticmethod
    def get_plans_by_club_id(club_id: str) -> List[Plan]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Plan WHERE fk_Club_id = %s AND price != 0',(club_id))
            data = cursor.fetchall()
            cursor.close
            plan_list = []
            for plan in data:
                plan_list.append(
                    Plan(
                        id = plan[0],
                        price=plan[1],
                        discount=plan[2],
                        priority=plan[3],
                        club_id=plan[4],
                        name=plan[5],
                        description=plan[6],
                        image=plan[7]
                    )
                )
            return plan_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
        