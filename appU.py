from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)



def db_connection():
    conn=None
    try:
        conn=sqlite3.connect('books.sqlite')
    except sqlite3.Error as e:
        print(e)
    return conn


@app.route("/books", methods=['GET','POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    books=None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book")
        books = [
            dict( id=row[0], author= row[1], language = row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)
        else:
            "No books found", 404
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        sql="""INSERT INTO book (author, language, title) VALUES (?,?,?)"""
        cursor.execute(sql,(new_author,new_lang,new_title))
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created sucessfully",201

@app.route('/books/<int:id>', methods=['GET','PUT','DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book=None
    if request.method=="GET":
        cursor.execute("SELECT * FROM book WHERE id=?",(id,))
        rows = cursor.fetchall()
        for r in rows:
            book=r
        if book is not None:
            return jsonify(book),200
        else:
            return "Something went wrong", 404
    if request.method=="PUT":
        sql="""UPDATE book SET title=?,author=?,language=? WHERE id=?"""
        updated_author = request.form['author']
        updated_lang = request.form['language']
        updated_title = request.form['title']
        updated_book={
            "id":id,
            "author":updated_author,
            "language":updated_lang,
            "title":updated_title
        }
        cursor.execute(sql,(updated_author,updated_lang,updated_title,id))
        conn.commit()
        return jsonify(updated_book)
    if request.method=="DELETE":
        sql="""DELETE FROM book WHERE id=?"""
        cursor.execute(sql,(id,))
        conn.commit()
        return "The book with id: {} has been deleted".format(id),200
if __name__== "__main__":
    app.run()
