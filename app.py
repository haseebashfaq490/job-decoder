import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="JobLens AI",
    page_icon="🧿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stSidebar"], [data-testid="collapsedControl"],
.stDeployButton { visibility: hidden !important; display: none !important; }

:root {
    --bg:      #08090d;
    --card:    #0f1117;
    --card2:   #13161f;
    --border:  rgba(255,255,255,0.07);
    --gold:    #f0a500;
    --gold-bg: rgba(240,165,0,0.10);
    --text:    #e8eaf0;
    --muted:   #4a5568;
    --mid:     #8892a4;
    --green:   #10b981;
    --r:       14px;
}

html, body, .stApp {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

.block-container {
    padding: 2rem 1.5rem 4rem !important;
    max-width: 780px !important;
}

/* ── NAV ── */
.nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 3.5rem;
}
.logo {
    display: flex;
    align-items: center;
    gap: 9px;
    font-family: 'Syne', sans-serif;
    font-size: 17px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.02em;
}
.logo-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--gold);
    box-shadow: 0 0 10px var(--gold);
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink {
    0%,100% { opacity:1; } 50% { opacity:0.4; }
}
.nav-right {
    display: flex; align-items: center; gap: 7px;
    font-size: 11px; color: var(--green);
    font-weight: 500;
}
.live-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
}

/* ── HERO ── */
.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 5px 14px;
    border-radius: 50px;
    border: 1px solid rgba(240,165,0,0.3);
    background: var(--gold-bg);
    font-size: 10px;
    font-weight: 600;
    color: var(--gold);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.headline {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.2rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: var(--text);
    margin-bottom: 1rem;
}
.headline em { font-style:normal; color: var(--gold); }
.subhead {
    font-size: 1rem;
    line-height: 1.7;
    color: var(--mid);
    font-weight: 300;
    margin-bottom: 2.5rem;
    max-width: 520px;
}
.chips {
    display: flex; flex-wrap: wrap; gap: 8px;
    margin-bottom: 2.5rem;
}
.chip {
    padding: 6px 14px;
    border-radius: 50px;
    border: 1px solid var(--border);
    background: var(--card);
    font-size: 11px;
    color: var(--mid);
    font-weight: 500;
}

/* ── INPUT CARD ── */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--r);
    overflow: hidden;
    margin-bottom: 16px;
}
.card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.25rem;
    border-bottom: 1px solid var(--border);
}
.card-title {
    font-size: 11px;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.card-badge {
    font-size: 10px;
    padding: 3px 10px;
    border-radius: 50px;
    background: var(--gold-bg);
    color: var(--gold);
    border: 1px solid rgba(240,165,0,0.25);
    font-weight: 600;
    letter-spacing: 0.06em;
}
.card-body { padding: 1.25rem; }

/* ── TEXTAREA ── */
.stTextArea label { display: none !important; }
.stTextArea textarea {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13.5px !important;
    line-height: 1.7 !important;
    padding: 1rem 1.1rem !important;
    caret-color: var(--gold) !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: rgba(240,165,0,0.5) !important;
    box-shadow: 0 0 0 3px rgba(240,165,0,0.07) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #2d3340 !important; }

/* ── BUTTON ── */
.stButton > button {
    width: 100% !important;
    background: var(--gold) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.8rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    margin-top: 10px !important;
}
.stButton > button:hover {
    background: #ffb820 !important;
    box-shadow: 0 6px 24px rgba(240,165,0,0.35) !important;
    transform: translateY(-1px) !important;
}

/* ── META ROW ── */
.meta-row {
    display: flex;
    gap: 10px;
    margin-top: 14px;
}
.meta-pill {
    flex: 1;
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 14px;
    text-align: center;
}
.meta-label { font-size: 10px; color: var(--muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 3px; }
.meta-value { font-size: 12px; color: var(--text); font-weight: 500; font-family: monospace; }
.meta-value.green { color: var(--green); }

/* ── RESULTS ── */
.result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.25rem;
    border-bottom: 1px solid var(--border);
    background: var(--card2);
}
.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
}
.done-badge {
    display: flex; align-items: center; gap: 6px;
    font-size: 10px; color: var(--green);
    border: 1px solid rgba(16,185,129,0.3);
    background: rgba(16,185,129,0.08);
    padding: 3px 10px; border-radius: 50px;
    font-weight: 600; letter-spacing: 0.06em;
}

.result-body { padding: 1.75rem 1.5rem; }

.stMarkdown h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--gold) !important;
    margin: 2rem 0 0.75rem !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid rgba(240,165,0,0.12) !important;
}
.stMarkdown h2:first-child { margin-top: 0 !important; }
.stMarkdown p {
    font-size: 14px !important;
    line-height: 1.75 !important;
    color: var(--mid) !important;
    margin-bottom: 0.4rem !important;
}
.stMarkdown li {
    font-size: 14px !important;
    line-height: 1.7 !important;
    color: var(--mid) !important;
    margin-bottom: 4px !important;
}
.stMarkdown strong { color: var(--text) !important; font-weight: 600 !important; }

/* ── DOWNLOAD ── */
.stDownloadButton > button {
    background: var(--card2) !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    padding: 7px 16px !important;
    margin-top: 1rem !important;
    width: auto !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    color: var(--text) !important;
    border-color: rgba(255,255,255,0.15) !important;
}

/* ── MISC ── */
.stSpinner > div { border-top-color: var(--gold) !important; }
.stWarning {
    background: rgba(240,165,0,0.08) !important;
    border: 1px solid rgba(240,165,0,0.2) !important;
    border-radius: 10px !important;
    font-size: 13px !important;
}
.divider { height:1px; background: var(--border); margin: 1.5rem 0; }
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #1e2535; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# NAV
st.markdown("""
<div class="nav">
    <div class="logo">
        <div class="logo-dot"></div>
        JobLens AI
    </div>
    <div class="nav-right">
        <div class="live-dot"></div>
        All systems live
    </div>
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="eyebrow">✦ AI-Powered Career Intelligence</div>
<div class="headline">Decode any job post<br>in <em>10 seconds.</em></div>
<div class="subhead">
    Paste a job description and get a brutally honest breakdown —
    what they actually want, hidden red flags, salary reality,
    and exactly how to position yourself to get the interview.
</div>
<div class="chips">
    <span class="chip">🚩 Red Flag Detector</span>
    <span class="chip">💰 Salary Estimator</span>
    <span class="chip">🎯 Skill Matcher</span>
    <span class="chip">🏢 Culture Decoder</span>
    <span class="chip">🔮 One-Line Truth</span>
    <span class="chip">⚡ 10 Second Analysis</span>
</div>
""", unsafe_allow_html=True)

# INPUT CARD
st.markdown("""
<div class="card">
    <div class="card-top">
        <div class="card-title">Job Description Input</div>
        <div class="card-badge">PASTE &amp; DECODE</div>
    </div>
    <div class="card-body">
""", unsafe_allow_html=True)

job_desc = st.text_area(
    label="job",
    height=260,
    placeholder="Paste the full job post here — title, responsibilities, requirements, about the company, everything. More text = sharper analysis.",
    label_visibility="collapsed"
)

decode_btn = st.button("⚡  Run Deep Analysis", use_container_width=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

# META ROW
st.markdown("""
<div class="meta-row">
    <div class="meta-pill">
        <div class="meta-label">Model</div>
        <div class="meta-value">llama-3.3-70b</div>
    </div>
    <div class="meta-pill">
        <div class="meta-label">Provider</div>
        <div class="meta-value">Groq Cloud</div>
    </div>
    <div class="meta-pill">
        <div class="meta-label">Latency</div>
        <div class="meta-value">~10 sec</div>
    </div>
    <div class="meta-pill">
        <div class="meta-label">Cost</div>
        <div class="meta-value green">Free</div>
    </div>
</div>
""", unsafe_allow_html=True)

# LOGIC
if decode_btn and job_desc.strip():
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are a brutally honest senior recruiter and career strategist with 15 years of experience. A job seeker is relying on your real expertise.

Analyze this job description thoroughly. Be specific, direct, and genuinely useful. No corporate fluff, no generic advice.

Respond with EXACTLY these 7 sections using these exact markdown headings:

## What they actually want
Cut through the corporate language. What are the 3-4 real, concrete requirements? What kind of person are they actually picturing?

## Red flags
Be direct. Identify specific warning signs in the language. E.g. "fast-paced" = burnout risk, "wear many hats" = understaffed, "competitive salary" with no number = below market. If genuinely no red flags, say so and explain why.

## Green flags
Specific positive signals. Quote the exact language that gave you a good impression.

## Realistic salary range
Give a specific dollar range (e.g. $85k–$105k). Base it on role, seniority signals, industry, and location hints. One sentence of reasoning.

## Culture signals
What do the writing style, word choices, and structure of this posting reveal about how this company actually operates day-to-day?

## Top 5 skills to highlight
Exactly 5 specific skills to emphasize in your resume and cover letter for THIS role. Tailored — not generic.

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

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="result-header">
            <div class="result-title">📊 Intelligence Report</div>
            <div class="done-badge">
                <div style="width:5px;height:5px;border-radius:50%;background:#10b981"></div>
                COMPLETE
            </div>
        </div>
        <div class="result-body">
    """, unsafe_allow_html=True)

    st.markdown(result)

    st.markdown("</div></div>", unsafe_allow_html=True)

    st.download_button(
        label="⬇  Download report (.txt)",
        data=result,
        file_name="joblens_report.txt",
        mime="text/plain"
    )

elif decode_btn:
    st.warning("Please paste a job description first.")