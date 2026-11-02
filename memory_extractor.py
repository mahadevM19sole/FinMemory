# import json
# from agent_framework import Agent
# from agent_framework.openai import OpenAIChatCompletionClient
# import os
# from dotenv import load_dotenv

# load_dotenv()


# chat_client = OpenAIChatCompletionClient(
#     model="openai/gpt-oss-120b",
#     api_key=os.getenv("GROQ_API_KEY"),
#     base_url="https://api.groq.com/openai/v1",
# )


# memory_extractor_agent = Agent(
#     client=chat_client,
#     name="MemoryExtractor",
#     instructions="""
# You extract important financial information from a user's message.

# Return ONLY valid JSON.

# Possible fields:

# {
#     "salary": "...",
#     "monthly_savings_goal": "...",
#     "risk_appetite": "...",
#     "food_spending": "...",
#     "rent": "...",
#     "monthly_expenses": "...",
#     "debt": "...",
#     "investment_preference": "..."
# }

# Rules:
# 1. Only include information explicitly provided by the user.
# 2. Do not guess or invent values.
# 3. If a field is not present, do not include it.
# 4. Return {} if there is no useful financial information.
# 5. Return JSON only. No markdown.
# """
# )


# async def extract_memory(user_message):

#     response = await memory_extractor_agent.run(user_message)#Send message to Memory Extractor

#     text = str(response).strip()

#     try:
#         return json.loads(text)#converts it into a Python dictionary:

#     except json.JSONDecodeError:
#         print("Warning: Could not parse memory:", text)
#         return {}

#         #vector_memory.py is responsible for semantic memory using FAISS

import json

from agent_framework import Agent
from agent_framework.openai import OpenAIChatCompletionClient

import os
from dotenv import load_dotenv


load_dotenv()


# ============================================================
# GROQ CLIENT
# ============================================================

chat_client = OpenAIChatCompletionClient(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


# ============================================================
# MEMORY EXTRACTOR AGENT
# ============================================================

memory_extractor_agent = Agent(

    client=chat_client,

    name="MemoryExtractor",

    instructions="""
You are a financial memory extraction agent.

Your job is to extract important financial information from
the user's latest message.

You will receive:

1. Current financial memory
2. New user message

Return ONLY valid JSON.

Possible fields:

{
    "salary": "...",
    "monthly_savings_goal": "...",
    "risk_appetite": "...",
    "food_spending": "...",
    "rent": "...",
    "monthly_expenses": "...",
    "debt": "...",
    "investment_preference": "..."
}


IMPORTANT RULES:

1. If the user directly provides a financial value,
   extract it.

Example:

User:
"I earn 45000 per month"

Return:

{
    "salary": "45000"
}


2. If the user changes an existing value, calculate the
   new value using the current financial memory.

Example:

Current memory:

{
    "salary": "98000"
}

User:

"my salary is increased by 1000"

Return:

{
    "salary": "99000"
}


3. Salary decrease must also be calculated.

Example:

Current salary = 98000

User:
"my salary decreased by 2000"

Return:

{
    "salary": "96000"
}


4. If the user says "increase by 10%" or "decrease by 10%",
   calculate the new value using the current value.


5. If the user asks a question but does not provide new
   financial information, return {}.

Example:

"What is my salary?"

Return:

{}


6. Do not guess or invent information.


7. Do not modify information unless the user's message
   explicitly changes it.


8. Return {} if there is no useful financial information.


9. Return JSON only.

Do not return markdown.
Do not explain anything.
"""
)


# ============================================================
# EXTRACT MEMORY
# ============================================================

async def extract_memory(user_message, current_memory):

    prompt = f"""
CURRENT FINANCIAL MEMORY:

{json.dumps(current_memory, indent=2)} #convert a Python dictionary/object into nicely formatted JSON text/string.


NEW USER MESSAGE:

{user_message}


Extract only the financial information that should be
stored or updated.

Remember:

- Current financial memory contains the current values.
- If the user says a value increased/decreased, calculate
  the new value.
- If there is no new financial information, return {{}}.
- Return ONLY valid JSON.
"""

    response = await memory_extractor_agent.run(prompt)

    text = str(response).strip()

    # --------------------------------------------------------
    # Remove accidental markdown code fences
    # --------------------------------------------------------
    #Sometimes an LLM doesn't return pure JSON.
    if text.startswith("```json"):
        text = text[7:] #remove those first 7 characters.

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        print("\n⚠ Memory extractor returned invalid JSON:")
        print(text)

        return {}