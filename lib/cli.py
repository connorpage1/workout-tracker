# lib/cli.py
import time
from termcolor import colored
from models.client import Client
from models.session import Session
from models.trainer import Trainer
from helpers import (
    exit_program,
    list_trainers,
    list_clients,
    list_sessions,
    find_trainer_by_name,
    find_client_by_name,
    add_new_client,
    add_new_trainer,
    find_session_by_date_and_time,
    add_new_session, 
    find_client_by_id,
    find_trainer_by_id
)


def main():
    Client.get_all()
    Session.get_all()
    Trainer.get_all()
    welcome_menu()
    time.sleep(1)
    while True:
        time.sleep(1)
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_trainers()
        elif choice == "2":
            list_clients()
        elif choice == "3":
            list_sessions()
        elif choice == "4":
            find_trainer_by_name()
        elif choice == "5":
            find_client_by_name()
        elif choice == "6":
            find_trainer_by_id()
        elif choice == "7":
            find_client_by_id()
        elif choice == "8":
            find_session_by_date_and_time()
        elif choice == "9":
            add_new_client()
        elif choice == "10":
            add_new_trainer()
        elif choice == "11":
            add_new_session()
        else:
            print(colored("Invalid choice", 'red'))


def welcome_menu():
    print(colored("""

        Welcome!
        
        
        
        
        
        """, "blue", attrs=['bold']))
def menu():
    print(colored("""      
[Main menu]
        
        """, "magenta"))
    print("Please select an option:")
    print("0. Exit the program")
    print("1. See all trainers")
    print("2. See all clients")
    print("3. See all sessions")
    print("4. Search for a trainer by name")
    print("5. Search for a client by name")
    print("6. Search for a trainer by id")
    print("7. Search for a client by id")
    print("8. Find a session by date and time")
    print("9. Add a new client")
    print("10. Add a new trainer")
    print("11. Create a new session")
    
    print()


if __name__ == "__main__":
    main()
