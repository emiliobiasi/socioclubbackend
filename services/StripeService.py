import os
from dotenv import load_dotenv
import stripe
from database.connection.Connection import connect_to_db

load_dotenv()

stripe.api_key = os.getenv('STRIPE_API_KEY')
stripe.api_version = '2023-10-16'

class StripeService:

    @staticmethod
    def create_account():
        try:
            account = stripe.Account.create(
                controller={
                    "stripe_dashboard": {
                    "type": "none",
                    },
                    "fees": {
                    "payer": "application"
                    },
                    "losses": {
                    "payments": "application"
                    },
                    "requirement_collection": "application",
                },
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True}
                },
                country="BR",
            )
            
            return account

        except Exception as e:
            print('An error occurred when calling the Stripe API to create an account:', e)
            raise e

    @staticmethod
    def create_account_link(connected_account_id: str):
        try:
            account_link = stripe.AccountLink.create(
                account=connected_account_id,
                return_url=f"http://localhost:5173/financeiro/{connected_account_id}",
                refresh_url=f"http://localhost:5173/financeiro/{connected_account_id}",
                type="account_onboarding",
            )
            return account_link

        except Exception as e:
            print('An error occurred when calling the Stripe API to create an account link:', e)
            raise e

    @staticmethod
    def update_account(account_id: str):
        try:
            connected_account = stripe.Account.modify(
                account_id,
                business_type="individual",
            )
            return connected_account

        except Exception as e:
            print('An error occurred when calling the Stripe API to update an account:', e)
            raise e
        
    @staticmethod
    def create_product_with_price(name: str, price: int, currency: str = "usd", interval: str = None, stripe_account: str = None):
        try:
            # Build request options
            request_options = {}
            if stripe_account:
                request_options['stripe_account'] = stripe_account
            
            print("stripe_acc: " + stripe_account)

            price_obj = stripe.Price.create(
                currency=currency,
                unit_amount=price,
                product_data={"name": name},
                recurring={"interval": interval} if interval else None,
                **request_options  # Pass request options here
            )
            return price_obj
        except Exception as e:
            print(e)
            raise e
        
    @staticmethod
    def vinculate(socioclub_id: int, stripe_id: str, price_id: str):
        query = 'insert into stripe(socioclub_id, stripe_id, price_id) values (%s, %s, %s)'
        t = (socioclub_id, stripe_id, price_id)

        StripeService._execute_query(query=query, t=t)
    
    @staticmethod
    def _execute_query(query:str, t: tuple):
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, t)
                connection.commit()
                cursor.close()
                connection.close()
            except Exception as e:
                print(e)
        else:
            raise Exception("Falha na conexão ao PostgreSQL")