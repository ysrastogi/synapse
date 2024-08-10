import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_openai_models():
    url = "https://api.openai.com/v1/models"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_KEY')}"
    }
    print(os.getenv('OPENAI_API_KEY'))
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data= response.get('data', [])
        model_ids = [item['id'] for item in data]
        return model_ids
    
    else:
        print(f"Failed to fetch models: {response.status_code}")
        return None