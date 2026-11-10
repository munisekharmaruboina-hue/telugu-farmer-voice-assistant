
import re
import datetime

from num2words import num2words

from advisor import advise
from tools.districts import crops_answer
from tools.places import find_place
from tools.weather import rain_forecast


NOT_UNDERSTOOD = "క్షమించండి, నాకు అర్థం కాలేదు. దయచేసి మళ్ళీ చెప్పండి."

NO_PRICE_INFO = (
    "క్షమించండి, ప్రస్తుతం ఈ రైతు సహాయక యాప్‌లో "
    "పంటల మార్కెట్ ధరల సమాచారం అందుబాటులో లేదు."
)


DAY_WORDS = {
    "ఒక": 1,
    "రెండు": 2,
    "మూడు": 3,
    "నాలుగు": 4,
    "ఐదు": 5,
    "ఆరు": 6,
    "ఏడు": 7,
}


def telugu_number(n):
    """Convert numbers into Telugu words for better voice pronunciation."""
    words = num2words(int(n), lang="te")

    if n >= 2000:
        words = words.replace("వేయి", "వేల")

    return words



def parse_day(q):
    """
    Returns (day offset, Telugu description).
    Returns None when the requested day is unclear.
    """

    if "వారం" in q:
        return None

    if "ఎల్లుండి" in q:
        return 2, "ఎల్లుండి"

    if "రేపు" in q:
        return 1, "రేపు"

    if any(w in q for w in ["ఈరోజు", "నేడు", "ఇవాళ", "ఇవ్వాళ"]):
        return 0, "ఈరోజు"

    if "రోజుల" in q:
        match = re.search(r"(\d+)\s*రోజుల", q)

        if match:
            n = int(match.group(1))
        else:
            n = None

            for word, value in DAY_WORDS.items():
                if word + "రోజుల" in q:
                    n = value
                    break

        if n is None:
            return None

        return n, f"{telugu_number(n)} రోజుల తర్వాత"

    return None


def weather_answer(question):
    """Answer rainfall questions using Open-Meteo."""

    q = question.replace(" ", "").replace("\u200c", "")

    parsed = parse_day(q)

    if parsed is None:
        return (
            "ఏ రోజు వాతావరణం తెలుసుకోవాలో చెప్పండి. "
            "ఈరోజు, రేపు లేదా ఎల్లుండి అని అడగండి."
        )

    day, when = parsed

    if day < 0 or day > 7:
        return "ఏడు రోజుల వరకు మాత్రమే వాతావరణ అంచనా అందించగలను."

    # Do not silently assume that every farmer is in Nellore.
    place = find_place(q)

    if not place:
        return (
            "మీ ఊరు లేదా పట్టణం పేరు చెప్పండి. "
            "ఉదాహరణకు నెల్లూరు, కావలి, తిరుపతి లేదా గుంటూరు."
        )

    name, lat, lon = place

    try:
        data = rain_forecast(
            lat=lat,
            lon=lon,
            day_offset=day
        )
    except (Exception) as error:
        print("Weather API error:", error)
        return "క్షమించండి, ప్రస్తుతం వాతావరణ సమాచారం పొందలేకపోతున్నాను."

    if not data:
        return "క్షమించండి, ప్రస్తుతం వాతావరణ సమాచారం అందుబాటులో లేదు."

    chance = data.get("rain_chance_pct")
    mm = data.get("rain_mm")

    if chance is None:
        return "క్షమించండి, వర్ష సూచన సమాచారం పూర్తిగా అందుబాటులో లేదు."

    chance = float(chance)
    mm = float(mm or 0)

    where = f"{name}లో"

    note = ""

    if day >= 3:
        note = " ఇది వాతావరణ అంచనా మాత్రమే, మారవచ్చు."

    if chance >= 60:
        text = f"{when} {where} వర్షం పడే అవకాశం ఎక్కువగా ఉంది."
    elif chance >= 30:
        text = f"{when} {where} వర్షం పడే అవకాశం కొంత ఉంది."
    else:
        return (
            f"{when} {where} వర్షం పడే అవకాశం తక్కువగా ఉంది."
            + note
        )

    if mm < 2.5:
        text += " తేలికపాటి జల్లులు పడవచ్చు."
    elif mm < 10:
        text += " మోస్తరు వర్షం పడవచ్చు."
    else:
        text += " భారీ వర్షం పడవచ్చు."

    return text + note




def is_price_question(question):
    """Identify market-price questions without generating prices."""
    words = ["ధర", "రేటు", "రేట్", "మార్కెట్", "price", "rate"]
    q = question.lower()
    return any(word in q for word in words)


def answer(question):
    """Main question router for the farmer assistant."""

    if not question or not isinstance(question, str):
        return NOT_UNDERSTOOD

    question = question.strip()

    if not question:
        return NOT_UNDERSTOOD

    # Weather questions
    if "వర్ష" in question:
        return weather_answer(question)

    # Market prices are currently unsupported.
    if is_price_question(question):
        return NO_PRICE_INFO

    # District crop information
    try:
        crops = crops_answer(question)
    except Exception as error:
        print("District information error:", error)
        crops = None

    if crops:
        return crops

    # General farming and crop-health questions
    try:
        reply = advise(question)
    except Exception as error:
        print("Advisor error:", error)
        return (
            "క్షమించండి, ప్రస్తుతం వ్యవసాయ సలహా పొందలేకపోతున్నాను. "
            "దయచేసి కొద్దిసేపటి తర్వాత మళ్ళీ ప్రయత్నించండి."
        )

    return reply or NOT_UNDERSTOOD


if __name__ == "__main__":
    print("Farmer Assistant Brain Test")
    print("---------------------------")

    test_questions = [
        "వరి ధర ఎంత?",
        "రేపు నెల్లూరులో వర్షం పడుతుందా?",
        "వరి పంటలో ఆకులపై మచ్చలు వస్తున్నాయి ఏమి చేయాలి?",
    ]

    for question in test_questions:
        print("\nQuestion:", question)
        print("Answer:", answer(question))
