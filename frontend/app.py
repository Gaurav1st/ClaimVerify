import os
import requests
import streamlit as st

st.set_page_config(page_title="ClaimVerify | Evidence first", page_icon="🔎", layout="wide")
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.markdown("""
<style>
.block-container {max-width: 1050px; padding-top: 2rem;}
.hero {padding: 1.6rem; border: 1px solid #dbe3ef; border-radius: 18px;
background: linear-gradient(120deg,#eff6ff,#f8fafc);}
.small-muted {color:#64748b;font-size:0.9rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🔎 ClaimVerify</h1><p>Evidence-first misinformation and claim review assistant</p><p class="small-muted">Check a claim, inspect the sources, and make an informed decision.</p></div>', unsafe_allow_html=True)
st.write("")
claim = st.text_area("Paste a news or social-media claim", height=120,
                     placeholder="Example: A specific public claim you want to verify...")
if st.button("Find evidence & review claim", type="primary", use_container_width=True):
    if len(claim.strip()) < 8:
        st.warning("Please enter a more detailed claim.")
    else:
        with st.spinner("Searching for relevant evidence..."):
            try:
                response = requests.post(f"{API_URL}/verify", json={"claim": claim.strip()}, timeout=60)
                response.raise_for_status()
                result = response.json()
                st.session_state["result"] = result
            except Exception as e:
                st.error(f"Could not reach the verification API. Start the backend first. Details: {e}")

result = st.session_state.get("result")
if result:
    st.divider()
    st.subheader("Review result")
    st.markdown(f"### {result['verdict']}")
    st.caption(f"Confidence: {result['confidence']}")
    st.write(result["explanation"])
    st.subheader(f"Retrieved evidence ({len(result['evidence'])})")
    if not result["evidence"]:
        st.info("No sources were retrieved for this claim.")
    for i, item in enumerate(result["evidence"], 1):
        with st.container(border=True):
            st.markdown(f"**{i}. [{item['title']}]({item['url']})**")
            st.write(item["snippet"])
            st.caption(item.get("source", ""))
    st.subheader("Important limitations")
    for item in result["limitations"]:
        st.write("• " + item)

st.divider()
st.caption("Academic prototype • Search snippets are not proof • Always verify original sources")
