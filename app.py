import streamlit as st
import json
import pandas as pd
from resume_parser import extract_text_from_pdf, clean_text
from scorer import calculate_score

st.set_page_config(
    page_title="AI Resume Shortlisting System",
    layout="wide"
)

st.markdown("""
<style>
div[data-testid="stSelectbox"] * {
    cursor: pointer !important;
}
</style>
""", unsafe_allow_html=True)

st.title("AI-Based Resume Shortlisting System")

with open("role_templates.json", "r") as f:
    JOB_TEMPLATES = json.load(f)

job_role = st.selectbox(
    "Select Job Role",
    options=list(JOB_TEMPLATES.keys())
)

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Analyze & Shortlist"):

    if not uploaded_files:
        st.warning("⚠️ Please upload at least one resume to analyze.")
        st.stop()

    results = []

    for file in uploaded_files:
        try:
            text = extract_text_from_pdf(file)
            text = clean_text(text)

            score = calculate_score(
                resume_text=text,
                job_role=job_role,
                job_templates=JOB_TEMPLATES
            )

            results.append({
                "Resume": file.name,
                "Score": int(round(score))
            })

        except Exception as e:
            st.error(f"❌ Error processing {file.name}: {e}")

    if not results:
        st.warning("⚠️ No valid resume data available for ranking.")
        st.stop()

    df = pd.DataFrame(results)
    df = df.sort_values(by="Score", ascending=False).reset_index(drop=True)

    df.insert(0, "Rank", df.index + 1)

    df["Rank"] = df["Rank"].astype(str)
    df["Score"] = df["Score"].astype(str)

    st.subheader("📊 Shortlisted Resumes (High → Low)")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Results",
        data=csv,
        file_name="shortlisted_resumes.csv",
        mime="text/csv"
    )
