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
                type='express',
                country='BR',
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True}
                },
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
    def vinculate(socioclub_id: int, stripe_id: str, price_id: str, column):

        print(socioclub_id)
        query = f'insert into stripe({column}, stripe_id, price_id) values (%s, %s, %s)'

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
        





    # NOVAS FUNÇÕES PARA ASSINATURAS

    @staticmethod
    def create_customer(email: str, name: str = None, stripe_account: str = None):
        try:
            request_options = {}
            if stripe_account:
                request_options['stripe_account'] = stripe_account

            customer = stripe.Customer.create(
                email=email,
                name=name,
                **request_options
            )
            return customer
        except Exception as e:
            print(f"Erro ao criar o cliente: {e}")
            raise e

    @staticmethod
    def create_subscription_product(name: str, price: int, currency: str = "usd", interval: str = "month", stripe_account: str = None):
        try:
            request_options = {}
            if stripe_account:
                request_options['stripe_account'] = stripe_account

            price_data = {
                "currency": currency,
                "unit_amount": price,
                "product_data": {"name": name},
                "recurring": {"interval": interval}
            }

            price_obj = stripe.Price.create(
                **price_data,
                **request_options
            )
            return price_obj
        except Exception as e:
            print(f"Erro ao criar o produto de assinatura na Stripe: {e}")
            raise e

    @staticmethod
    def create_checkout_session_for_subscription(price_id: str, success_url: str, cancel_url: str, stripe_account: str = None):
        try:
            request_options = {}
            if stripe_account:
                request_options['stripe_account'] = stripe_account

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='subscription',
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                success_url=success_url,
                cancel_url=cancel_url,
                **request_options
            )
            return session
        except Exception as e:
            print(f"Erro ao criar a sessão de checkout: {e}")
            raise e

    @staticmethod
    def retrieve_checkout_session(session_id: str, stripe_account: str = None):
        try:
            request_options = {}
            if stripe_account:
                request_options['stripe_account'] = stripe_account

            session = stripe.checkout.Session.retrieve(
                session_id,
                **request_options
            )
            return session
        except Exception as e:
            print(f"Erro ao recuperar a sessão de checkout: {e}")
            raise e

    @staticmethod
    def retrieve_subscription(subscription_id: str, stripe_account: str = None):
        try:
            request_options = {}
            if stripe_account:
                request_options['stripe_account'] = stripe_account

            subscription = stripe.Subscription.retrieve(
                subscription_id,
                **request_options
            )
            return subscription
        except Exception as e:
            print(f"Erro ao recuperar a assinatura: {e}")
            raise e
        
    @staticmethod
    def create_checkout_session(line_items: list, success_url: str, cancel_url: str, client_reference_id: str, stripe_account :str, mode: str):
        try:
            request_options = {}
            if stripe_account:
                request_options['stripe_account'] = stripe_account
            stripe_line_items = []
            for item in line_items:
                stripe_line_items.append({
                    'price': item['price_id'],
                    'quantity': item.get('quantity', 1),
                })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=stripe_line_items,
                mode=mode,
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=client_reference_id,
                **request_options
            )

            return session
        except Exception as e:
            print('Ocorreu um erro ao criar a sessão de checkout:', e)
            raise e
        
    @staticmethod
    def create_login_link(account_id: str):
        try:
            login_link = stripe.Account.create_login_link(account_id)
            return login_link
        except Exception as e:
            print(f"Erro ao criar o login link: {e}")
            raise e