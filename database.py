import psycopg2


class database:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def open_db(self):
        self.conn = psycopg2.connect(
            host="localhost",  # 호스트 값
            port="5432",  # 포트 값 받아 오고
            dbname="library",  # 다
            user="user1",  # 받아
            password="4444"  # 온다
        )
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.cursor.close()
        self.conn.close()
