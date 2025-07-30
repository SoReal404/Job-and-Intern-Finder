import streamlit as st
from matcher import match_internships

st.title("🧠 Internship Finder AI")
st.write("Automatically match internships based on your resume and skills.")

# Simulate scraped internships (later from scraper.py)
internships = [
    {
        "title": "AI/ML Intern - Remote",
        "company": "InnovateAI",
        "desc": "Work on computer vision tasks using PyTorch and YOLOv5. Collaborate with team to build and evaluate ML models.",
        "link": "https://example.com/ai-internship"
    },
    {
        "title": "Web Dev Intern",
        "company": "FrontendMasters",
        "desc": "Looking for someone skilled in React, HTML/CSS, and JavaScript. No ML experience needed.",
        "link": "https://example.com/web-dev-internship"
    },
    {
        "title": "Data Science Intern",
        "company": "DeepData",
        "desc": "Build data pipelines with Pandas and Scikit-learn. Involves hyperparameter tuning and model evaluation.",
        "link": "https://example.com/data-science-internship"
    }
]

resume = st.text_area("Paste your resume or skills here:", height=250)

if st.button("Match Internships"):
    if resume.strip() == "":
        st.warning("Please paste your resume to continue.")
    else:
        results = match_internships(resume, internships)
        for r in results:
            st.markdown(f"### {r['Title']} @ {r['Company']}")
            st.markdown(f"**Score:** {r['Score']}")
            st.markdown(f"{r['Description']}")
            st.markdown(f"[Apply Here]({r['Link']})")
            st.markdown("---")
