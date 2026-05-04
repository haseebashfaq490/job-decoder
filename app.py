import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Job Description Decoder",
    page_icon="🔍",
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
        margin-bottom: 2.5rem;
        animation: fadeIn 0.8s ease-out;
    }

    .hero-title {
        font-size: 3.8rem;
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
        color: #e4e4e7; /* BRIGHTENED from previous muted gray */
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

    /* Feature Pills */
    .pill-container {
        display: flex;
        justify-content: center;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }
    .feature-pill {
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.4);
        color: #c7d2fe; /* Brightened text */
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        backdrop-filter: blur(4px);
    }

    /* Target Streamlit's Native Text Area - FIXED CONTRAST */
    div[data-baseweb="textarea"] > div {
        background-color: rgba(9, 9, 11, 0.8) !important; /* Darker background */
        border: 1px solid #3f3f46 !important; /* Brighter border */
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    div[data-baseweb="textarea"] > div:hover {
        border-color: #52525b !important;
    }
    div[data-baseweb="textarea"] > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
        background-color: rgba(9, 9, 11, 0.95) !important;
    }
    textarea {
        color: #ffffff !important; /* Bright white text when typing */
        font-size: 1rem !important;
        padding: 1rem !important;
        line-height: 1.6 !important;
    }
    textarea::placeholder {
        color: #a1a1aa !important; /* Brightened placeholder text so it's readable */
    }

    /* Target Streamlit's Native Primary Button */
    button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        font-size: 1.2rem !important; /* Made button text slightly larger */
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

    /* Secondary Download Button */
    button[kind="secondary"] {
        background: rgba(39, 39, 42, 0.8) !important;
        border: 1px solid #52525b !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    button[kind="secondary"]:hover {
        border-color: #6366f1 !important;
        background: rgba(63, 63, 70, 1) !important;
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
    .stMarkdown p, .stMarkdown li {
        color: #e4e4e7 !important; /* Brightened output text */
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
    }
    .stMarkdown strong {
        color: #ffffff !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #09090b !important;
        border-right: 1px solid #27272a !important;
    }
    [data-testid="stSidebar"] * {
        color: #e4e4e7 !important; /* Forced all sidebar text to be brighter */
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

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🔍 How to use")
    st.markdown("""
    1. Find any job on LinkedIn or Indeed
    2. Copy the entire job post text
    3. Paste it into the box
    4. Click **Decode this job**
    """)
    st.divider()
    st.markdown("### 🎯 What you get")
    st.markdown("""
    - ✅ Plain-English translation
    - 🚩 Hidden red flags  
    - 💰 Salary estimate
    - 🎯 Top 5 skills to highlight
    - 🔮 The one-line truth
    """)
    st.divider()
    st.markdown("<small style='color:#a1a1aa'>Built with Groq + Llama 3<br>Open source</small>", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Job Description Decoder</div>
    <div class="hero-subtitle">
        <span class="viral-hook">Decode any job description in 10 seconds. ⚡</span>
        Stop guessing. Paste the corporate jargon below and let AI reveal the hidden red flags, the <em>real</em> salary range, and exactly what to say to get hired.
    </div>
    <div class="pill-container">
        <span class="feature-pill">🚩 Red Flag Detector</span>
        <span class="feature-pill">💰 Salary Estimator</span>
        <span class="feature-pill">🎯 Skill Matcher</span>
        <span class="feature-pill">🔮 Culture Translator</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
st.markdown('<span class="input-label">📋 PASTE JOB DESCRIPTION BELOW</span>', unsafe_allow_html=True)

job_desc = st.text_area(
    label="job",
    height=280,
    placeholder="e.g. 'We are looking for a rockstar fast-paced developer to wear many hats...'",
    label_visibility="collapsed"
)

decode_btn = st.button("🚀 Decode this job now", type="primary", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- APP LOGIC ---
if decode_btn:
    if not job_desc.strip():
        st.error("⚠️ Please paste a job description first.")
    else:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            st.error("⚠️ GROQ_API_KEY is not set in the environment variables.")
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
                result = response.choices[0].message.content

                st.success("Analysis Complete!")
                
                with st.container():
                    st.markdown(result)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.download_button(
                    label="⬇️ Download full analysis as .txt",
                    data=result,
                    file_name="job_decode.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"An error occurred while communicating with the AI: {str(e)}")