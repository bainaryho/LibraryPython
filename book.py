# 도서에 대한 클래스 선언
import psycopg2

from database import database
from show import show_book, show_complete, show_book_loan, show_error, show_cant_avail


class Book:
    def __init__(self, id, title, author, publisher):
        self.id = id
        self.title = title
        self.author = author
        self.publisher = publisher

    def book_input(self, db):  # 도서 입력 함수
        sql = "INSERT INTO Books VALUES (%s,%s,%s,%s, TRUE);"
        db.cursor.execute(sql, (int(self.id), self.title, self.author, self.publisher))
        db.conn.commit()


def new_book_id(db):  # book_id 자동 증가 함수
    try:
        sql = "SELECT max(book_id) FROM Books"
        db.cursor.execute(sql)
        result = db.cursor.fetchone()
        new_id = int(result[0])
        return new_id + 1
    except psycopg2.Error:
        return 1


def get_loan_id(searcher, db):  # 참조 하고 싶은 loan_id를 찾아오는 함수
    sql = "SELECT loan_id FROM Loans WHERE return_date IS NULL AND book_id=%s;" % ('\'' + searcher + '\'')
    db.cursor.execute(sql)
    result = db.cursor.fetchone()
    get_id = int(result[0])
    return get_id


def book_info(searcher, db):  # 도서 검색
    if searcher.isdigit():
        sql = "SELECT * FROM Books WHERE book_id= %s;"
        db.cursor.execute(sql, searcher)
    else:
        like_word = '\'%' + searcher + '%\''
        sql = "SELECT * FROM Books WHERE title LIKE %s" % (like_word)
        db.cursor.execute(sql)

    result = db.cursor.fetchall()
    show_book(result, '도서 정보 조회')


def book_loan(searcher, db):  # 대출 기능
    avail = available(searcher, db) #book.py/available 함수에서 대출이 가능한지 확인 후 대출합니다.
    if not avail:
        show_cant_avail(searcher)
        return

    try:
        if searcher.isdigit(): #숫자로만 입력받은 경우 판단
            update_sql = "UPDATE Books SET is_available = FALSE WHERE book_id= %s;" % ('\'' + searcher + '\'')
            insert_sql = "INSERT INTO Loans VALUES (default, %s, now(), null);" % ('\'' + searcher + '\'')

            db.cursor.execute(insert_sql)
            db.cursor.execute(update_sql)

            db.conn.commit()
        else:
            update_sql = "UPDATE Books SET is_available = FALSE WHERE book_id= %s;"
            insert_sql = "INSERT INTO Loans VALUES (default, %s, now(), null);"

            select_id = "SELECT book_id FROM Books WHERE title = %s " % ('\'' + searcher + '\'')

            db.cursor.execute(select_id)
            select_id = db.cursor.fetchone()

            db.cursor.execute(insert_sql, select_id)
            db.cursor.execute(update_sql, select_id)

            db.conn.commit()

    except psycopg2.Error:
        db.conn.rollback()
        show_error('대출')
        return

    show_complete('대출')


def book_return(searcher, db):  # 반납 기능
    avail = available(searcher, db) #book.py/available 함수에서 반납이 가능한지 확인 후 반납합니다.
    if avail:
        show_cant_avail(searcher)
        return

    try:
        if searcher.isdigit(): #숫자로만 입력받은 경우 판단
            # 반납)업데이트 전에 해당 시퀀스 값(loan_id)를 가져와야함. return_date가 비어있는거
            loan_id = get_loan_id(searcher, db)

            update_books = "UPDATE Books SET is_available = TRUE WHERE book_id= %s;" % ('\'' + searcher + '\'')
            update_loans = "UPDATE Loans SET return_date = now() WHERE book_id= %s AND loan_id= %s;"
            data = [searcher, loan_id]

            db.cursor.execute(update_loans, data)
            db.cursor.execute(update_books)
            db.conn.commit()

        else:
            select_id = "SELECT book_id FROM Books WHERE title = %s " % ('\'' + searcher + '\'')
            db.cursor.execute(select_id)
            select_id = db.cursor.fetchone()

            loan_id = get_loan_id(select_id, db)

            update_books = "UPDATE Books SET is_available = TRUE WHERE book_id= %s;"
            update_loans = "UPDATE Loans SET return_date = now() WHERE book_id= %s AND loan_id= %s;"
            data = [select_id, loan_id]

            db.cursor.execute(update_loans, data)
            db.cursor.execute(update_books, select_id)
            db.conn.commit()

    except psycopg2.Error:
        db.conn.rollback()
        show_error('반납')
        return

    show_complete('반납')


def book_loan_info(db):  # 전체 대출 목록 조회 함수
    sql = "SELECT B.book_id, B.title, B.author, B.publisher, L.loan_date, L.return_date " \
          "FROM Books AS B " \
          "INNER JOIN Loans AS L ON B.book_id = L.Book_id " \
          "ORDER BY loan_date desc ;"
    db.cursor.execute(sql)
    result = db.cursor.fetchall()
    show_book_loan(result)


def book_all(db):  # 전체 도서 목록 조회 함수
    sql = "SELECT * FROM Books ORDER BY book_id;"
    db.cursor.execute(sql)
    result = db.cursor.fetchall()
    show_book(result, '전체 도서 목록 조회')


def available(searcher, db):  # 대출 / 반납 가능 여부 판단 함수
    sql = "SELECT is_available FROM Books WHERE book_id=%s"
    sql_test = "SELECT is_available FROM Books WHERE book_id=%s" % ('\'' + searcher + '\'')

    if searcher.isdigit():
        db.cursor.execute(sql_test)

    else:
        select_id = "SELECT book_id FROM Books WHERE title = %s " % ('\'' + searcher + '\'')
        db.cursor.execute(select_id)
        select_id = db.cursor.fetchone()
        db.cursor.execute(sql, select_id)

    already = db.cursor.fetchone()

    if already[0] == True:
        return True
    else:
        return False
