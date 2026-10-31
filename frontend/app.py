import os
import requests
import streamlit as st
from typing import Dict, List, Optional
import re

# Page configuration
st.set_page_config(
    page_title="ClaimVerify — Don't Just Believe It. Verify It.",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# API configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "120"))

# Custom CSS for premium design
st.markdown("""
<style>
    /* Base styles */
    :root {
        --primary: #0f172a;
        --primary-light: #1e293b;
        --accent: #3b82f6;
        --accent-light: #60a5fa;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --neutral-50: #f8fafc;
        --neutral-100: #f1f5f9;
        --neutral-200: #e2e8f0;
        --neutral-300: #cbd5e1;
        --neutral-400: #94a3b8;
        --neutral-500: #64748b;
        --neutral-600: #475569;
        --neutral-700: #334155;
        --neutral-800: #1e293b;
        --neutral-900: #0f172a;
    }

    /* Container */
    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Navigation */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }

    .nav-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .nav-links {
        display: flex;
        gap: 2rem;
    }

    .nav-link {
        color: var(--neutral-600);
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s;
    }

    .nav-link:hover {
        color: var(--accent);
    }

    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--primary);
        margin-bottom: 1rem;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.125rem;
        color: var(--neutral-600);
        margin-bottom: 2rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Example claims */
    .example-claims {
        display: flex;
        gap: 0.75rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }

    /* Input section */
    .input-section {
        background: white;
        border: 1px solid var(--neutral-200);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }

    .input-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--neutral-700);
        margin-bottom: 0.5rem;
    }

    .char-counter {
        font-size: 0.75rem;
        color: var(--neutral-400);
        text-align: right;
        margin-top: 0.5rem;
    }

    /* Trust badge */
    .trust-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--neutral-50);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-size: 0.875rem;
        color: var(--neutral-600);
        margin-top: 1rem;
    }

    /* Result card */
    .result-card {
        background: white;
        border: 1px solid var(--neutral-200);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }

    /* Verdict badges */
    .verdict-badge {
        display: inline-block;
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    .verdict-supported {
        background: #dcfce7;
        color: #166534;
    }

    .verdict-refuted {
        background: #fee2e2;
        color: #991b1b;
    }

    .verdict-mixed {
        background: #fef3c7;
        color: #92400e;
    }

    .verdict-insufficient {
        background: #f1f5f9;
        color: #475569;
    }

    .verdict-needs-review {
        background: #fef9c3;
        color: #854d0e;
    }

    /* Confidence indicator */
    .confidence-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-left: 1rem;
    }

    .confidence-high {
        background: #dcfce7;
        color: #166534;
    }

    .confidence-medium {
        background: #fef3c7;
        color: #92400e;
    }

    .confidence-low {
        background: #f1f5f9;
        color: #475569;
    }

    /* Simple explanation */
    .simple-explanation {
        font-size: 1.125rem;
        color: var(--neutral-700);
        line-height: 1.6;
        margin: 1.5rem 0;
        padding: 1rem 0;
        border-top: 1px solid var(--neutral-200);
        border-bottom: 1px solid var(--neutral-200);
    }

    /* Why this result */
    .why-result {
        background: var(--neutral-50);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }

    .why-result h4 {
        margin: 0 0 1rem 0;
        color: var(--neutral-800);
        font-size: 1rem;
    }

    .why-result ul {
        margin: 0;
        padding-left: 1.25rem;
    }

    .why-result li {
        color: var(--neutral-600);
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }

    /* Evidence section */
    .evidence-section {
        margin-top: 2rem;
    }

    .evidence-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .evidence-card {
        background: white;
        border: 1px solid var(--neutral-200);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: box-shadow 0.2s;
    }

    .evidence-card:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    .evidence-title {
        font-weight: 600;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }

    .evidence-url {
        font-size: 0.875rem;
        color: var(--accent);
        margin-bottom: 0.75rem;
    }

    .evidence-snippet {
        color: var(--neutral-600);
        font-size: 0.9375rem;
        line-height: 1.6;
        margin-bottom: 0.75rem;
    }

    .evidence-meta {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.875rem;
        color: var(--neutral-500);
    }

    .source-badge {
        background: var(--neutral-100);
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--neutral-600);
    }

    /* Limitations section */
    .limitations-section {
        background: #fef3c7;
        border: 1px solid #fcd34d;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
    }

    .limitations-section h4 {
        margin: 0 0 1rem 0;
        color: #92400e;
        font-size: 1rem;
    }

    .limitations-section ul {
        margin: 0;
        padding-left: 1.25rem;
    }

    .limitations-section li {
        color: #78350f;
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }

    /* Loading animation */
    .loading-container {
        text-align: center;
        padding: 3rem 0;
    }

    .loading-stages {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-top: 2rem;
        text-align: left;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    }

    .loading-stage {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: var(--neutral-500);
        font-size: 0.9375rem;
    }

    .loading-stage.active {
        color: var(--accent);
        font-weight: 600;
    }

    .loading-stage.completed {
        color: var(--success);
    }

    /* Error states */
    .error-card {
        background: #fee2e2;
        border: 1px solid #fecaca;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0;
    }

    .error-card h4 {
        margin: 0 0 0.75rem 0;
        color: #991b1b;
        font-size: 1rem;
    }

    .error-card p {
        margin: 0;
        color: #7f1d1d;
        line-height: 1.6;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        border-top: 1px solid var(--neutral-200);
        margin-top: 3rem;
        color: var(--neutral-500);
        font-size: 0.875rem;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }

        .hero-subtitle {
            font-size: 1rem;
        }

        .example-claims {
            flex-direction: column;
            align-items: center;
        }

        .nav-links {
            display: none;
        }

        .input-section {
            padding: 1.5rem;
        }

        .result-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)


def classify_source(url: str) -> str:
    """Classify source based on URL patterns."""
    url_lower = url.lower()

    academic_patterns = ['.edu', '.ac.', 'scholar.google', 'researchgate', 'arxiv.org', 'pubmed']
    government_patterns = ['.gov', 'gov.', 'official']
    news_patterns = ['news', 'times', 'post', 'guardian', 'bbc', 'cnn', 'reuters', 'apnews']
    reference_patterns = ['wikipedia', 'britannica', 'worldbank', 'who.int', 'un.org']

    for pattern in academic_patterns:
        if pattern in url_lower:
            return "Academic"

    for pattern in government_patterns:
        if pattern in url_lower:
            return "Government"

    for pattern in news_patterns:
        if pattern in url_lower:
            return "News"

    for pattern in reference_patterns:
        if pattern in url_lower:
            return "Reference"

    return "Other"


def simplify_explanation(explanation: str) -> str:
    """Simplify AI-generated explanation for general audience."""
    # Keep it simple - return original if too complex to safely simplify
    if len(explanation) < 100:
        return explanation

    # Basic cleanup without changing meaning
    sentences = explanation.split('.')
    simplified = []

    for sentence in sentences[:3]:  # Max 3 sentences
        sentence = sentence.strip()
        if sentence and len(sentence) > 10:
            simplified.append(sentence)

    if simplified:
        return '. '.join(simplified) + ('.' if simplified[-1][-1] != '.' else '')

    return explanation


def get_verdict_display_label(verdict: str) -> str:
    """Map backend verdict to user-friendly display label."""
    mapping = {
        "Supported": "Likely True",
        "Refuted": "Likely False",
        "Mixed": "Partly True",
        "Insufficient Evidence": "Not Enough Evidence",
        "Needs Human Review": "Needs Manual Review"
    }
    return mapping.get(verdict, verdict)


def get_verdict_class(verdict: str) -> str:
    """Get CSS class for verdict badge."""
    mapping = {
        "Supported": "verdict-supported",
        "Refuted": "verdict-refuted",
        "Mixed": "verdict-mixed",
        "Insufficient Evidence": "verdict-insufficient",
        "Needs Human Review": "verdict-needs-review"
    }
    return mapping.get(verdict, "verdict-insufficient")


def get_confidence_class(confidence: str) -> str:
    """Get CSS class for confidence indicator."""
    mapping = {
        "High": "confidence-high",
        "Medium": "confidence-medium",
        "Low": "confidence-low"
    }
    return mapping.get(confidence, "confidence-low")


def generate_why_points(result: Dict) -> List[str]:
    """Generate 'Why this result' points based on actual evidence."""
    points = []
    verdict = result.get("verdict", "")
    evidence = result.get("evidence", [])
    explanation = result.get("explanation", "")

    # Extract insights from explanation
    if "insufficient" in explanation.lower() or "limited" in explanation.lower():
        points.append("Available sources do not directly confirm the claim.")
    elif "contradict" in explanation.lower() or "refute" in explanation.lower():
        points.append("Some evidence contradicts parts of the claim.")
    elif "support" in explanation.lower():
        points.append("Available evidence provides some support for the claim.")

    if len(evidence) < 3:
        points.append("More sources are needed for a complete analysis.")

    if not points:
        points.append("The evidence requires careful manual review.")

    return points[:3]


def deduplicate_evidence(evidence: List[Dict]) -> List[Dict]:
    """Remove duplicate URLs from evidence."""
    seen_urls = set()
    deduplicated = []

    for item in evidence:
        url = item.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            deduplicated.append(item)
        elif not url:
            deduplicated.append(item)

    return deduplicated


def render_navigation():
    """Render navigation bar."""
    st.markdown("""
    <div class="nav-container">
        <div class="nav-logo">
            🔎 ClaimVerify
        </div>
        <div class="nav-links">
            <a href="#" class="nav-link">Home</a>
            <a href="#" class="nav-link">How It Works</a>
            <a href="#" class="nav-link">About</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_hero():
    """Render hero section."""
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Don't Just Believe It. Verify It.</h1>
        <p class="hero-subtitle">
            Investigate claims, explore reliable evidence, and make informed decisions with AI-powered claim verification.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_example_claims():
    """Render clickable example claims."""
    examples = [
        "Coffee causes cancer",
        "The Great Wall of China is visible from space",
        "Humans only use 10% of their brain",
        "Goldfish have a 3-second memory"
    ]

    st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 1rem;">Try an example:</p>', unsafe_allow_html=True)

    cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with cols[i]:
            if st.button(example, key=f"example_{i}", use_container_width=True):
                st.session_state["claim_input"] = example
                st.rerun()


def render_claim_input():
    """Render claim input section."""
    st.markdown('<div class="input-section">', unsafe_allow_html=True)

    st.markdown('<div class="input-label">Enter a claim to verify</div>', unsafe_allow_html=True)

    default_claim = st.session_state.get("claim_input", "")
    claim = st.text_area(
        "Enter your claim",
        value=default_claim,
        height=120,
        placeholder="Example: A specific public claim you want to verify...",
        label_visibility="collapsed",
        key="claim_text"
    )

    # Character counter
    char_count = len(claim)
    st.markdown(f'<div class="char-counter">{char_count}/1000 characters</div>', unsafe_allow_html=True)

    # Verify button
    verify_clicked = st.button(
        "Verify Claim",
        type="primary",
        use_container_width=True,
        disabled=len(claim.strip()) < 8 or len(claim) > 1000
    )

    # Trust badge
    st.markdown("""
    <div class="trust-badge">
        <span>ℹ️</span>
        <span>Results are based on available web evidence. Always verify original sources.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    return claim, verify_clicked


def render_loading():
    """Render loading animation."""
    st.markdown("""
    <div class="loading-container">
        <h3>Analyzing your claim...</h3>
        <div class="loading-stages">
            <div class="loading-stage active">• Understanding the claim</div>
            <div class="loading-stage">• Searching for relevant evidence</div>
            <div class="loading-stage">• Reviewing available sources</div>
            <div class="loading-stage">• Analyzing supporting and contradicting information</div>
            <div class="loading-stage">• Preparing the result</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_result(result: Dict):
    """Render verification result."""
    verdict = result.get("verdict", "")
    display_verdict = get_verdict_display_label(verdict)
    verdict_class = get_verdict_class(verdict)
    confidence = result.get("confidence", "")
    confidence_class = get_confidence_class(confidence)
    claim = result.get("claim", "")
    explanation = result.get("explanation", "")
    evidence = result.get("evidence", [])
    limitations = result.get("limitations", [])

    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    # Verdict badge and confidence
    st.markdown(f"""
    <div>
        <span class="verdict-badge {verdict_class}">{display_verdict}</span>
        <span class="confidence-indicator {confidence_class}">
            Confidence: {confidence}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Submitted claim
    st.markdown(f"**Claim:** {claim}")

    # Simple explanation
    simple_explanation = simplify_explanation(explanation)
    st.markdown(f'<div class="simple-explanation">{simple_explanation}</div>', unsafe_allow_html=True)

    # Why this result
    why_points = generate_why_points(result)
    st.markdown('<div class="why-result">', unsafe_allow_html=True)
    st.markdown("#### Why this result?")
    for point in why_points:
        st.markdown(f"* {point}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Evidence section
    st.markdown('<div class="evidence-section">', unsafe_allow_html=True)

    deduplicated_evidence = deduplicate_evidence(evidence)

    with st.expander(f"Explore Evidence — {len(deduplicated_evidence)} Sources", expanded=True):
        if not deduplicated_evidence:
            st.info("No sources were retrieved for this claim.")
        else:
            for i, item in enumerate(deduplicated_evidence, 1):
                title = item.get("title", "Untitled source")
                url = item.get("url", "")
                snippet = item.get("snippet", "")
                source = item.get("source", url)
                source_category = classify_source(url)

                st.markdown(f'<div class="evidence-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="evidence-title">{i}. {title}</div>', unsafe_allow_html=True)

                if url:
                    st.markdown(f'<div class="evidence-url">🔗 <a href="{url}" target="_blank">{url}</a></div>', unsafe_allow_html=True)

                st.markdown(f'<div class="evidence-snippet">{snippet}</div>', unsafe_allow_html=True)

                st.markdown(f'''
                <div class="evidence-meta">
                    <span class="source-badge">{source_category}</span>
                    <span>{source[:50]}...</span>
                </div>
                ''', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Limitations
    st.markdown('<div class="limitations-section">', unsafe_allow_html=True)
    st.markdown("#### About this result")
    for limitation in limitations:
        st.markdown(f"* {limitation}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_error(error_message: str):
    """Render error state."""
    st.markdown(f"""
    <div class="error-card">
        <h4>⚠️ Something went wrong</h4>
        <p>{error_message}</p>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render footer."""
    st.markdown("""
    <div class="footer">
        <p>ClaimVerify • Academic prototype • Search snippets are not proof • Always verify original sources</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application."""
    # Clear claim input from session state if we want fresh start
    if "claim_input" in st.session_state and st.session_state.get("clear_input"):
        del st.session_state["claim_input"]
        st.session_state["clear_input"] = False

    # Navigation
    render_navigation()

    # Hero section
    render_hero()

    # Example claims
    render_example_claims()

    # Claim input
    claim, verify_clicked = render_claim_input()

    # Handle verification
    if verify_clicked and len(claim.strip()) >= 8:
        st.session_state["clear_input"] = True
        st.session_state["verifying"] = True
        st.session_state["current_claim"] = claim.strip()

    # Show loading state
    if st.session_state.get("verifying"):
        render_loading()

        try:
            current_claim = st.session_state.get("current_claim", claim.strip())
            response = requests.post(
                f"{API_URL}/verify",
                json={"claim": current_claim},
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()
            st.session_state["result"] = result
            st.session_state["verifying"] = False
            st.rerun()
        except requests.exceptions.Timeout:
            st.session_state["verifying"] = False
            render_error("The verification service is taking longer than expected. Please try again.")
        except requests.exceptions.ConnectionError:
            st.session_state["verifying"] = False
            render_error("Could not connect to the verification service. Please ensure the backend is running.")
        except requests.exceptions.HTTPError as e:
            st.session_state["verifying"] = False
            if e.response.status_code == 502:
                render_error("The verification service encountered an error. Please try again later.")
            else:
                render_error(f"An unexpected error occurred (Status: {e.response.status_code}).")
        except Exception as e:
            st.session_state["verifying"] = False
            render_error(f"An unexpected error occurred. Please try again.")

    # Show result if available
    if "result" in st.session_state and not st.session_state.get("verifying"):
        st.divider()
        render_result(st.session_state["result"])

        # New claim button
        if st.button("Verify Another Claim", use_container_width=True):
            del st.session_state["result"]
            st.rerun()

    # Footer
    render_footer()


if __name__ == "__main__":
    main()
