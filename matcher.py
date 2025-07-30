from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Load transformer model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def match_internships(user_resume, internships):
    profile_emb = model.encode(user_resume, convert_to_tensor=True)
    results = []

    for job in internships:
        job_emb = model.encode(job['desc'], convert_to_tensor=True)
        score = util.cos_sim(profile_emb, job_emb).item()
        results.append({
            "Title": job["title"],
            "Company": job["company"],
            "Description": job["desc"],
            "Score": round(score, 3),
            "Link": job["link"]
        })

    return sorted(results, key=lambda x: x["Score"], reverse=True)
