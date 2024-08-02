from models.client import Client, CONN as CLIENT_CONN, CURSOR as CLIENT_CURSOR
from models.trainer import Trainer, CONN as TRAINER_CONN, CURSOR as TRAINER_CURSOR
from models.session import Session, CONN as SESSION_CONN, CURSOR as SESSION_CURSOR

from faker import Faker
fake = Faker()

import random

def drop_tables():
    Session.drop_table()
    Trainer.drop_table()
    Client.drop_table()


def create_tables():
    Trainer.create_table()
    Client.create_table()
    Session.create_table()
    
    
if __name__ == "__main__":
    drop_tables()
    create_tables()

    
    trainer_specialties = ["Strength", "Cardio", "Bodybuilding", "Crossfit", "Physical Therapy", "Weight Loss", "Water Aerobics", "Yoga"]
    email_endings = ["@yahoo.com", "@outlook.com", "@flatironschool.org", "@gmail.com", "@outlook.com"]
    
    for _ in range(50):
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        Client.create(first_name, last_name, f"{first_name}.{last_name}{random.choice(email_endings)}")
        
    for _ in range(50):
        Trainer.create(fake.first_name(), fake.last_name(), random.choice(trainer_specialties))
    
    for _ in range(100):
        try:
            clients = Client.get_all()
            trainers = Trainer.get_all()
            date = fake.date_this_year(before_today=False, after_today=True),
            valid_date = date[0].strftime("%m/%d/%Y")
            Session.create(
                valid_date,
                fake.time("%I:%M %p"),
                random.sample(clients, 1)[0].id,
                random.sample(trainers, 1)[0].id
            )
            print("Created session")
        except Exception as e:
            print("Failed to create session because of error: ", e)
