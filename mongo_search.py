from pymongo import MongoClient
from utils import generate_embedding
import os

class MongoDBSearch:
    def __init__(self):
        self.hf_token = os.getenv('HUGGINGFACE_TOKEN')
        self.embedding_url = os.getenv('HUGGINGFACE_URL')

    def search_candidates(self, query):
        # Connect to MongoDB
        client = MongoClient(os.getenv('MONGO_URI'))
        db = client.Mercor
        collection = db.MercorDB

        # Use MongoDB to search for candidates
        search_results = collection.aggregate([
            {"$vectorSearch": {
                "queryVector": generate_embedding(query),
                "path": "skillName_embedding",
                "numCandidates": 100,
                "limit": 50,
                "index": "CandidateSemanticSearch",
            }}
        ])

        return list(search_results)