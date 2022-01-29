from Database.mysql_database import MySQLBookStoreDB
import requests
from DTOs.book import Book
from DTOs.order import Order
from Database.mongodb_database import MongoDbConnection
from flask import make_response
from suds.client import Client

class OrderService:
    def __init__(self):
        self.__mongo_db = MongoDbConnection()

    def add_order(self, order: Order):
        try:
            BOOK_SERVICE_IP = 'http://localhost'
            BOOK_SERVICE_PORT = '8081'
            BOOK_SERVICE_URI = '/api/bookcollection/books/check-stock/'

            URL = BOOK_SERVICE_IP + ':' + BOOK_SERVICE_PORT + BOOK_SERVICE_URI


            post_dict = {
                "books" : order.items
            }

            r = requests.post(URL, json=post_dict)
            if r.status_code == 200:
                BOOK_SERVICE_IP = 'http://localhost'
                BOOK_SERVICE_PORT = '8081'

                for it in order.items:
                    BOOK_SERVICE_URI = '/api/bookcollection/books/details/%s' % it['isbn']

                    URL = BOOK_SERVICE_IP + ':' + BOOK_SERVICE_PORT + BOOK_SERVICE_URI
                    rr = requests.get(URL, json=post_dict)
                    it['pret'] = rr.json()[6]
                    it['titlu'] = rr.json()[2]
                self.__mongo_db.insert_new_order(order)

            return make_response(r.text, r.status_code)

        except Exception as e:
            print(e)
            return "Eroare necunoscuta la serviciul de comenzi!", 500

    def get_orders(self, user_id):
        ret = []
        for el in  self.__mongo_db.get_orders_for_user(user_id):
            aux = {}
            aux['user_id'] = el['user_id']
            aux['data'] = el['data']
            aux['items'] = el['items']
            aux['status'] = el['status']

            ret.append(aux)


        return ret

