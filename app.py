from scraper import get_all_sources
from matcher import match_internships
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Internship Finder AI", layout="wide")
st.title("🎯 Internship Finder AI")
st.markdown("Find the most relevant internships from **multiple sources** using AI and NLP.")

# --- Query Selection ---
predefined_roles = [
    "Machine Learning Intern", "AI Research Intern", "Data Science Intern",
    "Computer Vision Intern", "NLP Intern", "Backend Developer Intern", "Full Stack Intern"
]
query = st.selectbox("🔍 Internship Role", predefined_roles)
custom_query = st.text_input("✏️ Or enter a custom role")
final_query = custom_query if custom_query else query

# --- Location Selection ---
location = st.selectbox("📍 Preferred Location", [
    "Remote", "Egypt", "United States", "Europe", "Canada", "Germany", "India", "Worldwide"
])

# --- SerpAPI Key ---
serpapi_key = st.text_input("🔐 SerpAPI Key (optional, for Google Jobs)", type="password")

# --- Resume Input ---
resume = st.text_area("🧠 Paste your resume, skills, or keywords here:", height=300)

# --- Main Button ---
if st.button("🚀 Search & Match"):
    if not resume.strip():
        st.warning("⚠️ Please paste your resume or skills first.")
    else:
        with st.spinner("🔄 Gathering internships from all sources..."):
            internships = get_all_sources(final_query, location, serpapi_key)

        if not internships:
            st.error("❌ No internships found. Try changing keywords or checking your API key.")
        else:
            with st.spinner("🧠 Matching internships to your resume..."):
                results = match_internships(resume, internships)

            st.success(f"✅ Found {len(results)} matched opportunities!")

            # Display results
            for r in results:
                st.markdown(f"### 🎓 {r['Title']} @ {r['Company']}")
                st.markdown(f"**Match Score:** `{r['Score']}`")
                st.markdown(r["Description"])
                st.markdown(f"[🌐 Apply Here]({r['Link']})", unsafe_allow_html=True)
                st.markdown("---")

            # Save to CSV
            df = pd.DataFrame(results)
            st.download_button(
                "⬇️ Download Results as CSV",
                data=df.to_csv(index=False),
                file_name="matched_internships.csv",
                mime="text/csv"
            )
