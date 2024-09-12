import stripe
import os

stripe.api_key = 'sk_test_51Py0ViCZCdbLViMvjE3a5YIDu11UCNfzQJum0nJBfrgYJ9nShCY5fCh7Tb3xwd2GmoOgeoEgfOLt71BUGr9UcKxX00XuKkLZJ9'

stripe.api_version = '2023-10-16'

from flask import Flask, jsonify, send_from_directory, request

app = Flask(__name__, static_folder='dist',
  static_url_path='/<path:path>', template_folder='dist')

@app.route('/account_link', methods=['POST'])
def create_account_link():
    try:
        connected_account_id = request.get_json().get('account')

        account_link = stripe.AccountLink.create(
          account=connected_account_id,
          return_url=f"http://localhost:4242/return/{connected_account_id}",
          refresh_url=f"http://localhost:4242/refresh/{connected_account_id}",
          type="account_onboarding",
        )

        return jsonify({
          'url': account_link.url,
        })
    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account link: ', e)
        return jsonify(error=str(e)), 500

@app.route('/account', methods=['POST'])
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

        return jsonify({
          'account': account.id,
        })
    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account: ', e)
        return jsonify(error=str(e)), 500

@app.route('/', defaults={'path': ''})

# Flask does not like serving static files with a sub-path, so just force them to serve up the frontend here
@app.route('/return/<path>')
@app.route('/refresh/<path>')
@app.route('/<path:path>')
def catch_all(path, **kwargs):
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(port=4242)