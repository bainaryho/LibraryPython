import psycopg2


class database:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def open_db(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname="library",
            user="user1",
            password="4444"
        )
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    # cursor.execute("SELECT title FROM Books")
    # rows = cursor.fetchone()
    # rows = cursor.fetchall()
    # for row in rows:
    #    print(row)
