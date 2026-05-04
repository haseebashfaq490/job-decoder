import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Job Description Decoder",
    page_icon="🔍",
    layout="centered" # Centered looks more like a polished web app tool
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
        padding-top: 3rem;
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
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #a1a1aa;
        max-width: 600px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.5;
    }

    /* Feature Pills */
    .pill-container {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }
    .feature-pill {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        color: #818cf8;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.02em;
        backdrop-filter: blur(4px);
    }

    /* Target Streamlit's Native Text Area */
    div[data-baseweb="textarea"] > div {
        background-color: rgba(24, 24, 27, 0.6) !important;
        border: 1px solid #27272a !important;
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    div[data-baseweb="textarea"] > div:hover {
        border-color: #3f3f46 !important;
    }
    div[data-baseweb="textarea"] > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
        background-color: rgba(24, 24, 27, 0.9) !important;
    }
    textarea {
        color: #f4f4f5 !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        line-height: 1.6 !important;
    }
    textarea::placeholder {
        color: #52525b !important;
    }

    /* Target Streamlit's Native Primary Button */
    button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
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
        background: rgba(39, 39, 42, 0.5) !important;
        border: 1px solid #3f3f46 !important;
        color: #e4e4e7 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    button[kind="secondary"]:hover {
        border-color: #6366f1 !important;
        color: white !important;
    }

    /* Output Markdown Styling */
    .stMarkdown h2 {
        color: #e0e7ff !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    .stMarkdown p, .stMarkdown li {
        color: #a1a1aa !important;
        font-size: 1rem !important;
        line-height: 1.7 !important;
    }
    .stMarkdown strong {
        color: #f4f4f5 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #09090b !important;
        border-right: 1px solid #27272a !important;
    }
    
    /* Input Label styling */
    .input-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #a1a1aa;
        margin-bottom: 0.5rem;
        display: block;
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
    st.markdown("<small style='color:#52525b'>Built with Groq + Llama 3<br>Open source</small>", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Job Description Decoder</div>
    <div class="hero-subtitle">
        Paste any job posting. AI reveals what the company actually wants, hidden red flags, salary estimates, and exactly what to say in your application.
    </div>
    <div class="pill-container">
        <span class="feature-pill">🚩 Red Flag Detector</span>
        <span class="feature-pill">💰 Salary Estimator</span>
        <span class="feature-pill">🎯 Skill Matcher</span>
        <span class="feature-pill">⚡ 10 Second Analysis</span>
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

# Note the `type="primary"` flag which hooks into our custom CSS
decode_btn = st.button("🔍 Decode this job", type="primary", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True) # Spacer

# --- APP LOGIC ---
if decode_btn:
    if not job_desc.strip():
        st.error("⚠️ Please paste a job description first.")
    else:
        # Groq Client Initialization
        # Note: Added error handling for missing API keys which is a best practice
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

                # Results Presentation
                st.success("Analysis Complete!")
                
                # We wrap the results in an expander or just a nice container
                with st.container():
                    st.markdown(result)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Download button defaults to secondary styling in our CSS
                st.download_button(
                    label="⬇️ Download full analysis as .txt",
                    data=result,
                    file_name="job_decode.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"An error occurred while communicating with the AI: {str(e)}")