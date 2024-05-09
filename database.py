from pymongo import MongoClient
from utils import generate_embedding
import os
import re
from numpy import dot
from numpy.linalg import norm
from datetime import datetime

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

    if not skill:
        skill = words[-2] if len(words) > 1 else None
        
# If no skill was found in the user's question, return an empty list
    if not skill:
        return []

    # Generate embedding for the user's question
    user_embedding = generate_embedding(skill) if skill else None

    # Connect to MongoDB
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client.Mercor
    collection = db.MercorDB

    # Fetch all candidates from MongoDB
    candidates = list(collection.find({}))

    # Calculate cosine similarity between the user's question and each candidate's skillName
    for candidate in candidates:
        candidate_embedding = candidate['skillName_embedding']
        similarity = dot(user_embedding, candidate_embedding)/(norm(user_embedding)*norm(candidate_embedding)) if user_embedding is not None else 0
        candidate['similarity'] = similarity

# Filter candidates based on skill, budget, and experience
    candidates = [candidate for candidate in candidates if 
              (skill and skill.lower() in candidate['skillName'].lower()) and 
              (not budget or ((candidate.get('fullTimeSalaryCurrency') and candidate.get('fullTimeSalary') and candidate['fullTimeSalary'].strip() and 
               currency and candidate['fullTimeSalaryCurrency'].lower() == currency.lower() and 
               candidate['fullTimeSalary'].isdigit() and int(candidate['fullTimeSalary']) <= int(budget)) or
               (candidate.get('partTimeSalaryCurrency') and candidate.get('partTimeSalary') and candidate['partTimeSalary'].strip() and 
               currency and candidate['partTimeSalaryCurrency'].lower() == currency.lower() and 
               candidate['partTimeSalary'].isdigit() and int(candidate['partTimeSalary']) <= int(budget)))) and 
              (not experience or ('experience' in candidate and candidate['experience'].isdigit() and int(candidate['experience']) >= int(experience)))]

    # Sort candidates by similarity and experience
    candidates.sort(key=lambda x: (-x['similarity'], -x.get('experience', 0)))

    # Return the top 1 most similar candidate
    return candidates[:5]

