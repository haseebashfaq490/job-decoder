import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Job Description Decoder",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
    /* Hide streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* Main container */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }

    /* Hero section */
    .hero {
        text-align: center;
        padding: 3rem 0 2rem;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.5);
        color: #a5b4fc;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 1.5rem;
        letter-spacing: 0.05em;
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 1rem;
        line-height: 1.1;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        max-width: 560px;
        margin: 0 auto 2.5rem;
        line-height: 1.6;
    }

    /* Stats row */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 3rem;
        flex-wrap: wrap;
    }

    .stat {
        text-align: center;
    }

    .stat-number {
        font-size: 1.5rem;
        font-weight: 700;
        color: #a5b4fc;
    }

    .stat-label {
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Input card */
    .input-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
    }

    .input-label {
        font-size: 14px;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.75rem;
        display: block;
    }

    /* Text area override */
    .stTextArea textarea {
        background: rgba(15, 12, 41, 0.6) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        padding: 1rem !important;
        transition: border-color 0.2s !important;
    }

    .stTextArea textarea:focus {
        border-color: rgba(99, 102, 241, 0.8) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }

    .stTextArea textarea::placeholder {
        color: #475569 !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2.5rem !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.2s !important;
        letter-spacing: 0.02em !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
    }

    /* Results card */
    .results-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        margin-top: 1.5rem;
    }

    .results-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    .results-title {
        font-size: 16px;
        font-weight: 700;
        color: #e2e8f0;
    }

    .results-badge {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #6ee7b7;
        padding: 3px 10px;
        border-radius: 50px;
        font-size: 11px;
        font-weight: 600;
    }

    /* Markdown output styling */
    .stMarkdown h2 {
        color: #a5b4fc !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin: 1.5rem 0 0.5rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1px solid rgba(165, 180, 252, 0.2) !important;
    }

    .stMarkdown p, .stMarkdown li {
        color: #cbd5e1 !important;
        font-size: 14px !important;
        line-height: 1.7 !important;
    }

    /* Feature pills */
    .features {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 2.5rem;
    }

    .feature-pill {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        color: #94a3b8;
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: 500;
    }

    /* Download button */
    .stDownloadButton > button {
        background: rgba(255,255,255,0.07) !important;
        color: #a5b4fc !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        margin-top: 1rem !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.9) !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
    }

    [data-testid="stSidebar"] * {
        color: #94a3b8 !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #6366f1 !important;
    }

    /* Warning */
    .stWarning {
        background: rgba(251, 191, 36, 0.1) !important;
        border: 1px solid rgba(251, 191, 36, 0.3) !important;
        border-radius: 10px !important;
        color: #fbbf24 !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🔍 How to use")
    st.markdown("""
1. Find any job on LinkedIn or Indeed
2. Copy the entire job post text
3. Paste it into the box
4. Click **Decode this job**
""")
    st.divider()
    st.markdown("**What you get:**")
    st.markdown("""
- ✅ Plain-English translation
- 🚩 Hidden red flags  
- 💰 Salary estimate
- 🎯 Top 5 skills to highlight
- 🔮 The one-line truth
""")
    st.divider()
    st.markdown("<small style='color:#475569'>Built with Groq + Llama 3<br>Completely free · Open source</small>", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-badge">🤖 Powered by Llama 3 · Completely Free</div>
    <div class="hero-title">Job Description<br>Decoder</div>
    <div class="hero-subtitle">
        Paste any job posting. AI reveals what the company actually wants,
        hidden red flags, salary estimates, and exactly what to say in your application.
    </div>
    <div class="features">
        <span class="feature-pill">🚩 Red Flag Detector</span>
        <span class="feature-pill">💰 Salary Estimator</span>
        <span class="feature-pill">🎯 Skill Matcher</span>
        <span class="feature-pill">🔮 Culture Decoder</span>
        <span class="feature-pill">⚡ 10 Second Analysis</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Input
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<span class="input-label">📋 Paste the full job description here</span>', unsafe_allow_html=True)

job_desc = st.text_area(
    label="job",
    height=250,
    placeholder="Copy the entire job post and paste it here — the more text, the better the analysis...",
    label_visibility="collapsed"
)

decode_btn = st.button("🔍 Decode this job", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Logic
if decode_btn and job_desc.strip():
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are an expert recruiter and career coach with 15 years of experience. A job seeker needs your honest, no-fluff analysis.

Analyze this job description and respond using EXACTLY these 7 sections with these exact headings:

## What they actually want
Translate corporate language into plain English. What are the 3-4 real requirements behind the buzzwords?

## Red flags
List any warning signs hidden in the language. Examples: "fast-paced" = high stress, "wear many hats" = understaffed, "rockstar" = toxic culture. Be direct. If there are none, say so honestly.

## Green flags
Any genuinely positive signals about the role or company culture.

## Realistic salary range
Based on the role, seniority level, and any location hints, give a realistic range. Explain your reasoning in one sentence.

## Culture signals
What does the specific language used tell you about how this company actually operates day-to-day?

## Top 5 skills to highlight
The exact 5 skills or experiences to emphasize in a cover letter and resume for THIS specific role. Be specific, not generic.

## The one-line truth
One brutally honest sentence summarizing this job opportunity.

JOB DESCRIPTION:
{job_desc}
"""

    with st.spinner("Decoding... hang tight ⚡"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )

    result = response.choices[0].message.content

    st.markdown("""
    <div class="results-card">
        <div class="results-header">
            <div class="results-title">📊 Decode Complete</div>
            <div class="results-badge">✓ Analysis ready</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(result)

    st.download_button(
        label="⬇️ Download full analysis as .txt",
        data=result,
        file_name="job_decode.txt",
        mime="text/plain"
    )

elif decode_btn and not job_desc.strip():
    st.warning("⚠️ Please paste a job description first.")