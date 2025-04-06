# streamlit_app.py
import streamlit as st
from app.analyzer import analyze_resume
from app.resume_parser import extract_text_from_pdf

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("🤖 AI Resume Analyzer")
st.write("Upload your resume and a job description to get insights.")

resume_file = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])
jd_text = st.text_area("🧾 Paste the job description here")

if st.button("🔍 Analyze"):
    if resume_file and jd_text:
        with st.spinner("Analyzing..."):
            resume_text = extract_text_from_pdf(resume_file)
            results = analyze_resume(resume_text, jd_text)

        st.subheader("✅ Match Score:")
        st.success(f"{results['match_score']}%")

        st.subheader("📌 Resume Keywords:")
        st.write(", ".join(results["resume_keywords"]))

        st.subheader("📌 Job Description Keywords:")
        st.write(", ".join(results["jd_keywords"]))

        st.subheader("🚨 Missing Keywords:")
        if results["missing_keywords"]:
            st.warning(", ".join(results["missing_keywords"]))
        else:
            st.success("Great! Your resume covers all major keywords.")
    else:
        st.error("Please upload a resume and paste a job description.")
