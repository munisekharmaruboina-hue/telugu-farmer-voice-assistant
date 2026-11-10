import sys
import requests
from config import GNANI_API_KEY

STT_URL = "https://api.vachana.ai/stt/v3"


def transcribe(audio_path, language_code="te-IN"):
    with open(audio_path, "rb") as f:
        resp = requests.post(
            STT_URL,
            headers={"X-API-Key-ID": GNANI_API_KEY},
            files={"audio_file": f},
            data={"language_code": language_code},
            timeout=60,
        )
    if not resp.ok:
        print("STT error", resp.status_code, resp.text)
        return None
    return resp.json().get("transcript", "")


if __name__ == "__main__":
    print(transcribe(sys.argv[1]))