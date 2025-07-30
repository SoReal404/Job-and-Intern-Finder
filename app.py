# app.py
import streamlit as st
import pandas as pd
from scraper import get_all_sources
from matcher import match_internships

st.set_page_config(page_title="Internship Finder AI", layout="wide")
st.title("🌟 Internship Finder AI")
st.markdown("Find the most relevant **internships** from multiple sources using AI and NLP.")

# --- Predefined Roles ---
predefined_roles = [
    "Machine Learning Intern", "AI Research Intern", "Data Science Intern",
    "Computer Vision Intern", "NLP Intern", "Backend Developer Intern", "Full Stack Intern",
    "UI/UX Intern", "Content Writing Intern", "Marketing Intern", "Software Engineer Intern"
]

query = st.selectbox("🔍 Choose an Internship Role", predefined_roles)
custom_query = st.text_input("✏️ Or enter a custom role")
final_query = custom_query if custom_query else query

# --- Location ---
location = st.selectbox("📍 Preferred Location", [
    "Remote", "Egypt", "United States", "Europe", "Canada", "Germany", "India", "Worldwide"
])

# --- SerpAPI Key ---
serpapi_key = st.text_input("🔐 SerpAPI Key (optional - enables Google Jobs scraping)", type="password")

# --- Resume / Skills ---
resume = st.text_area("🧠 Paste your resume, skills, or keywords here:", height=300, placeholder="""
e.g.
Python, SQL, Deep Learning, Problem Solving, Communication, Teamwork, Flask, OpenCV
""")

# --- Search & Match Button ---
if st.button("🚀 Search & Match"):
    if not resume.strip():
        st.warning("⚠️ Please paste your resume or keywords.")
    else:
        with st.spinner("🔎 Scraping internships from all sources..."):
            internships = get_all_sources(final_query, location, serpapi_key)

        if not internships:
            st.error("❌ No internships found. Try a different keyword or check your API key.")
        else:
            with st.spinner("🤖 Matching internships to your profile..."):
                results = match_internships(resume, internships)

            st.success(f"✅ Found {len(results)} matched opportunities!")

            for r in results:
                st.markdown(f"### 🎓 {r['Title']} @ {r['Company']}")
                st.markdown(f"**Match Score:** `{r['Score']}`")
                st.markdown(r["Description"])
                st.markdown(f"[🌐 Apply Here]({r['Link']})", unsafe_allow_html=True)
                st.markdown("---")

            df = pd.DataFrame(results)
            st.download_button(
                label="⬇️ Download Results as CSV",
                data=df.to_csv(index=False),
                file_name="matched_internships.csv",
                mime="text/csv"
            )
