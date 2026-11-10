
from tools.places import find_place


# ==================================================
# ANDHRA PRADESH DISTRICT CROP INFORMATION
# ==================================================

# Historical reference year for older district records.
SOURCE_YEAR = 2017

# Current official Tirupati district agriculture profile.
TIRUPATI_SOURCE = (
    "Tirupati District Agriculture Department profile"
)


# ==================================================
# 1. DISTRICT DATABASE
# ==================================================

DISTRICTS = {

    # --------------------------------------------------
    # NELLORE
    # Historical reference data
    # --------------------------------------------------

    "nellore": {
        "name": "నెల్లూరు",
        "kvk": "నెల్లూరు కృషి విజ్ఞాన కేంద్రం",

        "crops": [
            "వరి",
            "మినుములు",
            "చెరకు",
            "వేరుశెనగ",
            "శనగలు"
        ],

        "soils": [
            "ఎర్ర నేలలు",
            "తీర ఇసుక నేలలు",
            "నల్లరేగడి నేలలు"
        ],

        "fruits": [
            "నిమ్మ",
            "మామిడి",
            "బత్తాయి"
        ],

        "vegetables": [
            "మిరప",
            "బెండకాయ",
            "వంకాయ"
        ],

        "extra": "",

        "source_note": (
            "2017 నాటి ICAR-CRIDA జిల్లా వ్యవసాయ ప్రణాళిక"
        )
    },


    # --------------------------------------------------
    # KRISHNA
    # Historical reference data
    # --------------------------------------------------

    "krishna": {
        "name": "కృష్ణా",
        "kvk": "గరికపాడు కృషి విజ్ఞాన కేంద్రం",

        "crops": [
            "వరి",
            "మినుములు",
            "పత్తి",
            "మొక్కజొన్న",
            "చెరకు"
        ],

        "soils": [
            "నల్లరేగడి నేలలు",
            "ఎర్ర నేలలు"
        ],

        "fruits": [
            "మామిడి",
            "అరటి",
            "జామ"
        ],

        "vegetables": [
            "మిరప",
            "బెండకాయ",
            "టమాట",
            "దోసకాయ"
        ],

        "extra": "",

        "source_note": (
            "2017 నాటి ICAR-CRIDA జిల్లా వ్యవసాయ ప్రణాళిక; "
            "పాత జిల్లా సరిహద్దుల ఆధారంగా ఉన్న సమాచారం"
        )
    },


    # --------------------------------------------------
    # GUNTUR
    # Historical reference data
    # --------------------------------------------------

    "guntur": {
        "name": "గుంటూరు",
        "kvk": None,

        "crops": [
            "వరి",
            "పత్తి",
            "మినుములు",
            "మొక్కజొన్న",
            "కందులు"
        ],

        "soils": [
            "నల్లరేగడి నేలలు",
            "ఎర్ర నేలలు",
            "తీర ఇసుక నేలలు"
        ],

        "fruits": [],

        "vegetables": [],

        "extra": (
            "మిరప, పసుపు, పొగాకు కూడా ముఖ్యమైన పంటలు."
        ),

        "source_note": (
            "2017 నాటి ICAR-CRIDA జిల్లా వ్యవసాయ ప్రణాళిక; "
            "పాత జిల్లా సరిహద్దుల ఆధారంగా ఉన్న సమాచారం"
        )
    },


    # --------------------------------------------------
    # PRAKASAM
    # Historical reference data
    # --------------------------------------------------

    "prakasam": {
        "name": "ప్రకాశం",
        "kvk": "దర్శి కృషి విజ్ఞాన కేంద్రం",

        "crops": [
            "శనగలు",
            "వరి",
            "పత్తి",
            "కందులు",
            "పొగాకు"
        ],

        "soils": [
            "ఎర్ర నేలలు",
            "నల్లరేగడి నేలలు"
        ],

        "fruits": [
            "బత్తాయి",
            "మామిడి",
            "సపోటా"
        ],

        "vegetables": [
            "మిరప",
            "టమాట"
        ],

        "extra": "",

        "source_note": (
            "2017 నాటి ICAR-CRIDA జిల్లా వ్యవసాయ ప్రణాళిక"
        )
    },


    # --------------------------------------------------
    # TIRUPATI
    # Official district agriculture profile
    # --------------------------------------------------

    "tirupati": {
        "name": "తిరుపతి",
        "kvk": None,

        "crops": [
            "వరి",
            "వేరుశెనగ",
            "చెరకు",
            "మినుములు",
            "సజ్జలు",
            "నువ్వులు",
            "పొద్దుతిరుగుడు"
        ],

        "soils": [
            "ఇసుక కలిసిన బంకమట్టి నేలలు",
            "ఇసుక నేలలు",
            "బంకమట్టి నేలలు"
        ],

        "fruits": [
            "మామిడి",
            "నిమ్మ"
        ],

        "vegetables": [
            "టమాట"
        ],

        "extra": (
            "నీటి పారుదల సౌకర్యం ఉన్న ప్రాంతాల్లో వరి ప్రధాన పంట. "
            "వర్షాధార ప్రాంతాల్లో వేరుశెనగ ముఖ్యమైన పంట. "
            "చెరకు, మినుములు, సజ్జలు, నువ్వులు కూడా సాగు చేస్తారు."
        ),

        "source_note": TIRUPATI_SOURCE
    }
}


# ==================================================
# 2. CURRENT TOWN-TO-DISTRICT MAPPING
# ==================================================

TOWN_DISTRICT = {

    # Nellore
    "నెల్లూరు": "nellore",
    "కావలి": "nellore",

    # Krishna
    "మచిలీపట్నం": "krishna",

    # Guntur
    "గుంటూరు": "guntur",

    # Prakasam
    "ఒంగోలు": "prakasam",

    # Tirupati
    "తిరుపతి": "tirupati",
    "గూడూరు": "tirupati",
}


# ==================================================
# 3. DISTRICT NAME IDENTIFICATION
# ==================================================

DISTRICT_STEMS = [

    ("nellore", [
        "నెల్లూ"
    ]),

    ("krishna", [
        "కృష్ణ"
    ]),

    ("guntur", [
        "గుంటూ"
    ]),

    ("prakasam", [
        "ప్రకాశ",
        "ఒంగోలు"
    ]),

    ("tirupati", [
        "తిరుపతి"
    ]),
]


# ==================================================
# 4. FIND DISTRICT OR TOWN
# ==================================================

def locate(text):

    q = text.replace(" ", "")

    # First check known towns.
    place = find_place(q)

    if place and place[0] in TOWN_DISTRICT:
        return TOWN_DISTRICT[place[0]], place[0]

    # Then check district names.
    for key, stems in DISTRICT_STEMS:

        if any(stem in q for stem in stems):
            return key, None

    return None, None


# ==================================================
# 5. KVK LOOKUP
# ==================================================

def kvk_for(place):

    key = TOWN_DISTRICT.get(place)

    if key:
        return DISTRICTS[key]["kvk"]

    return None


# ==================================================
# 6. STATEWIDE RESPONSE
# ==================================================

def statewide_answer():

    return (
        "ఆంధ్రప్రదేశ్‌లో వివిధ ప్రాంతాల్లో వరి, "
        "వేరుశెనగ, మొక్కజొన్న, పత్తి, మిరప, "
        "చెరకు, పప్పుధాన్యాలు వంటి పంటలను సాగు చేస్తారు. "
        "ప్రతి జిల్లాలో నేల రకం, వర్షపాతం, నీటి వసతి "
        "ఆధారంగా పంటల సాగు మారుతుంది. "
        "నా ప్రస్తుత సమాచారంలో అన్ని జిల్లాల తాజా "
        "పంటల గణాంకాలు లేవు. "
        "మీకు ఏ జిల్లా గురించి తెలుసుకోవాలో చెప్పండి."
    )


# ==================================================
# 7. DISTRICT CROP ANSWER
# ==================================================

def crops_answer(text):

    q = text.replace(" ", "").lower()

    # Do not interfere with weather or market questions.
    if "ధర" in q or "వర్ష" in q:
        return None

    # Identify crop and district question intent.
    crop_question_words = [
        "పంటలు",
        "ఏపంట",
        "ప్రధానపంట",
        "పండిస్తారు",
        "సాగుచేస్తారు",
        "సాగుచేస్తున్నారు"
    ]

    if not any(word in q for word in crop_question_words):
        return None

    # Find district.
    key, place = locate(text)

    # --------------------------------------------------
    # A. STATEWIDE QUESTION
    # --------------------------------------------------

    if key is None:

        statewide_words = [
            "ఆంధ్రప్రదేశ్",
            "రాష్ట్రంలో",
            "రాష్ట్రమంతటా",
            "ఏజిల్లాలో",
            "జిల్లాలవారీగా"
        ]

        if any(word in q for word in statewide_words):
            return statewide_answer()

        return None

    # --------------------------------------------------
    # B. DISTRICT INFORMATION
    # --------------------------------------------------

    d = DISTRICTS[key]

    parts = []

    # Town identification.
    if place and place != d["name"]:
        parts.append(
            f"{place} ప్రస్తుతం {d['name']} జిల్లాలో ఉంది."
        )

    # Main crops.
    parts.append(
        f"{d['name']} జిల్లాలో ప్రధానంగా "
        f"{', '.join(d['crops'])} పంటలు సాగు చేస్తారు."
    )

    # Soil information.
    if d["soils"]:
        parts.append(
            f"ఈ ప్రాంతంలో {', '.join(d['soils'])} కనిపిస్తాయి."
        )

    # Fruits.
    if d["fruits"]:
        parts.append(
            f"ముఖ్యమైన పండ్ల పంటలు "
            f"{', '.join(d['fruits'])}."
        )

    # Vegetables.
    if d["vegetables"]:
        parts.append(
            f"ముఖ్యమైన కూరగాయలు "
            f"{', '.join(d['vegetables'])}."
        )

    # Additional information.
    if d["extra"]:
        parts.append(d["extra"])

    # Local agricultural guidance.
    if d["kvk"]:
        parts.append(
            f"మరిన్ని వివరాల కోసం {d['kvk']}ను "
            "సంప్రదించవచ్చు."
        )
    else:
        parts.append(
            "స్థానిక సాగు సలహాల కోసం మండల వ్యవసాయ "
            "అధికారిని సంప్రదించవచ్చు."
        )

    # Source and data age.
    parts.append(
        f"సమాచార ఆధారం: {d['source_note']}."
    )

    if key != "tirupati":
        parts.append(
            "ఈ సమాచారం పాత జిల్లా రికార్డుల ఆధారంగా ఉంది. "
            "ప్రస్తుత పంటల పరిస్థితులు మారి ఉండవచ్చు."
        )

    return " ".join(parts)
