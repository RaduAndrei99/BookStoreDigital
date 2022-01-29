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


import sys
  
# setting path
sys.path.append('F:\Faculty\An_IV\POS\Lab_Project')


from DTOs.user_credentials import UserCredentials


#voi folosi aceasta functia ca decorator pentru a proteja resursele care au nevoie de autentificare(de jwt)
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

            msg1, msg2, status_code = user_acces.service.validate_token(token)
            
            if status_code[1] == 401 or status_code[1] == 404:
              return jsonify({'message' : msg2[1]}), 401
            
          else:
            return jsonify({'message' : 'Token-ul lipseste!'}), 401
        except Exception as e:
          print("nasol")
          print(e)
          return jsonify({'message' : 'Eroare la validarea token-ului!'}), 500

        return f(*args, **kwargs)

    return decorated

#folosesc aceasta metoda ca decorator pentru a proteja resursele care au nevoie de drepturi de admin
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try: 
          token = None
          #token = request.get_json()['token']

          if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
            print(token)

            user_acces = Client('http://localhost:7789/?wsdl')

            msg1, msg2, status_code = user_acces.service.validate_token(token)
            
            if status_code[1] == 401 or status_code[1] == 404:
              return jsonify({'message' : msg2[1]}), 401
            elif status_code[1] == 200:
              if msg2[1] != 'admin':
                return jsonify({'message' : "Eroare! Nu ai drepturi pentru a accesa aceasta resursa!"}), 401
            else:
                return jsonify({'message' : msg2[1]}), 401           
          else:
            return jsonify({'message' : 'Token-ul lipseste!'}), 401
        except Exception as e:
          print("nasol")
          print(e)
          return jsonify({'message' : 'Eroare la validarea token-ului!'}), 500

        return f(*args, **kwargs)

    return decorated

#-------BOOKS-------
@app.route('/bookcollection/books', methods=['GET'])
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




@app.route('/create-book', methods=['POST'])
@admin_required
def create_book():
  try:
    BOOK_SERVICE_IP = 'http://localhost'
    BOOK_SERVICE_PORT = '8081'
    BOOK_SERVICE_URI = '/api/bookcollection/books/'

    URL = BOOK_SERVICE_IP + ':' + BOOK_SERVICE_PORT + BOOK_SERVICE_URI

    r = requests.post(URL, headers=request.headers, json = request.get_json())

    return r.json(), r.status_code
  except Exception as e:
    traceback.print_exc()
    return "Eroare la server!", 500


@app.route('/delete-book/<ISBN>', methods=['DELETE'])
@admin_required
def delete_book(ISBN):
  try:
    BOOK_SERVICE_IP = 'http://localhost'
    BOOK_SERVICE_PORT = '8081'
    BOOK_SERVICE_URI = '/api/bookcollection/books/%s/' % ISBN

    URL = BOOK_SERVICE_IP + ':' + BOOK_SERVICE_PORT + BOOK_SERVICE_URI

    r = requests.delete(URL, headers=request.headers, json = request.get_json())

    return r.json(), r.status_code
  except Exception as e:
    traceback.print_exc()
    return "Eroare la server!", 500


#---------USER----------
@app.route('/delete-user', methods=['DELETE'])
@admin_required#doar un admin va putea sa stearga un user
def delete_user():
  try:
    user_acces = Client('http://localhost:7789/?wsdl')
    response = user_acces.service.delete_user(request.get_json()['email'])

    return response[0], response[1]
  except Exception as e:
    traceback.print_exc()
    return "Eroare!", 500

@app.route('/change-role', methods=['PUT'])
@admin_required#doar un admin va putea sa schimbe rolul
def change_role():
  try:
    user_acces = Client('http://localhost:7789/?wsdl')
    response = user_acces.service.make_user_admin(request.get_json()['email'])

    return response[0], response[1]
  except Exception as e:
    traceback.print_exc()
    return "Eroare!", 500


@app.route('/login', methods=['POST'])
def login_user():
  try:
    auth = request.authorization
    if auth:
      user_acces = Client('http://localhost:7789/?wsdl')
      response = user_acces.service.login_user(auth.username, auth.password)
      print(response[1])
      return response[0], response[1]
      
    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

  except Exception as e:
    traceback.print_exc()
    return "Eroare!", 500


@app.route('/register', methods=['POST'])
def register_user():
  try:
    user_credentials_obj = UserCredentials(**request.get_json())
    user_acces = Client('http://localhost:7789/?wsdl')
    response = user_acces.service.register_user(user_credentials_obj.email, user_credentials_obj.hashedPassword)

    return response[0], response[1]
      
  except Exception as e:
    traceback.print_exc()
    return "Eroare la server!", 500

@app.route('/change-password', methods=['PUT'])
@token_required
def change_password():
  try:
    user_credentials_obj = UserCredentials(**request.get_json())
    token = request.headers['Authorization'].split()[1]
    user_acces = Client('http://localhost:7789/?wsdl')
    response = user_acces.service.change_password(token, user_credentials_obj.email, user_credentials_obj.hashedPassword)

    return response[0], response[1]
      
  except Exception as e:
    traceback.print_exc()
    return "Eroare la server!", 500


#----------ORDER----------

@app.route('/add-order', methods=['POST'])
@token_required
def add_order():
  try:
    BOOK_SERVICE_IP = 'http://localhost'
    BOOK_SERVICE_PORT = '8082'
    BOOK_SERVICE_URI = '/api/order/add-order'

    URL = BOOK_SERVICE_IP + ':' + BOOK_SERVICE_PORT + BOOK_SERVICE_URI
      

    r = requests.post(URL, headers=request.headers, json = request.get_json())

    return r.text, r.status_code
  except Exception as e:
    traceback.print_exc()
    return "Eroare!", 500

if __name__ == '__main__':
  app.run(port=8080)