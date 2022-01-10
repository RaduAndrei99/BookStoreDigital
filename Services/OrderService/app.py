import sys
  
# setting path
sys.path.append('F:\Faculty\An_IV\POS\Lab_Project')


from flask import Flask, make_response, request, jsonify
import json
from flask_cors import CORS
import requests
from Services.OrderService.order_service import OrderService
from DTOs.order import Order

from suds.client import Client

#folosit pentru a defini un decorator
from functools import wraps

#rest APP in flask
app = Flask(__name__)
#pentru CORS policy
cors = CORS(app, resources={r"/*": {"origins": "*"}})


order_service = OrderService()

#voi folosi aceasta functia ca decorator pentru a proteja resursele care au nevoie de autentificare
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try: 
          token = None
          #token = request.get_json()['token']

          if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
            print(token)

            user_acces = Client('http://localhost:7789/?wsdl')

            status_code = user_acces.service.validate_token(token)

            if status_code == 404:
              return jsonify({'message' : 'Token-ul este invalid!'}), 401
          else:
            return jsonify({'message' : 'Token-ul lipseste!'}), 401
        except Exception as e:
          print("nasol")
          print(e)
          return jsonify({'message' : 'Eroare la validarea token-ului!'}), 401

        return f(*args, **kwargs)

    return decorated

@app.route('/api/order/add-order', methods=['POST'])
@token_required
def add_order():
  try:
    data = request.get_json()
    print(data)
    order_obj = Order(**data)
    if order_service.add_order(order_obj):
      return make_response('Comanda a fost plasata cu succes!', 201)
    else:
      return make_response('Comanda nu a fost plasata!', 405)

  except Exception as e:
    print(e)
    return "Eroare!", 500

if __name__ == '__main__':
  app.run(port=8082)