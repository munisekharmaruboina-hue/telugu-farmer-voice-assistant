import hashlib
import os
import tempfile
import time
import streamlit as st
from stt import transcribe
from brain import NOT_UNDERSTOOD
from dialog import respond
from tts import synthesize

st.set_page_config(page_title="Farmer Voice Assistant", page_icon="🌾")
st.title("🌾 Farmer Voice Assistant")
st.caption("Ask in Telugu about weather, crop cultivation, pests, diseases and district farming information.")

with st.sidebar:
    st.header("Try asking")
    st.write("• రేపు మా ఊరిలో వర్షం పడుతుందా?")
    st.write("• వరి పంటకు ఏ ఎరువులు వేయాలి?")
    st.write("• వరి పంటకు ఎరువులు ఎప్పుడు వేయాలి?")
    if st.button("New conversation"):
        st.session_state["dialog_state"] = None
    st.divider()
    st.caption(
        "Built with Gnani Prisma (speech to text) and Timbre (text to speech). "
        "Rain forecast: Open-Meteo."
    )


@st.cache_resource
def get_cache():
    return {}


def cached(key, fn, ttl=None):
    cache = get_cache()
    hit = cache.get(key)
    if hit is not None and (ttl is None or time.time() - hit[1] < ttl):
        return hit[0]
    value = fn()
    if value:
        cache[key] = (value, time.time())
    return value


def run_stt(audio_bytes):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_bytes)
        path = f.name
    try:
        return transcribe(path)
    finally:
        os.remove(path)


def run_turn(question, state):
    reply, new_state = respond(question, state)
    if reply == NOT_UNDERSTOOD:
        return None
    return reply, new_state


def run_tts(text):
    path = synthesize(text, "samples/app_reply.wav")
    if not path:
        return None
    with open(path, "rb") as f:
        return f.read()


audio = st.audio_input("Press the mic, ask in Telugu, then press stop")

if audio is not None:
    audio_bytes = audio.getvalue()
    key = hashlib.md5(audio_bytes).hexdigest()
    if st.session_state.get("last_key") != key:
        start = time.time()
        with st.status("Working on it...", expanded=True) as status:
            st.write("Listening...")
            question = cached(("stt", key), lambda: run_stt(audio_bytes))
            if not question:
                status.update(label="Could not understand the audio", state="error")
                st.session_state["last_key"] = key
                st.session_state["result"] = None
                st.error("Could not understand the audio. Please try again.")
                st.stop()
            st.write("Looking up the answer...")
            state = st.session_state.get("dialog_state")
            turn = cached(("turn", question, repr(state)), lambda: run_turn(question, state), 600)
            reply, new_state = turn if turn else (NOT_UNDERSTOOD, None)
            st.write("Preparing the voice reply...")
            speech = cached(("tts", reply), lambda: run_tts(reply), 3600)
            status.update(
                label=f"Done in {time.time() - start:.0f} seconds",
                state="complete",
                expanded=False,
            )
        st.session_state["dialog_state"] = new_state
        st.session_state["last_key"] = key
        st.session_state["result"] = (question, reply, speech)

    result = st.session_state.get("result")
    if result:
        question, reply, speech = result
        st.subheader("You asked")
        st.write(question)
        st.subheader("Answer")
        st.write(reply)
        if speech:
            st.audio(speech, format="audio/wav", autoplay=True)
        else:
            st.warning("The voice reply is not available right now. The text answer is above.")
