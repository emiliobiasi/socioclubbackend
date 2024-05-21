from typing import List, Optional
from models.Product import Product
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values

projeto_raiz = os.getcwd()
caminho_env = os.path.join(projeto_raiz, '.env')
env_vars = dotenv_values(caminho_env)

if load_dotenv(caminho_env):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
else:
   raise Exception('Não foi possível achar o arquivo .env: ' + caminho_env)

class ProductService:

    @staticmethod
    def get_products() -> List[Product]:
        connection = connect_to_db()

        if connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Product')
            data = cursor.fetchall()
            cursor.close
            product_list = []
            print(data)
            for product in data:
                product_list.append(
                    Product(
                        id = product[0],
                        name=product[1],
                        description=product[2],
                        price=product[3],
                        club_id=product[4],
                        category_id=product[5],
                        image=product[6]
                    )
                )
            return product_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
        
    @staticmethod
    def get_products_by_club_id(club_id: str) -> List[Product]:
        connection = connect_to_db()

        if connection:
            
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Product WHERE fk_Club_id = %s',(club_id))
            data = cursor.fetchall()
            cursor.close()
            product_list = []
            print(data)
            for product in data:
                product_list.append(
                    Product(
                        id = product[0],
                        name=product[1],
                        description=product[2],
                        price=product[3],
                        club_id=product[4],
                        category_id=product[5],
                        image=product[6]
                    )
                )
            return product_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")