import os
from dotenv import load_dotenv
import stripe

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
    def create_product_with_price(name: str, price: int, currency: str = "usd", interval: str = None):
        try:
            
            price_obj = stripe.Price.create(
                currency=currency,
                unit_amount=price, 
                product_data={"name": name},
                recurring={"interval": interval} if interval else None
            )

            return {"price": price_obj}

        except Exception as e:
            raise e