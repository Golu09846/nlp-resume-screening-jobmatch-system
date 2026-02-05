# FILE: app/components/result_section.py

import streamlit as st

def render_results(resume_texts, final_scores, jd_clean_text, resume_names):
    st.header("📊 Resume–JD Match Results")

    for idx, (res_text, score, name) in enumerate(zip(resume_texts, final_scores, resume_names)):
        st.markdown("---")

        st.subheader(f"📝 Resume: {name}")
        st.success(f"🎯 Match Score: **{score}%**")

        with st.expander("📄 Cleaned Resume Text"):
            st.write(res_text)

        with st.expander("📝 Cleaned Job Description"):
            st.write(jd_clean_text)
