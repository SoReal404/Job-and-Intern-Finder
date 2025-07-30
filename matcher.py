from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_internships(resume_text, internships):
    corpus = [resume_text] + [job["desc"] for job in internships]
    vectorizer = TfidfVectorizer(stop_words="english").fit(corpus)
    resume_vec = vectorizer.transform([resume_text])
    job_vecs = vectorizer.transform([job["desc"] for job in internships])

    scores = cosine_similarity(resume_vec, job_vecs).flatten()
    results = []
    for i, job in enumerate(internships):
        job_copy = job.copy()
        job_copy["Score"] = round(float(scores[i]), 3)
        job_copy["Title"] = job.get("title", "No title")
        job_copy["Company"] = job.get("company", "Unknown")
        job_copy["Description"] = job.get("desc", "No description")
        job_copy["Link"] = job.get("link", "#")
        results.append(job_copy)

    return sorted(results, key=lambda x: x["Score"], reverse=True)
