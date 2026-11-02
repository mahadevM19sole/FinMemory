from sentence_transformers import SentenceTransformer

from vector_memory import VectorMemory


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create vector memory
memory = VectorMemory(dimension=384)


# Financial memories
memories = [
    "I earn ₹70,000 per month.",
    "I want to save ₹20,000 every month.",
    "My risk appetite is low.",
    "I spend ₹8,000 on food every month."
]


# Convert memories into vectors and store them
for index, text in enumerate(memories):

    vector = model.encode(text)

    memory.add_memory(
        f"memory_{index}",
        vector,
        text
    )


# Search using a different sentence
query = "How much money do I earn?"

query_vector = model.encode(query)

results = memory.search_memory(
    query_vector,
    n_results=2
)


print("\nSemantic Search Results:")

for result in results:
    print("-", result)