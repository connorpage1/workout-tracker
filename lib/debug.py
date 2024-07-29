#!/usr/bin/env python3
# lib/debug.py

# from models.__init__ import CONN, CURSOR
import ipdb
from models.client import Client, CONN as CLIENT_CONN, CURSOR as CLIENT_CURSOR
from models.trainer import Trainer, CONN as TRAINER_CONN, CURSOR as TRAINER_CURSOR
from models.session import Session, CONN as SESSION_CONN, CURSOR as SESSION_CURSOR

if __name__ == "__main__":
    Session.drop_table()
    Trainer.drop_table()
    Client.drop_table()
    
    Trainer.create_table()
    Client.create_table()
    Session.create_table()

    connor = Client("Connor", "Page", "connorpage@protonmail.com")
    connor.save()
    trainer = Trainer("Bill", "Whetherspoon", "Strength")
    trainer.save()
    session = Session("11/11/2024", "9:00 PM", connor.id, trainer.id)
    session.save()
    ipdb.set_trace()
