# lib/helpers.py
import re
import os 
from models.trainer import Trainer
from models.session import Session
from models.client import Client


def exit_program():
    print("Goodbye!")
    exit()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def list_trainers():
    if trainers := Trainer.get_all():
        for trainer in trainers:
            print(trainer)
    else:
        print(
            "I am sorry, we currently have no trainers on staff"
        )

def list_clients():
    if clients := Client.get_all():
        for client in clients:
            print(client)
    else:
        print(
            "No clients found"
        )

def list_sessions():
    if sessions:= Session.get_all():
        for session in sessions:
            print(session)
    else:
        print("I am sorry, it looks like we have no sessions in our system")


def find_trainer_by_name():
    first_name = input("Enter the trainer's first name: ")
    last_name = input("Enter the trainer's last name: ")
    if (len(first_name.strip()) 
        and re.match(r"^[a-zA-Z ]+$", first_name) 
        and first_name.title()
        and len(last_name.strip()) 
        and re.match(r"^[a-zA-Z ]+$", last_name) 
        and last_name.title()
        ):
        trainer = Trainer.find_by_name(first_name.title(), last_name.title())
        print(trainer) if trainer else print("No trainer found")
    else:
        print("Invalid name format.")

def find_client_by_name():
    first_name = input("Enter the clients's first name: ")
    last_name = input("Enter the client's last name: ")
    if (len(first_name.strip()) 
        and re.match(r"^[a-zA-Z ]+$", first_name) 
        and first_name.title()
        and len(last_name.strip()) 
        and re.match(r"^[a-zA-Z ]+$", last_name) 
        and last_name.title()
        ):
        client = Client.find_by_name(first_name.title(), last_name.title())
        print(client) if client else print("No client found")
    else:
        print("Invalid name format.")

def update_client_by_id(id, first_name, last_name, email):
    client = Client.find_by_id(id)
    client.first_name = first_name.title()
    client.last_name = last_name.title()
    client.email = email
    client = client.update()
    print(client)


def update_client():
    client_id = input("Enter the client's id: ")
    first_name = input("Enter the client's first name: ")
    last_name = input("Enter the client's last name: ")
    email = input("Enter the client's email: ")
    if (
        isinstance(client_id, str)
        and isinstance(first_name, str)
        and isinstance(last_name, str)
        and isinstance(email, str)
        and re.match(r"^\d+$", client_id)
        and int(client_id) > 0
        and len(first_name)
        and len(last_name)
        and len(email)
    ):
        try:
            update_client_by_id(client_id, first_name, last_name, email)
        except Exception as e:
            print("Error updating client: ", e)
    else:
        print("Invalid id, first name, last name, or email")

update_client()
clear_screen()