from scraper import scrape_internshala, scrape_google_jobs
from matcher import match_internships
import streamlit as st

st.title("🎯 Internship Finder AI")

option = st.selectbox("Select internship source", ["Internshala", "Google Jobs"])
query = st.text_input("Enter search term (e.g. machine learning)", "machine learning internship")
resume = st.text_area("Paste your resume or keywords here:", height=250)

if st.button("Search & Match"):
    with st.spinner("Fetching internships..."):
        if option == "Internshala":
            raw_jobs = scrape_internshala(query)
        else:
            raw_jobs = scrape_google_jobs(query=query)

        if not raw_jobs:
            st.warning("No internships found.")
        else:
            with st.spinner("Ranking matches..."):
                results = match_internships(resume, raw_jobs)
                for r in results:
                    st.markdown(f"### {r['Title']} @ {r['Company']}")
                    st.markdown(f"**Score:** {r['Score']}")
                    st.markdown(r["Description"])
                    st.markdown(f"[Apply Here]({r['Link']})")
                    st.markdown("---")
