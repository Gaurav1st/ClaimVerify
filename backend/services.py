import os
from typing import Dict, List
import requests

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
    except Exception:
        return []

def analyze_with_groq(claim: str, evidence: List[Dict]):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or not evidence:
        return None
    context = "\n\n".join(
        f"Source: {x['title']}\nURL: {x['url']}\nSnippet: {x['snippet']}"
        for x in evidence
    )
    prompt = f"""You are a cautious claim-review assistant. Do not assume search snippets are complete.
Assess the claim only against the evidence below. Return JSON with keys verdict, confidence,
explanation. verdict must be one of Supported, Refuted, Mixed, Insufficient Evidence.
Use Insufficient Evidence if sources do not directly establish the claim. Never invent facts.
CLAIM: {claim}
EVIDENCE:
{context}
"""
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=45
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def verify_claim(claim: str):
    import json
    evidence = search_evidence(claim)
    limitations = [
        "Search snippets may be incomplete, outdated, or taken out of context.",
        "This tool is an assistance system, not an authoritative fact-checking verdict.",
        "A human should open and review the cited sources before sharing a conclusion."
    ]
    if not evidence:
        return {
            "claim": claim, "verdict": "Insufficient Evidence", "confidence": "Low",
            "explanation": "No usable evidence could be retrieved. Try rephrasing the claim or check again later.",
            "evidence": [], "limitations": limitations
        }
    try:
        raw = analyze_with_groq(claim, evidence)
        if raw:
            result = json.loads(raw)
            allowed = {"Supported", "Refuted", "Mixed", "Insufficient Evidence"}
            verdict = result.get("verdict", "Insufficient Evidence")
            if verdict not in allowed:
                verdict = "Insufficient Evidence"
            return {
                "claim": claim, "verdict": verdict,
                "confidence": result.get("confidence", "Low"),
                "explanation": result.get("explanation", "Evidence needs manual review."),
                "evidence": evidence, "limitations": limitations
            }
    except Exception:
        pass
    return {
        "claim": claim, "verdict": "Needs Human Review", "confidence": "Low",
        "explanation": "Relevant search results were found, but automated reasoning is unavailable. Review the sources manually. Add a GROQ_API_KEY to enable AI-assisted evidence analysis.",
        "evidence": evidence, "limitations": limitations
    }
