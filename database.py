import sqlite3


CREATE_BEANS_TABLE = """
CREATE TABLE IF NOT EXISTS beans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    method TEXT NOT NULL,
    rating INTEGER NOT NULL
);
"""

INSERT_BEAN = "INSERT INTO beans (name, method, rating) VALUES (?, ?, ?);"

GET_ALL_BEANS = "SELECT * FROM beans;"
GET_BEANS_BY_NAME = "SELECT * FROM beans WHERE name = ?;"
GET_BEANS_BY_RATING = "SELECT * FROM beans WHERE rating = ?;"

UPDATE_BEAN_RATING = "UPDATE beans SET rating = ? WHERE name = ?;"

GET_BEST_PREPARATION_FOR_BEANS = """
SELECT * FROM beans
WHERE name = ?
ORDER BY rating DESC
LIMIT 1;
"""

DELETE_BEAN = "DELETE FROM beans WHERE name = ?;"


def connect():
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_tables(connection):
    with connection:
        connection.execute(CREATE_BEANS_TABLE)


def add_bean(connection, name, method, rating):
    with connection:
        connection.execute(INSERT_BEAN, (name, method, rating))


def get_all_beans(connection):
    with connection:
        return connection.execute(GET_ALL_BEANS).fetchall()


def get_beans_by_name(connection, name):
    with connection:
        return connection.execute(GET_BEANS_BY_NAME, (name,)).fetchall()


def get_beans_by_rating(connection, rating):
    with connection:
        return connection.execute(GET_BEANS_BY_RATING, (rating,)).fetchall()


def get_best_preparation_for_bean(connection, name):
    with connection:
        return connection.execute(GET_BEST_PREPARATION_FOR_BEANS, (name,)).fetchone()


def update_bean_rating(connection, name, rating):
    with connection:
        connection.execute(UPDATE_BEAN_RATING, (rating, name))


def delete_bean(connection, name):
    with connection:
        connection.execute(DELETE_BEAN, (name,))
