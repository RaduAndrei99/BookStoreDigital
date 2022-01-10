#!/usr/bin/env python3
import sys
  
# setting path
sys.path.append('F:\Faculty\An_IV\POS\Lab_Project')

import json
from pymongo import MongoClient
import pymongo

from DTOs.order import Order
from DTOs.book import Book

class MongoDbConnection():

    def __init__(self):
        f = open("../../Passwords/mongodb.txt", "r")
        self.__CONNECTION_STRING = f.readline()

        self.connect_to_database()

    def connect_to_database(self):

        client = MongoClient(self.__CONNECTION_STRING)

        # Create the database for our example (we will use the same database throughout the tutorial
        self.__db_name = client['user_shopping_list']
    
    def insert_new_order(self, order: Order):
        collection_name =  self.__db_name["orders"]
        #books = [Book("asdas", "asd", "asd", "asd", "asd").__dict__, Book("asdas", "asd", "asd", "asd", "asd").__dict__]
        #order = Order("asdsad", books, "expediata")
        
        collection_name.insert_one(order.__dict__)

    
if __name__ == "__main__":    
    
    db = MongoDbConnection()

    db.insert_stuff()