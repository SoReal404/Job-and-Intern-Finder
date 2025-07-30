from sentence_transformers import SentenceTransformer, util

# Load a lightweight and effective model
model = SentenceTransformer("all-MiniLM-L6-v2")

def match_internships(resume_text, internships, top_k=10):
    # Embed the resume or skills
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    # Embed all internship descriptions
    internship_embeddings = model.encode(
        [intern["desc"] for intern in internships],
        convert_to_tensor=True
    )

    # Compute cosine similarities
    scores = util.pytorch_cos_sim(resume_embedding, internship_embeddings)[0]

    # Add similarity scores to each internship
    results = []
    for i, internship in enumerate(internships):
        results.append({
            "Title": internship["title"],
            "Company": internship["company"],
            "Description": internship["desc"],
            "Link": internship["link"],
            "Score": round(float(scores[i]), 3)
        })

    # Sort by similarity score (descending)
    results = sorted(results, key=lambda x: x["Score"], reverse=True)

    return results[:top_k]
