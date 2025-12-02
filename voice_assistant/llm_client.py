import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_reply(prompt: str, history: list) -> str:
    # Inject constraints directly into the prompt
    instruct = (
        "Respond in Luxembourgish. Keep replies concise (but in a full sentence) and relevant to the user's query." \
        "Write out numbers with letters"
    )

    # Build history context (last 3 exchanges)
    history_text = ""
    for role, msg in history[-6:]:
        if role == "user":
            history_text += f"User: {msg}\n"
        else:
            history_text += f"Assistant: {msg}\n"

    full_prompt = f"{instruct}\n{history_text}User: {prompt}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    return response.text.strip()
