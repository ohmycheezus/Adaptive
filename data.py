import sqlite3


class Database:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cur = self.connection.cursor()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS info (id INTEGER PRIMARY KEY, city text)''')
        self.connection.commit()

    def fetch(self):
        self.cur.execute('''SELECT * FROM info''')
        rows = self.cur.fetchall()
        return rows

    def insert(self, city):
        self.cur.execute('''INSERT INTO info VALUES (NULL,?)''', (city,))
        self.connection.commit()

    def remove(self, id):
        self.cur.execute('''DELETE FROM info WHERE id=?''', (id,))
        self.connection.commit()

    def __del__(self):
        self.connection.close()

    def update(self, id, city):
        self.cur.execute('UPDATE info SET city = ? WHERE id = ?', (city, id))
        self.connection.commit()
