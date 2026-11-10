
import pytest

from advisor import advise, find_crop


CROP_TESTS = [
    ("వరి", "వరి పంటలో ఆకులపై గోధుమ రంగు మచ్చలు వస్తున్నాయి. ఏమి చేయాలి?", "paddy"),
    ("వేరుశెనగ", "వేరుశెనగ ఆకులపై గోధుమ రంగు మచ్చలు వస్తున్నాయి. ఏమి చేయాలి?", "groundnut"),
    ("మొక్కజొన్న", "మొక్కజొన్న ఆకులపై పురుగులు తిన్నట్లు రంధ్రాలు కనిపిస్తున్నాయి. ఏమి చేయాలి?", "maize"),
    ("పత్తి", "పత్తి ఆకుల అడుగు భాగంలో చిన్న తెల్ల పురుగులు కనిపిస్తున్నాయి. ఏమి చేయాలి?", "cotton"),
    ("మిరప", "మిరప ఆకులు ముడుచుకుంటున్నాయి. ఏమి చేయాలి?", "chilli"),
    ("టమాట", "టమాట ఆకులు పసుపు రంగులోకి మారుతున్నాయి. ఏమి చేయాలి?", "tomato"),
    ("అరటి", "అరటి ఆకులపై మచ్చలు కనిపిస్తున్నాయి. ఏమి చేయాలి?", "banana"),
    ("మామిడి", "మామిడి చెట్టులో పూత రాలిపోతోంది. ఏమి చేయాలి?", "mango"),
    ("చెరకు", "చెరకు కాండం ఎరుపు రంగులోకి మారుతోంది. ఏమి చేయాలి?", "sugarcane"),
    ("కందులు", "కందుల మొక్కలు వాడిపోతున్నాయి. ఏమి చేయాలి?", "redgram"),
]


@pytest.mark.parametrize("crop,question,expected_crop", CROP_TESTS)
def test_crop_identification(crop, question, expected_crop):
    assert find_crop(question) == expected_crop


@pytest.mark.parametrize("crop,question,expected_crop", CROP_TESTS)
def test_crop_advisor_returns_telugu_answer(crop, question, expected_crop):
    answer = advise(question)

    assert isinstance(answer, str)
    assert answer.strip()
    assert any("\u0c00" <= char <= "\u0c7f" for char in answer)
