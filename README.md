⚡ PromptPulse: Production AI Prompt Engineering Studio
PromptPulse is a quantitative LLMOps prompt auditing and benchmarking suite powered by Google Gemini Flash and Streamlit. It diagnoses prompt vulnerabilities, enforces production guardrails, and empirically tests prompts in real time.

🎯 The Problem
Over 80% of enterprise LLM failures stem from prompt ambiguity rather than model limitations. Unstructured drafts lead to hallucinations, security leaks, fragile outputs, and non-deterministic schemas.

💡 The Solution
PromptPulse introduces an automated prompt engineering pipeline:

4-Point Quantitative Audit: Scores drafts across Clarity, Context, Constraints, and Overall Quality (1–10 scale).

Vulnerability Diagnosis: Identifies missing delimiters, omitted negative constraints, and absent schema definitions.

Automated Reconstruction: Builds production-ready prompts embedding system roles, input delimitation, and explicit output contracts.

Live Empirical Test Lab: Simultaneously executes both the raw draft and optimized prompt against Gemini Flash to verify output differences side-by-side.

🛠️ Tech Stack
Interface: Streamlit

Intelligence Engine: Google Gemini Flash (gemini-2.5-flash)

SDK: google-genai

Output Validation: Zero-shot JSON schema enforcement

🚀 Setup & Execution
Clone the repository:

Bash
git clone https://github.com/debipriya-queen/PromptPulse.git
cd PromptPulse
Install dependencies:

Bash
pip install -r requirements.txt
Run the studio:

streamlit run Hackathon.py

Bash
streamlit run Hackathon.py
