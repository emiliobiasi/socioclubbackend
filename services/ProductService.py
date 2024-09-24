from typing import List, Optional
from models.products.Product import Product
from models.products.CreateProduct import CreateProduct
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
    def buy_product(client_id: str, product_id:str):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO Buy (fk_Client_id, fk_Product_id) VALUES (%s, %s)',
                (client_id, product_id)
            )
            connection.commit()
            cursor.close()
            connection.close()
        else:
            raise Exception('Falha na conexão ao PostgreSQL')
        
    @staticmethod
    def get_bought_products_by_client_id(client_id:str) -> List[Product]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT p.* FROM Product p JOIN Buy b ON p.id = b.fk_Product_id WHERE b.fk_Client_id = %s',
                (client_id)
            )
            data = cursor.fetchall()
            cursor.close()
            connection.close()

            product_list = []
            
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
            raise Exception('Falha na conexão ao PostgreSQL')
        
    @staticmethod
    def create_product(new_product: CreateProduct):
        query = f'''
            insert into product (name, description, price, image, category_id, club_id)
            values (
                {new_product.name},
                {new_product.description},
                {new_product.price},
                {new_product.image},
                {new_product.category_id},
                {new_product.club_id},
            )
        '''

        ProductService._execute_query(query=query)

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