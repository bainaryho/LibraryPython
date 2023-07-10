# 도서 관리 콘솔 어플리케이션
import psycopg2

from book import *
from database import database
from show import *

if __name__ == '__main__':
    db = database(None, None)  # db 객체 생성
    db.open_db()  # db 열기
    manu_temp = None #메뉴 선택 변수 추가

    while 1:
        main_choice = show_main()

        if main_choice == 1:  # 도서 정보 조회
            searcher = show_sub('정보 조회')
            book_info(searcher, db)

        elif main_choice == 2:  # 도서 대출
            searcher = show_sub('대출')
            book_loan(searcher, db)

        elif main_choice == 3:  # 도서 반납
            searcher = show_sub('반납')
            book_return(searcher, db)

        elif main_choice == 4:  # 도서 추가
            new_id = new_book_id(db)
            add = show_add()  # list 타입 리턴 도서 정보
            newbook = Book(new_id, add[0], add[1], add[2])
            newbook.book_input(db)

        elif main_choice == 5:  # 대출 도서 조회
            book_loan_info(db)

        elif main_choice == 6:  # 전체 도서 조회
            book_all(db)

        elif main_choice == 0:  # 종료
            db.close_db()  # db 닫기
            break

        else:
            print('다시 입력 해주세요')