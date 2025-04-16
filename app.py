import database
from database import connect, delete_bean

MENU_PROMPT = """-- COFFEE BEAN APP2 --

Please choose one of these options:

1) Add a new bean.
2) See all beans.
3) Find a bean by name.
4) See which preparation method is best for a bean.
5) Delete a bean.
6) Search for a bean with rating.
7) Exit.

Your selection:"""


def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != "7":
        if user_input == "1":
           prompt_add_new_bean(connection)
        elif user_input == "2":
            prompt_see_all_beans(connection)
        elif user_input == "3":
            prompt_find_bean(connection)
        elif user_input == "4":
            prompt_find_best_method(connection)
        elif user_input == "5":
            prompt_delete_bean(connection)
        elif user_input == "6":
            prompt_search_bean_rating(connection)
        else:
            print("Invalid input, please try again!")


def prompt_add_new_bean(connection):
    name = input("Enter bean name: ")
    method = input("Enter how you've prepared it: ")
    rating = int(input("Enter your rating score (0-100): "))

    database.add_bean(connection, name, method, rating)

def prompt_see_all_beans(connection):
    beans = database.get_all_beans(connection)

    for bean in beans:
        print(f"{bean[1]} ({bean[2]}) - {bean[3]}/100")

def prompt_find_bean(connection):
    name = input("Enter bean name to find: ")
    beans = database.get_beans_by_name(connection, name)

    for bean in beans:
        print(f"{bean[1]} ({bean[2]}) - {bean[3]}/100")

def prompt_find_best_method(connection):
    name = input("Enter bean name to find: ")
    beans = database.get_beans_by_name(connection, name)

    for bean in beans:
        print(f"{bean[1]} ({bean[2]}) - {bean[3]}/100")

def prompt_delete_bean(connection):
    name = input("Enter bean name to delete: ")
    beans = database.get_beans_by_name(connection, name)

    for bean in beans:
        database.delete_bean(connection, name)

def prompt_search_bean_rating(connection):
    rating = int(input("Enter bean rating to search: "))
    beans = database.get_beans_by_rating(connection, rating)

    for bean in beans:
        print(f"{bean[1]} ({bean[2]}) - {bean[3]}/100")

menu()
