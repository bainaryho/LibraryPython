# 도서에 대한 클래스 선언
import psycopg2

from database import database
from show import show_book, show_complete, show_book_loan, show_error


class Book:
    def __init__(self, id, title, author, publisher):
        self.id = id
        self.title = title
        self.author = author
        self.publisher = publisher

    def book_input(self, db):
        sql = "INSERT INTO Books VALUES (%s,%s,%s,%s, TRUE);"
        db.cursor.execute(sql, (int(self.id), self.title, self.author, self.publisher))
        db.conn.commit()


def new_book_id(db):
    sql = "SELECT max(book_id) FROM Books;"
    db.cursor.execute(sql)
    result = db.cursor.fetchone()
    new_id = int(result[0])
    return new_id+1


def book_info(searcher, db):
    if searcher.isdigit():
        sql = "SELECT * FROM Books WHERE book_id= %s;"
        db.cursor.execute(sql, searcher)
    else:
        like_word = '\'%' + searcher + '%\''
        sql = "SELECT * FROM Books WHERE title LIKE %s" % (like_word)
        db.cursor.execute(sql)

    result = db.cursor.fetchall()
    show_book(result, '도서 정보 조회')


def book_loan(searcher, db):
    select_id = "SELECT book_id FROM Books WHERE title = %s " % ('\'' + searcher + '\'')
    db.cursor.execute(select_id)
    select_id = db.cursor.fetchone()

    update_sql = "UPDATE Books SET is_available = FALSE WHERE book_id= %s;"
    insert_sql = "INSERT INTO Loans VALUES (default, %s, now(), null);"

    try:
        if searcher.isdigit():
            db.cursor.execute(insert_sql, searcher)
            db.cursor.execute(update_sql, searcher)
        else:
            db.cursor.execute(insert_sql, select_id)
            db.cursor.execute(update_sql, select_id)
    except psycopg2.Error:
        db.conn.rollback()
        show_error('대출')
        return

    db.conn.commit()
    show_complete('대출')


def book_return(searcher, db):
    select_id = "SELECT book_id FROM Books WHERE title = %s " % ('\'' + searcher + '\'')
    db.cursor.execute(select_id)
    select_id = db.cursor.fetchone()

    update_books = "UPDATE Books SET is_available = TRUE WHERE book_id= %s;"
    update_loans = "UPDATE Loans SET return_date = now() WHERE book_id= %s;"

    try:
        if searcher.isdigit():
            db.cursor.execute(update_loans, searcher)
            db.cursor.execute(update_books, searcher)
        else:
            db.cursor.execute(update_loans, select_id)
            db.cursor.execute(update_books, select_id)
    except psycopg2.Error:
        db.conn.rollback()
        show_error('반납')
        return

    db.conn.commit()
    show_complete('반납')


def book_loan_info(db):
    sql = "SELECT B.book_id, B.title, B.author, B.publisher, L.loan_date, L.return_date " \
          "FROM Books AS B " \
          "INNER JOIN Loans AS L ON B.book_id = L.Book_id " \
          "WHERE is_available = FALSE " \
          "ORDER BY return_date desc ;"
    db.cursor.execute(sql)
    result = db.cursor.fetchall()
    show_book_loan(result)


def book_all(db):
    sql = "SELECT * FROM Books ORDER BY book_id;"
    db.cursor.execute(sql)
    result = db.cursor.fetchall()
    show_book(result, '전체 도서 목록 조회')
