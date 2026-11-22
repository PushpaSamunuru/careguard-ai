# CareGuard AI

**Healthcare Call-Summary Verification API** · **Rule-based prototype v0.2.0**

[Live API documentation](https://careguard-ai-3ibv.onrender.com/docs) · [GitHub source](https://github.com/PushpaSamunuru/careguard-ai)

CareGuard AI is a Python and FastAPI prototype that compares call transcripts with AI-generated summaries, flags potential inconsistencies, and indicates when a human should review the result. It is designed as a *demonstration of verification and evaluation techniques* using synthetic examples.

> **Important:** This is a limited, rule-based prototype, **not** a clinically validated tool or medical device. It is not intended for clinical decisions or production processing of protected health information. Do not submit real patient data to the publicly accessible demo.

## What it checks

- **Call classification:** identifies `monthly_check_in`, `agency_call`, `patient_inquiry`, or `other` using phrase patterns.
- **Category mismatch:** flags cases where the generated summary names a different recognized call category.
- **Unsupported symptom mentions:** detects selected symptoms present in the summary but not mentioned in the transcript.
- **Contradictory symptom mentions:** compares simple positive/negative status for selected symptoms, such as *denies chest pain* vs. *reported chest pain*.
- **Human-review flag:** returns `review_required` and a `reason` for downstream review workflows.

The current symptom vocabulary covers chest pain, shortness of breath, fever, dizziness, and headache. Negation is detected using limited text patterns; complex context, phrasing, and clinical meaning are **not** reliably handled.

## Try the live API

**Swagger UI:** https://careguard-ai-3ibv.onrender.com/docs

Open **POST /verify**, select **Try it out**, paste this synthetic request, then click **Execute**:

```json
{
  "transcript": "The caller denies having chest pain.",
  "summary": "The caller reported chest pain."
}
```

Example response from the deployed API:

```json
{
  "transcript_category": "other",
  "summary_category": "other",
  "category_mismatch": false,
  "unsupported_claims": [],
  "contradicted_claims": ["chest_pain"],
  "review_required": true,
  "reason": "contradicted_claims"
}
```

A matching summary of the same statement produces `contradicted_claims: []`, but may still require review because the call category is `other` and evidence is insufficient for category classification.

> The public Render free-tier instance may sleep when idle, so the first request can be slow.

## Architecture

```text
Synthetic transcript + generated summary
                 |
                 v
         FastAPI POST /verify
                 |
                 v
           verify() logic
          /      |       \
   Classify   Symptoms   Symptom polarity
   call type   present    / negation
          \      |       /
                 v
     Review decision + reason
                 |
                 v
            JSON response
```

The verification logic lives in `src/careguard/core.py` and the HTTP interface in `src/careguard/api.py`. The app uses deterministic regular-expression matching; it does **not** call an LLM for its verification decisions.

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/` | Service information |
| GET | `/health` | Basic health response |
| POST | `/verify` | Compare transcript and summary |

## Run locally

Requires **Python 3.11+**.

```bash
git clone https://github.com/PushpaSamunuru/careguard-ai.git
cd careguard-ai
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies and launch the API:

```bash
python -m pip install -e ".[dev]"
python -m pip install fastapi uvicorn
uvicorn careguard.api:app --reload
```

Open http://127.0.0.1:8000/docs.

## Tests and evaluation

```bash
python -m pytest -q
python evaluate.py
```

The repository includes unit tests for classification, mismatch flagging, unsupported mentions, and symptom contradictions. In local testing, **13 automated tests passed**.

The evaluation script uses **12 hand-crafted synthetic cases** and previously reported:

| Metric | Result |
| --- | --- |
| Category accuracy | 12/12 (100%) |
| Review precision | 4/4 (100%) |
| Review recall | 4/4 (100%) |

These metrics describe a **small smoke-test dataset**, not performance on independent or real-world healthcare conversations. They must not be interpreted as evidence of clinical reliability.

## Limitations and future work

- Fixed categories and a small symptom vocabulary.
- Regex-based polarity checks can fail with negation scope, paraphrases, multiple speakers, or complex sentences.
- Unknown categories are conservatively flagged for review.
- No independent benchmark, clinical validation, authentication, or production patient-data safeguards.
- Future improvements: expand synthetic edge-case tests, test negation scope and paraphrases, add CI, and improve API robustness.

## Project links

- **Live demo:** https://careguard-ai-3ibv.onrender.com/docs
- **Repository:** https://github.com/PushpaSamunuru/careguard-ai
- **Developer portfolio:** https://pushpasamunuru.com/
