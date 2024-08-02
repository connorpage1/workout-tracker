import sqlite3
import re

CONN = sqlite3.connect('database.db')

CURSOR = CONN.cursor()
from helper import Helper

class Session(Helper):
    all_ = {}
    def __init__(self, date, time, client_id, trainer_id, id=None):
        self.date = date
        self.time = time
        self.client_id = client_id
        self.trainer_id = trainer_id
        self.id = id
    
    def __repr__(self):
        return f"""Session {self.id}: {self.date} @ {self.time}
                Trainer: {Trainer.find_by_id(self.trainer_id).full_name()}
                Client: {Client.find_by_id(self.client_id).full_name()}
                """
    
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if not isinstance(date, str):
            raise TypeError("Date must be a string")
        elif not re.match(
            r"([0][1-9]|[1][0-2])\/([0][1-9]|[12][0-9]|[3][01])\/\d{4}", date
        ):
            raise ValueError("Date must be in format MM/DD/YYYY")
        else:
            self._date = date

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        if not isinstance(time, str):
            raise TypeError("Time must be a string")
        elif not re.match(r"([0][0-9]|[1][0-2]):[0-5][0-9]\s(AM|PM)", time):
            raise ValueError("Time must be in format HH:MM AM or HH:MM PM")
        else:
            self._time = time
    

    @property
    def trainer_id(self):
        return self._trainer_id

    @trainer_id.setter
    def trainer_id(self, trainer_id):
        if not isinstance(trainer_id, int):
            raise TypeError("trainer_id must be an integer")
        elif trainer_id < 1 or not Trainer.find_by_id(trainer_id):
            raise ValueError(
                "Trainer ID must be a positive integer and point to an existing client"
            )
        else:
            self._trainer_id = trainer_id

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        if not isinstance(client_id, int):
            raise TypeError("Client_id must be must be an integer")
        elif client_id < 1 or not Client.find_by_id(client_id):
            raise ValueError(
                "Client_id must be a positive integer and point to an existing client"
            )
        else:
            self._client_id = client_id
    
    
    def trainer(self):
        return Trainer.find_by_id(self.trainer_id) if self.trainer_id else None

    def client(self):
        return Client.find_by_id(self.client_id) if self.client_id else None
    
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
            raise e
    
    @classmethod
    def create(cls, date, time, client_id, trainer_id):
        # Initialize a new obj with the info provided
        new_session = cls(date, time, client_id, trainer_id)
        # save the obj to make sure it's in the db
        new_session.save()
        return new_session

    @classmethod
    def new_from_db(cls):
        CURSOR.execute(
            """
            SELECT * FROM sessions
            ORDER BY id DESC
            LIMIT 1;
        """
        )
        row = CURSOR.fetchone()
        session = cls(row[1], row[2], row[3], row[4], row[0])
        cls.all_[session.id] = session
        return session

    @classmethod
    def get_all(cls):
        CURSOR.execute(
            """
            SELECT * FROM sessions; 
        """
        )
        rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[0]) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute(
            """
            SELECT * FROM sessions
            WHERE id is ?;
        """,
            (id,),
        )
        row = CURSOR.fetchone()
        return cls(row[1], row[2], row[3], row[4], row[0]) if row else None
    @classmethod
    def find_by_date_and_time(cls, date, time):
        CURSOR.execute(
            """
            SELECT * FROM sessions
            WHERE date is ? AND time is ?;
        """,
            (date, time),
        )
        row = CURSOR.fetchone()
        return cls(row[1], row[2], row[3], row[4], row[0]) if row else None
    
    @classmethod
    def find_or_create_by(cls, date, time, client_id, trainer_id):
        return cls.find_by_date_and_time(date, time) or cls.create(
            date, time, client_id, trainer_id
        )

    #! Utility ORM Instance Methods
    def update(self):
        CURSOR.execute(
            """
            UPDATE sessions
            SET date = ?, time = ?, client_id = ?, trainer_id = ?
            WHERE id = ?
        """,
            (
                self.date,
                self.time,
                self.client_id,
                self.trainer_id,
                self.id,
            ),
        )
        CONN.commit()
        type(self).all[self.id] = self
        return self

    def delete(self):
        CURSOR.execute(
            """
            DELETE FROM sessions
            WHERE id = ?;
        """,
            (self.id,),
        )
        CONN.commit()
        #! Remove memoized object
        del type(self).all[self.id]
        #! Nullify id
        self.id = None
        return self

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
            raise e    




from models.trainer import Trainer
from models.client import Client