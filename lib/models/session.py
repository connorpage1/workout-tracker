import sqlite3

CONN = sqlite3.connect('database.db')

CURSOR = CONN.cursor()
from helper import Helper

class Session(Helper):
    all_ ={}
    def __init__(self, date, time, client_id, trainer_id, id=None):
        self.date = date
        self.time = time
        self.client_id = client_id
        self.trainer_id = trainer_id
        self.id = id
        
    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(f"""
                    CREATE TABLE IF NOT EXISTS {cls.pascal_to_camel_plural()} (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        time TEXT,
                        client_id INTEGER,
                        trainer_id INTEGER,
                        FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
                        FOREIGN KEY (trainer_id) REFERENCES trainers(id) ON DELETE CASCADE
                    );
                """)
        except sqlite3.IntegrityError as e:
            return e
        
    @classmethod
    def drop_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                        DROP TABLE IF EXISTS {cls.pascal_to_camel_plural()}
                    """
                )
        except sqlite3.IntegrityError as e:
            return e
    
    def save(self):
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                    INSERT INTO {type(self).pascal_to_camel_plural()}
                    (date, time, client_id, trainer_id)
                    VALUES
                    (?, ?, ?, ?)
                """, (self.date, self.time, self.client_id, self.trainer_id)
                )
                self.id = CURSOR.lastrowid
                type(self).all_[self.id] = self
        except sqlite3.IntegrityError as e:
            return e    