
from careguard.core import detect_unsupported_claims, verify


def test_detects_invented_chest_pain():
    transcript = "Patient called about an appointment."
    summary = "Patient called about an appointment and reported chest pain."

    result = verify(transcript, summary)

    assert result["category_mismatch"] is False
    assert result["unsupported_claims"] == ["chest_pain"]
    assert result["review_required"] is True


def test_supported_symptom():
    transcript = "Patient called about an appointment and reported chest pain."
    summary = "Patient called about an appointment and reported chest pain."

    result = verify(transcript, summary)

    assert result["unsupported_claims"] == []
    assert result["review_required"] is False


def test_multiple_unsupported_claims():
    result = detect_unsupported_claims(
        "Patient called about an appointment.",
        "Patient reported fever and headache."
    )

    assert result == ["fever", "headache"]


def test_no_symptom_mentions():
    result = detect_unsupported_claims(
        "Agency called about caregiver scheduling.",
        "Agency confirmed caregiver schedule."
    )

    assert result == []
def test_detects_contradicted_symptom():
    transcript = "The caller denies having chest pain."
    summary = "The caller reported chest pain."

    result = verify(transcript, summary)

    assert result["review_required"] is True
def test_detects_chest_pain_contradiction():
    result = verify(
        "The caller denies having chest pain.",
        "The caller reported chest pain."
    )

    assert result["contradicted_claims"] == ["chest_pain"]
    assert result["reason"] == "contradicted_claims"


def test_detects_fever_contradiction():
    result = verify(
        "The caller has no fever.",
        "The caller reported fever."
    )

    assert result["contradicted_claims"] == ["fever"]


def test_preserves_negative_symptom():
    result = verify(
        "Monthly wellness check-in. The caller denies chest pain.",
        "Monthly wellness check-in. The caller denies chest pain."
    )

    assert result["contradicted_claims"] == []


def test_detects_multiple_contradictions():
    result = verify(
        "The caller denies chest pain and fever.",
        "The caller reported chest pain and fever."
    )

    assert result["contradicted_claims"] == ["chest_pain", "fever"]
