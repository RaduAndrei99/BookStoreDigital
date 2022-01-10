import sys
  
# setting path
sys.path.append('F:\Faculty\An_IV\POS\Lab_Project')


from flask import Flask, request, jsonify
import mysql.connector
import traceback
import json
from flask_cors import CORS
from Database.mysql_database import MySQLBookStoreDB
from DTOs.book import Book
from DTOs.author import Author
from DTOs.book_to_author import BookToAuthor
from Services.BooksService.book_service import BookService
 
f = open("../../Passwords/mysql.txt", "r")
mysql_db = MySQLBookStoreDB( "db_manager", f.readline())

book_store_db = mysql_db.get_connection()

db_cursor = book_store_db.cursor()

#serviciul responsabil cu operatiile CRUD peste carti si autori(cu relatiile repesctive)
book_service = BookService()

#rest APP in flask
app = Flask(__name__)
#pentru CORS policy
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#numarul default de carti afisate pe pagina
DEFAULT_ITEMS_PER_PAGE = 20

#------------------------carti----------------------------------

@app.route('/api/bookcollection/books/<ISBN>/', methods=['GET'])
def books_route_get(ISBN):
  try:
    isbn = ISBN

    verbose = request.args.get('verbose', default = "false", type = str)
    
    json_return_data = book_service.get_books(isbn, verbose)

    return jsonify(json_return_data), 200
  except Exception as e:
      traceback.print_exc()
      return "Eroare necunoscuta la server!", 500


@app.route('/api/bookcollection/books/', methods=['POST'])
def books_route_post():
  try:
    data = request.get_json()

    book_obj = Book(**data)

    book_service.add_book(book_obj)

    return "Carte inserata cu succes!", 201

  except mysql.connector.errors.IntegrityError:
    return "Cartea cu acest ISBN exista deja!", 400
  except Exception as e:
    traceback.print_exc()
    return "Eroare necunoscuta la server!", 500


@app.route('/api/bookcollection/books/<ISBN>/', methods=['PUT'])
def books_route_put(ISBN):
  try:
    data = request.get_json()

    book_obj = Book(**data)
    book_service.update_book(book_obj)

    return "Carte actualizata cu succes!", 201
  except Exception as e:
    traceback.print_exc()
    return "Eroare necunoscuta la server!", 500

@app.route('/api/bookcollection/books/<ISBN>/', methods=['DELETE'])
def books_rout_delete(ISBN):
  try:
    isbn = ISBN
    
    book_service.delete_book(isbn)

    return "Cartea s-a sters cu succes!", 200
      
  except Exception as e:
      traceback.print_exc()
      return "Eroare necunoscuta la server!", 500

#----------------------------------------------------------------


#------------------------autori----------------------------------

@app.route('/api/bookcollection/authors/<ID>/', methods=['GET'])
def authors_route_get(ID):
  try:
    id = ID
    
    book_json = mysql_db.get_author(id)

    return book_json, 200
  except Exception as e:
      traceback.print_exc()
      return "Eroare necunoscuta la server!", 500


@app.route('/api/bookcollection/authors/', methods=['POST'])
def authors_route_post():
  try:
    data = request.get_json()
    author_obj = Author(**data)

    mysql_db.store_author(author_obj)

    return "Autor inserat cu succes!", 201

  except mysql.connector.errors.IntegrityError:
    return "Ceva eroare ca autorul exista deja?!", 500
  except Exception as e:
    traceback.print_exc()
    return "Eroare necunoscuta la server!", 500

@app.route('/api/bookcollection/authors/<ID>/', methods=['PUT'])
def authors_rout_put(ID):
  try:
    id = ID
    data = request.get_json()

    author_obj = Author(**data)
    mysql_db.update_author(author_obj, id)

    return "Autor actualizata cu succes!", 201
  except Exception as e:
    traceback.print_exc()
    return "Eroare necunoscuta la server!", 500

@app.route('/api/bookcollection/authors/<ID>/', methods=['DELETE'])
def authors_rout_delete(ID):
  try:
    id = ID
    
    mysql_db.delete_author(id)

    return "Autorul s-a sters cu succes!", 200

  except Exception as e:
      traceback.print_exc()
      return "Eroare necunoscuta la server!", 500

#----------------------------------------------------------------


#------------------------carti-autori---------------------------

@app.route('/api/bookcollection/books/<ISBN>/authors/', methods=['GET'])
def books_authors_route_get(ISBN):
  try:
    isbn = ISBN
    try:
      book_json = json.dumps(mysql_db.get_books_to_authors(isbn))
      return book_json, 200
    except IndexError:
      return "Nu s-a gasit nicio carte cu acest ISBN!", 404

  except Exception as e:
      traceback.print_exc()
      return "Eroare necunoscuta la server!", 500


@app.route('/api/bookcollection/books/<ISBN>/authors/', methods=['POST'])
def books_authors_route_post(ISBN):
  try:
    data = request.get_json()
    author_obj = BookToAuthor(**data)
    mysql_db.store_book_to_author(author_obj)
    
    return "Autor inserat cu succes pentru cartea selectata!", 201
  except Exception as e:
    return "Eroare necunoscuta la server!", 500

@app.route('/api/bookcollection/books/<ISBN>/authors/', methods=['PUT'])
def books_authors_route_put(ISBN):
  try:
    isbn = ISBN
    data = request.get_json()

    obj = BookToAuthor(**data)
    mysql_db.update_book_to_author(obj, isbn)

    return "Autor actualizata cu succes!", 201
  except Exception as e:
    traceback.print_exc()
    return "Eroare necunoscuta la server!", 500

@app.route('/api/bookcollection/books/<ISBN>/authors/', methods=['DELETE'])
def books_authors_route_delete(ISBN):
  try:
    isbn = ISBN
    
    mysql_db.delete_book_to_author(isbn)

    return "Autorii au fost stersi cu succes!", 200

  except Exception as e:
      traceback.print_exc()
      return "Eroare necunoscuta la server!", 500

#----------------------------------------------------------------


#get pentru carti per pagina
#----------------------------------------------------------------

@app.route('/api/bookcollection/books/', methods=['GET'])
def books_filter_get():
  try:
    page_number = request.args.get('page', default = 1, type = int)
    items_per_page = request.args.get('items_per_page', default = DEFAULT_ITEMS_PER_PAGE, type = int)

    gen_literar = request.args.get('genre', default = "", type = str)
    an_publicare = request.args.get('year', default = 0, type = int)

    sql_statement = ""
    val = []
    if gen_literar == "" and an_publicare != 0:
      sql_statement = "SELECT * FROM carte WHERE an_publicare=%s LIMIT %s OFFSET %s"
      val.append(an_publicare)
    elif an_publicare == 0 and gen_literar != "":
      sql_statement = "SELECT * FROM carte WHERE gen_literar=%s LIMIT %s OFFSET %s"
      val.append(gen_literar)
    elif gen_literar != "" and an_publicare != 0:
      sql_statement = "SELECT * FROM carte WHERE gen_literar=%s AND an_publicare=%s LIMIT %s OFFSET %s"
      val.append(gen_literar)
      val.append(an_publicare)
    else:
      sql_statement = "SELECT * FROM carte LIMIT %s OFFSET %s"

    val.append(items_per_page)
    val.append(items_per_page * (page_number-1))


    db_cursor.execute(sql_statement, val)

    #pentru a lua denumirile 
    row_headers=[x[0] for x in db_cursor.description] 

    res = db_cursor.fetchall()
    json_data=[]
    for result in res:
      json_data.append(dict(zip(row_headers,result)))

    ret_json = {"carti" : json_data}

    return jsonify(ret_json), 200


  except Exception as e:
      traceback.print_exc()
      return "Eroare necunoscuta la server!", 500
#----------------------------------------------------------------

#cautare dupa numele autorilor(partial sau exact)
#----------------------------------------------------------------
@app.route('/api/bookcollection/authors/', methods=['GET'])
def authors_filter_get():
  try:
    nume_autor = request.args.get('name', default = "", type = str)
    match_type = request.args.get('match', default = "partial", type = str)

    sql_statement = ""
    val = []
    if nume_autor != "":
      if match_type != "exact":
        nume_autor = "%" + nume_autor + "%"
        sql_statement = "SELECT * FROM autor WHERE nume LIKE %s OR prenume LIKE %s"
      elif match_type == "exact":
        sql_statement = "SELECT * FROM autor WHERE nume = %s OR prenume = %s"

      val.append(nume_autor)
      val.append(nume_autor)

    else:
      sql_statement = "SELECT * FROM autor"

    print(sql_statement)
    print(val)

    db_cursor.execute(sql_statement, val)

    res = db_cursor.fetchall()

    authors_json = json.dumps(res)

    return authors_json, 200

  except Exception as e:
      traceback.print_exc()
      return "Eroare necunoscuta la server!", 500

#obtin lista de autori pentru o carte
#----------------------------------------------------------------  
@app.route('/api/bookcollection/books/authors/<ISBN>/', methods=['GET'])
def get_authors_by_isbn(ISBN):
  try:
    isbn = ISBN

    authors = book_service.get_author_by_isbn(isbn)

    return jsonify(authors), 200

  except Exception as e:
      traceback.print_exc()
      return "Eroare necunoscuta la server!", 500
#----------------------------------------------------------------  

#verificare daca o carte este in stoc
#----------------------------------------------------------------  
@app.route('/api/bookcollection/books/check-stock/<ISBN>', methods=['POST'])
def check_book_stock(ISBN):
  try:
    isbn = ISBN

    if book_service.verify_book_stock(isbn):
      return "Stock-ul este suficient!", 200
    else:
      return "Stock-ul este insuficient!", 404


  except Exception as e:
      traceback.print_exc()
      return "Eroare necunoscuta la server!", 404
#----------------------------------------------------------------  


#OpenAPI - bookstore
#----------------------------------------------------------------  
#de facut
@app.route('/api/bookcollection/', methods=['OPTIONS'])
def authors_route_options():

  f = open('OpenAPI/bookcollection.json',)
  data = json.load(f)

  return data, 200
  

if __name__ == '__main__':
  app.run(port=8081)