class LLMSource:
    AZURE = "azure"
    OPENAI = "openai"
    OLLAMA = "ollama"

class ModelSource:
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"


class LLMModelSource:
    AZURE = ["gpt-4o", "gpt-4-turbo-preview"]
    OPENAI = ["gpt-4o", ""]

def fetch_openai_models():
    url = "https://api.openai.com/v1/models"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        models = response.json()
        return models
    else:
        print(f"Failed to fetch models: {response.status_code}")
        return None
