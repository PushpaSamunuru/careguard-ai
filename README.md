# 

# \# CareGuard AI

# 

# \### Healthcare Call-Summary Verification API

# 

# CareGuard AI is a Python-based, rule-driven prototype designed to identify potential inconsistencies between healthcare call transcripts and their generated summaries.

# 

# The system flags selected unsupported symptom claims, contradictory symptom statements, category mismatches, and insufficient evidence for human review.

# 

# \*\*Status:\*\* Prototype v0.2.0 — synthetic data only.

# 

# \## Features

# 

# \- Call classification into four categories:

# &#x20; - Monthly check-in

# &#x20; - Agency call

# &#x20; - Patient inquiry

# &#x20; - Other

# \- Category mismatch detection

# \- Unsupported symptom-claim detection

# \- Positive/negative symptom contradiction detection

# \- Human-review flagging

# \- REST API built with FastAPI

# \- Interactive Swagger documentation

# \- Automated unit tests

# \- Synthetic evaluation dataset

# 

# \## Tech Stack

# 

# \- Python

# \- FastAPI

# \- Pydantic

# \- Uvicorn

# \- Pytest

# \- Regular expressions

# \- JSONL

# 

# \## Project Structure

# 

# ```text

# careguard-ai/

# ├── data/

# │   └── cases.jsonl

# ├── src/

# │   └── careguard/

# │       ├── api.py

# │       └── core.py

# ├── tests/

# │   ├── test\_claims.py

# │   └── test\_core.py

# ├── evaluate.py

# ├── pyproject.toml

# └── README.md

# ```

# 

# \## Installation

# 

# From the project directory:

# 

# ```powershell

# python -m venv .venv

# .\\.venv\\Scripts\\python.exe -m pip install -e ".\[dev]"

# .\\.venv\\Scripts\\python.exe -m pip install fastapi uvicorn

# ```

# 

# For an existing environment located in the parent directory, use `..\\.venv\\Scripts\\python.exe` instead.

# 

# \## Start the API

# 

# ```powershell

# python -m uvicorn careguard.api:app --reload

# ```

# 

# Open:

# 

# http://127.0.0.1:8000/docs

# 

# \## API Endpoints

# 

# | Method | Endpoint | Purpose |

# |---|---|---|

# | GET | `/` | API welcome message |

# | GET | `/health` | Health check |

# | POST | `/verify` | Verify transcript-summary consistency |

# 

# \## Example Request

# 

# POST `/verify`

# 

# ```json

# {

# &#x20; "transcript": "The caller denies having chest pain.",

# &#x20; "summary": "The caller reported chest pain."

# }

# ```

# 

# \## Example Response

# 

# ```json

# {

# &#x20; "transcript\_category": "other",

# &#x20; "summary\_category": "other",

# &#x20; "category\_mismatch": false,

# &#x20; "unsupported\_claims": \[],

# &#x20; "contradicted\_claims": \["chest\_pain"],

# &#x20; "review\_required": true,

# &#x20; "reason": "contradicted\_claims"

# }

# ```

# 

# The prototype identifies a contradiction and flags the summary for human review.

# 

# \## Testing

# 

# Run automated tests:

# 

# ```powershell

# python -m pytest -q

# ```

# 

# Latest local test result:

# 

# \*\*13 tests passed.\*\*

# 

# Run the synthetic evaluation:

# 

# ```powershell

# python evaluate.py

# ```

# 

# Results on 12 handcrafted synthetic examples:

# 

# | Metric | Result |

# |---|---|

# | Category accuracy | 12/12 (100%) |

# | Review precision | 4/4 (100%) |

# | Review recall | 4/4 (100%) |

# 

# These results are limited smoke-test results and do not demonstrate performance on independent or real-world data.

# 

# \## Limitations

# 

# \- Uses deterministic rules, not a trained machine-learning or large-language model.

# \- Supports only selected symptom concepts and phrase patterns.

# \- Negation detection is limited and may misinterpret complex sentences.

# \- May miss synonyms, temporal context, speaker attribution, and mixed-intent calls.

# \- Does not reliably detect all hallucinations or factual inconsistencies.

# \- Human-review flags are not medical safety certifications.

# \- No independent clinical validation has been performed.

# 

# \*\*Privacy:\*\* Use synthetic data only. Do not submit protected health information, patient records, or confidential employer data.

# 

# \## Future Improvements

# 

# \- Independent held-out evaluation

# \- Expanded clinical terminology and contradiction detection

# \- LLM-assisted verification with grounded evidence

# \- Human review workflow

# \- Audit logging

# \- Monitoring dashboard

# \- Deployment and continuous integration

# 

# \## Disclaimer

# 

# CareGuard AI is an educational software engineering prototype. It is not a medical device, clinical decision-support system, or production-ready healthcare application.



