from scraper import get_all_sources
from matcher import match_internships
import streamlit as st

st.set_page_config(page_title="Internship Finder AI", layout="wide")
st.title("🎯 Internship Finder AI")

st.markdown("Find the most relevant internships from **multiple sources** using AI.")

query = st.text_input("🔍 Internship Search Keywords", "machine learning intern")
location = st.text_input("📍 Preferred Location", "Remote")
serpapi_key = st.text_input("🔐 SerpAPI Key (optional - for Google Jobs)", type="password")

resume = st.text_area("🧠 Paste your resume, skills, or keywords here:", height=300)

if st.button("🚀 Search & Match"):
    if not resume.strip():
        st.warning("Please paste your resume or skills first.")
    else:
        with st.spinner("🔄 Gathering internships..."):
            internships = get_all_sources(query, location, serpapi_key)

        if not internships:
            st.error("❌ No internships found. Try changing your keyword or checking your API key.")
        else:
            with st.spinner("🧠 Matching internships to your profile..."):
                results = match_internships(resume, internships)

                st.success(f"✅ Found {len(results)} opportunities!")
                for r in results:
                    st.markdown(f"### 🎓 {r['Title']} @ {r['Company']}")
                    st.markdown(f"**Score:** `{r['Score']}`")
                    st.markdown(r["Description"])
                    st.markdown(f"[🌐 Apply Here]({r['Link']})", unsafe_allow_html=True)
                    st.markdown("---")
