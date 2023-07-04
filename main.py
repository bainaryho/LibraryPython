# 도서 관리 콘솔 어플리케이션
from book import Book
from show import *

book1 = Book('1', '제목', '이진호', '사자출판사', '대출가능')

while 1:
    show_main()
    main_choice = int(input('|-> 사용자 선택 : '))
    print('+-------------------------')

    if main_choice == 1:  # 도서 정보 조회
        book1.book_info()

    elif main_choice == 2:  # 도서 대출
        show_sub('대출')
        book1.book_loan()

    elif main_choice == 3:  # 도서 반납
        show_sub('반납')
        book1.book_return()

    elif main_choice == 4:  # 대출 정보 조회
        book1.book_loan_info()

    elif main_choice == 5:  # 도서 추가
        book1.book_input()

    elif main_choice == 0:  # 종료
        break

    else:
        print('다시 입력')
