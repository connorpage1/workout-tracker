import sqlite3
from helper import Helper

CONN = sqlite3.connect('database.db')

CURSOR = CONN.cursor()

class Trainer(Helper):
    all_ = {}
    def __init__(self, first_name, last_name, specialty, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.specialty = specialty
        self.id = id
    
    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(f"""
                    CREATE TABLE IF NOT EXISTS {cls.pascal_to_camel_plural()}(
                        id INTEGER PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        specialty TEXT
                    );        
                    """)
        except sqlite3.IntegrityError as e:
            return e
        
    @classmethod
    def drop_table(cls):
        try:
            with CONN:
                CURSOR.execute(f"""
                    DROP TABLE IF EXISTS {cls.pascal_to_camel_plural()}
                """)
                
        except sqlite3.IntegrityError as e:
            return e
    def save(self):
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                    INSERT INTO {type(self).pascal_to_camel_plural()}
                    (first_name, last_name, specialty)
                    VALUES
                    (?, ?, ?)
                """, (self.first_name, self.last_name, self.specialty)
                )
                self.id = CURSOR.lastrowid
                type(self).all_[self.id] = self
        except sqlite3.IntegrityError as e:
            return e