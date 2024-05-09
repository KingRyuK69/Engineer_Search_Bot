from pymongo import MongoClient
from utils import generate_embedding
import os
import re

def fetch_and_embed_candidates(user_question):
    # Parse the user's question
    skill = None
    budget = None
    currency = None
    experience = None
    words = user_question.split()
    for i, word in enumerate(words):
        if word == "in" and i < len(words) - 1:
            skill = words[i + 1]
        elif word == "of" and i < len(words) - 1:
            match = re.match(r"(\d+)(\D+)", words[i + 1])
            if match:
                budget, currency = match.groups()
        elif word == "experience":
            try:
                experience = int(words[i - 1])
            except ValueError:
                continue

    # Connect to MongoDB
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client.Mercor
    collection = db.MercorDB

    # Construct the query based on the parsed user question
    query = {}
    if skill:
        query["skillName"] = {"$regex": skill, "$options" :'i'}
    if budget and budget.isdigit():
        budget = int(budget)
        query["$or"] = [
            {"$and": [{"fullTimeSalary": {"$lte": budget}}, {"fullTimeSalaryCurrency": currency}, {"fullTimeSalary": {"$ne": None}}]}, 
            {"$and": [{"partTimeSalary": {"$lte": budget}}, {"partTimeSalaryCurrency": currency}, {"partTimeSalary": {"$ne": None}}]}
        ]
    if experience:
        query["$expr"] = {"$gte": [{"$subtract": [{"$year": "$endDate"}, {"$year": "$startDate"}]}, experience]}

    # Fetch candidates from MongoDB
    candidates = list(collection.find(query))

    # Generate embeddings for each candidate's skillName
    embedding_count = 0  # Initialize counter
    for candidate in candidates:
        embedding = generate_embedding(candidate['skillName'])
        if embedding is not None:
            candidate['skillName_embedding'] = embedding
            collection.replace_one({'_id': candidate['_id']}, candidate)
            embedding_count += 1  # Increment counter

    print(f"Number of embeddings created: {embedding_count}")
    return candidates