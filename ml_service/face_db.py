import os
import numpy as np
import faiss
from deepface import DeepFace

class FaceDatabase:
    def __init__(self, index_path='faiss_index.bin'):
        self.index_path = index_path
        self.dimension = 128 # Facenet dimension
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)

    def extract_embedding(self, image_path):
        try:
            result = DeepFace.represent(img_path=image_path, model_name='Facenet', enforce_detection=False)
            if isinstance(result, list) and len(result) > 0:
                embedding = result[0]['embedding']
                return np.array(embedding, dtype='float32')
            return None
        except Exception as e:
            print(f"Error extracting embedding: {e}")
            return None

    def add_face(self, image_path):
        embedding = self.extract_embedding(image_path)
        if embedding is not None:
            embedding = np.expand_dims(embedding, axis=0)
            self.index.add(embedding)
            faiss.write_index(self.index, self.index_path)
            return self.index.ntotal - 1 # return the ID (0-indexed)
        return -1

    def search_face(self, image_path, threshold=10.0): # Facenet L2 distance threshold is roughly 10
        if self.index.ntotal == 0:
            return -1, float('inf')
        
        embedding = self.extract_embedding(image_path)
        if embedding is not None:
            embedding = np.expand_dims(embedding, axis=0)
            distances, indices = self.index.search(embedding, 1)
            
            if len(distances) > 0 and distances[0][0] < threshold:
                return int(indices[0][0]), float(distances[0][0])
        return -1, float('inf')

# Singleton instance
face_db = FaceDatabase()
