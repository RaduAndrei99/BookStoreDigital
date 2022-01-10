from flask import Flask, make_response, request, jsonify
import traceback
import json
from flask_cors import CORS
import requests

from DTOs.order import Order
from suds.client import Client

#folosit pentru a defini un decorator
from functools import wraps

#rest APP in flask
app = Flask(__name__)
#pentru CORS policy
cors = CORS(app, resources={r"/*": {"origins": "*"}})


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


@app.route('/bookcollection/books', methods=['GET'])
@token_required
def get_books():
  try:
    BOOK_SERVICE_IP = 'http://localhost'
    BOOK_SERVICE_PORT = '8081'
    BOOK_SERVICE_URI = '/api/bookcollection/books/'

    URL = BOOK_SERVICE_IP + ':' + BOOK_SERVICE_PORT + BOOK_SERVICE_URI

    r = requests.get(URL)

    return r.json(), 200
  except Exception as e:
    traceback.print_exc()
    return "Eroare!", 500

@app.route('/bookcollection/books/<ISBN>/authors/', methods=['GET'])
def books_authors_route_get(ISBN):
  try:
    BOOK_SERVICE_IP = 'http://localhost'
    BOOK_SERVICE_PORT = '8081'
    BOOK_SERVICE_URI = '/api/bookcollection/books/%s/authors/' % ISBN

    URL = BOOK_SERVICE_IP + ':' + BOOK_SERVICE_PORT + BOOK_SERVICE_URI

    r = requests.get(URL)

    return r.json(), 200
  except Exception as e:
    traceback.print_exc()
    return "Eroare!", 500

@app.route('/login')
def login_user():
  try:
    auth = request.authorization
    #user_credentials_obj = UserCredentials(**request.get_json())
    if auth:
      user_acces = Client('http://localhost:7789/?wsdl')
      response = user_acces.service.login_user(auth.username, auth.password)
      print(response[1])
      return response[0], response[1]
      
    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

  except Exception as e:
    traceback.print_exc()
    return "Eroare!", 500

@app.route('/add-order', methods=['POST'])
@token_required
def add_order():
  try:
    BOOK_SERVICE_IP = 'http://localhost'
    BOOK_SERVICE_PORT = '8082'
    BOOK_SERVICE_URI = '/api/order/add-order'

    URL = BOOK_SERVICE_IP + ':' + BOOK_SERVICE_PORT + BOOK_SERVICE_URI
    
    print(request.get_json())
  

    r = requests.post(URL, headers=request.headers, json = request.get_json())

    return r.text, r.status_code
  except Exception as e:
    traceback.print_exc()
    return "Eroare!", 500

if __name__ == '__main__':
  app.run(port=8080)