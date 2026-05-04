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

# --- FUTURISTIC NEON CSS STYLING ---
st.markdown("""
<style>
    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Futuristic Dark Theme Background */
    .stApp {
        background-color: #0b0f19;
        background-image: radial-gradient(circle at 50% -20%, #1e293b 0%, #0b0f19 80%);
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
        background-color: rgba(17, 24, 39, 0.7);
        border-radius: 20px;
        padding: 5px;
        border: 1px solid rgba(56, 189, 248, 0.15);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.05);
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
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
        color: #e2e8f0 !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #38bdf8 0%, #8b5cf6 100%) !important;
        color: white !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.4) !important;
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
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        background: linear-gradient(to right, #e0f2fe, #38bdf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(56, 189, 248, 0.2);
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #cbd5e1;
        max-width: 650px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }
    .viral-hook {
        color: #38bdf8;
        font-weight: 800;
        font-size: 1.4rem;
        display: block;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }

    /* ---------------------------------
       INPUT FIELDS & BUTTONS
       --------------------------------- */
    div[data-baseweb="textarea"] > div,
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 16px;
        transition: all 0.3s ease;
        backdrop-filter: blur(12px);
    }
    div[data-baseweb="textarea"] > div:focus-within,
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.3), 0 0 20px rgba(139, 92, 246, 0.15) !important;
        background-color: rgba(15, 23, 42, 0.9) !important;
    }
    textarea {
        color: #f8fafc !important;
        font-size: 1.05rem !important;
        padding: 1.2rem !important;
    }
    textarea::placeholder {
        color: #64748b !important;
    }

    button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1.5rem !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.03em !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
        margin-top: 1rem !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.5) !important;
        background: linear-gradient(135deg, #7dd3fc 0%, #a78bfa 100%) !important;
    }

    /* Output Markdown Styling */
    .stMarkdown h2 {
        color: #bae6fd !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        margin-top: 2rem !important;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2) !important;
        padding-bottom: 0.5rem !important;
    }
    
    .input-label {
        font-size: 0.9rem;
        font-weight: 700;
        color: #94a3b8;
        margin-bottom: 0.5rem;
        display: block;
        letter-spacing: 0.1em;
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
        <div class="hero-title">Decode The Matrix</div>
        <div class="hero-subtitle">
            <span class="viral-hook">Expose any job description in 10 seconds.</span>
            Corporate jargon is designed to hide the truth. Paste the job post below and let autonomous AI extract the real salary, red flags, and exact skills they are actually filtering for.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">Terminal Input // Paste Job Description</span>', unsafe_allow_html=True)
    job_desc = st.text_area(
        label="job_decode",
        height=280,
        placeholder="e.g. 'Looking for a rockstar ninja to wear many hats in a fast-paced environment...'",
        label_visibility="collapsed"
    )

    decode_btn = st.button("Initialize Decode Sequence ⚡", type="primary", use_container_width=True, key="btn_decode")

    if decode_btn:
        if not job_desc.strip():
            st.error("⚠️ Terminal empty: Please paste a job description first.")
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
            with st.spinner("Bypassing corporate jargon... ⚡"):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    st.success("Decode Sequence Complete.")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ==========================================
# TAB 2: RESUME GRADER
# ==========================================
with tab2:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Beat The ATS</div>
        <div class="hero-subtitle">
            <span class="viral-hook">Force multiply your interview rate.</span>
            Upload your resume and the target job description. The algorithm will reverse-engineer the ATS filters and tell you exactly which bullet points are holding you back.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_resume = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
    
    st.markdown('<span class="input-label" style="margin-top: 1rem;">Target Coordinates // Paste Job Description</span>', unsafe_allow_html=True)
    job_target = st.text_area(
        label="job_target",
        height=200,
        placeholder="Paste the target job description here to align the algorithm...",
        label_visibility="collapsed"
    )

    grade_btn = st.button("Execute Resume Analysis 🎯", type="primary", use_container_width=True, key="btn_grade")

    if grade_btn:
        if not uploaded_resume or not job_target.strip():
            st.error("⚠️ Data missing: Please provide both the PDF and the job description.")
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
            with st.spinner("Analyzing parameters against target requirements... 🕵️‍♂️"):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    st.success("Analysis Complete.")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error reading or analyzing: {str(e)}")