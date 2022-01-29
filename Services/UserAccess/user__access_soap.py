
import logging

from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Integer
from spyne.model.primitive import Unicode

from spyne.util.simple import wsgi_soap_application

import jwt
import datetime

from jwt.exceptions import InvalidSignatureError, DecodeError, ExpiredSignatureError
from suds.sudsobject import Iter

import sys
  
# setting path
sys.path.append('F:\Faculty\An_IV\POS\Lab_Project')
from Database.mysql_database import MySQLBookStoreDB
from Database.Exceptions.exceptions import EmailAlreadyExistsException, EmailNotFoundException

f = open("../../Passwords/mysql.txt", "r")
mysql_db = MySQLBookStoreDB( "db_manager", f.readline())

class SomeObject(ComplexModel):
    __namespace__ = 'spyne.examples.jwt.soap'

    i = Integer
    s = Unicode


class JWTService(ServiceBase):
    __out_header__ = SomeObject

    __secret_key = "SECRET_KEY"
    __ADMIN_ID = 2

    @srpc(Unicode, Unicode, _returns=(Unicode, Integer))  
    def register_user(email, password):
        try:
            mysql_db.create_user(email, password)
            return "Inregistrat cu succes!", 201
        except EmailAlreadyExistsException as e:
            return e.message, 409
        except Exception as e:
            print(e)
            return e.message, 500

    @srpc(Unicode, _returns=(Unicode, Integer))  
    def make_user_admin(email ):
        try:
            mysql_db.update_user_role(email, JWTService.__ADMIN_ID)
            return "Utilizatorul este acum un admin!", 201
        except EmailNotFoundException as e:
            return e.message, 404
        except Exception as e:
            print(e)
            return e.message, 500

    @srpc(Unicode, _returns=(Unicode, Integer))  
    def delete_user(email):
        try:
            mysql_db.delete_user(email)
            return "Utilizator sters cu success!", 201
        except EmailNotFoundException as e:
            return "Utilizator cu acest email nu exista!", 404
        except Exception as e:
            print(e)
            return e.message, 500

    @srpc(Unicode, Unicode, Unicode, _returns=(Unicode, Integer))  
    def change_password(token, email, new_password):
        try:
            decoded_jwt = jwt.decode(token, JWTService.__secret_key, algorithms=['HS256'])

            if(decoded_jwt['email'] != email and decoded_jwt['sub'] != mysql_db.get_user_id(email)):
                return "Nu aveti dreptul sa modificati parola acestui cont!", 401

            mysql_db.change_password(email, new_password)
            return "Parola modificata cu succes!", 201
        except EmailNotFoundException as e:
            return "Utilizator cu acest email nu exista!", 404
        except Exception as e:
            print(e)
            return e.message, 500

    #verific daca id-ul dat ca parametru se potriveste cu cel din jwt pentru a determina daca utilizatorul poate face 
    #diverse operatii(de ex. sa adauge o comanda, dar doar pentru el, nu si pentru alti utilizatori)
    @srpc(Unicode, Integer, _returns=(Unicode, Integer))  
    def verify_authority(token, user_id):
        try:
            decoded_jwt = jwt.decode(token, JWTService.__secret_key, algorithms=['HS256'])

            if(decoded_jwt['sub'] != user_id):
                return "Nu aveti accesul la aceasta resursa decat daca folositi datele dumneavoastra!", 401

            return "Aveti acces!", 200
        except ExpiredSignatureError as e:
            mysql_db.blakclist_jwt(token)
            return "Semnatura este expirata!", 401
        except InvalidSignatureError as e:
            mysql_db.blakclist_jwt(token)
            return "Semnatura invalida!", 401
        except DecodeError as e:
            mysql_db.blakclist_jwt(token)
            return "Token-ul este in format invalid!", 401
        except Exception as e:
            print(e)
            return e.message, 500

    @srpc(Unicode, Unicode,  _returns=(Unicode, Integer))  
    def login_user(email, password):
        try:
            if mysql_db.verify_user(email, password):
                payload = {
                    'iss' : "http://127.0.0.1:7789",
                    'sub' : mysql_db.get_user_id(email),
                    'email' : email,
                    #aproximativ 24 de ore
                    'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=86400),
                    'role' : mysql_db.get_user_role(email)
                }

                token = jwt.encode(payload, JWTService.__secret_key)

                return token, 200
            else:
                return "Email/parola incorect/a!", 401
        except Exception as e:
            print(e)
            return "Eroare interna la server-ul de UAC!", 500

    @srpc(Unicode, _returns=(Unicode, Unicode, Integer))  
    def validate_token(token):
        try:
            decoded_jwt = jwt.decode(token, JWTService.__secret_key, algorithms=['HS256'])

            return str(decoded_jwt['sub']), decoded_jwt['role'], 200
        except ExpiredSignatureError as e:
            mysql_db.blakclist_jwt(token)
            return "Eroare la validarea token-ului!", "Semnatura este expirata!", 401
        except InvalidSignatureError as e:
            mysql_db.blakclist_jwt(token)
            return "Eroare la validarea token-ului!", "Semnatura invalida!", 401
        except DecodeError as e:
            mysql_db.blakclist_jwt(token)
            return "Eroare la validarea token-ului!", "Token-ul este in format invalid!", 401
        except Exception as e:
            print(type(e))
            return  "Eroare la validarea token-ului!", "Eroare necunoscuta!", 404

    @srpc(Unicode, _returns=(Unicode, Unicode, Integer))  
    def destroy_token(token):
        try:
            #din cate am inteles, din descriere, oricum ar fi jwt-ul(expirat, invalid, etc) tot ar trebui salvat in db, deci nu vad de ce as ma iicnerca sa il decoeez ??
            mysql_db.blakclist_jwt(token)
        except Exception as e:
            print(type(e))
            return  "Eroare la distrugerea token-ului!", "Eroare necunoscuta!", 404


if __name__=='__main__':
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:7789")
    logging.info("wsdl is at: http://localhost:7789/?wsdl")

    wsgi_app = wsgi_soap_application([JWTService], 'spyne.examples.jwt.soap')
    server = make_server('127.0.0.1', 7789, wsgi_app)
    server.serve_forever()
