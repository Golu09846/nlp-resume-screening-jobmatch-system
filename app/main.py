# FILE: app/main.py

# FIX: Add root directory for imports
import sys
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)
sys.path.append(PARENT_DIR)

import streamlit as st

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
    save_result
)

# SECTION PARSER
from app.utils.section_parser import SectionParser


st.set_page_config(page_title="NLP Resume Screening System", layout="wide")

# Initialize NLP engines
resume_parser = ResumeParser()
jd_parser = JDParser()
embed_model = EmbeddingModel()
similarity_engine = SimilarityEngine()
scoring_engine = ScoringEngine()


def main():

    # CREATE TABLES ON START
    create_tables()

    render_sidebar()

    st.title("📄 NLP Resume Screening & Job Match System")

    tab1, tab2, tab3 = st.tabs([
        "📤 Upload Resumes",
        "📝 Upload Job Description",
        "📊 Match Results"
    ])

    # ============================================================
    # TAB 1 → Upload Resumes
    # ============================================================
    with tab1:
        render_resume_upload()

    # ============================================================
    # TAB 2 → Upload Job Description
    # ============================================================
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



            except Exception as e:
                st.error(f"JD saving error: {e}")

    # ============================================================
    # TAB 3 → MATCH RESULTS
    # ============================================================
    with tab3:
        st.header("📊 Match Results")

        if "resume_files" not in st.session_state:
            st.warning("⚠ Please upload resumes first.")
            return
        
        if "jd_text" not in st.session_state:
            st.warning("⚠ Please upload or paste a Job Description.")
            return

        resumes = st.session_state["resume_files"]
        jd_raw_text = st.session_state["jd_text"]

        # ---------------------------
        # PROCESS JD
        # ---------------------------
        st.info("Processing Job Description...")

        jd_info = jd_parser.process_jd(jd_raw_text)
        jd_clean_text = jd_info["clean_text"]
        jd_skills = jd_info["skills"]
        jd_emb = embed_model.get_embedding(jd_clean_text)

        # ---------------------------
        # PROCESS MULTIPLE RESUMES
        # ---------------------------
        resume_clean_texts = []
        resume_skills_list = []
        resume_names = []

        st.info("Extracting resume texts & sections...")

        for file in resumes:

            # Resume name without extension
            resume_name = os.path.splitext(file.name)[0]
            resume_names.append(resume_name)

            # Clean resume text
            raw_text, clean_text = resume_parser.get_resume_text(file)
            resume_clean_texts.append(clean_text)

            # Skill match (basic)
            detected_skills = [s for s in jd_skills if s in clean_text]
            resume_skills_list.append(detected_skills)

            # ---------------------------
            # Extract resume SECTIONS (name/email/phone/etc)
            # ---------------------------
            sections = SectionParser.get_sections(raw_text)   # ← RAW TEXT gives correct name/email/phone

            # Extract original file bytes
            file_bytes = file.read()

            # ---------------------------
            # SAVE RESUME INTO DATABASE
            # ---------------------------
            save_resume(
                filename=resume_name,
                filedata=file_bytes,
                clean_text=clean_text,
                skills=detected_skills,

                name=sections["name"],
                email=sections["email"],
                phone=sections["phone"],
                education=sections["education"],
                experience=sections["experience"],
                projects=sections["projects"]
            )

        # ---------------------------
        # BATCH EMBEDDINGS
        # ---------------------------
        st.info("Generating embeddings...")

        resume_embs = embed_model.get_batch_embeddings(resume_clean_texts)

        # ---------------------------
        # CALCULATE SCORES
        # ---------------------------
        st.info("Calculating match scores...")

        final_scores = []

        for resume_emb, skills in zip(resume_embs, resume_skills_list):

            semantic_score = similarity_engine.calculate_similarity(resume_emb, jd_emb)

            final_score = scoring_engine.calculate_final_score(
                semantic_score,
                skills,
                jd_skills
            )

            final_scores.append(final_score)

            save_result(
                resume_id=1,   # placeholder mapping (admin panel upgrade me fix hoga)
                jd_id=1,
                semantic_score=semantic_score,
                final_score=final_score
            )

        st.success("✔ Matching Completed Successfully!")

        render_results(
            resume_clean_texts,
            final_scores,
            jd_clean_text,
            resume_names
        )


if __name__ == "__main__":
    main()
