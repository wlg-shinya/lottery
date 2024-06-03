import psycopg2

class Database():
    def __init__(self):
        self.connection = psycopg2.connect("postgres://postgres:postgres@localhost:8502/lottery")
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def execute(self, query: str) -> str:
        self.cursor.execute(query)
        return self.cursor.fetchall()
