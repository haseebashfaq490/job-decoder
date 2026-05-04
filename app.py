import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="JobLens AI",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }

.stApp {
    background: #080a0f !important;
    font-family: 'DM Sans', sans-serif !important;
}

.block-container {
    padding: 3rem 2rem 4rem !important;
    max-width: 780px !important;
}

[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] * { color: #8892a4 !important; }
[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; font-family: 'Syne', sans-serif !important; }
[data-testid="stSidebar"] strong { color: #f0a500 !important; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.stTextArea textarea {
    background: #0d1117 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
    padding: 1rem 1.2rem !important;
    caret-color: #f0a500 !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: rgba(240,165,0,0.5) !important;
    box-shadow: 0 0 0 3px rgba(240,165,0,0.07) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #2a3040 !important; }
.stTextArea label {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #4a5568 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

.stButton > button {
    width: 100% !important;
    background: #f0a500 !important;
    color: #000 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.8rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    margin-top: 8px !important;
}
.stButton > button:hover {
    background: #ffb820 !important;
    box-shadow: 0 6px 24px rgba(240,165,0,0.3) !important;
    transform: translateY(-1px) !important;
}

.stMarkdown h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #f0a500 !important;
    margin: 2rem 0 0.75rem !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid rgba(240,165,0,0.12) !important;
}
.stMarkdown p {
    font-size: 14.5px !important;
    line-height: 1.75 !important;
    color: #8892a4 !important;
}
.stMarkdown li {
    font-size: 14px !important;
    line-height: 1.7 !important;
    color: #8892a4 !important;
    margin-bottom: 4px !important;
}
.stMarkdown strong { color: #e2e8f0 !important; font-weight: 600 !important; }

hr { border-color: rgba(255,255,255,0.06) !important; margin: 1.5rem 0 !important; }

.stDownloadButton > button {
    background: #0d1117 !important;
    color: #4a5568 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    width: auto !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    color: #e2e8f0 !important;
    border-color: rgba(255,255,255,0.2) !important;
}

.stSpinner > div { border-top-color: #f0a500 !important; }

.stWarning {
    background: rgba(240,165,0,0.08) !important;
    border: 1px solid rgba(240,165,0,0.2) !important;
    border-radius: 10px !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #080a0f; }
::-webkit-scrollbar-thumb { background: #1a2030; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔍 JobLens AI")
    st.markdown("---")
    st.markdown("**How to use**")
    st.markdown("""
1. Find any job on LinkedIn or Indeed
2. Copy the **entire** job post text
3. Paste it into the box
4. Click **Run Deep Analysis**
""")
    st.markdown("---")
    st.markdown("**What you get**")
    st.markdown("""
- 🎯 What they actually want
- 🚩 Hidden red flags
- ✅ Green flags
- 💰 Realistic salary range
- 🏢 Culture signals
- ⚡ Top 5 skills to highlight
- 🔮 The one-line truth
""")
    st.markdown("---")
    st.markdown("""
<div style="font-size:11px; color:#2d3748; line-height:1.6">
Powered by Llama 3.3 70B<br>
via Groq Cloud<br>
100% free · No data stored
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding: 1rem 0 2.5rem;">
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 5px 16px;
        border-radius: 50px;
        border: 1px solid rgba(240,165,0,0.3);
        background: rgba(240,165,0,0.08);
        font-size: 10px;
        font-weight: 600;
        color: #f0a500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    ">
        ✦ AI-Powered Career Intelligence
    </div>
    <div style="
        font-family: 'Syne', sans-serif;
        font-size: clamp(2.4rem, 5vw, 3.4rem);
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -0.03em;
        color: #f0f0f0;
        margin-bottom: 1rem;
    ">
        Decode any job post<br>in <span style="color:#f0a500">10 seconds.</span>
    </div>
    <div style="
        font-size: 1rem;
        line-height: 1.7;
        color: #4a5568;
        font-weight: 300;
        max-width: 500px;
        margin: 0 auto 2rem;
    ">
        Paste a job description and get a brutally honest breakdown —
        what they actually want, hidden red flags, salary reality,
        and exactly how to position yourself.
    </div>
    <div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-bottom:0.5rem;">
        <span style="padding:6px 14px; border-radius:50px; border:1px solid rgba(255,255,255,0.07); background:#0d1117; font-size:11px; color:#4a5568;">🚩 Red Flags</span>
        <span style="padding:6px 14px; border-radius:50px; border:1px solid rgba(255,255,255,0.07); background:#0d1117; font-size:11px; color:#4a5568;">💰 Salary Estimate</span>
        <span style="padding:6px 14px; border-radius:50px; border:1px solid rgba(255,255,255,0.07); background:#0d1117; font-size:11px; color:#4a5568;">🎯 Skill Match</span>
        <span style="padding:6px 14px; border-radius:50px; border:1px solid rgba(255,255,255,0.07); background:#0d1117; font-size:11px; color:#4a5568;">🏢 Culture Decoder</span>
        <span style="padding:6px 14px; border-radius:50px; border:1px solid rgba(255,255,255,0.07); background:#0d1117; font-size:11px; color:#4a5568;">🔮 One-Line Truth</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background:#0d1117;
    border:1px solid rgba(255,255,255,0.07);
    border-radius:16px;
    overflow:hidden;
    margin-bottom:12px;
">
    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
        padding:1rem 1.25rem;
        border-bottom:1px solid rgba(255,255,255,0.06);
    ">
        <span style="font-size:11px; font-weight:700; color:#2d3748; text-transform:uppercase; letter-spacing:0.1em;">
            Job Description Input
        </span>
        <span style="
            font-size:10px; padding:3px 10px; border-radius:50px;
            background:rgba(240,165,0,0.1); color:#f0a500;
            border:1px solid rgba(240,165,0,0.2); font-weight:600; letter-spacing:0.06em;
        ">PASTE &amp; DECODE</span>
    </div>
    <div style="padding:1.25rem 1.25rem 0.5rem;">
""", unsafe_allow_html=True)

job_desc = st.text_area(
    label="Paste the full job description here",
    height=260,
    placeholder="Copy the entire job post — title, responsibilities, requirements, about the company, salary info. The more text, the sharper the analysis.",
    label_visibility="collapsed"
)

decode_btn = st.button("⚡  Run Deep Analysis", use_container_width=True)

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; gap:10px; margin-top:10px; margin-bottom:2rem;">
    <div style="flex:1; background:#0d1117; border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:10px 14px; text-align:center;">
        <div style="font-size:10px; color:#2d3748; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:3px;">Model</div>
        <div style="font-size:12px; color:#e2e8f0; font-family:monospace;">llama-3.3-70b</div>
    </div>
    <div style="flex:1; background:#0d1117; border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:10px 14px; text-align:center;">
        <div style="font-size:10px; color:#2d3748; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:3px;">Provider</div>
        <div style="font-size:12px; color:#e2e8f0; font-family:monospace;">Groq Cloud</div>
    </div>
    <div style="flex:1; background:#0d1117; border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:10px 14px; text-align:center;">
        <div style="font-size:10px; color:#2d3748; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:3px;">Speed</div>
        <div style="font-size:12px; color:#e2e8f0; font-family:monospace;">~10 sec</div>
    </div>
    <div style="flex:1; background:#0d1117; border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:10px 14px; text-align:center;">
        <div style="font-size:10px; color:#2d3748; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:3px;">Cost</div>
        <div style="font-size:12px; color:#10b981; font-family:monospace;">$0.00</div>
    </div>
</div>
""", unsafe_allow_html=True)

if decode_btn and job_desc.strip():
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are a brutally honest senior recruiter and career strategist with 15 years of experience at top-tier companies. A job seeker is relying on your real expertise.

Analyze this job description thoroughly. Be specific, direct, and genuinely useful. No corporate fluff, no generic advice.

Respond with EXACTLY these 7 sections using these exact markdown headings:

## What they actually want
Cut through the corporate language. What are the 3-4 real, concrete requirements? What kind of person are they actually picturing?

## Red flags
Be direct. Identify specific warning signs in the language. E.g. "fast-paced" = burnout risk, "wear many hats" = understaffed, "competitive salary" with no number = below market. If genuinely no red flags, say so and explain why.

## Green flags
Specific positive signals. Quote the exact language that gave you a good impression.

## Realistic salary range
Give a specific dollar range (e.g. $85k-$105k). Base it on role, seniority signals, industry, and location hints. One sentence of reasoning.

## Culture signals
What do the writing style, word choices, and structure of this posting reveal about how this company actually operates day-to-day?

## Top 5 skills to highlight
Exactly 5 specific skills to emphasize in your resume and cover letter for THIS role. Tailored, not generic.

## The one-line truth
One single memorable sentence that captures the honest reality of this opportunity.

JOB DESCRIPTION:
{job_desc}
"""

    with st.spinner("Analyzing... ⚡"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1800
        )

    result = response.choices[0].message.content

    st.markdown("""
    <div style="
        background:#0d1117;
        border:1px solid rgba(255,255,255,0.07);
        border-radius:16px;
        overflow:hidden;
        margin-top:1rem;
    ">
        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding:1rem 1.25rem;
            border-bottom:1px solid rgba(255,255,255,0.06);
            background:#0a0c14;
        ">
            <span style="font-family:'Syne',sans-serif; font-size:14px; font-weight:700; color:#e2e8f0;">
                📊 Intelligence Report
            </span>
            <span style="
                display:flex; align-items:center; gap:6px;
                font-size:10px; color:#10b981;
                border:1px solid rgba(16,185,129,0.3);
                background:rgba(16,185,129,0.08);
                padding:3px 10px; border-radius:50px;
                font-weight:600; letter-spacing:0.06em;
            ">
                <span style="width:5px;height:5px;border-radius:50%;background:#10b981;display:inline-block;"></span>
                COMPLETE
            </span>
        </div>
        <div style="padding:1.75rem 1.5rem;">
    """, unsafe_allow_html=True)

    st.markdown(result)

    st.markdown("</div></div>", unsafe_allow_html=True)

    st.download_button(
        label="⬇  Download full report (.txt)",
        data=result,
        file_name="joblens_report.txt",
        mime="text/plain"
    )

elif decode_btn:
    st.warning("⚠️ Please paste a job description first.")
