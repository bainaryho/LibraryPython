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


def new_book_id(db):  # loans의 id 자동 증가 함수
    sql = "SELECT max(book_id) FROM Books;"
    db.cursor.execute(sql)
    result = db.cursor.fetchone()
    new_id = int(result[0])
    return new_id + 1


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
    avail = available(searcher, db)
    if not avail:
        show_cant_avail(searcher)
        return

    try:
        if searcher.isdigit():
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
    avail = available(searcher, db)
    if avail:
        show_cant_avail(searcher)
        return

    try:
        if searcher.isdigit():
            update_books = "UPDATE Books SET is_available = TRUE WHERE book_id= %s;" % ('\'' + searcher + '\'')
            update_loans = "UPDATE Loans SET return_date = now() WHERE book_id= %s;" % ('\'' + searcher + '\'')
            db.cursor.execute(update_loans)
            db.cursor.execute(update_books)
            db.conn.commit()

        else:
            update_books = "UPDATE Books SET is_available = TRUE WHERE book_id= %s;"
            update_loans = "UPDATE Loans SET return_date = now() WHERE book_id= %s;"
            select_id = "SELECT book_id FROM Books WHERE title = %s " % ('\'' + searcher + '\'')
            db.cursor.execute(select_id)
            select_id = db.cursor.fetchone()
            db.cursor.execute(update_loans, select_id)
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
        print('정수형 입력 확인')
        db.cursor.execute(sql_test)
        print('cursor 정상 작동')
    else:
        print('문자형 입력 확인')
        select_id = "SELECT book_id FROM Books WHERE title = %s " % ('\'' + searcher + '\'')
        db.cursor.execute(select_id)
        select_id = db.cursor.fetchone()
        db.cursor.execute(sql, select_id)
        print('cursor 정상 작동')

    already = db.cursor.fetchone()

    print('판단 시작')
    if already[0] == True:
        print('판단 결과 대출 가능')
        return True
    else:
        print('판단 결과 대출중')
        return False
