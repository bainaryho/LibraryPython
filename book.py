#도서에 대한 클래스 선언
class Book:
    def __init__(self, id, title, author, publisher, is_available):
        self.id = id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.is_available = is_available
