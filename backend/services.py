import os
import json
from typing import Dict, List

from dotenv import load_dotenv
from groq import Groq

# Load environment variables from project root .env
load_dotenv()


def search_evidence(query: str, limit: int = 6) -> List[Dict]:
    """Retrieve public search snippets. Search results are leads, not proof."""
    try:
        from ddgs import DDGS

        results = DDGS().text(query, max_results=limit)

        evidence = []

        for item in results or []:
            evidence.append({
                "title": item.get("title", "Untitled source"),
                "url": item.get("href", ""),
                "snippet": item.get("body", ""),
                "source": item.get("source") or item.get("href", "")
            })

        return evidence

    except Exception as exc:
        print(f"Evidence search error: {type(exc).__name__}: {exc}")
        return []


def analyze_with_groq(claim: str, evidence: List[Dict]):
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing.")

    if not evidence:
        return None

    context = "\n\n".join(
        f"Source: {x['title']}\n"
        f"URL: {x['url']}\n"
        f"Snippet: {x['snippet']}"
        for x in evidence
    )

    prompt = f"""
You are a cautious claim verification assistant.

Analyze the claim using ONLY the supplied evidence.

Rules:
1. Do not assume search snippets are complete.
2. Never invent facts or sources.
3. Supported means evidence directly supports the claim.
4. Refuted means reliable evidence directly contradicts it.
5. Mixed means evidence supports and contradicts different parts.
6. Insufficient Evidence means the evidence is inadequate.

Return a valid JSON object with exactly these keys:
- verdict
- confidence
- explanation

Allowed verdicts:
Supported, Refuted, Mixed, Insufficient Evidence

Confidence must be:
High, Medium, or Low.

CLAIM:
{claim}

EVIDENCE:
{context}
"""

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.6,
        max_completion_tokens=2048,
        reasoning_effort="low",
        include_reasoning=False,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Groq returned an empty response.")

    return content


def verify_claim(claim: str):
    limitations = [
        "Search snippets may be incomplete, outdated, or taken out of context.",
        "This tool is an assistance system, not an authoritative fact-checking verdict.",
        "A human should open and review the cited sources before sharing a conclusion."
    ]

    evidence = search_evidence(claim)

    if not evidence:
        return {
            "claim": claim,
            "verdict": "Insufficient Evidence",
            "confidence": "Low",
            "explanation": "No usable evidence could be retrieved. Try rephrasing the claim or check again later.",
            "evidence": [],
            "limitations": limitations
        }

    try:
        raw = analyze_with_groq(claim, evidence)
        result = json.loads(raw)

        allowed = {
            "Supported",
            "Refuted",
            "Mixed",
            "Insufficient Evidence"
        }

        verdict = result.get("verdict", "Insufficient Evidence")

        if verdict not in allowed:
            verdict = "Insufficient Evidence"

        confidence = result.get("confidence", "Low")

        if confidence not in {"High", "Medium", "Low"}:
            confidence = "Low"

        return {
            "claim": claim,
            "verdict": verdict,
            "confidence": confidence,
            "explanation": result.get(
                "explanation",
                "Evidence needs manual review."
            ),
            "evidence": evidence,
            "limitations": limitations
        }

    except Exception as exc:
        print(f"AI analysis error: {type(exc).__name__}: {exc}")

        return {
            "claim": claim,
            "verdict": "Needs Human Review",
            "confidence": "Low",
            "explanation": (
                "Evidence was retrieved, but AI analysis failed. "
                "Check the backend terminal for the exact error."
            ),
            "evidence": evidence,
            "limitations": limitations
        }