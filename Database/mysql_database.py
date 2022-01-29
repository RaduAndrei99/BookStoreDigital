#!/usr/bin/env python3

from DTOs.book import Book
from DTOs.author import Author
from DTOs.book_to_author import BookToAuthor
from DTOs.list_of_books import ListOfBooks
from DTOs.user_credentials import UserCredentials

from Database.Exceptions.exceptions import EmailAlreadyExistsException, EmailNotFoundException, BookNotFoundException, OutOfStockException

import mysql.connector

import json

class MySQLBookStoreDB():
    __HOST = '127.0.0.1' 
    __DATABASE = 'book_store'
    __CONNECT_TIMEOUT = 5

    def __init__(self, user, password):
        self.__user = user

        try:
            self.connect_to_database(user, password)
        except Exception as e:
            print("***** ->" + str(e))

    def connect_to_database(self, username, password):
        self.__db_connection = mysql.connector.connect(
            host=MySQLBookStoreDB.__HOST, 
            user = username, 
            passwd = password, 
            database = MySQLBookStoreDB.__DATABASE,
            connect_timeout=self.__CONNECT_TIMEOUT)

    def get_connection(self):
        return self.__db_connection

    def store_book(self, book: Book):
        sql_statement = "INSERT INTO carte (isbn, titlu, editura, an_publicare, gen_literar) VALUES ( %s, %s, %s, %s, %s)"

        val = []
        val.append(book.isbn)
        val.append(book.titlu)
        val.append(book.editura)
        val.append(book.an_publicare)
        val.append(book.gen_literar)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

        self.__db_connection.commit()

    def get_books(self, isbn, verbose="false"):
        sql_statement = ""
        if verbose == "true":
            sql_statement = "SELECT * FROM carte WHERE ISBN=%s"
        else:
            sql_statement = "SELECT isbn, titlu, gen_literar FROM carte WHERE ISBN=%s"

        val = []
        val.append(isbn)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)
        res = db_cursor.fetchall()

        return res[0]

    def update_book(self, book: Book):
        #first get the id of the book
        sql = "SELECT id_carte FROM carte WHERE isbn=%s"
        val = []
        val.append(book.isbn)
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql, val)

        id_carte = db_cursor.fetchall()[0][0]

        sql = "UPDATE carte SET isbn=%s, titlu=%s, editura=%s, an_publicare=%s, gen_literar=%s WHERE id_carte=%s"
        val = []
        val.append(book.isbn)
        val.append(book.titlu)
        val.append(book.editura)
        val.append(book.an_publicare)
        val.append(book.gen_literar)
        val.append(id_carte)
        print(val)
        db_cursor.execute(sql, val)

        self.__db_connection.commit()

    def delete_book(self, isbn):

        sql_statement = "DELETE FROM carte_la_stoc WHERE id_carte=(SELECT id_carte FROM carte WHERE isbn=%s)"

        val = []
        val.append(isbn)
        
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)
        self.__db_connection.commit()
 

        sql_statement = "DELETE FROM carte_la_autor WHERE id_carte=(SELECT id_carte FROM carte WHERE isbn=%s)"

        val = []
        val.append(isbn)
        
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)
        self.__db_connection.commit()


        sql_statement = "DELETE FROM carte WHERE isbn=%s"

        val = []
        val.append(isbn)
        
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)
        self.__db_connection.commit()


    def store_author(self, author: Author):
        sql_statement = "INSERT INTO autor (nume, prenume) VALUES (%s, %s)"

        val = []
        val.append(author.nume)
        val.append(author.prenume)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

        self.__db_connection.commit()

    def get_author(self, id):
        sql_statement = "SELECT * FROM autor WHERE id_autor=%s"
        val = []
        val.append(id)
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)
        res = db_cursor.fetchall()

        return res[0]

    def delete_author(self, id):
        sql_statement = "DELETE FROM autor WHERE id_autor=%s"

        val = []
        val.append(id)
        
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

    def update_author(self, author:Author, id):
        sql = "UPDATE autor SET nume=%s, prenume=%s WHERE id_autor=%s"
        val = []
        val.append(author.nume)
        val.append(author.prenume)
        val.append(id)
         
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql, val)

        self.__db_connection.commit()

    def update_book_to_author(self, book_to_author: BookToAuthor, isbn):
        sql = "UPDATE carte_la_autor SET id_carte=%s, id_autor=%s, autor_index=%s WHERE id_autor=(SELECT id_carte FROM carte WHERE isbn=%s)"
        val = []
        val.append(book_to_author.id_carte)
        val.append(book_to_author.id_autor)
        val.append(book_to_author.autor_index)
        val.append(isbn)
            
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql, val)

        self.__db_connection.commit()

    def get_author_by_isbn(self, isbn):
        sql = "SELECT nume, prenume FROM autor a INNER JOIN carte_la_autor ca ON a.id_autor = ca.id_autor INNER JOIN carte c ON ca.id_carte = c.id_carte WHERE c.isbn=%s"
        val = []
        val.append(isbn)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql, val)
        res = db_cursor.fetchall()

        return res

    def get_books_to_authors(self, isbn):
        return_json = {"Carte": "","Autori":""};  

        sql_statement = "SELECT * FROM autor WHERE id_autor IN (SELECT id_autor FROM carte_la_autor WHERE id_carte=(SELECT id_carte FROM carte WHERE ISBN=%s))"
        val = []
        val.append(isbn)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)
        res = db_cursor.fetchall()
        return_json["Autori"] = res


        sql_statement = "SELECT * FROM carte WHERE isbn=%s"

        db_cursor.execute(sql_statement, val)
        res = db_cursor.fetchall()
        return_json["Carte"] = res[0]

        return return_json

    def store_book_to_author(self, book_to_author: BookToAuthor):
        db_cursor = self.__db_connection.cursor()

        #determin index-ul pentru urmatorul autor al cartii
        autor_index = 0
        sql_statement = "SELECT autor_index FROM carte_la_autor WHERE id_carte=%s LIMIT 1"  
        val = []
        val.append(book_to_author.id_carte)
        db_cursor.execute(sql_statement, val)
        res = db_cursor.fetchall()
        autor_index = res[0][0]

        #inserez in baza de date noua legatura carte->autor
        sql_statement = "INSERT INTO carte_la_autor (id_carte, id_autor, autor_index) VALUES (%s, %s, %s)"
        val = []
        val.append(book_to_author.id_carte)
        val.append(book_to_author.id_autor)
        val.append(autor_index)
        
        db_cursor.execute(sql_statement, val)

        self.__db_connection.commit()

    def delete_book_to_author(self, isbn):
        sql_statement = "DELETE FROM carte_la_autor WHERE id_carte=(SELECT id_carte FROM carte WHERE isbn=%s)"
        val = []
        val.append(isbn)
    
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)
    
    def is_book_available(self, list_of_books: ListOfBooks):
        for book in list_of_books.books:
            isbn = book['isbn']
            quantity = book['cantitate']

            sql_statement = "SELECT stoc FROM carte_la_stoc WHERE id_carte=(SELECT id_carte FROM carte WHERE isbn=%s)"
            val = []
            val.append(isbn)
        
            db_cursor = self.__db_connection.cursor()

            db_cursor.execute(sql_statement, val)
            res = db_cursor.fetchall()
            if len(res) == 0: 
                self.__db_connection.rollback()
                raise BookNotFoundException("Cartea cu isbn-ul " + str(isbn) + " nu exista!")

            stoc = res[0][0]

            if stoc - quantity >= 0:
                sql_statement = "UPDATE carte_la_stoc SET stoc=%s WHERE id_carte=(SELECT id_carte FROM carte WHERE isbn=%s)"
                val = []
                val.append(str(stoc - quantity))
                val.append(isbn)

                db_cursor = self.__db_connection.cursor()

                db_cursor.execute(sql_statement, val)
            else:
                self.__db_connection.rollback()
                raise OutOfStockException("Cartea cu isbn-ul " + str(isbn) + " nu mai este in stock sau stock-ul nu este suficient!")

        self.__db_connection.commit()


    def create_user(self, email, password):
        sql_statement = "SELECT * FROM user where email=%s"

        val = []
        val.append(email)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

        res = db_cursor.fetchall()
        if len(res) > 0:
            raise EmailAlreadyExistsException("Email-ul deja exista in baza de date!")


        sql_statement = "INSERT INTO user (email, user_password, id_role) VALUES ( %s, %s, (SELECT id_role from user_role WHERE role_name=\"client\"))"

        val = []
        val.append(email)
        val.append(password)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

        self.__db_connection.commit()



    def delete_user(self, email):
        sql_statement = "SELECT * FROM user where email=%s"

        val = []
        val.append(email)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

        res = db_cursor.fetchall()
        if len(res) == 0:
            raise EmailNotFoundException("Email-ul introdus nu exista!")

        sql_statement = "DELETE FROM user WHERE email=%s"

        val = []
        val.append(email)
        
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)
        self.__db_connection.commit()


    def verify_user(self, email, password):
        sql_statement = "SELECT * FROM user where email=%s"

        val = []
        val.append(email)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

        res = db_cursor.fetchall()
        if len(res) == 0:
            return False
        else:         
            print(res)
            if( res[0][2] == password):
                return True
            else:
                return False 

    def change_password(self, email, new_password):
        sql_statement = "SELECT * FROM user where email=%s"

        val = []
        val.append(email)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

        res = db_cursor.fetchall()
        if len(res) == 0:
            raise EmailNotFoundException("Email-ul introdus nu exista!")
            
        sql = "UPDATE user SET user_password=%s WHERE email=%s"
        val = []
        val.append(new_password)
        val.append(email)

            
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql, val)

        self.__db_connection.commit()
    
    def update_user_role(self, email, new_id):
        sql = "UPDATE user SET id_role=%s WHERE email=%s"
        val = []
        val.append(new_id)
        val.append(email)

            
        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql, val)

        self.__db_connection.commit()

    def get_user_id(self, email):
        sql_statement = "SELECT * FROM user where email=%s"

        val = []
        val.append(email)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

        res = db_cursor.fetchall()
        if len(res) == 0:
            raise EmailNotFoundException("Email-ul introdus nu exista!")
        else:         
            return res[0][0]

    def get_user_role(self, email):
        sql_statement = "SELECT role_name FROM user_role WHERE id_role=(SELECT id_role FROM user WHERE email=%s)"

        val = []
        val.append(email)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

        res = db_cursor.fetchall()
        if len(res) == 0:
            raise EmailNotFoundException("Email-ul introdus nu exista!")
        else:         
            return res[0][0]

    def blakclist_jwt(self, jwt):
        sql_statement = "INSERT INTO jwt_blacklist(blacklisted_jwt) VALUES (%s)"

        val = []
        val.append(jwt)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

        self.__db_connection.commit()

    def get_book_details(self, isbn):
        ret = []

        sql_statement = "SELECT * FROM carte WHERE isbn=%s"

        val = []
        val.append(isbn)

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)

        res = db_cursor.fetchall()
        if len(res) == 0:
            raise BookNotFoundException("Cartea cu isbn-ul " + str(isbn) + " nu exista!")
        
        for it in res[0]:
            ret.append(it)


        sql_statement = "SELECT * FROM carte_la_stoc WHERE id_carte=%s"

        val = []
        val.append(res[0][0])

        db_cursor = self.__db_connection.cursor()

        db_cursor.execute(sql_statement, val)
        res = db_cursor.fetchall()

        ret.append(res[0][3])

        return ret

