import database

MENU_PROMPT = """\n-- COFFEE BEAN APP --

Please choose one of these options:

1) Add a new bean
2) See all beans
3) Find a bean by name
4) See best preparation method for a bean
5) Delete a bean
6) Search for a bean with rating
7) Update a bean rating
0) Exit

Your selection: """


def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != "0":

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

        elif user_input == "7":
            prompt_update_rating(connection)

        else:
            print("Invalid input, please try again!")

    print("Goodbye.")


def prompt_add_new_bean(connection):
    name = input("Enter bean name: ").strip()
    method = input("Enter preparation method: ").strip()

    try:
        rating = int(input("Enter rating (0-100): "))
        if rating < 0 or rating > 100:
            print("Rating must be between 0 and 100.")
            return
    except ValueError:
        print("Invalid rating. Must be a number.")
        return

    database.add_bean(connection, name, method, rating)
    print("Bean added successfully!")


def prompt_see_all_beans(connection):
    beans = database.get_all_beans(connection)

    if not beans:
        print("No beans found.")
        return

    print("\n--- ALL BEANS ---")
    for bean in beans:
        print(f"{bean['name']} ({bean['method']}) - {bean['rating']}/100")


def prompt_find_bean(connection):
    name = input("Enter bean name to find: ").strip()
    beans = database.get_beans_by_name(connection, name)

    if not beans:
        print("No bean found.")
        return

    for bean in beans:
        print(f"{bean['name']} ({bean['method']}) - {bean['rating']}/100")


def prompt_find_best_method(connection):
    name = input("Enter bean name: ").strip()
    bean = database.get_best_preparation_for_bean(connection, name)

    if bean:
        print(
            f"Best preparation for {bean['name']} "
            f"is {bean['method']} with rating {bean['rating']}/100"
        )
    else:
        print("No bean found.")


def prompt_delete_bean(connection):
    name = input("Enter bean name to delete: ").strip()
    database.delete_bean(connection, name)
    print("Bean(s) deleted.")


def prompt_search_bean_rating(connection):
    try:
        rating = int(input("Enter rating to search: "))
    except ValueError:
        print("Invalid rating.")
        return

    beans = database.get_beans_by_rating(connection, rating)

    if not beans:
        print("No beans found with that rating.")
        return

    for bean in beans:
        print(f"{bean['name']} ({bean['method']}) - {bean['rating']}/100")


def prompt_update_rating(connection):
    name = input("Enter bean name to update: ").strip()

    try:
        rating = int(input("Enter new rating (0-100): "))
        if rating < 0 or rating > 100:
            print("Rating must be between 0 and 100.")
            return
    except ValueError:
        print("Invalid rating.")
        return

    database.update_bean_rating(connection, name, rating)
    print("Rating updated!")


menu()
