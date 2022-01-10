from Database.mysql_database import MySQLBookStoreDB
from DTOs.book import Book

class BookService:
    def __init__(self):
        self.__mysql_db = MySQLBookStoreDB( "db_manager", "1991129_man")

    def add_book(self, isbn):
        self.__mysql_db.create_book(isbn)
    
    def get_books(self, isbn, verbose):
        return self.__mysql_db.get_books(isbn, verbose)
    
    def update_book(self, book: Book):
        self.__mysql_db.update_book(book)
    
    def delete_book(self, isbn):
        self.__mysql_db.delete_book(isbn)
    
    def get_author_by_isbn(self, isbn):
        return self.__mysql_db.get_author_by_isbn(isbn)

    def verify_book_stock(self, isbn):
        return self.__mysql_db.is_book_available(isbn)