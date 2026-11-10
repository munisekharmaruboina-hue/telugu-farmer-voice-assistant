
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")

URL = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"models/{MODEL}:generateContent"
)

SYSTEM = (
    "You are a friendly farming advisor for Telugu-speaking farmers "
    "in Andhra Pradesh. Reply in natural Telugu script using short, "
    "clear sentences. Give safe, evidence-based general guidance. "
    "Never invent fertilizer doses, pesticide names, chemical quantities, "
    "or confirmed disease diagnoses. If information is missing, say so."
)


def ask_llm(question, system=None):
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY is missing in .env")
        return None

    gen = {
        "temperature": 0.3,
        "maxOutputTokens": 1024
    }

    if os.getenv("GEMINI_THINKING_OFF"):
        gen["thinkingConfig"] = {"thinkingBudget": 0}

    body = {
        "system_instruction": {
            "parts": [{"text": system or SYSTEM}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": question}]
            }
        ],
        "generationConfig": gen
    }

    try:
        resp = requests.post(
            URL,
            headers={
                "x-goog-api-key": GEMINI_API_KEY,
                "Content-Type": "application/json"
            },
            json=body,
            timeout=60
        )

        if not resp.ok:
            print("LLM error:", resp.status_code, resp.text[:300])
            return None

        data = resp.json()

        if os.getenv("DEBUG_LLM"):
            print("Usage:", data.get("usageMetadata"))

        return (
            data["candidates"][0]["content"]["parts"][0]["text"].strip()
        )

    except requests.exceptions.RequestException as e:
        print("LLM request failed:", type(e).__name__)
        return None

    except (KeyError, IndexError, TypeError):
        print("LLM returned no usable text.")
        return None


if __name__ == "__main__":
    question = "వరి పంటలో సాధారణంగా కనిపించే సమస్యలు ఏమిటి?"
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])

    print(ask_llm(question))
