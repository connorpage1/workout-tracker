# lib/helpers.py
import re
import time
import os
from termcolor import colored, cprint
from models.trainer import Trainer
from models.session import Session
from models.client import Client


def exit_program():
    print("""
        
Goodbye!



""",)
    time.sleep(2)
    clear_screen()
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
        if trainer := Trainer.find_by_name(first_name.title(), last_name.title()):
            cprint(trainer, 'green')
            trainer_menu(trainer)
        else:
            cprint("No trainer found", 'red')
    else:
        cprint("Invalid name format.", 'red')

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
        if client := Client.find_by_name(first_name.title(), last_name.title()):
            cprint(client, 'green')
            client_menu(client)
        else:
            cprint("No client found", 'red')
    else:
        cprint("Invalid name format.", 'red')
def find_trainer_by_id():
    trainer_id = input("Enter trainer id: ")
    if len(trainer_id.strip()):
        if trainer := Trainer.find_by_id(int(trainer_id)):
            cprint(trainer, 'green')
            trainer_menu(trainer)
        else:
            print(colored("No trainer found", "red"))
    else: 
        print(colored("Invalid id", "red"))
def find_client_by_id():
    client_id = input("Enter client id: ")
    if len(client_id.strip()):
        if client := Client.find_by_id(int(client_id)):
            cprint(client, 'green')
            client_menu(client)
        else:
            print(colored("No client found", "red"))
    else: 
        print(colored("Invalid id", "red"))
def find_session_by_date_and_time():
    date = input("Enter the session date (MM/DD/YYYY): ")
    time = input("Enter the session time (HH:MMAM or HH:MMPM): ")
    if isinstance(date, str) and isinstance(time, str) and len(date) and len(time):
        session = Session.find_by_date_and_time(date, time)
        cprint(session, 'green') if session else cprint("No session found", 'red')
    else:
        cprint("Invalid date or time", 'red')

def update_client_by_id(id, first_name, last_name, email):
    client = Client.find_by_id(id)
    client.first_name = first_name.title()
    client.last_name = last_name.title()
    client.email = email
    client = client.update()
    cprint(f'Client updated {client}', 'green')
    return client


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
            cprint(f"Error updating client: {e}", 'red')
    else:
        cprint("Invalid id, first name, last name, or email", 'red')

def update_trainer_by_id(id, first_name, last_name, specialty):
    trainer = Trainer.find_by_id(id)
    trainer.first_name = first_name.title()
    trainer.last_name = last_name.title()
    trainer.specialty = specialty
    trainer = trainer.update()
    cprint(f"Trainer updated {trainer}", 'green')
    return trainer


def update_trainer():
    trainer_id = input("Enter the trainer's id: ")
    first_name = input("Enter the trainer's first name: ")
    last_name = input("Enter the trainer's last name: ")
    specialty = input("Enter the trainer's specialty: ")
    if (
        isinstance(trainer_id, str)
        and isinstance(first_name, str)
        and isinstance(last_name, str)
        and isinstance(specialty, str)
        and re.match(r"^\d+$", trainer_id)
        and int(trainer_id) > 0
        and len(first_name)
        and len(last_name)
        and len(specialty)
    ):
        try:
            update_trainer_by_id(trainer_id, first_name, last_name, specialty)
        except Exception as e:
            print("Error updating trainer: ", e)
    else:
        print("Invalid id, first name, last name, or specialty")

def client_menu(client_obj):
    while True:
        print()
        print(f"""
[Client: {client_obj.full_name()}]
Please select an option: 
            """)
        print("0. Return to main menu")
        print(f"1. Update {client_obj.first_name}'s first name")
        print(f"2. Update {client_obj.first_name}'s last name")
        print(f"3. Update {client_obj.first_name}'s email")
        print(f"4. Update all of {client_obj.first_name}'s information")
        print(f"5. See all training sessions for {client_obj.first_name}")
        print("6. Delete client records")
        print()
        choice = input("> ")
        if choice == '0':
            break
        elif choice == '1':
            new_first_name = input("Enter a new first name: ")
            client_obj = update_client_by_id(client_obj.id, new_first_name, client_obj.last_name, client_obj.email)
        elif choice == "2":
            new_last_name = input("Enter a new last name: ")
            client_obj = update_client_by_id(client_obj.id, client_obj.first_name, new_last_name, client_obj.email)
        elif choice == "3":   
            new_email = input("Enter a new email: ")
            client_obj = update_client_by_id(client_obj.id, client_obj.first_name, client_obj.last_name, new_email)
        elif choice == "4":
            new_first_name = input("Enter a new first name: ")
            new_last_name = input("Enter a new last name: ")
            new_email = input("Enter a new email: ")
            client_obj = update_client_by_id(client_obj.id, new_first_name, new_last_name, new_email)       
        elif choice == '5':
            if sessions := client_obj.sessions():
                print(sessions)
            else:
                cprint(f"No sessions found for {client_obj.first_name}, 'red")
        elif choice == '6':
            client_obj.delete()
            print(colored("Client deleted", 'yellow'))
            break
        else:
            print("Invalid input")
def trainer_menu(trainer_obj):
    while True:
        print()
        print(f"""
[Trainer: {trainer_obj.full_name()}]
Please select an option: 
            """)
        print("0. Return to main menu")
        print(f"1. Update {trainer_obj.first_name}'s first name")
        print(f"2. Update {trainer_obj.first_name}'s last name")
        print(f"3. Update {trainer_obj.first_name}'s specialty")
        print(f"4. Update all of {trainer_obj.first_name}'s information")
        print(f"5. See all training sessions for {trainer_obj.first_name}")
        print(f"6. See all clients for {trainer_obj.first_name}")
        print("7. Delete trainer records")
        print()
        choice = input("> ")
        if choice == '0':
            break
        elif choice == '1':
            new_first_name = input("Enter a new first name: ")
            trainer_obj = update_trainer_by_id(trainer_obj.id, new_first_name, trainer_obj.last_name, trainer_obj.specialty)
        elif choice == "2":
            new_last_name = input("Enter a new last name: ")
            trainer_obj = update_trainer_by_id(trainer_obj.id, trainer_obj.first_name, new_last_name, trainer_obj.specialty)
        elif choice == "3":   
            new_specialty = input("Enter a new specialty: ")
            trainer_obj = update_trainer_by_id(trainer_obj.id, trainer_obj.first_name, trainer_obj.last_name, new_specialty)
        elif choice == "4":
            new_first_name = input("Enter a new first name: ")
            new_last_name = input("Enter a new last name: ")
            new_specialty = input("Enter a new specialty: ")
            trainer_obj = update_trainer_by_id(trainer_obj.id, new_first_name, new_last_name, new_specialty)       
        elif choice == '5':
            if sessions := trainer_obj.sessions():
                print(sessions)
            else:
                print(colored(f"No sessions found for {trainer_obj.first_name}", 'red'))
        elif choice == '6':
            if clients := trainer_obj.clients():
                print(clients)
            else:
                print(colored(f"No clients found for {trainer_obj.first_name}", 'red'))
        elif choice == '7':
            trainer_obj.delete()
            print(colored("Trainer deleted", 'yellow'))
            break
        else:
            print(colored("Invalid input", "red"))
        
def add_new_client():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    email = input("Email: ")
    
    try:
        Client.create(first_name, last_name, email)
        print(colored("Client created", 'green'))
    except Exception as e:
        print(colored(f"Client not created: {e}", "red"))
        
def add_new_trainer():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    specialty = input("Specialty: ")
    
    try:
        Trainer.create(first_name, last_name, specialty)
        print(colored("Trainer created", 'green'))
    except Exception as e:
        print(colored(f"Trainer not created: {e}", "red"))
        
        
def add_new_session():
    date = input("Enter the appointment date (MM/DD/YYYY): ")
    time = input("Enter the appointment time (HH:MM AM or HH:MM PM): ")
    client_id = input("Enter the client's id: ")
    trainer_id = input("Enter the trainer's id: ")
    if (
        Client.find_by_id(client_id)
        and Trainer.find_by_id(trainer_id)
        and len(date)
        and len(time)
        ):
        try:
            session = Session.create(
                date, time, int(client_id), int(trainer_id)
            )
            cprint(f"Successfully created {session}", 'green')
        except Exception as e:
            print(colored(f"Error creating appointment: {e}", "red"))
    else:
        cprint("Invalid date, time, client id, or trainer id", 'red')