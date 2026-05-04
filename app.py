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

with st.sidebar:
    st.header("How to use")
    st.markdown("""
1. Find any job posting on LinkedIn, Indeed, or any site
2. Copy the entire job post text
3. Paste it into the box
4. Click **Decode this job**

**What you get:**
- Plain-English translation
- Hidden red flags
- Salary estimate
- Exactly what to write in your cover letter
""")
    st.divider()
    st.caption("Built with Groq + Llama 3 · Completely free")

st.title("🔍 Job Description Decoder")
st.markdown("Paste any job posting below. AI reveals what the company actually means, red flags, salary estimates, and exactly what to highlight in your application.")

job_desc = st.text_area(
    "Paste the full job description here",
    height=280,
    placeholder="Copy the entire job post and paste it here..."
)

decode_btn = st.button("Decode this job", use_container_width=False)

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

    with st.spinner("Decoding... this takes about 10 seconds"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )

    result = response.choices[0].message.content

    st.divider()
    st.markdown(result)
    st.divider()

    st.download_button(
        label="Download this decode as .txt",
        data=result,
        file_name="job_decode.txt",
        mime="text/plain"
    )

elif decode_btn and not job_desc.strip():
    st.warning("Please paste a job description first.")