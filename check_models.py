import requests
import json
import os
from dotenv import load_dotenv

# Load from the langgraph folder where the .env is located
load_dotenv("/Users/charanb/Desktop/TGL_Customised/final_ui/langgraph/.env")
api_key = os.getenv("OPENROUTER_API_KEY")

print(f"Checking models for API Key: {api_key[:10]}...")

response = requests.get(
    url="https://openrouter.ai/api/v1/models",
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

if response.status_code == 200:
    models = response.json().get("data", [])
    # Print the first 10 models found
    print(f"Successfully found {len(models)} models.")
    print("Top available models:")
    for m in models[:20]:
        print(f"- {m['id']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
