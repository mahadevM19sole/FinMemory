# from database import (
#     initialize_database,
#     save_memory,
#     get_memory,
#     get_all_memory,
#     save_message,
#     get_conversation_history,
# )

# #This class provides all the memory operations your application needs.
# class FinMemory:

#     def __init__(self):#Initialize database

#         # Create database/tables
#         initialize_database()

#         # -------------------------
#         # Short-Term Memory
#         # Lives only during current execution
#         # -------------------------
#         self.short_term_memory = []

#     # ======================================================
#     # SHORT-TERM MEMORY
#     # ======================================================

#     def add_to_short_term(self, role, message):#function adds a message to short-term memory.
#         """Store recent conversation in RAM."""
#         self.short_term_memory.append({
#             "role": role,
#             "message": message
#         })

#     def get_short_term_memory(self, limit=10):
#         """Return last N messages."""
#         return self.short_term_memory[-limit:] #it returns only the last 10.

#     def clear_short_term(self):
#         """Clear current session memory."""
#         self.short_term_memory = []

#     # ======================================================
#     # SESSION / PERSISTENT MEMORY,SQLite.
#     # ======================================================

#     def remember(self, key, value):
#         save_memory(key, value) #It calls:save_memory() from database.py.

#     def recall(self, key): #retrieves one specific memory.
#         return get_memory(key)

#     def get_profile(self):#This retrieves all stored financial facts.
#         return get_all_memory()

#     # ======================================================
#     # CONVERSATION HISTORY
#     # ======================================================

#     def save_conversation(self, role, message):
#         save_message(role, message)

#     def get_history(self): #retrieves previous conversations from SQLite.
#         return get_conversation_history()

from database import (
    initialize_database,
    save_memory,
    get_memory,
    get_all_memory,
    save_message,
    get_conversation_history,
)
#It provides a common interface for short-term memory, persistent financial memory, and conversation history.”

class FinMemory:

    def __init__(self):

        # Create database and tables
        initialize_database()

        # ====================================================
        # SHORT-TERM MEMORY
        # ====================================================

        self.short_term_memory = []

    # ========================================================
    # SHORT-TERM MEMORY
    # ========================================================

    def add_to_short_term(self, role, message):

        self.short_term_memory.append({
            "role": role,
            "message": message
        })

    def get_short_term_memory(self, limit=10):

        return self.short_term_memory[-limit:]

    def clear_short_term(self):

        self.short_term_memory = []

    # ========================================================
    # SQLITE PERSISTENT MEMORY
    # ========================================================

    def remember(self, key, value):

        save_memory(key, value) ##It calls:save_memory() from database.py.

    def recall(self, key): ##retrieves one specific memory.

        return get_memory(key)

    def get_profile(self):

        return get_all_memory()

    # ========================================================
    # CONVERSATION HISTORY
    # ========================================================

    def save_conversation(self, role, message):

        save_message(role, message)

    def get_history(self):

        return get_conversation_history()