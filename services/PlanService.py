from typing import List
from models.plans.Plan import Plan
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
from datetime import datetime

from models.plans.RegisterPlan import RegisterPlan

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
            cursor.execute('SELECT id, price, discount, priority, fk_Club_id, name, description, image FROM Plan')
            data = cursor.fetchall()
            cursor.close
            plan_list = []
            
            for plan in data:
                print(plan)
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
            print(data)
            cursor.close()
            plan_list = []
            for plan in data:
                plan_list.append(
                    Plan(
                        id = plan[0],
                        price=plan[1],
                        discount=plan[2],
                        priority=plan[3],
                        club_id=plan[7],
                        name=plan[6],
                        description=plan[5],
                        image=plan[4]
                    )
                )
            return plan_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
        
    @staticmethod
    def create_plan(plan: RegisterPlan):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                '''
                    INSERT INTO Plan (
                        name,
                        description,
                        image,
                        price,
                        discount,
                        priority,
                        fk_Club_id
                    ) VALUES (
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
                    plan.name,
                    plan.description,
                    plan.image,
                    plan.price,
                    plan.discount,
                    plan.priority,
                    plan.club_id
                )
            )
        connection.commit()
        cursor.close()
        connection.close()
    
    @staticmethod
    def delete_plan(plan_id: str):
        delete_query = "delete from plan where id = %s"
        delete_tuple = (plan_id)

        PlanService._execute_query(delete_query, delete_tuple)
    
    @staticmethod
    def _execute_query(query:str, t: tuple):
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                cursor.close()
                connection.close()
            except Exception as e:
                print(e)
        else:
            raise Exception("Falha na conexão ao PostgreSQL")