
import re

LABELS = ('monthly_check_in', 'agency_call', 'patient_inquiry', 'other')

PATTERNS = {
    'monthly_check_in': [
        r'\bmonthly (?:wellness )?check[ -]?in\b',
        r'\bmonthly follow[ -]?up\b',
        r'\bmonthly wellness call\b'
    ],
    'agency_call': [
        r'\bagency\b',
        r'\bcaregiver (?:schedule|shift)\b',
        r'\bstaffing\b'
    ],
    'patient_inquiry': [
        r'\bappointment\b',
        r'\bmedication question\b',
        r'\bservice question\b'
    ],
}

# Limited demonstration vocabulary.
# This is not a comprehensive medical terminology list.
CLAIM_PATTERNS = {
    'chest_pain': r'\bchest pain\b',
    'shortness_of_breath': r'\bshortness of breath\b',
    'fever': r'\bfever\b',
    'dizziness': r'\bdizz(?:y|iness)\b',
    'headache': r'\bheadache\b',
}


def classify(text: str) -> str:
    """Conservative baseline: abstain on ties or missing evidence."""
    counts = {
        label: sum(
            bool(re.search(p, text.lower()))
            for p in patterns
        )
        for label, patterns in PATTERNS.items()
    }

    best = max(counts.values(), default=0)

    winners = [
        label for label, count in counts.items()
        if count == best and count > 0
    ]

    return winners[0] if len(winners) == 1 else 'other'


def extract_claims(text: str) -> set[str]:
    """Find mentions of selected medical concepts."""
    return {
        claim
        for claim, pattern in CLAIM_PATTERNS.items()
        if re.search(pattern, text, re.IGNORECASE)
    }


def detect_unsupported_claims(
    transcript: str,
    summary: str
) -> list[str]:
    """
    Flag selected medical concepts mentioned in the summary
    but absent from the transcript.

    This checks mentions, not clinical meaning or negation.
    """
    transcript_claims = extract_claims(transcript)
    summary_claims = extract_claims(summary)

    return sorted(summary_claims - transcript_claims)
def extract_claim_statuses(text: str) -> dict[str, str]:
    """Identify selected claims as positive or negative mentions."""
    statuses = {}

    negation_pattern = (
        r"(?:\bdenies?\b|\bdenied\b|\bno\b|\bwithout\b|"
        r"\bnot\b|\bnegative\s+for\b|"
        r"\bdoes\s+not\s+have\b|\bdo\s+not\s+have\b)"
        r"(?:\s+\w+){0,4}\s*$"
    )

    for claim, pattern in CLAIM_PATTERNS.items():
        mentions = []

        for match in re.finditer(pattern, text, re.IGNORECASE):
            context = text[max(0, match.start() - 60):match.start()]
            context = context.rstrip(" ,;:")

            if re.search(negation_pattern, context, re.IGNORECASE):
                mentions.append("negative")
            else:
                mentions.append("positive")

        if mentions:
            statuses[claim] = (
                mentions[0] if len(set(mentions)) == 1 else "mixed"
            )

    return statuses


def verify(transcript: str, summary: str) -> dict:
    transcript_label = classify(transcript)
    summary_label = classify(summary)

    mismatch = (
        summary_label != 'other'
        and summary_label != transcript_label
    )

    uncertain = (
        transcript_label == 'other'
        or summary_label == 'other'
    )

    transcript_status = extract_claim_statuses(transcript)
    summary_status = extract_claim_statuses(summary)

    unsupported_claims = sorted(
        set(summary_status) - set(transcript_status)
    )

    contradicted_claims = sorted(
        claim
        for claim in set(transcript_status) & set(summary_status)
        if (
            transcript_status[claim] in ('positive', 'negative')
            and summary_status[claim] in ('positive', 'negative')
            and transcript_status[claim] != summary_status[claim]
        )
    )

    review_required = (
        mismatch
        or uncertain
        or bool(unsupported_claims)
        or bool(contradicted_claims)
        or any(
            status == 'mixed'
            for status in transcript_status.values()
        )
        or any(
            status == 'mixed'
            for status in summary_status.values()
        )
    )

    if mismatch:
        reason = 'category_mismatch'
    elif contradicted_claims:
        reason = 'contradicted_claims'
    elif unsupported_claims:
        reason = 'unsupported_claims'
    elif uncertain:
        reason = 'insufficient_evidence'
    else:
        reason = 'baseline_checks_passed'

    return {
        'transcript_category': transcript_label,
        'summary_category': summary_label,
        'category_mismatch': mismatch,
        'unsupported_claims': unsupported_claims,
        'contradicted_claims': contradicted_claims,
        'review_required': review_required,
        'reason': reason,
    }
def has_negation(text: str) -> bool:
    """Check whether text contains selected negation words."""
    pattern = r'\b(denies|denied|no|without)\b'
    return bool(re.search(pattern, text, re.IGNORECASE))