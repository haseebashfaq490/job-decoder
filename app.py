import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import PyPDF2 # New import for reading PDFs

load_dotenv()

st.set_page_config(
    page_title="Career AI Toolkit",
    page_icon="🚀",
    layout="centered"
)

# --- ADVANCED CSS STYLING ---
st.markdown("""
<style>
    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Modern Dark Theme Background */
    .stApp {
        background-color: #09090b;
        background-image: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #09090b 70%);
        color: #fafafa;
    }

    /* Adjust main container padding */
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }

    /* Hero Section Styling */
    .hero-container {
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 0.8s ease-out;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        line-height: 1.1;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #e4e4e7;
        max-width: 650px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }
    
    .viral-hook {
        color: #818cf8;
        font-weight: 700;
        font-size: 1.3rem;
        display: block;
        margin-bottom: 0.5rem;
    }

    /* Target Streamlit Tabs */
    button[data-baseweb="tab"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #a1a1aa !important;
        background-color: transparent !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #818cf8 !important;
    }

    /* Target Streamlit's Native Text Area & File Uploader */
    div[data-baseweb="textarea"] > div,
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(9, 9, 11, 0.8) !important;
        border: 1px dashed #3f3f46 !important;
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    div[data-baseweb="textarea"] > div:focus-within,
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
        background-color: rgba(9, 9, 11, 0.95) !important;
    }
    textarea {
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        line-height: 1.6 !important;
    }
    textarea::placeholder {
        color: #a1a1aa !important;
    }

    /* Target Streamlit's Native Primary Button */
    button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39) !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
    }

    /* Output Markdown Styling */
    .stMarkdown h2 {
        color: #e0e7ff !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    .stMarkdown h3 {
        color: #818cf8 !important;
        font-size: 1.1rem !important;
    }
    .stMarkdown p, .stMarkdown li {
        color: #e4e4e7 !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
    }
    
    /* Input Label styling */
    .input-label {
        font-size: 1rem;
        font-weight: 700;
        color: #e4e4e7;
        margin-bottom: 0.5rem;
        display: block;
        letter-spacing: 0.05em;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
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
            <span class="viral-hook">Decode any job description in 10 seconds. ⚡</span>
            Stop guessing. Paste the corporate jargon below and let AI reveal the hidden red flags, the <em>real</em> salary range, and exactly what to say to get hired.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">📋 PASTE JOB DESCRIPTION BELOW</span>', unsafe_allow_html=True)
    job_desc = st.text_area(
        label="job_decode",
        height=280,
        placeholder="e.g. 'We are looking for a rockstar fast-paced developer to wear many hats...'",
        label_visibility="collapsed"
    )

    decode_btn = st.button("🚀 Decode this job now", type="primary", use_container_width=True, key="btn_decode")

    if decode_btn:
        if not job_desc.strip():
            st.error("⚠️ Please paste a job description first.")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error("⚠️ GROQ_API_KEY is not set.")
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
            with st.spinner("Decoding corporate jargon... ⚡"):
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
        <div class="hero-title">Resume Grader</div>
        <div class="hero-subtitle">
            <span class="viral-hook">Beat the ATS. 🎯</span>
            Upload your resume and paste the job description. AI will score your fit and tell you exactly which bullet points to rewrite.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    
    st.markdown('<span class="input-label" style="margin-top: 1rem;">📋 PASTE JOB DESCRIPTION</span>', unsafe_allow_html=True)
    job_target = st.text_area(
        label="job_target",
        height=200,
        placeholder="Paste the target job description here...",
        label_visibility="collapsed"
    )

    grade_btn = st.button("📈 Score my resume", type="primary", use_container_width=True, key="btn_grade")

    if grade_btn:
        if not uploaded_resume or not job_target.strip():
            st.error("⚠️ Please upload a PDF resume AND paste a job description.")
        else:
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_resume)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()

            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error("⚠️ GROQ_API_KEY is not set.")
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
            with st.spinner("Analyzing resume against job requirements... 🕵️‍♂️"):
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