def show_main():
    print('+-------------------------')
    print('|도서관 관리 시스템 메인 메뉴')
    print('|-------------------------')
    print('| 1. 도서 찾기')
    print('| 2. 도서 대출')
    print('| 3. 도서 반납')
    print('| 4. 대출 조회')
    print('| 5. 도서 추가')
    print('| 6. 전체 도서 조회')
    print('| 0. 종료')
    print('|-------------------------')
    main_choice = int(input('|-> 사용자 선택 : '))
    print('+-------------------------')
    return main_choice


def show_sub(service):
    print('+-------------------------')
    print('|도서', service, '서브 메뉴')
    print('|-------------------------')
    print('|도서 ID 또는 이름을 입력하세요')
    print('|-------------------------')
    choice = input('|-> 사용자 입력 : ')
    print('+-------------------------\n')
    return choice


def show_add():
    print('+-------------------------')
    print('|도서 입력 메뉴')
    print('|-------------------------')
    bid = input('|도서ID를 입력하세요 :')
    title = input('|도서명을 입력하세요 :')
    author = input('|저자를 입력하세요 :')
    publisher = input('|출판사를 입력하세요 :')
    print('+-------------------------')
    book = [bid, title, author, publisher]
    return book