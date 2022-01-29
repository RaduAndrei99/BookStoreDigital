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

@app.route('/api/order/add-order', methods=['POST'])
def add_order():
  try:
    data = request.get_json()
    order_obj = Order(**data)

    # token = request.headers['Authorization'].split()[1]
    # user_acces = Client('http://localhost:7789/?wsdl')
    # #remote procedure call petru a verifica daca pot adauga aceasta comanda
    # response = user_acces.service.verify_authority(token, order_obj.user_id)

    #if response[1] == 200:
    res = order_service.add_order(order_obj)
    return res, 201
   
  except Exception as e:
    print(e)
    return "Eroare!", 500

@app.route('/api/order/get-orders/<USER_ID>', methods=['GET'])
def get_orders(USER_ID):
  try:

    # token = request.headers['Authorization'].split()[1]
    # user_acces = Client('http://localhost:7789/?wsdl')
    # #remote procedure call petru a verifica daca pot adauga aceasta comanda
    # response = user_acces.service.verify_authority(token, USER_ID)
    res = order_service.get_orders(USER_ID)
    print(res)


    return jsonify(res), 201 
  except Exception as e:
    print(e)
    return "Eroare!", 500

if __name__ == '__main__':
  app.run(port=8082)