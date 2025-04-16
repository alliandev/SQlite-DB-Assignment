import sqlite3


CREATE_BEANS_TABLE = "CREATE TABLE IF NOT EXISTS beans (id INTEGER PRIMARY KEY, name TEXT, method TEXT, rating INTEGER);"

INSERT_BEAN = "INSERT INTO beans (name, method, rating) VALUES (?, ?, ?);"

GET_ALL_BEANS = "SELECT * FROM beans;"
GET_BEANS_BY_NAME = "SELECT * FROM beans WHERE name = ?;"
GET_BEANS_BY_RATING = "SELECT * FROM beans WHERE rating = ?;"
GET_BEST_PREPARATION_FOR_BEANS = """
SELECT * FROM beans
WHERE name = ?
ORDER BY rating DESC
LIMIT 1;"""

DELETE_BEAN = "DELETE FROM beans WHERE name = ?;"

def connect():
    return sqlite3.connect("data.db")


def create_tables(connection):
    with connection:
        connection.execute(CREATE_BEANS_TABLE)


def add_bean(connection, name, method, rating):
    with connection:
        return connection.execute(INSERT_BEAN, (name, method, rating))

def get_all_beans(connection):
    with connection:
        return connection.execute(GET_ALL_BEANS).fetchall()

def get_beans_by_name(connection, name):
    with connection:
        return connection.execute(GET_BEANS_BY_NAME, (name,)).fetchall()

def get_best_preparation_for_bean(connection, name):
    with connection:
        return connection.execute(GET_BEST_PREPARATION_FOR_BEANS, (name,)).fetchone()

def delete_bean(connection, name):
    with connection:
        return connection.execute(DELETE_BEAN, (name,)).fetchall()

def get_beans_by_rating(connection, rating):
    with connection:
        return connection.execute(GET_BEANS_BY_RATING, (rating,)).fetchall()
