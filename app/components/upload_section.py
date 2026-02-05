# FILE: app/components/upload_section.py

import streamlit as st
from app.utils.file_handler import read_pdf, read_txt

# -------------------------------------------------------
# MULTIPLE RESUME UPLOAD SECTION
# -------------------------------------------------------
def render_resume_upload():
    st.header("📤 Upload Multiple Resumes (PDF/DOCX)")
    st.caption("Upload 5–10 resumes")

    resumes = st.file_uploader(
        "Select resumes (PDF or DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if resumes:
        st.success(f"{len(resumes)} resume(s) uploaded successfully!")
        st.session_state["resume_files"] = resumes


# -------------------------------------------------------
# JOB DESCRIPTION UPLOAD SECTION
# -------------------------------------------------------
def render_jd_upload():
    st.header("📝 Job Description Input")

    method = st.radio(
        "Choose JD Input Method:",
        ["Paste Text", "Upload JD File (PDF/TXT)"]
    )

    # If user pastes text
    if method == "Paste Text":
        jd_text = st.text_area(
            "Paste Job Description here",
            height=260
        )
        if jd_text.strip():
            st.session_state["jd_text"] = jd_text
            st.success("Job Description saved!")

    # If user uploads file
    else:
        jd_file = st.file_uploader("Upload JD File", type=["pdf", "txt"])

        if jd_file:
            fname = jd_file.name.lower()

            # pdf handling
            if fname.endswith(".pdf"):
                extracted = read_pdf(jd_file)
            else:
                extracted = read_txt(jd_file)

            st.text_area("Extracted JD Text:", extracted, height=260)
            st.session_state["jd_text"] = extracted
            st.success("Job Description extracted successfully!")
