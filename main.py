# import asyncio

# from sentence_transformers import SentenceTransformer

# from agent import finmemory_agent
# from memory import FinMemory
# from memory_extractor import extract_memory
# from vector_memory import VectorMemory


# # ============================================================
# # MEMORY OBJECTS
# # ============================================================

# memory = FinMemory()

# # all-MiniLM-L6-v2 produces 384-dimensional vectors
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2") #This model converts text into a numerical vector.

# # Persistent FAISS memory
# vector_memory = VectorMemory(dimension=384) #checks whether a FAISS index already exists.If it exists:
# #Loading existing FAISS index..
# #Creating new FAISS index...

# # ============================================================
# # SQLITE / PERSISTENT MEMORY CONTEXT
# # ============================================================

# def build_memory_context():
#     """
#     Build persistent financial profile context.

#     Data comes from SQLite.
#     """

#     profile = memory.get_profile()

#     if not profile:
#         return "No previous financial information available."

#     context = "User Financial Profile:\n"

#     for key, value in profile.items():
#         context += f"- {key}: {value}\n"

#     return context


# # ============================================================
# # SHORT-TERM MEMORY
# # ============================================================

# def build_short_term_context():
#     """
#     Use only the last 4 messages from the current conversation.

#     Each message is limited to 1000 characters to prevent
#     the LLM prompt from becoming too large.
#     """

#     messages = memory.get_short_term_memory(limit=4)

#     if not messages:
#         return "No recent conversation."

#     context = "Recent Conversation:\n"

#     for msg in messages:

#         message = msg["message"][:1000]

#         context += f"{msg['role']}: {message}\n"

#     return context


# # ============================================================
# # CONVERSATION HISTORY
# # ============================================================
# #gets previous conversations from SQLite.
# def build_history_context():
#     """
#     Load previous conversation from SQLite.

#     Only the last 4 messages are used.
#     Each message is limited to 1000 characters.
#     """

#     history = memory.get_history()

#     if not history:
#         return "No previous conversation history."

#     context = "Recent Previous Conversation:\n"

#     for role, message in history[-4:]:

#         # Prevent very long assistant responses from
#         # increasing the LLM prompt size.
#         message = message[:1000]

#         context += f"{role}: {message}\n"

#     return context


# # ============================================================
# # VECTOR / FAISS MEMORY
# # ============================================================

# def build_vector_context(user_input):
#     """
#     Perform semantic search using FAISS.

#     Only 2 results are returned.
#     Each result is limited to 500 characters.
#     """

#     query_vector = embedding_model.encode(user_input) #sentence is converted into a 384-dimensional vector.

#     results = vector_memory.search_memory(#FAISS searches its stored vectors.
#         query_vector,
#         n_results=2
#     )

#     # Debug information
#     print("\n[FAISS SEARCH]")
#     print("Query:", user_input)
#     print("Results:", results)

#     if not results:
#         return "No relevant semantic memories."

#     context = "Relevant Semantic Memories:\n"

#     for result in results:

#         text = result["text"][:500]

#         context += f"- {text}\n"

#     return context


# # ============================================================
# # MAIN APPLICATION
# # ============================================================

# async def main():

#     print("=" * 50)
#     print("       FinMemory - Financial Advisor")
#     print("=" * 50)

#     print("Memory features:")
#     print("✓ Short-term memory")
#     print("✓ Persistent SQLite memory")
#     print("✓ Conversation history")
#     print("✓ Persistent FAISS semantic memory")
#     print("✓ Sentence Transformer embeddings")
#     print("✓ MAF Agent + Groq")
#     print()

#     print("Type 'exit' to stop.")
#     print()

#     while True:

#         # ----------------------------------------------------
#         # USER INPUT
#         # ----------------------------------------------------

#         user_input = input("You: ").strip()

#         if not user_input:
#             continue

#         if user_input.lower() == "exit":

#             print("\nGoodbye!")
#             break


#         # ----------------------------------------------------
#         # ADD USER MESSAGE TO SHORT-TERM MEMORY
#         # ----------------------------------------------------

#         memory.add_to_short_term(
#             "user",
#             user_input
#         )


#         # ----------------------------------------------------
#         # BUILD MEMORY CONTEXT
#         # ----------------------------------------------------

#         memory_context = build_memory_context()

#         short_term_context = build_short_term_context()

#         history_context = build_history_context()

#         vector_context = build_vector_context(
#             user_input
#         )


#         # ----------------------------------------------------
#         # BUILD FINAL PROMPT
#         # ----------------------------------------------------

#         prompt = f"""
# You are FinMemory, a context-aware personal financial advisor.

# Your job is to help the user with:

# - Monthly budgeting
# - Spending tracking
# - Savings goals
# - Investment preferences
# - Financial planning

# Use the available memory to personalize your response.

# ==================================================
# PERSISTENT FINANCIAL MEMORY
# ==================================================

# {memory_context}

# ==================================================
# SHORT-TERM MEMORY
# ==================================================

# {short_term_context}

# ==================================================
# CONVERSATION HISTORY
# ==================================================

# {history_context}

# ==================================================
# SEMANTIC VECTOR MEMORY
# ==================================================

# {vector_context}

# ==================================================
# CURRENT USER MESSAGE
# ==================================================

# {user_input}

# ==================================================
# IMPORTANT RULES
# ==================================================

# 1. Use previous financial information when relevant.

# 2. If the user asks about information they already provided,
#    answer using memory.

# 3. Do not ask the user to repeat information that is already
#    available in memory.

# 4. Do not invent financial information.

# 5. Keep the answer concise and practical.

# 6. Avoid unnecessarily long tables or explanations.

# 7. Do not guarantee investment returns.

# 8. Consider the user's risk appetite when discussing
#    financial options.

# 9. If important information is missing, ask a short
#    follow-up question.

# 10. Prefer a concise answer unless the user asks for
#     detailed financial planning.
# """


#         # ----------------------------------------------------
#         # CALL FINMEMORY AGENT
#         # ----------------------------------------------------

#         try:

#             response = await finmemory_agent.run(prompt) #This is your Microsoft Agent Framework agent.Your agent.py creates

#             response_text = str(response).strip()

#         except Exception as e:

#             print("\n❌ Agent Error:")
#             print(e)
#             print()

#             # Do not continue memory processing if the
#             # main agent failed.
#             continue


#         # ----------------------------------------------------
#         # DISPLAY RESPONSE
#         # ----------------------------------------------------

#         print("\nFinMemory:")
#         print(response_text)
#         print()


#         # ----------------------------------------------------
#         # ADD ASSISTANT RESPONSE TO SHORT-TERM MEMORY
#         # ----------------------------------------------------

#         memory.add_to_short_term(
#             "assistant",
#             response_text
#         )


#         # ----------------------------------------------------
#         # SAVE CONVERSATION TO SQLITE
#         # ----------------------------------------------------

#         memory.save_conversation(
#             "user",
#             user_input
#         )

#         memory.save_conversation(
#             "assistant",
#             response_text
#         )


#         # ----------------------------------------------------
#         # EXTRACT IMPORTANT FINANCIAL MEMORY
#         # ----------------------------------------------------

#         try:

#             extracted_memory = await extract_memory( #Find important financial facts from the user's message.
#                 user_input
#             )

#         except Exception as e:

#             print("⚠ Memory extraction error:")
#             print(e)

#             extracted_memory = {}


#         # ----------------------------------------------------
#         # SAVE EXTRACTED MEMORY TO SQLITE
#         # ----------------------------------------------------

#         if extracted_memory:

#             print("---- Memory Updated ----")

#             for key, value in extracted_memory.items():

#                 memory.remember( #Extracted information is stored in SQLite
#                     key,
#                     value
#                 )

#                 print(
#                     f"{key} = {value}"
#                 )

#             print("------------------------")
#             print()


#         # ----------------------------------------------------
#         # ADD ONLY USEFUL FINANCIAL INFORMATION TO FAISS
#         # ----------------------------------------------------

#         if extracted_memory:

#             current_vector = embedding_model.encode(
#                 user_input
#             )

#             vector_memory.add_memory(#stores the vector in FAISS.
#                 f"memory_{len(vector_memory.memories)}",
#                 current_vector,
#                 user_input
#             )

#             print(
#                 "✓ Financial information added to FAISS"
#             )

#         else:

#             print(
#                 "✓ No useful financial information added to FAISS"
#             )


# # ============================================================
# # PROGRAM ENTRY POINT
# # ============================================================

# if __name__ == "__main__":

#     asyncio.run(main())

import asyncio

from sentence_transformers import SentenceTransformer

from agent import finmemory_agent
from memory import FinMemory
from memory_extractor import extract_memory
from vector_memory import VectorMemory


# ============================================================
# MEMORY OBJECTS
# ============================================================

memory = FinMemory()


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ============================================================
# FAISS MEMORY
# ============================================================

vector_memory = VectorMemory(
    dimension=384
)


# ============================================================
# SQLITE MEMORY CONTEXT
# ============================================================

def build_memory_context():

    profile = memory.get_profile() #gets the current financial profile from SQLite.

    if not profile:

        return "No previous financial information available."

    context = "User Financial Profile:\n"

    for key, value in profile.items():

        context += f"- {key}: {value}\n"

    return context


# ============================================================
# SHORT-TERM MEMORY CONTEXT
# ============================================================

def build_short_term_context():

    messages = memory.get_short_term_memory(
        limit=4
    )

    if not messages:

        return "No recent conversation."

    context = "Recent Conversation:\n"

    for msg in messages:

        message = msg["message"][:1000]

        context += (
            f"{msg['role']}: {message}\n"
        )

    return context


# ============================================================
# CONVERSATION HISTORY
# ============================================================

def build_history_context():

    history = memory.get_history()

    if not history:

        return "No previous conversation history."

    context = "Recent Previous Conversation:\n"

    for role, message in history[-4:]:

        message = message[:1000]

        context += (
            f"{role}: {message}\n"
        )

    return context


# ============================================================
# FAISS VECTOR CONTEXT
# ============================================================

def build_vector_context(user_input):

    query_vector = embedding_model.encode(
        user_input
    )

    results = vector_memory.search_memory(
        query_vector,
        n_results=2
    )

    print("\n[FAISS SEARCH]")
    print("Query:", user_input)
    # print("Results:", results)

    if not results:

        return "No relevant semantic memories."

    context = "Relevant Semantic Memories:\n"

    for result in results:

        text = result["text"][:500]

        context += f"- {text}\n"

    return context


# ============================================================
# MEMORY DEBUG
# ============================================================

# def print_memory_debug(
#     memory_context,
#     short_term_context,
#     history_context,
#     vector_context
# ):

    print("\n")
    print("=" * 70)
    print("                    MEMORY DEBUG")
    print("=" * 70)

    print("\n[1] SQLITE - USER MEMORY")
    print("-" * 70)
    print(memory_context)

    print("\n[2] SHORT-TERM MEMORY")
    print("-" * 70)
    print(short_term_context)

    print("\n[3] SQLITE - CONVERSATION HISTORY")
    print("-" * 70)
    print(history_context)

    print("\n[4] FAISS SEMANTIC MEMORY")
    print("-" * 70)
    print(vector_context)

    print("\n")
    print("=" * 70)
    print("                    END DEBUG")
    print("=" * 70)
    print()


# ============================================================
# MAIN
# ============================================================

async def main():

    print("=" * 50)
    print("       FinMemory - Financial Advisor")
    print("=" * 50)

    print("Memory features:")
    print("✓ Short-term memory")
    print("✓ Persistent SQLite memory")
    print("✓ Conversation history")
    print("✓ Persistent FAISS semantic memory")
    print("✓ Sentence Transformer embeddings")
    print("✓ MAF Agent + Groq")
    print()

    print("Type 'exit' to stop.")
    print()

    # ========================================================
    # MAIN LOOP
    # ========================================================

    while True:

        # ----------------------------------------------------
        # USER INPUT
        # ----------------------------------------------------

        user_input = input("You: ").strip()

        if not user_input:

            continue

        if user_input.lower() == "exit":

            print("\nGoodbye!")

            break

        # ====================================================
        # STEP 1
        # ADD USER MESSAGE TO SHORT-TERM MEMORY
        # ====================================================

        memory.add_to_short_term(
            "user",
            user_input
        )

        # ====================================================
        # STEP 2
        # GET CURRENT SQLITE MEMORY
        # ====================================================

        current_memory = memory.get_profile()

        # ====================================================
        # STEP 3
        # EXTRACT / UPDATE MEMORY
        #
        # IMPORTANT:
        # This happens BEFORE the main agent.
        # ====================================================

        try:

            extracted_memory = await extract_memory(
                user_input,
                current_memory
            )

        except Exception as e:

            print("\n⚠ Memory extraction error:")
            print(e)

            extracted_memory = {}

        # ====================================================
        # STEP 4
        # SAVE UPDATED MEMORY TO SQLITE
        # ====================================================

        if extracted_memory:

            print("\n---- Memory Updated ----")

            for key, value in extracted_memory.items():

                memory.remember(
                    key,
                    value
                )

                print(
                    f"{key} = {value}"
                )

            print("------------------------")
            print()

        # ====================================================
        # STEP 5
        # ADD FINANCIAL MESSAGE TO FAISS
        # ====================================================

        if extracted_memory:

            current_vector = embedding_model.encode(
                user_input
            )

            vector_memory.add_memory(
                f"memory_{len(vector_memory.memories)}",
                current_vector,
                user_input
            )

            print(
                "✓ Financial information added to FAISS"
            )

        else:

            print(
                "✓ No useful financial information "
                "added to FAISS"
            )

        # ====================================================
        # STEP 6
        # BUILD ALL MEMORY CONTEXT
        #
        # Notice:
        # SQLite is now already updated.
        # ====================================================

        memory_context = build_memory_context() #Gets current SQLite data.

        short_term_context = build_short_term_context() #Gets recent conversation.

        history_context = build_history_context() #Gets previous conversation history.

        vector_context = build_vector_context( #Gets relevant FAISS memories.
            user_input
        )

        # ====================================================
        # STEP 7
        # DEBUG MEMORY
        # ====================================================

        # print_memory_debug(
        #     memory_context,
        #     short_term_context,
        #     history_context,
        #     vector_context
        # )

        # ====================================================
        # STEP 8
        # BUILD FINAL AGENT PROMPT
        # ====================================================

        prompt = f"""
You are FinMemory, a context-aware personal financial advisor.

Help the user with:

- Monthly budgeting
- Spending tracking
- Savings goals
- Investment preferences
- Financial planning

Use the available memory to personalize your response.

==================================================
PERSISTENT FINANCIAL MEMORY
==================================================

{memory_context}

==================================================
SHORT-TERM MEMORY
==================================================

{short_term_context}

==================================================
CONVERSATION HISTORY
==================================================

{history_context}

==================================================
SEMANTIC VECTOR MEMORY
==================================================

{vector_context}

==================================================
CURRENT USER MESSAGE
==================================================

{user_input}

==================================================
IMPORTANT RULES
==================================================

1. Use PERSISTENT FINANCIAL MEMORY as the source of truth
   for current financial values.

2. If FAISS contains an older financial value and SQLite
   contains a newer value, use the SQLite value.

3. Use short-term memory for the current conversation.

4. Use conversation history when previous conversations
   are relevant.

5. Use FAISS for semantic/historical context.

6. Do not invent financial information.

7. Do not ask the user to repeat information already
   available in memory.

8. Do not guarantee investment returns.

9. Consider the user's risk appetite.

10. Keep the answer concise and practical.

11. If important information is missing, ask a short
    follow-up question.
"""

        # ====================================================
        # STEP 9
        # CALL FINMEMORY AGENT
        # ====================================================

        print(
            "[AGENT] Sending prompt to FinMemory agent..."
        )

        try:

            response = await finmemory_agent.run(
                prompt
            )

            response_text = str(
                response
            ).strip()

        except Exception as e:

            print("\n❌ Agent Error:")
            print(e)
            print()

            continue

        # ====================================================
        # STEP 10
        # DISPLAY RESPONSE
        # ====================================================

        print("\nFinMemory:")
        print(response_text)
        print()

        # ====================================================
        # STEP 11
        # ADD ASSISTANT RESPONSE TO SHORT-TERM MEMORY
        # ====================================================

        memory.add_to_short_term(
            "assistant",
            response_text
        )

        # ====================================================
        # STEP 12
        # SAVE CONVERSATION HISTORY
        # ====================================================

        memory.save_conversation(
            "user",
            user_input
        )

        memory.save_conversation(
            "assistant",
            response_text
        )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    asyncio.run(main())