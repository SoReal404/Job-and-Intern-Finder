# app.py
from scraper import get_all_sources
from matcher import match_internships
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Internship & Job Finder AI", layout="wide")
st.title("🎯 Internship & Job Finder AI")
st.markdown("Find the most relevant **internships** or **jobs** from multiple sources using AI and NLP.")

# --- Search Type ---
search_type = st.radio("🧭 What are you searching for?", ["Internships", "Jobs"])

# --- Predefined Roles ---
predefined_roles = [
    "Machine Learning Intern", "AI Research Intern", "Data Science Intern",
    "Computer Vision Intern", "NLP Intern", "Backend Developer Intern", "Full Stack Intern",
    "UI/UX Designer", "Warehouse Manager", "Content Writer", "Software Engineer", "Data Analyst"
]

query = st.selectbox("🔍 Choose a Role", predefined_roles)
custom_query = st.text_input("✏️ Or enter a custom role")

# Final query
final_query = custom_query if custom_query else query
if search_type == "Jobs":
    final_query = final_query.replace("Intern", "").strip()

# --- Location ---
location = st.selectbox("📍 Preferred Location", [
    "Remote", "Egypt", "United States", "Europe", "Canada", "Germany", "India", "Worldwide"
])

# --- SerpAPI Key ---
serpapi_key = st.text_input("🔐 SerpAPI Key (optional - enables Google Jobs)", type="password")

# --- Resume / Skills ---
resume = st.text_area("🧠 Paste your resume, skills, or keywords here:", height=300, placeholder="""
e.g.
Python, SQL, Deep Learning, Problem Solving, Computer Vision, Flask, FastAPI, Communication, Teamwork
""")

# --- Main Button ---
if st.button("🚀 Search & Match"):
    if not resume.strip():
        st.warning("⚠️ Please paste your resume or skill keywords.")
    else:
        with st.spinner("🔎 Scraping listings from all sources..."):
            results_raw = get_all_sources(final_query, location, serpapi_key, search_type)

        if not results_raw:
            st.error("❌ No results found. Try a different keyword or check your API key.")
        else:
            with st.spinner("🤖 Matching results to your resume..."):
                results = match_internships(resume, results_raw)

            st.success(f"✅ Found {len(results)} matched opportunities!")

            # Display results
            for r in results:
                st.markdown(f"### 💼 {r['Title']} @ {r['Company']}")
                st.markdown(f"**🔢 Match Score:** `{r['Score']}`")
                st.markdown(r["Description"])
                st.markdown(f"[🌐 Apply Here]({r['Link']})", unsafe_allow_html=True)
                st.markdown("---")

            # Download as CSV
            df = pd.DataFrame(results)
            st.download_button(
                label="⬇️ Download Results as CSV",
                data=df.to_csv(index=False),
                file_name="matched_opportunities.csv",
                mime="text/csv"
            )
