# 도서에 대한 클래스 선언
from database import database


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
        return


def book_info(searcher, db):
    if searcher.isdigit():
        sql = "SELECT * FROM Books WHERE book_id= %s "
        db.cursor.execute(sql, searcher)
    else:
        like_word = '\'%'+searcher+'%\''
        sql = "SELECT * FROM Books WHERE title LIKE %s" % (like_word)
        db.cursor.execute(sql)

    result = db.cursor.fetchall()
    print('+-------------------------')
    print('|도서 정보 조회')
    print('|-------------------------')
    print('|도서ID | 도서명 | 저자 | 출판사 | 상태')
    print('|-------------------------')
    for book in result:
        if book[4] == True:
            print('|', book[0], '|', book[1], '|', book[2], '|', book[3], '|대출 가능')
        else:
            print('|', book[0], '|', book[1], '|', book[2], '|', book[3], '|대출 중')
    print('|-------------------------')
    input('|-> Enter : 메뉴로')
    print('+-------------------------\n')
    return

def book_loan(searcher, db):
    if searcher.isdigit():
        update_sql = "UPDATE Books SET is_available = FALSE WHERE book_id= %s "
        insert_sql = "INSERT INTO Loans VALUES (default, %s, now(), null);"

        db.cursor.execute(insert_sql, searcher)
        db.cursor.execute(update_sql, searcher)

    else:
        select_id = "SELECT book_id FROM Books WHERE title = %s " % ('\''+searcher+'\'')
        db.cursor.execute(select_id)
        select_id = db.cursor.fetchone()

        update_sql = "UPDATE Books SET is_available = FALSE WHERE book_id= %s "
        insert_sql = "INSERT INTO Loans VALUES (default, %s, now(), null);"

        db.cursor.execute(insert_sql, select_id)
        db.cursor.execute(update_sql, select_id)

    print('+-------------------------')
    print('|대출이 완료 되었습니다')
    db.conn.commit()
    print('|-------------------------')
    input('|-> Enter : 메뉴로')
    print('+-------------------------\n')
    return


def book_return(searcher, db):
    # 도서 반납 기능 (기본)
    # (기본) 반납을 원하는 도서의 ID 혹은 이름을 입력하여 반납합니다.
    # (기본) 반납하면 도서의 상태가 대출 가능으로 변경됩니다.
    pass
    db.conn.commit()


def book_loan_info():
    # 대출 정보 조회 기능 (심화)
    # 대출한 도서의 정보를 모두 조회할 수 있습니다.
    # 대출 정보는 도서의 ID, 이름, 저자, 출판사, 대출 날짜, 반납일자로 구성됩니다.
    # 대출 정보는 대출 날짜를 기준으로 내림차순으로 정렬됩니다.
    pass

def book_all(db):
    sql = "SELECT * FROM Books;"
    db.cursor.execute(sql)
    result = db.cursor.fetchall()

    print('+-------------------------')
    print('|전체 도서 목록 조회')
    print('|-------------------------')
    print('|도서ID | 도서명 | 저자 | 출판사 | 상태')
    print('|-------------------------')
    for book in result:
        if book[4] == True:
            print('|', book[0], '|', book[1], '|', book[2], '|', book[3], '|대출 가능')
        else:
            print('|', book[0], '|', book[1], '|', book[2], '|', book[3], '|대출 중')
    print('|-------------------------')
    input('|-> Enter : 메뉴로')
    print('+-------------------------\n')
    return