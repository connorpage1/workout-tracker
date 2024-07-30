from models.client import Client, CONN as CLIENT_CONN, CURSOR as CLIENT_CURSOR
from models.trainer import Trainer, CONN as TRAINER_CONN, CURSOR as TRAINER_CURSOR
from models.session import Session, CONN as SESSION_CONN, CURSOR as SESSION_CURSOR

from faker import Faker
fake = Faker()

import random

if __name__ == "__main__":
    Session.drop_table()
    Trainer.drop_table()
    Client.drop_table()
    
    Trainer.create_table()
    Client.create_table()
    Session.create_table()
    
    trainer_specialties = ["Strength", "Cardio", "Bodybuilding", "Crossfit", "Physical Therapy", "Weight Loss", "Water Aerobics", "Yoga"]
    
    for _ in range(10):
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        email_endings = ["@yahoo.com", "@outlook.com", "@flatironschool.org", "@gmail.com", "@outlook.com"]
        Client.create(first_name, last_name, f"{first_name}.{last_name}{random.choice(email_endings)}")
        
    for _ in range(10):
        Trainer.create(fake.first_name(), fake.last_name(), random.choice(trainer_specialties))