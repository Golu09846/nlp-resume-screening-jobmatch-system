# FILE: app/components/sidebar.py

import streamlit as st

def render_sidebar():
    st.sidebar.title("⚙️ Controls")

    st.sidebar.markdown(
        """
        ### 📌 Instructions
        - Upload multiple resumes  
        - Upload/Paste Job Description  
        - Go to *Match Results* tab  
        - Get your ATS score instantly  
        """
    )

    st.sidebar.markdown("---")
    st.sidebar.info("Built with NLP + SBERT + ATS Scoring")
