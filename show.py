def show_main():
    print('+-------------------------')
    print('| 도서관 관리 시스템 메인 메뉴')
    print('|-------------------------')
    print('| 1. 도서 찾기')
    print('| 2. 도서 대출')
    print('| 3. 도서 반납')
    print('| 4. 도서 추가')
    print('| 5. 대출 도서 조회')
    print('| 6. 전체 도서 조회')
    print('| 0. 종료')
    print('|-------------------------')
    main_choice = int(input('|-> 사용자 선택 : '))
    print('+-------------------------\n')
    return main_choice


def show_sub(service):
    print('+-------------------------')
    print('| 도서', service, '서브 메뉴')
    print('|-------------------------')
    print('|도서 ID 또는 이름을 입력하세요')
    print('|-------------------------')
    choice = input('|-> 사용자 입력 : ')
    print('+-------------------------\n')
    return choice


def show_add():
    print('+-------------------------')
    print('| 도서 입력 메뉴')
    print('|-------------------------')
    title = input('| 도서명을 입력하세요 : ')
    author = input('| 저자를 입력하세요 : ')
    publisher = input('| 출판사를 입력하세요 : ')
    print('+-------------------------\n')
    book = [title, author, publisher]
    return book


def show_book(result, word):
    print('+-------------------------')
    print('|', word)
    print('|-------------------------')
    print('| 도서ID | 도서명 | 저자 | 출판사 | 상태')
    print('|-------------------------')
    for book in result:
        if book[4] == True:
            print('|', book[0], '|', book[1], '|', book[2], '|', book[3], '|대출 가능')
        else:
            print('|', book[0], '|', book[1], '|', book[2], '|', book[3], '|대출 중')
    print('|-------------------------')
    input('|[조회 종료] q입력 후 Enter : ')
    print('+-------------------------\n')


def show_book_loan(result):
    print('+-------------------------')
    print('| 대출 도서 목록 조회')
    print('|-------------------------')
    print('| 도서ID | 도서명 | 저자 | 출판사 | 대출 날짜 ㅣ 반납 일자')
    print('|-------------------------')
    for book in result:
        print('|', book[0], '|', book[1], '|', book[2], '|', book[3], '|', book[4], '|', book[5])
    print('|-------------------------')
    input('|[조회 종료] q입력 후 Enter : ')
    print('+-------------------------\n')


def show_complete(word):
    print('+-------------------------')
    print('| ', word, '이 완료 되었습니다')
    print('|-------------------------')
    input('|[조회 종료] q입력 후 Enter : ')
    print('+-------------------------\n')


def show_error(word):
    print('+-------------------------')
    print('|', word, '도서명 ERROR')
    print('|-------------------------')
    print('| 입력하신 이름의 도서가 없습니다')
    print('|', word, '은 정확한 도서명이 요구됩니다')
    print('|-------------------------')
    input('|[메인 이동] q입력 후 Enter : ')
    print('+-------------------------\n')


def show_already_loan():
    print('+-------------------------')
    print('| 도서가 이미 대출중 입니다')
    print('|-------------------------')
    input('|[메인 이동] q입력 후 Enter : ')
    print('+-------------------------\n')
