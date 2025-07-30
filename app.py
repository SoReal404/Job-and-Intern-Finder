from scraper import get_all_sources
from matcher import match_internships
import streamlit as st

st.title("🤖 Internship Finder AI")

query = st.text_input("Search keywords", "machine learning intern")
location = st.text_input("Location (optional)", "Remote")
serpapi_key = st.text_input("SerpAPI Key (optional)", type="password")

resume = st.text_area("Paste your resume/skills", height=250)

if st.button("🔍 Search All Sources & Match"):
    if not resume.strip():
        st.warning("Paste your resume to continue.")
    else:
        with st.spinner("Collecting internships..."):
            internships = get_all_sources(query, location, serpapi_key)

        if not internships:
            st.error("No internships found. Try different keywords or check your API key.")
        else:
            with st.spinner("Matching to your profile..."):
                results = match_internships(resume, internships)
                for r in results:
                    st.markdown(f"### {r['Title']} @ {r['Company']}")
                    st.markdown(f"**Score:** {r['Score']}")
                    st.markdown(r["Description"])
                    st.markdown(f"[Apply Here]({r['Link']})")
                    st.markdown("---")
