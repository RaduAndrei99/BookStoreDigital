from Database.mysql_database import MySQLBookStoreDB
import requests
from DTOs.book import Book
from DTOs.order import Order
from Database.mongodb_database import MongoDbConnection

class OrderService:
    def __init__(self):
        self.__mongo_db = MongoDbConnection()

    def verify_stock(self, isbn):
        try:
            BOOK_SERVICE_IP = 'http://localhost'
            BOOK_SERVICE_PORT = '8081'
            BOOK_SERVICE_URI = '/api/bookcollection/books/check-stock/%s' % isbn

            URL = BOOK_SERVICE_IP + ':' + BOOK_SERVICE_PORT + BOOK_SERVICE_URI

            r = requests.post(URL)
            print(r.status_code)
            if r.status_code == 200:
                return True
            else:
                return False

        except Exception as e:
            print(e)
            return False

    def add_order(self, order: Order):
        for book in order.items:
            if not self.verify_stock(book['isbn']):
                print(book)
                return False

        self.__mongo_db.insert_new_order(order)

        return True


