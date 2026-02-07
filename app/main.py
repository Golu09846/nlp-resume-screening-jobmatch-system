# FILE: app/main.py

# FIX: Add project root to Python path
import sys
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)
sys.path.append(PARENT_DIR)

import streamlit as st
import pandas as pd

# COMPONENTS
from app.components.sidebar import render_sidebar
from app.components.upload_section import render_resume_upload, render_jd_upload
from app.components.result_section import render_results

# SERVICES
from app.services.resume_parser import ResumeParser
from app.services.jd_parser import JDParser
from app.services.embedding_model import EmbeddingModel
from app.services.similarity_engine import SimilarityEngine
from app.services.scoring_engine import ScoringEngine

# DATABASE
from app.utils.database import (
    create_tables,
    save_resume,
    save_jd,
    save_result,
    get_all_resumes,
    get_all_jds,
    get_all_results
)

# SECTION PARSER
from app.utils.section_parser import SectionParser


# --------------------------------------------------------
# STREAMLIT PAGE CONFIG
# --------------------------------------------------------
st.set_page_config(page_title="NLP Resume Screening ATS", layout="wide")

# Google Search Console verification
st.markdown("""
<meta name="google-site-verification" content="nhpR9bCyEPd8pKaJQJmW_uwkFDQEH7VH5Pd8dyxjucA" />
""", unsafe_allow_html=True)


# --------------------------------------------------------
# INIT NLP ENGINES
# --------------------------------------------------------
resume_parser = ResumeParser()
jd_parser = JDParser()
embed_model = EmbeddingModel()
similarity_engine = SimilarityEngine()
scoring_engine = ScoringEngine()


# ================================================================
#                      ADMIN LOGIN BLOCK
# ================================================================
ADMIN_ID = "Abdullah1502"
ADMIN_PASS = "112006"


def admin_login():
    st.subheader("🔐 Admin Login")
    user = st.text_input("Admin ID")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == ADMIN_ID and pwd == ADMIN_PASS:
            st.session_state["is_admin"] = True
            st.success("Admin Logged In")
        else:
            st.error("Invalid credentials")


# ================================================================
#                      ADMIN DASHBOARD
# ================================================================
def admin_dashboard():
    st.title("🔐 Admin Dashboard – Resume ATS")

    menu = st.sidebar.radio(
        "Navigate",
        ["📄 All Resumes", "📝 All Job Descriptions", "📊 Match Results"]
    )

    # -------------------------------------------------------
    # 1) ALL RESUMES
    # -------------------------------------------------------
    if menu == "📄 All Resumes":
        st.header("📄 Uploaded Resumes")

        resumes = get_all_resumes()

        if not resumes:
            st.warning("No resumes found.")
            return

        df = pd.DataFrame(resumes)

        st.dataframe(df[[
            "id", "filename", "name", "email", "phone", "uploaded_at"
        ]])

        selected = st.selectbox("Select resume:", df["filename"].tolist())

        if selected:
            row = next(r for r in resumes if r["filename"] == selected)

            st.subheader(f"📝 Resume: {row['filename']}")

            col1, col2 = st.columns(2)

            with col1:
                st.write("### 👤 User Info")
                st.write("**Name:**", row["name"])
                st.write("**Email:**", row["email"])
                st.write("**Phone:**", row["phone"])
                st.write("### 🧠 Skills")
                st.write(row["skills"])

            with col2:
                st.write("### 🎓 Education")
                st.write(row["education"])
                st.write("### 💼 Experience")
                st.write(row["experience"])
                st.write("### 📌 Projects")
                st.write(row["projects"])

            st.write("### 📜 Cleaned Resume Text")
            st.write(row["clean_text"])

            st.download_button(
                "⬇ Download Resume",
                data=row["filedata"],
                file_name=row["filename"] + ".pdf"
            )

    # -------------------------------------------------------
    # 2) ALL JOB DESCRIPTIONS
    # -------------------------------------------------------
    elif menu == "📝 All Job Descriptions":
        st.header("📝 Uploaded Job Descriptions")

        jds = get_all_jds()

        if not jds:
            st.warning("No job descriptions found.")
            return

        df = pd.DataFrame(jds)
        st.dataframe(df[["id", "role", "skills", "uploaded_at"]])

        jd_selected = st.selectbox("Select JD:", df["id"].tolist())

        if jd_selected:
            row = next(j for j in jds if j["id"] == jd_selected)

            st.subheader("📄 Raw JD")
            st.write(row["raw_jd"])

            st.subheader("🧹 Cleaned JD")
            st.write(row["clean_jd"])

            st.subheader("🧩 Skills")
            st.write(row["skills"])

            st.subheader("👨‍💼 Role")
            st.write(row["role"])

    # -------------------------------------------------------
    # 3) ALL MATCH RESULTS
    # -------------------------------------------------------
    elif menu == "📊 Match Results":
        st.header("📊 Resume–JD Match Results")

        results = get_all_results()

        if not results:
            st.warning("No match results found.")
            return

        df = pd.DataFrame(results)
        st.dataframe(df)

        st.subheader("📈 Final Score Distribution")
        st.bar_chart(df["final_score"])


# ================================================================
#                      USER PANEL (NORMAL USERS)
# ================================================================
def user_panel():

    st.title("📄 NLP Resume Screening & Job Match System")

    create_tables()

    tab1, tab2, tab3 = st.tabs([
        "📤 Upload Resumes",
        "📝 Upload Job Description",
        "📊 Match Results"
    ])

    # -----------------------------------------------
    # TAB 1 → RESUME UPLOAD
    # -----------------------------------------------
    with tab1:
        render_resume_upload()

    # -----------------------------------------------
    # TAB 2 → JD UPLOAD
    # -----------------------------------------------
    with tab2:
        render_jd_upload()

        if "jd_text" in st.session_state:
            try:
                jd_info = jd_parser.process_jd(st.session_state["jd_text"])
                save_jd(
                    raw_jd=st.session_state["jd_text"],
                    clean_jd=jd_info["clean_text"],
                    skills=jd_info["skills"],
                    role=jd_info["role"]
                )
            except:
                pass

    # -----------------------------------------------
    # TAB 3 → MATCH RESULTS
    # -----------------------------------------------
    with tab3:
        if "resume_files" not in st.session_state:
            st.warning("Upload resumes first.")
            return
        if "jd_text" not in st.session_state:
            st.warning("Upload/paste a JD first.")
            return

        resumes = st.session_state["resume_files"]
        jd_raw_text = st.session_state["jd_text"]

        jd_info = jd_parser.process_jd(jd_raw_text)
        jd_clean = jd_info["clean_text"]
        jd_skills = jd_info["skills"]
        jd_emb = embed_model.get_embedding(jd_clean)

        resume_texts = []
        resume_names = []
        resume_skills_list = []

        for file in resumes:
            name = os.path.splitext(file.name)[0]
            resume_names.append(name)

            raw_text, clean_text = resume_parser.get_resume_text(file)
            resume_texts.append(clean_text)

            sections = SectionParser.get_sections(raw_text)

            detected = [s for s in jd_skills if s in clean_text]
            resume_skills_list.append(detected)

            save_resume(
                filename=name,
                filedata=file.read(),
                clean_text=clean_text,
                skills=detected,
                name=sections["name"],
                email=sections["email"],
                phone=sections["phone"],
                education=sections["education"],
                experience=sections["experience"],
                projects=sections["projects"]
            )

        resume_embs = embed_model.get_batch_embeddings(resume_texts)

        final_scores = []
        for emb, skills in zip(resume_embs, resume_skills_list):
            sim = similarity_engine.calculate_similarity(emb, jd_emb)
            score = scoring_engine.calculate_final_score(sim, skills, jd_skills)
            final_scores.append(score)

            save_result(
                resume_id=1,
                jd_id=1,
                semantic_score=sim,
                final_score=score
            )

        render_results(resume_texts, final_scores, jd_clean, resume_names)


# ================================================================
# RUN APP → ADMIN OR USER PANEL
# ================================================================
def main_router():

    render_sidebar()

    st.sidebar.markdown("---")
    choice = st.sidebar.selectbox("Select Mode:", ["User Panel", "Admin Login", "Admin Dashboard"])

    if choice == "User Panel":
        user_panel()

    elif choice == "Admin Login":
        admin_login()

    elif choice == "Admin Dashboard":
        if "is_admin" in st.session_state and st.session_state["is_admin"]:
            admin_dashboard()
        else:
            st.error("❌ Please login as admin first.")


main_router()
