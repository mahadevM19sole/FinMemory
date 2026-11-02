# import faiss#library that performs vector similarity search.
# import numpy as np
# from pathlib import Path


# class VectorMemory:

#     def __init__(
#         self,
#         dimension=384,
#         index_path="data/faiss.index"
#     ):
#         self.dimension = dimension #How many numbers/elements are present in each embedding vector.
#         self.index_path = Path(index_path)

#         self.index = None
#         self.memories = [] #This stores the metadata associated with your vectors.

#         self.load() #Does an old FAISS index already exist?

#     # ========================================================
#     # CREATE / LOAD INDEX
#     # ========================================================

#     def load(self):
#         """
#         Load an existing FAISS index if it exists.
#         Otherwise create a new empty index.
#         """

#         if self.index_path.exists():

#             print("Loading existing FAISS index...")

#             self.index = faiss.read_index(
#                 str(self.index_path)
#             )

#             # Load metadata
#             metadata_path = self.index_path.with_suffix(".npy") #use this file to store metadata.

#             if metadata_path.exists():

#                 self.memories = np.load( #loads the saved metadata back into Python.
#                     metadata_path,
#                     allow_pickle=True
#                 ).tolist()

#             print(
#                 f"FAISS loaded: {self.index.ntotal} vectors"
#             )

#         else:

#             print("Creating new FAISS index...")

#             self.index = faiss.IndexFlatL2( #means FAISS uses L2/Euclidean distance for similarity comparison.
#                 self.dimension
#             )

#     # ========================================================
#     # SAVE INDEX
#     # ========================================================

#     def save(self):
#         """
#         Save FAISS index and memory metadata to disk.
#         """

#         self.index_path.parent.mkdir(
#             parents=True,
#             exist_ok=True
#         )

#         # Save FAISS index saves the vector index to:
#         faiss.write_index(
#             self.index,
#             str(self.index_path)
#         )

#         # Save metadata
#         metadata_path = self.index_path.with_suffix(".npy")

#         np.save(
#             metadata_path,
#             np.array(
#                 self.memories,
#                 dtype=object
#             )
#         )

#         print(
#             f"FAISS saved: {self.index.ntotal} vectors"
#         )

#     # ========================================================
#     # ADD MEMORY
#     # ========================================================

#     def add_memory(
#         self,
#         memory_id,
#         vector,
#         text
#     ):

#         vector = np.array( #Convert vector to NumPy format,FAISS expects vectors in an appropriate numerical array format.
#             [vector],
#             dtype="float32"
#         )

#         self.index.add(vector) #Add this embedding to my vector index."

#         self.memories.append({
#             "id": memory_id,
#             "text": text
#         })

#         # Save immediately
#         self.save()

#     # ========================================================
#     # SEARCH MEMORY
#     # ========================================================
#     #Given a query embedding, find the most similar stored vectors.
#     def search_memory(
#         self,
#         query_vector,
#         n_results=3 #Return up to 3 relevant memories.
#     ):

#         if self.index.ntotal == 0:
#             return []

#         query_vector = np.array(
#             [query_vector],
#             dtype="float32"
#         )
#         #FAISS performs similarity search
#         distances, indexes = self.index.search(
#             query_vector,
#             min(
#                 n_results,
#                 self.index.ntotal
#             )
#         )

#         results = []

#         for distance, index in zip( #It pairs the distance with its corresponding index:
#             distances[0], #FAISS returns arrays in a 2D structure.
#             indexes[0]
#         ):  

#             if index != -1: #FAISS can return -1 when there isn't a valid result for a requested position.

#                 results.append({#This converts the FAISS result into a useful Python dictionary.
#                     "id": self.memories[index]["id"],#FAISS tells us WHICH memory is similar. self.memories tells us WHAT that memory actually says.
#                     "text": self.memories[index]["text"],
#                     "distance": float(distance)
#                 })

#         return results
import faiss
import numpy as np

from pathlib import Path

#It manages the FAISS index, stores embeddings and metadata, saves/loads the index, and performs semantic searches.”
class VectorMemory:

    def __init__(
        self,
        dimension=384,
        index_path="data/faiss.index"
    ):

        self.dimension = dimension

        self.index_path = Path(index_path)

        self.index = None

        self.memories = []

        self.load()

    # ========================================================
    # LOAD / CREATE INDEX
    # ========================================================

    def load(self):

        if self.index_path.exists():

            print("Loading existing FAISS index...")

            self.index = faiss.read_index(
                str(self.index_path)
            )

            metadata_path = self.index_path.with_suffix(".npy") ##use this file to store metadata.

            if metadata_path.exists():

                self.memories = np.load(
                    metadata_path,
                    allow_pickle=True
                ).tolist()

            print(
                f"FAISS loaded: {self.index.ntotal} vectors"
            )

        else:

            print("Creating new FAISS index...")

            self.index = faiss.IndexFlatL2(
                self.dimension
            )

    # ========================================================
    # SAVE
    # ========================================================

    def save(self):

        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(self.index_path)
        )

        metadata_path = self.index_path.with_suffix(".npy")

        np.save(
            metadata_path,
            np.array(
                self.memories,
                dtype=object
            )
        )

        print(
            f"FAISS saved: {self.index.ntotal} vectors"
        )

    # ========================================================
    # ADD MEMORY
    # ========================================================

    def add_memory(
        self,
        memory_id,
        vector,
        text
    ):

        vector = np.array(
            [vector],
            dtype="float32"
        )

        self.index.add(vector)

        self.memories.append({
            "id": memory_id,
            "text": text
        })

        self.save()

    # ========================================================
    # SEARCH
    # ========================================================

    def search_memory(
        self,
        query_vector,
        n_results=3
    ):

        if self.index.ntotal == 0:

            return []

        query_vector = np.array(
            [query_vector],
            dtype="float32"
        )

        distances, indexes = self.index.search(
            query_vector,
            min(
                n_results,
                self.index.ntotal
            )
        )

        results = []

        for distance, index in zip(
            distances[0],
            indexes[0]
        ):

            if index != -1:

                results.append({
                    "id": self.memories[index]["id"],
                    "text": self.memories[index]["text"],
                    "distance": float(distance)
                })

        return results