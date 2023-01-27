from client import Client
import sqlite3


class SQLite:
    def __init__(self, database):
        self.client = Client()
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    def create_table_weapons(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS [Weapons] (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT NOT NULL UNIQUE,
            caliber TEXT,
            name TEXT,
            type TEXT,
            rec INTEGER,
            ergo INTEGER,
            rpm INTEGER
            )""")

    def create_table_ammo(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS [Ammo] (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT NOT NULL UNIQUE,
            caliber TEXT,
            name TEXT,
            dmg INTEGER,
            pen INTEGER,
            acc TEXT,
            rec TEXT,
            frag TEXT
            )""")

    def insert_weapons(self):
        self.cursor.executemany("""
            INSERT INTO [Weapons] (item_id, caliber, name, type, rec, ergo, rpm)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (item_id)
            DO UPDATE SET
            caliber = EXCLUDED.caliber,
            name = EXCLUDED.name,
            type = EXCLUDED.type,
            rec = EXCLUDED.rec,
            ergo = EXCLUDED.ergo,
            rpm = EXCLUDED.rpm
            """, self.client.get_weapons_list())

    def insert_ammo(self):
        self.cursor.executemany("""
            INSERT INTO [Ammo] (item_id, caliber, name, dmg, pen, acc, rec, frag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (item_id)
            DO UPDATE SET
            caliber = EXCLUDED.caliber,
            name = EXCLUDED.name,
            dmg = EXCLUDED.dmg,
            pen = EXCLUDED.pen,
            acc = EXCLUDED.acc,
            rec = EXCLUDED.rec,
            frag = EXCLUDED.frag
            """, self.client.get_ammo_list())

    def read_selection(self, query):
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            print(row)


if __name__ == '__main__':
    with SQLite('./resources/eft.db') as c:
        c.create_table_weapons()
        c.create_table_ammo()

        c.insert_weapons()
        c.insert_ammo()

        c.read_selection('SELECT * FROM Weapons')
        c.read_selection('SELECT * FROM Ammo')
