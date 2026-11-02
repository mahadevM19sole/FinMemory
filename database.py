# import sqlite3
# from pathlib import Path


# DB_PATH = Path("data/finmemory.db")


# def get_connection():
#     DB_PATH.parent.mkdir(parents=True, exist_ok=True)
#     return sqlite3.connect(DB_PATH)

# #This function creates your tables.
# def initialize_database():

#     connection = get_connection()
#     cursor = connection.cursor() #cursor is basically the object you use to execute SQL commands.

#     # Store important user information
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS user_memory (
#             key TEXT PRIMARY KEY,
#             value TEXT
#         )
#     """)

#     # Store complete conversation history
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS conversation_history (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             role TEXT NOT NULL,
#             message TEXT NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#     """)

#     connection.commit() #Save the database changes permanently.
#     connection.close()


# def save_memory(key, value):

#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute("""
#         INSERT OR REPLACE INTO user_memory (key, value)
#         VALUES (?, ?)
#     """, (key, value))

#     connection.commit()
#     connection.close()

# #retrieves one particular piece of information.
# def get_memory(key):

#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute(
#         "SELECT value FROM user_memory WHERE key = ?",
#         (key,)
#     )

#     result = cursor.fetchone()

#     connection.close()

#     if result:
#         return result[0]

#     return None

# #This gets all the user's stored financial information.
# def get_all_memory():

#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute(
#         "SELECT key, value FROM user_memory"
#     )

#     results = cursor.fetchall()

#     connection.close()

#     return dict(results)


# #working with the conversation history.
# def save_message(role, message):

#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute("""
#         INSERT INTO conversation_history (role, message)
#         VALUES (?, ?)
#     """, (role, message))

#     connection.commit()
#     connection.close()

# #This function retrieves the conversation:
# #retrieve the previous conversation from the SQLite conversation_history table
# def get_conversation_history():

#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute("""
#         SELECT role, message
#         FROM conversation_history
#         ORDER BY id
#     """)

#     results = cursor.fetchall() #Gets all rows returned by the SQL query.

#     connection.close()

#     return results

import sqlite3
from pathlib import Path


DB_PATH = Path("data/finmemory.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


# ============================================================
# INITIALIZE DATABASE
# ============================================================
#“It handles SQLite database creation, inserting/updating financial memory, and storing/retrieving conversation history.”
def initialize_database():

    connection = get_connection()
    cursor = connection.cursor() #cursor is basically the object you use to execute SQL commands.

    # --------------------------------------------------------
    # USER MEMORY
    # Stores current structured financial information
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # --------------------------------------------------------
    # CONVERSATION HISTORY
    # Stores complete conversation
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# USER MEMORY
# ============================================================

def save_memory(key, value):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO user_memory (key, value)
        VALUES (?, ?)
    """, (key, str(value)))

    connection.commit()
    connection.close()


def get_memory(key):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT value FROM user_memory WHERE key = ?",
        (key,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None


def get_all_memory():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT key, value FROM user_memory"
    )

    results = cursor.fetchall()

    connection.close()

    return dict(results)


# ============================================================
# CONVERSATION HISTORY
# ============================================================

def save_message(role, message):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO conversation_history (role, message)
        VALUES (?, ?)
    """, (role, message))

    connection.commit()
    connection.close()


def get_conversation_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT role, message
        FROM conversation_history
        ORDER BY id
    """)

    results = cursor.fetchall()

    connection.close()

    return results