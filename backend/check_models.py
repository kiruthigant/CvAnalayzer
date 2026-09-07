import os
from dotenv import load_dotenv
import httpx

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

r = httpx.get("https://api.groq.com/openai/v1/models", headers={"Authorization": f"Bearer {api_key}"})
data = r.json()
print([m["id"] for m in data.get("data", [])])
