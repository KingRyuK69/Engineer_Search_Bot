import os
import requests
import json
import logging
import time

def generate_embedding(text: str) -> list[float]:
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"}
    data = json.dumps({"inputs": text})
    for _ in range(5):  # Retry up to 5 times
        response = requests.post(os.getenv('HUGGINGFACE_URL'), headers=headers, data=data)
        if response.status_code == 200:
            return response.json()  # Return the entire list
        elif response.status_code == 503 and "loading" in response.text:
            time.sleep(20)  # Wait for 20 seconds before retrying
        else:
            logging.error(f"Failed to get embedding for text: {text}")
            logging.error(f"Response status code: {response.status_code}")  # Log the status code
            logging.error(f"Response: {response.text}")  # Log the response
            return None