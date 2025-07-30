import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from typing import List

# ---------- MASTER SCRAPER FUNCTION ----------
def get_all_sources(query="machine learning intern", location="Remote", serpapi_key=None, search_type="Internships") -> List[dict]:
    all_jobs = []

    # Internshala
    try:
        all_jobs += scrape_internshala(query, search_type)
    except Exception as e:
        print("Internshala failed:", e)

    # Google Jobs
    if serpapi_key:
        try:
            all_jobs += scrape_google_jobs(query, location, serpapi_key)
        except Exception as e:
            print("Google Jobs failed:", e)

    # Remotive
    try:
        all_jobs += scrape_remotive(query, search_type)
    except Exception as e:
        print("Remotive failed:", e)

    return all_jobs

# ---------- INTERN SHALA SCRAPER ----------
def scrape_internshala(query="machine learning", search_type="Internships"):
    url = f"https://internshala.com/internships/keywords-{quote(query)}/"
    if search_type == "Jobs":
        # Internshala doesn't post jobs — skip if in job mode
        return []

    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    internships = []
    listings = soup.find_all("div", class_="individual_internship")

    for listing in listings[:10]:
        link_tag = listing.find("a", href=True)
        relative_link = link_tag["href"] if link_tag else ""
        full_link = "https://internshala.com" + relative_link

        title_tag = listing.find("div", class_="heading_4_5")
        title = title_tag.text.strip() if title_tag else "No title"

        company_tag = listing.find("a", class_="link_display_like_text")
        company = company_tag.text.strip() if company_tag else "No company"

        desc = listing.get_text(separator=" ").strip()

        internships.append({
            "title": title,
            "company": company,
            "desc": desc[:400] + "...",
            "link": full_link
        })

    return internships

# ---------- GOOGLE JOBS via SERPAPI ----------
def scrape_google_jobs(query, location, serpapi_key):
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": serpapi_key
    }

    r = requests.get("https://serpapi.com/search", params=params)
    data = r.json()
    jobs = data.get("jobs_results", [])

    internships = []
    for job in jobs:
        internships.append({
            "title": job.get("title", "No title"),
            "company": job.get("company_name", "Unknown company"),
            "desc": job.get("description", "")[:400] + "...",
            "link": job.get("job_google_link", "#")
        })

    return internships

# ---------- REMOTIVE SCRAPER ----------
def scrape_remotive(query="machine learning", search_type="Internships"):
    filter_term = "intern" if search_type == "Internships" else "junior"
    url = f"https://remotive.io/api/remote-jobs?search={quote(query)}"
    jobs = requests.get(url).json().get("jobs", [])

    return [{
        "title": job["title"],
        "company": job["company_name"],
        "desc": job["description"][:400] + "...",
        "link": job["url"]
    } for job in jobs if filter_term in job["title"].lower()]
