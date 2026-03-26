from flask import Flask, render_template, request, redirect
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/author')
def author():
    return render_template('author.html')


@app.route('/library')
def library():
    conn = get_db_connection()
    books = conn.execute('select * from books').fetchall()
    conn.close()
    return render_template('library.html', books=books)


@app.route('/book/<int:id>')
def book_detail(id):
    conn = get_db_connection()
    book = conn.execute('select * from books where id = ?', (id,)).fetchone()
    conn.close()
    return render_template('book_detail.html', book=book)


@app.route('/add_book', methods=['post'])
def add_book():

    title = request.form['title']
    author = request.form['author']
    description = request.form['description']
    year = request.form['year']

    image = request.files['image']
    filename = image.filename

    if filename != "":
        image.save(os.path.join('templates/images', filename))

    conn = get_db_connection()

    conn.execute(
        'insert into books (title, author, description, year, image_url, created_at) values (?, ?, ?, ?, ?, ?)',
        (title, author, description, year, filename, datetime.now())
    )

    conn.commit()
    conn.close()

    return redirect('/library')


@app.route('/delete/<int:id>')
def delete_book(id):

    conn = get_db_connection()

    conn.execute('delete from books where id = ?', (id,))

    conn.commit()
    conn.close()

    return redirect('/library')


if __name__ == '__main__':
    app.run(debug=True)