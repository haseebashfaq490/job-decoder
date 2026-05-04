import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import PyPDF2

load_dotenv()

st.set_page_config(
    page_title="Career AI Toolkit",
    page_icon="🚀",
    layout="centered"
)

# --- PREMIUM MODERN CSS STYLING ---
st.markdown("""
<style>
    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Professional Dark Theme Background */
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(circle at 50% -20%, #1e293b 0%, #0f172a 80%);
        color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }

    /* ---------------------------------
       MODERN GLOWING TABS
       --------------------------------- */
    div[data-baseweb="tab_list"] {
        background-color: rgba(30, 41, 59, 0.8);
        border-radius: 20px;
        padding: 5px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        display: flex;
        justify-content: center;
        margin-bottom: 2.5rem;
    }
    button[data-baseweb="tab"] {
        border-radius: 15px !important;
        padding: 12px 24px !important;
        margin: 0 4px !important;
        background-color: transparent !important;
        color: #94a3b8 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #f1f5f9 !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    }

    /* ---------------------------------
       HERO SECTION & TYPOGRAPHY
       --------------------------------- */
    .hero-container {
        text-align: center;
        margin-bottom: 2.5rem;
        animation: fadeIn 0.8s ease-out;
    }
    .hero-title {
        font-size: 3.8rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        background: linear-gradient(to right, #ffffff, #e0f2fe, #bae6fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #cbd5e1;
        max-width: 650px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }
    .viral-hook {
        color: #38bdf8;
        font-weight: 800;
        font-size: 1.35rem;
        display: block;
        margin-bottom: 0.5rem;
        letter-spacing: 0.01em;
    }

    /* ---------------------------------
       INPUT FIELDS & HIGH CONTRAST
       --------------------------------- */
    div[data-baseweb="textarea"] > div {
        background-color: #1e293b !important; 
        border: 2px solid #334155 !important;
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    div[data-baseweb="textarea"] > div:focus-within {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.15) !important;
        background-color: #0f172a !important;
    }
    textarea {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        padding: 1.2rem !important;
    }
    textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    /* --- AGGRESSIVE FILE UPLOADER FIX --- */
    /* Target the main dropzone container */
    [data-testid="stFileUploader"] > section {
        background-color: #1e293b !important;
        border: 2px dashed #475569 !important;
        border-radius: 16px !important;
    }
    /* Force all text inside the uploader to be bright */
    [data-testid="stFileUploader"] div, 
    [data-testid="stFileUploader"] span, 
    [data-testid="stFileUploader"] small {
        color: #e2e8f0 !important;
    }
    /* Target the exact 'Browse files' button Streamlit generates */
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
    }
    [data-testid="stFileUploader"] button:hover {
        border-color: #0ea5e9 !important;
        color: #0ea5e9 !important;
    }

    /* ---------------------------------
       BUTTONS
       --------------------------------- */
    button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        margin-top: 1rem !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4) !important;
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
    }

    /* Output Markdown Styling */
    .stMarkdown h2 {
        color: #bae6fd !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2) !important;
        padding-bottom: 0.5rem !important;
    }
    
    .input-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
        display: block;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- APP LAYOUT (TABS) ---
tab1, tab2 = st.tabs(["🔍 Job Decoder", "📄 Resume Grader"])

# ==========================================
# TAB 1: JOB DECODER
# ==========================================
with tab1:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Job Description Decoder</div>
        <div class="hero-subtitle">
            <span class="viral-hook">Cut through corporate jargon in 10 seconds. ⚡</span>
            Stop guessing what hiring managers want. Paste the job post below and let AI reveal the hidden red flags, the true salary range, and the exact skills they are filtering for.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">📋 PASTE THE FULL JOB DESCRIPTION BELOW</span>', unsafe_allow_html=True)
    job_desc = st.text_area(
        label="job_decode",
        height=280,
        placeholder="e.g. 'We are looking for a rockstar to wear many hats in a fast-paced environment...'",
        label_visibility="collapsed"
    )

    decode_btn = st.button("Decode this job now 🚀", type="primary", use_container_width=True, key="btn_decode")

    if decode_btn:
        if not job_desc.strip():
            st.error("⚠️ Please paste a job description first.")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error("⚠️ System Error: GROQ_API_KEY is not set.")
                st.stop()
                
            client = Groq(api_key=api_key)
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
            with st.spinner("Analyzing corporate jargon... ⚡"):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    st.success("Analysis Complete!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ==========================================
# TAB 2: RESUME GRADER
# ==========================================
with tab2:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Smart Resume Matcher</div>
        <div class="hero-subtitle">
            <span class="viral-hook">See your resume through the eyes of the ATS. 🎯</span>
            Upload your resume and the target job description. The algorithm will score your fit and tell you exactly which bullet points to rewrite to land the interview.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">📄 UPLOAD YOUR RESUME (PDF)</span>', unsafe_allow_html=True)
    uploaded_resume = st.file_uploader("resume_uploader", type=["pdf"], label_visibility="collapsed")
    
    st.markdown('<span class="input-label" style="margin-top: 1rem;">🎯 PASTE THE TARGET JOB DESCRIPTION</span>', unsafe_allow_html=True)
    job_target = st.text_area(
        label="job_target",
        height=200,
        placeholder="Paste the target job description here to check your match score...",
        label_visibility="collapsed"
    )

    grade_btn = st.button("Score my resume fit 📊", type="primary", use_container_width=True, key="btn_grade")

    if grade_btn:
        if not uploaded_resume or not job_target.strip():
            st.error("⚠️ Please provide both your PDF resume and the job description.")
        else:
            pdf_reader = PyPDF2.PdfReader(uploaded_resume)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()

            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error("⚠️ System Error: GROQ_API_KEY is not set.")
                st.stop()
                
            client = Groq(api_key=api_key)
            prompt = f"""You are an elite Technical Recruiter and ATS (Applicant Tracking System) algorithm. 
I am going to provide you with my RESUME and a JOB DESCRIPTION.

Please grade my resume out of 100 based on how well it fits this job description. 
Use EXACTLY the following structure and headings:

## Overall Match Score: [Insert Score]/100
Give a brief 2-sentence verdict on my chances of getting an interview.

## 📊 Dimension Breakdowns
Score each out of 100 and provide a one-sentence justification.
* **Keyword Match:** [Score]/100 - [Justification]
* **Experience Relevance:** [Score]/100 - [Justification]
* **Impact & Metrics:** [Score]/100 - [Justification]
* **ATS Friendliness:** [Score]/100 - [Justification]

## 🔴 Critical Gaps
What are the top 2-3 things missing from my resume that this job description explicitly asks for?

## ✍️ Bullet Point Rewrites
Identify 2 weak bullet points from my resume and rewrite them to be stronger, more metric-driven, and better aligned with the job description. Format as:
* **Original:** [Quote my bullet]
* **Upgraded:** [Your improved rewrite]

---
JOB DESCRIPTION:
{job_target}

RESUME TEXT:
{resume_text}
"""
            with st.spinner("Scoring resume against job requirements... 🕵️‍♂️"):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    st.success("Scoring Complete!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error reading or analyzing: {str(e)}")