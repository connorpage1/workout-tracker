import sqlite3
from helper import Helper
import re

CONN = sqlite3.connect('database.db')

CURSOR = CONN.cursor()

class Trainer(Helper):
    all_ = {}
    def __init__(self, first_name, last_name, specialty, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.specialty = specialty
        self.id = id
    
    def __repr__(self):
        return f"<Trainer {self.id}: {self.first_name} {self.last_name}, Specialty: {self.specialty}>"
    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, new_name):
        if not isinstance(new_name, str):
            raise TypeError("Name must be a string")
        elif not re.match(r"^[A-z-]{1,50}$", new_name):
            raise ValueError("First name must be between 1 and 50 characters and can only consist of letters and dashes")
        else:
            self._first_name = new_name

    
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_name):
        if not isinstance(new_name, str):
            raise TypeError("Name must be a string")
        elif not re.match(r"^[A-z-]{1,50}$", new_name):
            raise ValueError("Last name must be between 1 and 50 characters and can only consist of letters and dashes")
        else:
            self._last_name = new_name
    
    @property
    def specialty(self):
        return self._specialty
    
    
    @specialty.setter
    def specialty(self, new_specialty):
        if not isinstance(new_specialty, str):
            raise TypeError("Specialty must be a string")
        else:
            self._specialty = new_specialty
        
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
        
    @classmethod
    def create(cls, first_name, last_name, specialty):
        new_trainer = cls(first_name, last_name, specialty)
        
        # Save to db
        new_trainer.save()
        
        return new_trainer
    
    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute(
            """
            SELECT * FROM clients
            WHERE id is ?;
        """,
            (id,),
        )
        row = CURSOR.fetchone()
        return cls(row[1], row[2], row[3], row[0]) if row else None
    
    def update(self):
        CURSOR.execute(
            """
            UPDATE clients
            SET first_name = ?, last_name = ?, specialty = ?
            WHERE id = ?
        """,
            (self.first_name, self.last_name, self.specialty, self.id),
        )
        CONN.commit()
        type(self).all[self] = self
        return self
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