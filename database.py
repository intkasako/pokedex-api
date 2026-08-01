import sqlite3
def init_db():
    connection = sqlite3.connect("pokedex.db")
    connection.row_factory = sqlite3.Row
    connection.executescript(open("schema.sql").read())
    connection.executescript(open("seed.sql").read())
    connection.close()

def get_connection():
    connection = sqlite3.connect("pokedex.db")
    connection.row_factory = sqlite3.Row
    return connection