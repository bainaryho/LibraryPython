import psycopg2
from dotenv import load_dotenv
import  os

class database:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    load_dotenv()

    def open_db(self):
        self.conn = psycopg2.connect(
            #DB정보는 env파일에서 관리합니다.
            host=os.environ.get("admin_host"),
            port=os.environ.get("admin_port"),
            dbname=os.environ.get("admin_dbname"),
            user=os.environ.get("admin_user"),
            password=os.environ.get("admin_password")
        )
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.cursor.close()
        self.conn.close()
