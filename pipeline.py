import sys
from stt import transcribe
from brain import answer
from tts import synthesize


def run(audio_path, out_path="samples/reply.wav"):
    question = transcribe(audio_path)
    if not question:
        print("Could not understand the audio.")
        return None
    print("Question:", question)
    reply = answer(question)
    print("Reply:", reply)
    return synthesize(reply, out_path)


if __name__ == "__main__":
    print(run(sys.argv[1]))