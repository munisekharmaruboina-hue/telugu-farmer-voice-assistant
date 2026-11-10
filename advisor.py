
import os
import re
import unicodedata

from llm import ask_llm
from symptom_matcher import match_symptoms


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.join(BASE_DIR, "knowledge")


# --------------------------------------------------
# 2. SUPPORTED CROPS
# --------------------------------------------------

CROPS = {
    "paddy": {
        "name": "వరి",
        "aliases": ["వరి", "వడ్లు", "బియ్యం పంట", "paddy", "rice"],
    },
    "groundnut": {
        "name": "వేరుశెనగ",
        "aliases": ["వేరుశెనగ", "వేరుశనగ", "పల్లీలు", "groundnut", "peanut"],
    },
    "maize": {
        "name": "మొక్కజొన్న",
        "aliases": ["మొక్కజొన్న", "మొక్కజొన్న పంట", "maize", "corn"],
    },
    "cotton": {
        "name": "పత్తి",
        "aliases": ["పత్తి", "కాటన్", "cotton"],
    },
    "chilli": {
        "name": "మిరప",
        "aliases": ["మిరప", "మిర్చి", "మిరపకాయ", "chilli", "chili"],
    },
    "tomato": {
        "name": "టమాట",
        "aliases": [
            "టమాట", "టమాటా", "టమటా",
            "టమోటా", "టొమాటో", "tomato",
        ],
    },
    "banana": {
        "name": "అరటి",
        "aliases": ["అరటి", "అరటిపండు", "banana"],
    },
    "mango": {
        "name": "మామిడి",
        "aliases": ["మామిడి", "మామిడి పంట", "mango"],
    },
    "sugarcane": {
        "name": "చెరకు",
        "aliases": ["చెరకు", "కర్రచెరకు", "sugarcane"],
    },
    "redgram": {
        "name": "కందులు",
        "aliases": [
            "కందులు",
            "కందుల",
            "కంది",
            "కంది పంట",
            "కందుల పంట",
            "కందుల మొక్కలు",
            "తూర్",
            "redgram",
            "red gram",
            "pigeonpea",
            "pigeon pea",
            "arhar",
            "toor dal",
        ],
    },
}


# --------------------------------------------------
# 3. QUESTION KEYWORDS
# --------------------------------------------------

CROP_HEALTH_WORDS = [
    "వ్యాధి", "తెగులు", "పురుగు", "పురుగులు",
    "ఆకులు పసుపు", "ఆకులు వాడి", "మొక్క వాడి",
    "మచ్చలు", "కుళ్ళు", "ఎండిపోతుంది",
    "వాడిపోతున్నాయి", "రంధ్రాలు", "తెల్ల పురుగులు",
    "ఆకులు ముడుచు", "పూత రాలిపోవడం",
    "కాయలు రాలిపోవడం", "పంట సమస్య",
    "నల్లి", "దోమ", "పేనుబంక",
    "వాడిపోతుంది", "పసుపు రంగు",
    "spots", "disease", "pest", "insects",
    "yellow leaves", "wilting", "holes",
    "leaf curl", "damage", "rot",
    "పూత రాలిపోతోంది",
    "పూలు రాలిపోతున్నాయి",
    "కాండం ఎరుపు రంగులోకి మారుతోంది",
    "కాండం లోపల ఎరుపు",
    "చెరకు లోపల ఎరుపు",
]

PEST_WORDS = [
    "పురుగు మందు", "మందు", "స్ప్రే",
    "పిచికారీ", "పురుగుల నివారణ",
    "pesticide", "insecticide", "spray",
    "chemical treatment",
]

FERTILIZER_WORDS = [
    "ఎరువు", "ఎరువులు", "యూరియా",
    "డిఏపీ", "పొటాష్", "ఎరువు మోతాదు",
    "ఎప్పుడు వేయాలి", "ఎంత వేయాలి",
    "fertilizer", "urea", "dap", "potash",
    "nutrients",
]


# --------------------------------------------------
# 4. SYSTEM PROMPT
# --------------------------------------------------

BASE = """
మీరు ఆంధ్రప్రదేశ్ రైతులకు సహాయం చేసే తెలుగు వ్యవసాయ సహాయకులు.

సమాధానాలు సులభమైన, సహజమైన తెలుగులో ఇవ్వాలి.

ముఖ్యమైన నియమాలు:

1. రైతు అడిగిన ప్రశ్నకు నేరుగా సమాధానం ఇవ్వండి.
2. అవసరమైనప్పుడు మాత్రమే అదనపు ప్రశ్నలు అడగండి.
3. ఒక లక్షణం ఆధారంగా వ్యాధిని ఖచ్చితంగా నిర్ధారించవద్దు.
4. సాధ్యమైన కారణాలను మాత్రమే వివరించండి.
5. రైతుకు సురక్షితమైన ప్రాథమిక జాగ్రత్తలు చెప్పండి.
6. నిర్ధారణ లేకుండా పురుగుమందు పేర్లు చెప్పవద్దు.
7. ఎరువుల మోతాదులు, రసాయన మోతాదులు కల్పించవద్దు.
8. సమాచారం సరిపోకపోతే స్పష్టంగా తెలియజేయండి.
9. స్థానిక వ్యవసాయ అధికారి లేదా రైతు భరోసా కేంద్రం
   సలహా అవసరమైతే సూచించండి.
10. సమాధానం సాధారణంగా 4 నుంచి 6 చిన్న వాక్యాల్లో ఉండాలి.
11. అవసరం లేని ఇంగ్లీష్ పదాలను ఉపయోగించవద్దు.
12. జ్ఞాన ఫైళ్లలోని సమాచారాన్ని అధికారికంగా
    ధృవీకరించిన సిఫార్సులుగా చూపించవద్దు.
13. రైతుకు అర్థమయ్యే విధంగా మాట్లాడండి.
14. ఊహించి మందులు, ఎరువులు లేదా దిగుబడి వివరాలు చెప్పవద్దు.
15. సమస్యను అర్థం చేసుకోవడానికి అవసరమైన అదనపు
    వివరాలు మాత్రమే అడగండి.
16. Do not advise removing, burning or destroying plants
    based only on a suspected disease.
17. Recommend plant removal only when supported by
    verified crop-specific guidance and appropriate confirmation.
18. Do not give generic precautions that are unrelated
    to the suspected problem.
19. Distinguish normal crop development, environmental
    stress, pest damage and possible disease where relevant.
20. Do not recommend changing irrigation, cutting leaves, pruning,
    removing plants or selecting planting material unless the advice
    is supported by verified crop-specific information and the
    situation justifies it.
21. Avoid generic advice such as keeping water levels correct or
    maintaining cleanliness unless it is relevant to the reported symptoms.
22. Ask no more than two useful follow-up questions at a time.
    Use natural, respectful Telugu that farmers can easily understand.
23. For mango flower drop, distinguish normal flower drop from
    possible weather stress, insect damage or disease.
    Do not assume that flower drop alone indicates disease.
24. For sugarcane internal red discoloration, ask about white patches,
    unusual smell, drying leaves and affected plants.
    Do not confirm red rot from colour alone.
25. Use grammatically correct, natural Telugu in every response.
26. Never invent Telugu agricultural words or use meaningless phrases.
27. Use common terms such as:
    - పురుగుల దాడి
    - ఆకులపై మచ్చలు
    - పూత రాలడం
    - కాండం లోపల రంగు మారడం
    - మొక్కలు వాడిపోవడం
28. Avoid unnatural expressions such as:
    - పురుగుల ఆశ్రయం
    - పురుగుల ఆశశించటం
    - మొక్కల భాకాలు
29. Before responding, check Telugu spelling, grammar and sentence clarity.
30. Do not give the same generic precautions for every crop.
31. Give crop-specific follow-up questions based on reported symptoms.
32. Do not recommend planting material or seed selection without
    verified crop-specific guidance.
33. Do not ask farmers to upload, send, or show photos.
    The current application does not support image analysis.
34. Use relevant follow-up questions to collect missing
    information instead of requesting photos.
    35. Always begin farmer-facing answers with:
    "నమస్కారం రైతు సోదరా."

36. Do not use unusual greetings such as:
    "రైతు అన్నదూత", "రైతు అన్న" or "అండి".

37. Ask a maximum of two follow-up questions in each response.

38. Do not add irrigation, cleanliness or other precautions
    unless they are relevant to the reported problem.

39. Use familiar Telugu agricultural terminology.
    Prefer commonly understood words over invented terms.

40. Check Telugu spelling and grammar before responding.

41. Do not repeat the same advice in multiple sentences.
42. Never invent disease names, pest names or agricultural terms.

43. Avoid unnatural Telugu expressions such as:
    - తెగుళ్ల ఆశ్రయం
    - నల్లని నోళ్లు
    - పురుగుల ఆశ్రయం

44. If the exact agricultural term is uncertain,
    describe the symptom in simple Telugu instead.

45. Do not introduce possible causes unless they are
    supported by the crop knowledge or relevant symptom clues.

46. Ask a maximum of TWO question sentences in the entire answer.
    Combine related details into one clear question when necessary.

47. Do not repeat the same follow-up question in different words.

48. For sugarcane internal red discoloration, distinguish
    internal red patches, white areas, unusual smell and leaf drying.
    Do not diagnose red rot from one symptom.

49. For yellow leaves, distinguish older and younger leaves,
    leaf patterns and possible pest symptoms.
    Do not automatically attribute yellowing to nutrient deficiency.

50. Keep every answer concise, natural and easy for
    an Andhra Pradesh farmer to understand.

51. Use correct, commonly understood Telugu agricultural terminology.

52. For cotton whitefly, use "తెల్లదోమ ఉండే అవకాశం ఉంది" instead of "తెల్లదోమ ఆశించే అవకాశం".

53. For chilli mite damage, use "నల్లి పురుగులు" or simply "చిన్న రసం పీల్చే పురుగులు" when uncertain. Never use "నారాయణ పురుగులు".

54. For paddy brown leaf spots, use the natural expression "ఆకులపై మచ్చల తెగులు ఉండే అవకాశం ఉంది" only when supported by the symptoms. Do not use "ఆకు మచ్చల సూచనలు".

55. Do not mention water stress, nutrient deficiency, viruses or pests as possible causes unless the reported symptoms or knowledge file support them.

56. Check every Telugu sentence for spelling, grammar and natural farmer-friendly wording before responding. Avoid malformed or incomplete words.
"""


# --------------------------------------------------
# 5. SAFE FALLBACK
# --------------------------------------------------

SAFE_FALLBACK = (
    "క్షమించండి రైతు సోదరా. "
    "ప్రస్తుతం మీ ప్రశ్నకు సరైన సమాధానం ఇవ్వలేకపోతున్నాను. "
    "పంట పేరు, పంట వయస్సు మరియు సమస్య వివరాలు చెప్పండి. "
    "అవసరమైతే మీ స్థానిక వ్యవసాయ అధికారి "
    "లేదా రైతు భరోసా కేంద్రాన్ని సంప్రదించండి."
)


# --------------------------------------------------
# 6. TEXT NORMALIZATION
# --------------------------------------------------

def normalize_text(text):
    return unicodedata.normalize(
        "NFC",
        str(text)
    ).strip().lower()


# --------------------------------------------------
# 7. CROP IDENTIFICATION
# --------------------------------------------------

def find_crop(question):

    question = normalize_text(question)

    for crop, details in CROPS.items():

        for alias in details["aliases"]:

            alias = normalize_text(alias)

            if not alias:
                continue

            # Telugu substring matching.
            if any("\u0c00" <= char <= "\u0c7f" for char in alias):

                if alias in question:
                    return crop

            # English whole-word matching.
            else:

                pattern = (
                    r"(?<![a-z])"
                    + re.escape(alias)
                    + r"(?![a-z])"
                )

                if re.search(pattern, question):
                    return crop

    return None


# --------------------------------------------------
# 8. QUESTION CLASSIFICATION
# --------------------------------------------------

def is_pesticide_question(question):

    question = normalize_text(question)

    return any(word in question for word in PEST_WORDS)


def is_fertilizer_question(question):

    question = normalize_text(question)

    return any(word in question for word in FERTILIZER_WORDS)


def is_crop_health_question(question):

    question = normalize_text(question)

    return any(word in question for word in CROP_HEALTH_WORDS)


# --------------------------------------------------
# 9. LOAD CROP KNOWLEDGE
# --------------------------------------------------

def load_facts(crop):

    path = os.path.join(
        KB_DIR,
        f"{crop}.txt"
    )

    try:

        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()

    except (OSError, UnicodeError):

        return None

    blocked_patterns = [
        r"\d+\s*:\s*\d+\s*:\s*\d+",
        r"\d+(?:\.\d+)?\s*(?:kg|g|ml|litre|liter)",
        r"\d+(?:\.\d+)?\s*(?:per acre|per hectare)",
    ]

    safe_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        blocked = any(
            re.search(pattern, line, re.IGNORECASE)
            for pattern in blocked_patterns
        )

        if not blocked:
            safe_lines.append(line)

    if not safe_lines:
        return None

    return "\n".join(safe_lines)


# --------------------------------------------------
# 10. SUPPORTED CROP LIST
# --------------------------------------------------

def covered_names():

    return [
        details["name"]
        for crop, details in CROPS.items()
        if load_facts(crop)
    ]


# --------------------------------------------------
# 11. TELUGU RESPONSE CHECK
# --------------------------------------------------

def is_clean_telugu(text):

    if not isinstance(text, str):
        return False

    return any(
        "\u0c00" <= char <= "\u0c7f"
        for char in text
    )


# --------------------------------------------------
# 12. SAFE FOLLOW-UP QUESTIONS
# --------------------------------------------------

def crop_health_question(question):

    crop = find_crop(question)

    if crop:

        crop_name = CROPS[crop]["name"]

        return (
            f"మీరు {crop_name} పంటలో సమస్య ఉందని చెప్పారు. "
            "పంట వయస్సు ఎంత? ఆకులపైనా, కాండంపైనా, "
            "వేర్లపైనా లేదా పండ్లపైనా లక్షణాలు కనిపిస్తున్నాయి? "
            "ఈ సమస్య ఎన్ని మొక్కలకు వచ్చింది?"
        )

    return (
        "దయచేసి ఏ పంటలో సమస్య ఉందో చెప్పండి. "
        "పంట వయస్సు, కనిపిస్తున్న లక్షణాలు మరియు "
        "సమస్య ఉన్న మొక్కల సంఖ్య వివరించండి."
    )


def ask_crop_for_fertilizer():

    return (
        "దయచేసి మీ పంట పేరు, పంట వయస్సు, "
        "మీ జిల్లా మరియు నేల పరీక్ష వివరాలు చెప్పండి. "
        "ఈ వివరాలు లేకుండా ఎరువు మోతాదు చెప్పడం సురక్షితం కాదు."
    )


def ask_crop_for_pesticide():

    return (
        "దయచేసి ఏ పంటలో సమస్య ఉందో, "
        "ఏ పురుగు లేదా లక్షణం కనిపిస్తోందో చెప్పండి. "
        "సమస్యను గుర్తించకుండా మందు పేరు లేదా మోతాదు "
        "చెప్పడం సురక్షితం కాదు."
    )


# --------------------------------------------------
# 13. SAFE LLM CALL
# --------------------------------------------------

def get_llm_reply(question, system):

    try:

        reply = ask_llm(
            question,
            system=system
        )

        if reply and is_clean_telugu(reply):
            return reply.strip()

    except Exception as error:

        print(
            "Advisor LLM error:",
            type(error).__name__
        )

    return None


# --------------------------------------------------
# 14. MAIN FARMING ADVISOR
# --------------------------------------------------

def advise(question):

    question = normalize_text(question)

    if not question:
        return "దయచేసి మీ వ్యవసాయ ప్రశ్నను అడగండి."

    crop = find_crop(question)

    health_question = is_crop_health_question(question)
    pesticide_question = is_pesticide_question(question)
    fertilizer_question = is_fertilizer_question(question)

    # ----------------------------------------------
    # A. PESTICIDE QUESTIONS
    # ----------------------------------------------

    if pesticide_question:

        if not crop:
            return ask_crop_for_pesticide()

        facts = load_facts(crop)

        if not facts:
            return SAFE_FALLBACK

        system = BASE + facts + """

ప్రత్యేక పురుగుమందుల భద్రతా నియమాలు:

పురుగుమందు పేరు, బ్రాండ్, మోతాదు లేదా
పిచికారీ షెడ్యూల్ చెప్పవద్దు.

ముందుగా పురుగు లేదా వ్యాధిని గుర్తించాల్సిన
అవసరాన్ని వివరించండి.

పంట వయస్సు, పురుగు లక్షణాలు మరియు
నష్టం వివరాలు అడగండి.

స్థానిక వ్యవసాయ అధికారి లేదా రైతు భరోసా
కేంద్రం సలహా తీసుకోవాలని సూచించండి.
"""

        reply = get_llm_reply(question, system)

        if reply:
            return reply

        return (
            "పురుగు లేదా తెగులు ఏదో గుర్తించకుండా "
            "మందు పేరు లేదా మోతాదు చెప్పడం సురక్షితం కాదు. "
            "పంట వయస్సు మరియు కనిపిస్తున్న పురుగు లక్షణాలను "
            "స్థానిక వ్యవసాయ అధికారి లేదా రైతు భరోసా "
            "కేంద్రానికి వివరించండి."
        )

    # ----------------------------------------------
    # B. FERTILIZER QUESTIONS
    # ----------------------------------------------

    if fertilizer_question:

        if not crop:
            return ask_crop_for_fertilizer()

        facts = load_facts(crop)

        system = (
            BASE
            + (facts or "No crop-specific facts available.")
            + """

ప్రత్యేక ఎరువుల భద్రతా నియమాలు:

ఎరువు మోతాదు, నిష్పత్తి లేదా వేసే షెడ్యూల్ చెప్పవద్దు.

సిఫార్సులు నేల పరీక్ష, పంట దశ, రకం మరియు
స్థానిక వ్యవసాయ సూచనలపై ఆధారపడతాయని వివరించండి.

పంట వయస్సు, జిల్లా మరియు నేల పరీక్ష వివరాలు అడగండి.

ఎరువుల సిఫార్సులను కల్పించవద్దు.
"""
        )

        reply = get_llm_reply(question, system)

        if reply:
            return reply

        return (
            "ఎరువు రకం, మోతాదు మరియు వేసే సమయం "
            "నేల పరీక్ష, పంట దశ మరియు స్థానిక సిఫార్సులపై "
            "ఆధారపడి ఉంటాయి. మీ నేల పరీక్ష వివరాలతో "
            "స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి."
        )

    # ----------------------------------------------
    # C. HEALTH QUESTIONS WITHOUT CROP NAME
    # ----------------------------------------------

    if health_question and not crop:
        return crop_health_question(question)

    # ----------------------------------------------
    # D. UNKNOWN CROP
    # ----------------------------------------------

    if not crop:

        names = ", ".join(covered_names())

        return (
            "దయచేసి ఏ పంట గురించి అడుగుతున్నారో చెప్పండి. "
            "ప్రస్తుతం నేను ఈ పంటల గురించి సమాచారం అందించగలను: "
            f"{names}."
        )

    # ----------------------------------------------
    # E. LOAD CROP KNOWLEDGE
    # ----------------------------------------------

    facts = load_facts(crop)

    if not facts:

        return (
            f"క్షమించండి, {CROPS[crop]['name']} పంటకు "
            "సంబంధించిన సమాచారం ప్రస్తుతం అందుబాటులో లేదు. "
            "స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి."
        )

    # ----------------------------------------------
    # F. CROP HEALTH AND SYMPTOM MATCHING
    # ----------------------------------------------

    system = BASE + facts

    if health_question:

        matches = match_symptoms(crop, question)

        if matches:

            matched_causes = "\n".join(
                f"- {item['possible_cause']} "
                f"(matching clues: {', '.join(item['matched_keywords'])})"
                for item in matches
            )

            system += f"""

POSSIBLE SYMPTOM MATCHES — SCREENING CLUES ONLY:

{matched_causes}

IMPORTANT:

These are preliminary keyword matches, NOT confirmed diagnoses.

Use them only as possible explanations.

Explain what additional signs would help distinguish them.

Never tell the farmer that a disease or pest is confirmed.
"""

        else:

            system += """

SYMPTOM MATCHING:

No predefined symptom rule matched this question.

Do not invent a disease or pest diagnosis.

Use only relevant crop facts and ask for more details.
"""

        system += """

SPECIAL CROP HEALTH INSTRUCTIONS:

Explain only possible causes supported by the supplied facts
and relevant screening clues.

Do not confirm any disease or pest based on one symptom.

Give safe preliminary precautions.

Ask the most important follow-up questions first.

Do not recommend chemical treatments.

If the available facts are insufficient,
clearly explain the uncertainty.
"""

       
    else:

        system += """

GENERAL CROP QUESTION INSTRUCTIONS:

1. Identify the exact question before answering:
   nursery sowing, main-field transplanting, suitable
   soil, crop duration, varieties or cultivation practices.

2. Use the relevant section of the supplied crop knowledge.
   Never confuse two different farming operations.

3. IMPORTANT: DISTINGUISH SOWING AND TRANSPLANTING.
   - "నారు ఎప్పుడు పోయాలి?" means nursery sowing.
   - "నారు ఎప్పుడు నాటాలి?" means transplanting
     seedlings into the main field.
   - "విత్తనాలు ఎప్పుడు వేయాలి?" means sowing seeds.

4. For nursery sowing questions:
   Give the nursery sowing periods from the crop calendar.

5. For transplanting questions:
   Give only verified transplanting information.
   If the facts provide seedling age, explain it.
   Do not repeat nursery sowing months as transplanting dates.
   Ask when the nursery was sown if that information is missing.
   Consider seedling growth and local field conditions.

6. Do not calculate or invent a fixed transplanting date
   when the nursery sowing date or seedling condition is unknown.

7. For other sowing calendar questions:
   Check the relevant crop calendar and explain
   available seasonal or regional differences.

8. Clearly describe dates as general reference periods.
   Do not present historical district-specific dates
   as current statewide recommendations.

9. Give useful available information FIRST.
   Then ask one or two relevant follow-up questions.

10. If the supplied knowledge is insufficient,
    clearly explain the uncertainty.
    Never invent dates, varieties, fertilizer doses,
    chemical treatments or agricultural recommendations.

11. Answer entirely in natural, simple Telugu.
    Do not use Hindi words or Hindi script.

12. Keep the answer short, clear and useful to farmers.
"""


    reply = get_llm_reply(question, system)

    if reply:
        return reply

    return SAFE_FALLBACK


# --------------------------------------------------
# 15. DIRECT TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("Supported crops:")
    print(covered_names())

    print("\nEnter your farming question:")
    question = input("> ")

    print("\nFarmer Assistant:")
    print(advise(question))
