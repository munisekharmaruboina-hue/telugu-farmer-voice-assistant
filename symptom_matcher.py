
import re
import unicodedata


# Possible symptom-to-pest/disease matches.
# These are screening clues, NOT confirmed diagnoses.

SYMPTOM_RULES = {
    "tomato": [
        {
            "name": "Whitefly (తెల్లదోమ)",
            "keywords": [
                "తెల్ల పురుగులు", "తెల్లదోమ",
                "whitefly", "white flies",
                "ఆకుల కింద తెల్ల"
            ],
        },
        {
            "name": "Thrips (తామర పురుగులు)",
            "keywords": [
                "వెండి రంగు", "వెండి రంగులో",
                "వెండి మచ్చలు", "తామర పురుగులు",
                "thrips", "silvery leaves", "silver patches"
            ],
        },
        {
            "name": "Early blight (ఆకు మచ్చ తెగులు)",
            "keywords": [
                "వలయాల మచ్చలు", "గుండ్రంగా గోధుమ",
                "గోధుమ రంగు మచ్చలు", "circular rings",
                "early blight"
            ],
        },
        {
            "name": "Possible leaf curl problem (ఆకు ముడుత)",
            "keywords": [
                "ఆకులు ముడుచు", "ఆకులు వంకర",
                "ఆకులు ముడత", "leaf curl", "curling leaves"
            ],
        },
        {
            "name": "Possible Fusarium wilt (ఫ్యుసేరియం విల్ట్)",
            "keywords": [
                "తేమ ఉన్నప్పటికీ వాడి",
                "నేలలో తేమ ఉన్నప్పటికీ",
                "పసుపు రంగులోకి మారి వాడి",
                "fusarium wilt", "wilt despite moist soil"
            ],
        },
    ],

    "paddy": [
        {
    "name": "Possible leaf spot symptoms (ఆకు మచ్చల సూచనలు)",
    "keywords": [
        "ఆకులపై గోధుమ రంగు మచ్చలు",
        "గోధుమ రంగు మచ్చలు",
    ],
},
    ],

    "groundnut": [
        {
            "name": "Possible groundnut leaf spot",
            "keywords": [
                "వేరుశెనగ ఆకులపై గోధుమ",
                "గోధుమ రంగు మచ్చలు",
                "early leaf spot", "late leaf spot",
                "ఆకు మచ్చ"
            ],
        },
    ],

    "maize": [
        {
            "name": "Possible fall armyworm (కత్తెర పురుగు)",
            "keywords": [
                "ఆకులపై రంధ్రాలు", "ఆకుల్లో రంధ్రాలు",
                "సుడిలో పురుగులు", "సుడులలో పురుగులు",
                "విసర్జన పదార్థాలు", "fall armyworm",
                "whorl damage"
            ],
        },
    ],

    "cotton": [
        {
            "name": "Whitefly (తెల్లదోమ)",
            "keywords": [
                "తెల్ల పురుగులు", "తెల్లదోమ",
                "ఆకుల అడుగు భాగంలో", "whitefly"
            ],
        },
    ],

    "chilli": [
        {
            "name": "Possible thrips (తామర పురుగులు)",
            "keywords": [
                "వెండి రంగు", "వెండి మచ్చలు",
                "తామర పురుగులు", "thrips"
            ],
        },
        {
            "name": "Possible mite damage (నల్లి)",
            "keywords": [
                "ఆకులు పైకి ముడుచు",
                "ఆకులు చిన్నవిగా",
                "నల్లి", "mites"
            ],
        },
        {
            "name": "Possible leaf curl problem",
            "keywords": [
                "ఆకులు ముడుచు", "ఆకులు వంకర",
                "leaf curl"
            ],
        },
    ],

    "banana": [
        {
            "name": "Possible Sigatoka leaf spot",
            "keywords": [
                "అరటి ఆకులపై మచ్చ",
                "సిగాటోకా", "sigatoka",
                "ఆకులపై గోధుమ మచ్చలు"
            ],
        },
    ],

    "mango": [
        {
            "name": "Possible mango hopper",
            "keywords": [
                "మామిడి పూతపై పురుగులు",
                "పూతపై చిన్న పురుగులు",
                "మామిడి హాపర్", "mango hopper"
            ],
        },
        {
    "name": "Possible flower drop causes (పూత రాలడానికి వివిధ కారణాలు)",
    "keywords": [
        "పూత రాలిపోతోంది",
        "పూలు రాలిపోతున్నాయి",
        "పూత రాలిపోవడం",
    ],
},
    ],

    "sugarcane": [
        {
            "name": "Possible red rot (ఎర్ర కుళ్ళు తెగులు)",
            "keywords": [
                "కాండం లోపల ఎరుపు",
                "చెరకు లోపల ఎరుపు",
                "ఎర్ర కుళ్ళు", "red rot",
                "కాండం ఎరుపు రంగులోకి మారుతోంది",
            ],
        },
    ],

    "redgram": [
        {
            "name": "Possible wilt or root problem",
            "keywords": [
                "కందుల మొక్కలు వాడి",
                "వేర్లు కుళ్ళు", "మొక్కలు వాడిపోతున్నాయి",
                "wilt", "root rot"
            ],
        },
    ],
}


def normalize(text):
    """Normalize Telugu and English text."""
    return unicodedata.normalize(
        "NFC", str(text)
    ).strip().lower()


def match_symptoms(crop, question):
    """
    Return possible symptom matches for a supported crop.

    A match is only a clue for further questioning.
    It is not a confirmed diagnosis.
    """

    crop = normalize(crop)
    question = normalize(question)

    rules = SYMPTOM_RULES.get(crop, [])

    matches = []

    for rule in rules:
        matched_keywords = []

        for keyword in rule["keywords"]:
            keyword = normalize(keyword)

            if keyword in question:
                matched_keywords.append(keyword)

        if matched_keywords:
            matches.append({
                "possible_cause": rule["name"],
                "matched_keywords": matched_keywords,
                "status": "possible_only",
            })

    return matches


if __name__ == "__main__":
    test_questions = [
        (
            "tomato",
            "టమాట మొక్కల ఆకుల కింద తెల్ల పురుగులు కనిపిస్తున్నాయి"
        ),
        (
            "tomato",
            "టమాట ఆకులపై చిన్న పురుగులు ఉన్నాయి, ఆకులు వెండి రంగులో మారుతున్నాయి"
        ),
        (
            "tomato",
            "టమాట ఆకులపై గుండ్రంగా గోధుమ రంగు మచ్చలు, వాటి చుట్టూ వలయాలు ఉన్నాయి"
        ),
        (
            "maize",
            "మొక్కజొన్న ఆకులపై రంధ్రాలు కనిపిస్తున్నాయి"
        ),
    ]

    for crop, question in test_questions:
        print("\nCrop:", crop)
        print("Question:", question)
        print("Matches:", match_symptoms(crop, question))
