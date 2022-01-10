
import logging

from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer
from spyne.model.primitive import Unicode

from spyne.util.simple import wsgi_soap_application

import jwt
import datetime

from suds.sudsobject import Iter

class SomeObject(ComplexModel):
    __namespace__ = 'spyne.examples.jwt.soap'

    i = Integer
    s = Unicode


class JWTService(ServiceBase):
    __out_header__ = SomeObject

    __secret_key = "SECRET_KEY"

    @srpc(Unicode, Unicode,  _returns=(Unicode, Integer))  
    def login_user(email, password):
        try:
            payload = {
                'email' : email,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=1000)
                }

            if password and password == 'secret':
                token = jwt.encode(payload, JWTService.__secret_key)
                return token, 200
            else:
                return "Parola este incorecta!", 401
        except Exception as e:
            return "Token invalid!", 401

    @srpc(Unicode, _returns=Integer)  
    def validate_token(token):
        try:
            decoded_jwt = jwt.decode(token, JWTService.__secret_key, algorithms=['HS256'])

            return 200
        except Exception as e:
            print(e)
            return 404


if __name__=='__main__':
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:7789")
    logging.info("wsdl is at: http://localhost:7789/?wsdl")

    wsgi_app = wsgi_soap_application([JWTService], 'spyne.examples.jwt.soap')
    server = make_server('127.0.0.1', 7789, wsgi_app)
    server.serve_forever()
