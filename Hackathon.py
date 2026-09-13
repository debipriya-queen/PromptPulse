import streamlit as st
import json
from google import genai
from google.genai import types

st.set_page_config(
    page_title="PromptPulse | AI Prompt Engineering Studio",
    page_icon="⚡",
    layout="wide"
)

# 1. API Configuration
API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"
client = genai.Client(api_key=API_KEY)

# 2. Header & Overview
st.title("⚡ PromptPulse: Production Prompt Engineering Studio")
st.caption("Benchmark, audit, and auto-engineer prompts for production-grade LLM reliability.")

# 3. Sidebar Controls
with st.sidebar:
    st.header("⚙️ Target Domain Persona")
    domain = st.selectbox(
        "Optimization Target:",
        [
            "General Assistant",
            "Software & Scripting",
            "Data Science & Analytics",
            "Executive & Workplace",
            "Marketing & Copywriting"
        ]
    )
    st.divider()
    st.markdown("### 🏆 Pitch Talking Points")
    st.markdown("- **Core Problem:** 80% of LLM failures are prompt ambiguity issues.")
    st.markdown("- **Solution:** Automated schema-enforced prompt restructuring.")
    st.markdown("- **Engine:** Gemini Flash zero-shot audit pipeline.")

# 4. Interactive Quick-Load Presets
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

st.markdown("##### 💡 Load Quick Benchmark Preset:")
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("💻 Python Web Scraper", use_container_width=True):
        st.session_state.user_prompt = "write python code to scrape real estate prices from a listing site"
with b2:
    if st.button("✉️ Manager Medical Leave", use_container_width=True):
        st.session_state.user_prompt = "write an email asking my manager for 3 days medical leave"
with b3:
    if st.button("📢 Skincare Ad Script", use_container_width=True):
        st.session_state.user_prompt = "write an instagram reel hook script for a face serum"

# 5. Input Area
user_input = st.text_area(
    "Input Raw / Draft Prompt:",
    value=st.session_state.user_prompt,
    placeholder="Type or click a preset above...",
    height=110
)

# 6. Evaluation System Instruction
SYSTEM_INSTRUCTION = f"""
You are PromptPulse, an elite prompt engineer.
Target Persona: {domain}

Audit the user's prompt and output ONLY a valid JSON object matching this schema:
{{
  "overall_score": ,
  "clarity_score": ,
  "context_score": ,
  "constraints_score": ,
  "flaws": [
    "",
    ""
  ],
  "perfected_prompt": "",
  "best_practices_used": [
    "",
    ""
  ]
}}
CRITICAL: All scores must be integers between 1 and 10. Return strictly JSON without markdown backticks.
"""

if st.button("🚀 Audit & Optimize Prompt", type="primary", use_container_width=True):
    if user_input.strip():
        with st.spinner("Analyzing prompt architecture..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.1
                    )
                )

                raw_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(raw_text)

                def normalize_score(s):
                    val = float(s)
                    return round(val / 10.0 if val > 10 else val, 1)

                st.session_state.audit = data
                st.session_state.orig_input = user_input
                st.session_state.overall = normalize_score(data.get("overall_score", 5))
                st.session_state.clarity = normalize_score(data.get("clarity_score", 5))
                st.session_state.context = normalize_score(data.get("context_score", 5))
                st.session_state.constraints = normalize_score(data.get("constraints_score", 5))

            except Exception as e:
                st.error(f"Audit error: {e}")
    else:
        st.warning("Please enter a prompt or select a preset.")

# 7. Results Display
if "audit" in st.session_state:
    res = st.session_state.audit
    st.divider()

    # Multi-Dimensional Metric Dashboard
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Overall Quality", f"{st.session_state.overall} / 10")
    with m2:
        st.metric("Clarity Score", f"{st.session_state.clarity} / 10")
    with m3:
        st.metric("Context Delivery", f"{st.session_state.context} / 10")
    with m4:
        st.metric("Constraint Rigor", f"{st.session_state.constraints} / 10")

    st.progress(min(max(st.session_state.overall / 10.0, 0.0), 1.0))

    # Presentation Tabs
    tab_audit, tab_live = st.tabs(["📊 Prompt Audit & Architecture", "🧪 Live Test Lab"])

    with tab_audit:
        col_flaws, col_tech = st.columns(2)
        with col_flaws:
            st.subheader("⚠️ Missing Guardrails & Flaws")
            for f in res.get("flaws", []):
                st.markdown(f"- ❌ {f}")
        with col_tech:
            st.subheader("🛠️ Applied Techniques")
            for t in res.get("best_practices_used", []):
                st.markdown(f"- ✅ **{t}**")

        st.divider()
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("### ❌ Unoptimized Draft")
            st.text_area("raw", value=st.session_state.orig_input, height=220, disabled=True, label_visibility="collapsed")
        with col_right:
            st.markdown("### ✨ Production-Grade Prompt")
            st.code(res.get("perfected_prompt", ""), language="markdown")

    with tab_live:
        st.markdown("### 🧪 Side-by-Side Execution Proof")
        st.caption("Demonstrate the actual difference to the judges by executing both prompts through Gemini Flash live.")
        
        if st.button("⚡ Run Real-Time Comparative Test"):
            with st.spinner("Generating live responses from both prompts..."):
                t1, t2 = st.columns(2)
                with t1:
                    st.markdown("#### Output from Raw Draft:")
                    raw_eval = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=st.session_state.orig_input
                    )
                    st.info(raw_eval.text)
                with t2:
                    st.markdown("#### Output from Production Prompt:")
                    opt_eval = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=res.get("perfected_prompt", "")
                    )
                    st.success(opt_eval.text)