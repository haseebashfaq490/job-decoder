import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="JobLens AI",
    page_icon="🧿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }
[data-testid="stSidebar"] { display: none; }
[data-testid="collapsedControl"] { display: none; }
.stDeployButton { display: none; }

:root {
    --bg: #080a0f;
    --surface: #0d1117;
    --surface2: #131920;
    --border: rgba(255,255,255,0.07);
    --border-hover: rgba(255,255,255,0.15);
    --gold: #f0a500;
    --gold-dim: rgba(240,165,0,0.15);
    --gold-glow: rgba(240,165,0,0.08);
    --text: #e8eaf0;
    --text-muted: #5a6478;
    --text-mid: #8892a4;
    --green: #10b981;
    --red: #ef4444;
    --blue: #3b82f6;
    --radius: 16px;
}

.stApp {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Noise texture overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

/* Ambient glow */
.stApp::after {
    content: '';
    position: fixed;
    top: -200px;
    left: 50%;
    transform: translateX(-50%);
    width: 800px;
    height: 600px;
    background: radial-gradient(ellipse, rgba(240,165,0,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── TOP NAV ── */
.nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 3rem;
    border-bottom: 1px solid var(--border);
    background: rgba(8,10,15,0.8);
    backdrop-filter: blur(20px);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
}

.nav-logo-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--gold);
    box-shadow: 0 0 12px var(--gold);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 12px var(--gold); }
    50% { opacity: 0.5; box-shadow: 0 0 4px var(--gold); }
}

.nav-pills {
    display: flex;
    gap: 6px;
}

.nav-pill {
    padding: 5px 14px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-muted);
    border: 1px solid var(--border);
    background: transparent;
    letter-spacing: 0.02em;
}

.nav-pill.active {
    color: var(--gold);
    border-color: rgba(240,165,0,0.3);
    background: var(--gold-dim);
}

.nav-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: var(--text-muted);
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
}

/* ── HERO ── */
.hero {
    max-width: 760px;
    margin: 5rem auto 4rem;
    padding: 0 2rem;
    text-align: center;
    position: relative;
    z-index: 1;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    border-radius: 50px;
    border: 1px solid rgba(240,165,0,0.25);
    background: var(--gold-glow);
    font-size: 11px;
    font-weight: 500;
    color: var(--gold);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 4.5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: var(--text);
    margin-bottom: 1.5rem;
}

.hero-title em {
    font-style: normal;
    color: var(--gold);
}

.hero-desc {
    font-size: 1.05rem;
    line-height: 1.7;
    color: var(--text-mid);
    max-width: 540px;
    margin: 0 auto 3rem;
    font-weight: 300;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    margin-bottom: 0;
}

.feature-chip {
    padding: 8px 10px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--surface);
    font-size: 11px;
    color: var(--text-muted);
    text-align: center;
    font-weight: 500;
}

.feature-chip span {
    display: block;
    font-size: 16px;
    margin-bottom: 3px;
}

/* ── MAIN LAYOUT ── */
.main-grid {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 24px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem 4rem;
    position: relative;
    z-index: 1;
}

/* ── INPUT PANEL ── */
.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
}

.panel-header {
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: var(--text);
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.panel-badge {
    font-size: 10px;
    padding: 3px 10px;
    border-radius: 50px;
    background: var(--gold-dim);
    color: var(--gold);
    border: 1px solid rgba(240,165,0,0.2);
    font-weight: 600;
    letter-spacing: 0.06em;
}

.panel-body { padding: 1.5rem; }

/* Text area */
.stTextArea { margin-bottom: 0 !important; }
.stTextArea label { display: none !important; }
.stTextArea textarea {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13.5px !important;
    line-height: 1.7 !important;
    padding: 1rem 1.25rem !important;
    resize: none !important;
    caret-color: var(--gold) !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: rgba(240,165,0,0.4) !important;
    box-shadow: 0 0 0 3px rgba(240,165,0,0.06) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: var(--text-muted) !important; }

/* Button */
.stButton > button {
    width: 100% !important;
    background: var(--gold) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    margin-top: 12px !important;
}
.stButton > button:hover {
    background: #fbb830 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 30px rgba(240,165,0,0.3) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── SIDEBAR PANEL ── */
.info-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    margin-bottom: 16px;
}

.info-card-header {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid var(--border);
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.info-card-body { padding: 1.25rem; }

.step-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 14px;
}

.step-num {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 6px;
    background: var(--gold-dim);
    border: 1px solid rgba(240,165,0,0.2);
    color: var(--gold);
    font-size: 11px;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 1px;
}

.step-text {
    font-size: 13px;
    color: var(--text-mid);
    line-height: 1.5;
}

.output-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    font-size: 12.5px;
    color: var(--text-mid);
}
.output-item:last-child { border-bottom: none; }
.output-icon { font-size: 14px; width: 20px; text-align: center; }

.model-badge {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 14px;
    background: var(--bg);
    border-radius: 10px;
    margin-bottom: 10px;
}
.model-label { font-size: 11px; color: var(--text-muted); }
.model-value { font-size: 12px; color: var(--text); font-weight: 500; font-family: monospace; }

/* ── RESULTS ── */
.results-wrap {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem 4rem;
    position: relative;
    z-index: 1;
}

.results-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
}

.results-panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 1.75rem;
    border-bottom: 1px solid var(--border);
    background: var(--surface2);
}

.results-panel-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 0.02em;
}

.live-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: var(--green);
    border: 1px solid rgba(16,185,129,0.3);
    background: rgba(16,185,129,0.1);
    padding: 4px 12px;
    border-radius: 50px;
    font-weight: 600;
}

.results-body { padding: 2rem 1.75rem; }

/* Result section styling */
.stMarkdown h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--gold) !important;
    margin: 2rem 0 0.75rem !important;
    padding-bottom: 0.6rem !important;
    border-bottom: 1px solid rgba(240,165,0,0.15) !important;
}
.stMarkdown h2:first-child { margin-top: 0 !important; }

.stMarkdown p {
    font-size: 14.5px !important;
    line-height: 1.75 !important;
    color: var(--text-mid) !important;
    margin-bottom: 0.5rem !important;
}

.stMarkdown ul, .stMarkdown ol {
    padding-left: 1.2rem !important;
}

.stMarkdown li {
    font-size: 14px !important;
    line-height: 1.7 !important;
    color: var(--text-mid) !important;
    margin-bottom: 4px !important;
}

.stMarkdown strong {
    color: var(--text) !important;
    font-weight: 600 !important;
}

/* Download button */
.stDownloadButton > button {
    background: var(--surface2) !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-size: 12px !important;
    padding: 8px 18px !important;
    margin-top: 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    border-color: var(--border-hover) !important;
    color: var(--text) !important;
}

/* Spinner */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* Warning */
.stWarning {
    background: rgba(251,191,36,0.08) !important;
    border: 1px solid rgba(251,191,36,0.2) !important;
    border-radius: 10px !important;
    color: #fbbf24 !important;
    font-size: 13px !important;
}

/* Divider */
.section-divider {
    height: 1px;
    background: var(--border);
    margin: 1.5rem 0;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #1e2535; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2a3348; }

@media (max-width: 900px) {
    .main-grid { grid-template-columns: 1fr; }
    .feature-grid { grid-template-columns: repeat(3, 1fr); }
    .nav { padding: 1rem 1.5rem; }
    .nav-pills { display: none; }
    .hero { margin: 3rem auto 2.5rem; }
}
</style>
""", unsafe_allow_html=True)

# ── NAV ──
st.markdown("""
<div class="nav">
    <div class="nav-logo">
        <div class="nav-logo-dot"></div>
        JobLens AI
    </div>
    <div class="nav-pills">
        <div class="nav-pill active">Decoder</div>
        <div class="nav-pill">Resume Match</div>
        <div class="nav-pill">Salary Intel</div>
    </div>
    <div class="nav-status">
        <div class="status-dot"></div>
        All systems live
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered Career Intelligence</div>
    <div class="hero-title">Decode any job post<br>in <em>10 seconds</em></div>
    <div class="hero-desc">
        Paste a job description and get an honest, no-fluff breakdown —
        what they actually want, hidden red flags, salary reality,
        and exactly how to position yourself.
    </div>
    <div class="feature-grid">
        <div class="feature-chip"><span>🚩</span>Red Flags</div>
        <div class="feature-chip"><span>✅</span>Green Flags</div>
        <div class="feature-chip"><span>💰</span>Salary Est.</div>
        <div class="feature-chip"><span>🎯</span>Skill Match</div>
        <div class="feature-chip"><span>🔮</span>Truth Score</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MAIN GRID ──
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

col1, col2 = st.columns([1.6, 1])

with col1:
    st.markdown("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title">Job Description Input</div>
            <div class="panel-badge">PASTE & DECODE</div>
        </div>
        <div class="panel-body">
    """, unsafe_allow_html=True)

    job_desc = st.text_area(
        label="job",
        height=300,
        placeholder="Paste the full job description here — include everything: responsibilities, requirements, about the company, benefits. The more text, the sharper the analysis.",
        label_visibility="collapsed"
    )

    decode_btn = st.button("⚡  Run Deep Analysis", use_container_width=True)

    st.markdown("""
        <p style="font-size:11px; color: #2d3748; text-align:center; margin-top:12px; font-weight:500;">
        Powered by Llama 3.3 70B via Groq · No data stored · 100% free
        </p>
    </div></div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-header">How it works</div>
        <div class="info-card-body">
            <div class="step-item">
                <div class="step-num">1</div>
                <div class="step-text">Find any job on LinkedIn, Indeed, or any job board</div>
            </div>
            <div class="step-item">
                <div class="step-num">2</div>
                <div class="step-text">Copy the entire job post — title, description, requirements, everything</div>
            </div>
            <div class="step-item">
                <div class="step-num">3</div>
                <div class="step-text">Paste it into the box and click Run Deep Analysis</div>
            </div>
            <div class="step-item" style="margin-bottom:0">
                <div class="step-num">4</div>
                <div class="step-text">Get your honest, expert breakdown in ~10 seconds</div>
            </div>
        </div>
    </div>

    <div class="info-card">
        <div class="info-card-header">Analysis output</div>
        <div class="info-card-body">
            <div class="output-item"><span class="output-icon">🎯</span> What they actually want</div>
            <div class="output-item"><span class="output-icon">🚩</span> Hidden red flags</div>
            <div class="output-item"><span class="output-icon">✅</span> Genuine green flags</div>
            <div class="output-item"><span class="output-icon">💰</span> Realistic salary range</div>
            <div class="output-item"><span class="output-icon">🏢</span> Culture signals</div>
            <div class="output-item"><span class="output-icon">⚡</span> Top 5 skills to highlight</div>
            <div class="output-item"><span class="output-icon">🔮</span> The one-line truth</div>
        </div>
    </div>

    <div class="info-card">
        <div class="info-card-header">Model info</div>
        <div class="info-card-body">
            <div class="model-badge">
                <span class="model-label">Model</span>
                <span class="model-value">llama-3.3-70b</span>
            </div>
            <div class="model-badge">
                <span class="model-label">Provider</span>
                <span class="model-value">Groq Cloud</span>
            </div>
            <div class="model-badge" style="margin-bottom:0">
                <span class="model-label">Cost</span>
                <span class="model-value" style="color:#10b981">$0.00</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close main-grid

# ── RESULTS ──
if decode_btn and job_desc.strip():
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are a brutally honest senior recruiter and career strategist with 15 years of experience at top-tier companies. A job seeker is relying on your expertise.

Analyze this job description thoroughly. Be specific, direct, and genuinely useful. No generic advice.

Respond with EXACTLY these 7 sections using these exact markdown headings:

## What they actually want
Cut through the corporate language. What are the 3-4 real, concrete requirements? What kind of person are they picturing?

## Red flags
Identify specific warning signs in the language used. Be direct — "fast-paced environment" often means burnout culture, "self-starter" often means no management support, "competitive salary" with no number often means below market. If there are genuinely no red flags, say so clearly and explain why.

## Green flags
Specific positive signals that suggest this is a healthy role/company. Quote the exact language that gave you this impression.

## Realistic salary range
Give a specific range (e.g. $85k–$105k) based on the role, seniority signals, industry, and any location hints. Explain your reasoning in 1-2 sentences.

## Culture signals
What does the writing style, word choices, and structure of this job post reveal about how this company actually operates? Be insightful.

## Top 5 skills to highlight
List exactly 5 specific skills or experiences to emphasize in your resume and cover letter for THIS role specifically. Not generic skills — tailored to this exact posting.

## The one-line truth
One single sentence that cuts to the heart of this opportunity. Make it memorable and honest.

JOB DESCRIPTION TO ANALYZE:
{job_desc}
"""

    with st.spinner("Running deep analysis..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1800
        )

    result = response.choices[0].message.content

    st.markdown("""
    <div class="results-wrap">
        <div class="results-panel">
            <div class="results-panel-header">
                <div class="results-panel-title">
                    📊 &nbsp;Intelligence Report
                </div>
                <div class="live-badge">
                    <div style="width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981"></div>
                    Analysis complete
                </div>
            </div>
            <div class="results-body">
    """, unsafe_allow_html=True)

    st.markdown(result)

    st.markdown('</div></div></div>', unsafe_allow_html=True)

    st.markdown('<div style="max-width:1200px;margin:0 auto;padding:0 2rem 4rem;">', unsafe_allow_html=True)
    st.download_button(
        label="⬇  Download full report (.txt)",
        data=result,
        file_name="joblens_report.txt",
        mime="text/plain"
    )
    st.markdown('</div>', unsafe_allow_html=True)

elif decode_btn and not job_desc.strip():
    st.markdown('<div style="max-width:1200px;margin:0 auto;padding:0 2rem;">', unsafe_allow_html=True)
    st.warning("Please paste a job description before running the analysis.")
    st.markdown('</div>', unsafe_allow_html=True)