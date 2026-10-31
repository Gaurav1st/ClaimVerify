# ClaimVerify — AI Misinformation & Claim Verification Assistant

An academic prototype that retrieves public web evidence for a user-submitted claim and presents a cautious review with source links.

## Team
- Brijesh Kumar Trigun — 2401920100129
- Anmol Sherawat — 2401920100073
- Anurag Mishra — 2401920100084
- Gaurav Dwivedi — 2401920100145

## Current implementation
- FastAPI backend with `/health` and `/verify` endpoints.
- Streamlit user interface.
- Web evidence retrieval through DDGS.
- Optional Groq LLM analysis when `GROQ_API_KEY` is configured.
- Four cautious verdict classes: Supported, Refuted, Mixed, Insufficient Evidence.
- Fallback to Needs Human Review when AI analysis is not configured.

## Important limitations
This is a prototype, not a certified fact-checking service. Search snippets are not proof. Results may be incomplete, search can fail, and an LLM can make mistakes. Always open original sources and review them manually. Do not present model outputs as verified facts.

## Run locally
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

Set `GROQ_API_KEY` in your environment or `.env` if AI-assisted analysis is desired. Do not commit secrets.

Terminal 1:
```bash
uvicorn backend.main:app --reload --port 8000
```

Terminal 2:
```bash
streamlit run frontend/app.py
```

Open the Streamlit URL shown in the terminal. API docs: http://localhost:8000/docs

## Deployment
- Deploy the API using the included `render.yaml`.
- Deploy the Streamlit frontend separately (for example, Streamlit Community Cloud).
- Set `API_URL` in the frontend deployment to the deployed API URL.
- Add `GROQ_API_KEY` as a secret environment variable, not in source code.

## Suggested academic methodology
Claim input → web evidence retrieval → evidence inspection → optional LLM-assisted synthesis → cautious verdict → human review.

## Future scope
- Evidence deduplication and credibility metadata.
- Sentence-transformer embeddings and vector search (FAISS/Chroma).
- Cross-source stance/NLI model.
- Hindi and multilingual claim support.
- User feedback and reviewer dashboard.
- Dataset-based evaluation with documented precision, recall and F1.

## License
For academic demonstration and learning.
