import sys
import requests
from config import GNANI_API_KEY

TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"


def synthesize(text, out_path="output.wav", voice="Varuni"):
    resp = requests.post(
        TTS_URL,
        headers={"X-API-Key-ID": GNANI_API_KEY, "Content-Type": "application/json"},
        json={
            "text": text,
            "voice": voice,
            "model": "timbre-v2.5",
            "language": "te-IN",
            "speed": 1.0,
            "audio_config": {
                "sample_rate": 48000,
                "num_channels": 1,
                "sample_width": 2,
                "encoding": "linear_pcm",
                "container": "wav",
            },
        },
        timeout=60,
    )
    if not resp.ok:
        print("TTS error", resp.status_code, resp.text)
        return None
    with open(out_path, "wb") as f:
        f.write(resp.content)
    return out_path


if __name__ == "__main__":
    text = sys.argv[1]
    voice = sys.argv[2] if len(sys.argv) > 2 else "Varuni"
    print(synthesize(text, f"samples/tts_{voice}.wav", voice))