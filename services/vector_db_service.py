# services/vector_db_service.py
# This service manages the vector database (FAISS) for efficient similarity search.

import faiss
import numpy as np
import json
import os
from sklearn.preprocessing import normalize

class VectorDBService:
    """
    A singleton service for managing the FAISS vector index and character metadata.
    It handles loading the data, searching for matches, and includes a fallback
    to create dummy data if the actual index/metadata is not found.
    """
    def __init__(self, index_path="embeddings/marvel_vectors.index", metadata_path="embeddings/metadata.json"):
        """
        Initializes the service by loading the FAISS index and metadata file.
        If these files are not found, it logs a warning and creates dummy data.
        """
        print("Initializing VectorDBService...")
        try:
            # Load the FAISS index from the specified file.
            self.index = faiss.read_index(index_path)
            # Load the corresponding metadata.
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            print("FAISS index and metadata loaded successfully.")
        except (RuntimeError, FileNotFoundError):
            # This is a fallback for development. In a production scenario,
            # the absence of these files should be a critical error.
            print("WARN: Could not find FAISS index or metadata. Creating dummy data for development.")
            self.create_dummy_data()

    def create_dummy_data(self):
        """
        Generates a dummy FAISS index and metadata list for development and testing.
        This allows the API to run without requiring the real data from Prompt #2.
        """
        # 1. Define the dimension of the vectors (must match the face recognition model).
        embedding_dim = 512
        num_dummies = 5

        # 2. Create a flat L2 (Euclidean distance) index.
        self.index = faiss.IndexFlatL2(embedding_dim)

        # 3. Generate random 512-dimensional vectors.
        dummy_embeddings = np.random.rand(num_dummies, embedding_dim).astype('float32')

        # 4. Normalize the vectors to unit length (L2 norm). This is crucial for
        #    converting L2 distance to cosine similarity later.
        normalize(dummy_embeddings, axis=1, norm='l2', copy=False)

        # 5. Add the normalized vectors to the FAISS index.
        self.index.add(dummy_embeddings)

        # 6. Create corresponding dummy metadata. The order must match the embeddings.
        self.metadata = [
            {"character_name": "Dummy Iron Man", "image_url": "https://path/to/dummy/iron_man.jpg"},
            {"character_name": "Dummy Thor", "image_url": "https://path/to/dummy/thor.jpg"},
            {"character_name": "Dummy Captain America", "image_url": "https://path/to/dummy/cap.jpg"},
            {"character_name": "Dummy Hulk", "image_url": "https://path/to/dummy/hulk.jpg"},
            {"character_name": "Dummy Black Widow", "image_url": "https://path/to/dummy/widow.jpg"},
        ]
        print(f"Created a dummy FAISS index with {num_dummies} entries.")

    def find_closest_match(self, user_embedding: np.ndarray, top_k: int = 1) -> tuple:
        """
        Performs a similarity search in the FAISS index to find the closest character match.

        Args:
            user_embedding (np.ndarray): The 512-dim embedding of the user's face.
            top_k (int): The number of closest matches to retrieve (default is 1).

        Returns:
            tuple: A tuple containing the matched character's metadata (dict) and the similarity score (float).
        """
        # 1. FAISS search method requires a 2D array, so we reshape the 1D user embedding.
        user_embedding_2d = np.expand_dims(user_embedding, axis=0)

        # 2. Perform the search.
        # `search` returns two arrays:
        # - D: Distances to the k nearest neighbors.
        # - I: Indices of the k nearest neighbors.
        distances, indices = self.index.search(user_embedding_2d, top_k)

        # 3. Extract the index and distance of the top match (k=0).
        best_match_index = indices[0][0]
        distance = distances[0][0]

        # 4. Convert L2 distance to a cosine similarity score.
        # This formula is valid because the vectors in the index are normalized.
        # A smaller distance means a higher similarity.
        # Similarity = 1 indicates a perfect match.
        similarity = 1 - (distance**2 / 2)

        # 5. Retrieve the metadata of the matched character using the index.
        matched_character_meta = self.metadata[best_match_index]

        return matched_character_meta, float(similarity)

# --------------------------------------------------------------------------
# Singleton Instance
# --------------------------------------------------------------------------
# Create a single, globally accessible instance of the VectorDBService.
# This prevents reloading the index and metadata on every API call.
vector_db_service = VectorDBService()
