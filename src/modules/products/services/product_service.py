from typing import List, Optional
from models.products.Product import Product
from models.products.CreateProduct import CreateProduct
from database.connection.Connection import connect_to_db

from src.modules.products.models.product_stripe import ProductStripe
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
            cursor.execute('SELECT id, name, description, price, fk_Club_id, fk_ProductCategory_id, image FROM Product')
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
            cursor.execute('SELECT id, name, description, price, fk_Club_id, fk_ProductCategory_id, image FROM Product WHERE fk_Club_id = %s',(club_id))
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
                'SELECT p.id, p.name, p.description, p.price, p.fk_Club_id, p.fk_ProductCategory_id, p.image FROM Product p JOIN Buy b ON p.id = b.fk_Product_id WHERE b.fk_Client_id = %s',
                (client_id)
            )
            data = cursor.fetchall()
            cursor.close()
            connection.close()

            product_list = []
            
            for product in data:
                product_list.append(
                    Product(
                        id= product[0],
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
        
        create_query = '''
            insert into product (name, description, price, image, fk_Club_id, fk_ProductCategory_id)
            values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            returning id, name, description, price, image, fk_Club_id, fk_ProductCategory_id;
        ''' 

        create_tuple = (
            new_product.name,
            new_product.description,
            new_product.price,
            new_product.image,
            new_product.club_id,
            new_product.category_id
        )

        data = ProductService._execute_select_one_query(query=create_query, t=create_tuple)

        return Product(
            id=data[0],
            name=data[1],
            description=data[2],
            price=data[3],
            image=data[4],
            club_id=data[5],
            category_id=data[6]
        )
    
    @staticmethod
    def delete_product(product_id: str):
        delete_query = "DELETE FROM product WHERE id = %s"
        delete_tuple = (product_id,)

        ProductService._execute_query(delete_query, delete_tuple)
    
    @staticmethod
    def get_stripe_products_by_club_id(club_id: str):
        print(club_id)
        select_query = '''
            select p.id, p.name, p.description, p.price, p.image, p.fk_ProductCategory_id, s.stripe_id, s.price_id
            from product p 
            join stripe s on p.id = s.fk_Product_id
            where p.fk_Club_id = %s
        '''
        select_tuple = (club_id,)

        data = ProductService._execute_select_all_query(query=select_query, t=select_tuple)

        ret = []

        for product in data:
            ret.append(
                ProductStripe(
                    id=product[0],
                    name=product[1],
                    description=product[2],
                    price=product[3],
                    image=product[4],
                    category_id=product[5],
                    stripe_id=product[6],
                    price_id=product[7],
                )
            )

        return ret

    @staticmethod
    def _execute_query(query: str, params=None):
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                if params: 
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                connection.commit()
                cursor.close()
                connection.close()
            except Exception as e:
                print(f"Erro ao executar a query: {e}")
                raise e
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
    
    @staticmethod
    def _execute_select_one_query(query: str, t: tuple):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query, t)
            data = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()

            return data
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