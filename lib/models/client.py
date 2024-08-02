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
        elif not re.match(r"^[A-z-]{1,50}$", new_name):
            raise ValueError("First name must be between 1 and 50 characters and can only consist of letters and dashes")
        else:
            self._first_name = new_name

    
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_name):
        if type(new_name) is not str:
            raise TypeError("Name must be a string")
        elif not re.match(r"^[A-z-]{1,50}$", new_name):
            raise ValueError("Last name must be between 1 and 50 characters and can only consist of letters and dashes")
        else:
            self._last_name = new_name
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, new_email):
        if not isinstance(new_email, str):
            raise TypeError("Email must be a string")
        elif not re.match(r"^[\w\.-]+@+[\w-]+\.+[\w\.]{2,}$", new_email):
            raise ValueError("Emails must be in the format you@domain.com")
        else:
            self._email = new_email
    
    def sessions(self):
        CURSOR.execute(
            """
            SELECT * FROM sessions
            WHERE client_id = ?
        """,
            (self.id,),
        )
        rows = CURSOR.fetchall()
        return [Session(row[1], row[2], row[3], row[4], row[0]) for row in rows]
    
    
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
        except sqlite3.Error as e:
            raise TypeError(e) from e
        
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
    @classmethod
    def create(cls, first_name, last_name, email):
        new_client = cls(first_name, last_name, email)
        
        # Save to db
        new_client.save()
        
        return new_client

    @classmethod
    def new_from_db(cls):
        CURSOR.execute(
            """
            SELECT * FROM clients
            ORDER BY id DESC
            LIMIT 1;
        """
        )
        row = CURSOR.fetchone()
        return cls(row[1], row[2], row[3], row[0])

    @classmethod
    def get_all(cls):
        CURSOR.execute(
            """
            SELECT * FROM clients; 
        """
        )
        rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[3], row[0]) for row in rows]

    @classmethod
    def find_by_name(cls, first_name, last_name):
        CURSOR.execute(
            """
            SELECT * FROM doctors
            WHERE first_name is ? 
            AND last_name is ?;
        """,
            (first_name, last_name),
        )
        row = CURSOR.fetchone()
        return cls(row[1], row[2], row[3], row[0]) if row else None

    @classmethod
    def find_or_create_by(cls, first_name, last_name, email):
        return cls.find_by_name(first_name, last_name) or cls.create(
            first_name, last_name, email
        )

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
            SET first_name = ?, last_name = ?, email = ?
            WHERE id = ?
        """,
            (self.first_name, self.last_name, self.email, self.id),
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
                    (first_name, last_name, email)
                    VALUES
                    (?, ?, ?)
                """, (self.first_name, self.last_name, self.email)
                )
                self.id = CURSOR.lastrowid
                type(self).all_[self.id] = self
                return self
        except sqlite3.Error as e:
            raise e  
        
    def delete(self):
        CURSOR.execute(
            """
            DELETE FROM doctors
            WHERE id = ?
        """,
            (self.id,),
        )
        CONN.commit()
        del type(self).all[self.id]
        self.id = None
        return self


from session import Session