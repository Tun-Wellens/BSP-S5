import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_reply(prompt: str) -> str:
    # Inject constraints directly into the prompt
    instruct = (
        "Respond in Luxembourgish. Keep replies concise (but in a full sentence) and relevant to the user's query." \
        "Write out numbers with letters"
    )

    full_prompt = f"{instruct}\nUser: {prompt}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    return response.text.strip()
