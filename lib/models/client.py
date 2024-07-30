import sqlite3
import re

CONN = sqlite3.connect('database.db')

CURSOR = CONN.cursor()
from helper import Helper

class Client(Helper):
    all_ = {}
    def __init__(self, first_name, last_name, email, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.id = id
    
    def __repr__(self):
        return f"<Client {self.id}: {self.first_name} {self.last_name}, {self.email}>"
    
    # Attributes and properties
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, new_name):
        if type(new_name) is not str:
            raise TypeError("Name must be a string")
        elif not re.match(r"[A-z-]{1,50}", new_name):
            raise ValueError("Names must be between 1 and 50 characters and can only consist of letters and dashes")
        else:
            self._first_name = new_name

    
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_name):
        if type(new_name) is not str:
            raise TypeError("Name must be a string")
        elif not re.match(r"[A-z-]{1,50}", new_name):
            raise ValueError("Names must be between 1 and 50 characters and can only consist of letters and dashes")
        else:
            self._last_name = new_name
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, new_email):
        if not isinstance(new_email, str):
            raise TypeError("Email must be a string")
        elif not re.match(r"^[\w\.-]+@+[\w-]+\.+[\w\.]{2,}", new_email):
            raise ValueError("Emails must be in the format you@domain.com")
        else:
            self._email = new_email
    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(f"""
                    CREATE TABLE IF NOT EXISTS {cls.pascal_to_camel_plural()} (
                        id INTEGER PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT UNIQUE
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
                    (first_name, last_name, email)
                    VALUES
                    (?, ?, ?)
                """, (self.first_name, self.last_name, self.email)
                )
                self.id = CURSOR.lastrowid
                type(self).all_[self.id] = self
        except sqlite3.IntegrityError as e:
            return e    