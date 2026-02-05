# FILE: app/admin_app.py

import sys
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)
sys.path.append(PARENT_DIR)

import streamlit as st
import pandas as pd

from app.utils.database import (
    get_all_resumes,
    get_all_jds,
    get_all_results,
    create_tables,
)

st.set_page_config(page_title="Admin Dashboard - Resume ATS", layout="wide")


def main():

    st.title("🔐 Admin Dashboard – Resume Screening ATS")
    # CREATE TABLES IF NOT EXIST
    create_tables()
    menu = st.sidebar.radio(
        "Navigate",
        ["📄 All Resumes", "📝 All Job Descriptions", "📊 Match Results"]
    )

    # -------------------------------------------------------
    # 1) SHOW ALL RESUMES
    # -------------------------------------------------------
    if menu == "📄 All Resumes":
        st.header("📄 Uploaded Resumes")

        resumes = get_all_resumes()

        if not resumes:
            st.warning("No resumes found in database.")
            return

        # Convert DB rows → DataFrame
        df = pd.DataFrame(resumes)

        # Show only useful columns
        st.dataframe(df[[
            "id", "filename", "name", "email", "phone", "uploaded_at"
        ]])

        selected = st.selectbox(
            "Select a resume to view details:",
            df["filename"].tolist()
        )

        if selected:
            row = next(r for r in resumes if r["filename"] == selected)

            st.subheader(f"📝 Resume: {row['filename']}")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 👤 Personal Info")
                st.write(f"**Name:** {row['name']}")
                st.write(f"**Email:** {row['email']}")
                st.write(f"**Phone:** {row['phone']}")

                st.markdown("### 🧠 Skills Matched")
                st.write(row["skills"])

            with col2:
                st.markdown("### 🎓 Education")
                st.write(row["education"] or "Not Found")

                st.markdown("### 💼 Experience")
                st.write(row["experience"] or "Not Found")

                st.markdown("### 📌 Projects")
                st.write(row["projects"] or "Not Found")

            st.markdown("### 📜 Cleaned Resume Text")
            st.write(row["clean_text"])

            # ---------------- DOWNLOAD ORIGINAL RESUME ----------------
            st.download_button(
                "⬇ Download Original Resume",
                data=row["filedata"],
                file_name=row["filename"] + ".pdf"
            )

    # -------------------------------------------------------
    # 2) SHOW ALL JDS
    # -------------------------------------------------------
    elif menu == "📝 All Job Descriptions":
        st.header("📝 Uploaded Job Descriptions")

        jds = get_all_jds()

        if not jds:
            st.warning("No job descriptions found.")
            return

        df = pd.DataFrame(jds)

        st.dataframe(df[["id", "role", "skills", "uploaded_at"]])

        jd_selected = st.selectbox("Select JD to view:", df["id"].tolist())

        if jd_selected:
            row = next(j for j in jds if j["id"] == jd_selected)

            st.subheader("📄 Raw JD")
            st.write(row["raw_jd"])

            st.subheader("🧹 Cleaned JD")
            st.write(row["clean_jd"])

            st.subheader("🧩 Extracted Skills")
            st.write(row["skills"])

            st.subheader("👨‍💼 Job Role")
            st.write(row["role"])

    # -------------------------------------------------------
    # 3) MATCH RESULTS
    # -------------------------------------------------------
    elif menu == "📊 Match Results":
        st.header("📊 Resume–JD Match History")

        results = get_all_results()

        if not results:
            st.warning("No match results found.")
            return

        df = pd.DataFrame(results)

        st.dataframe(df)

        st.subheader("📈 Score Distribution")
        st.bar_chart(df["final_score"])


if __name__ == "__main__":
    main()
