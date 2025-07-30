import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# ---------- INTERN SHALA SCRAPER ----------
from typing import List

def get_all_sources(query="machine learning intern", location="Remote", serpapi_key=None) -> List[dict]:
    all_jobs = []

    # Internshala
    try:
        all_jobs += scrape_internshala(query)
    except Exception as e:
        print("Internshala error:", e)

    # Google Jobs via SerpAPI
    if serpapi_key:
        try:
            all_jobs += scrape_google_jobs(query, location, serpapi_key)
        except Exception as e:
            print("Google Jobs error:", e)

    return all_jobs

def scrape_internshala(query="machine learning"):
    url = f"https://internshala.com/internships/keywords-{quote(query)}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    internships = []

    listings = soup.find_all("div", class_="individual_internship")

    for listing in listings[:10]:
        # Find actual link to the internship
        link_tag = listing.find("a", href=True)
        relative_link = link_tag["href"] if link_tag else None
        full_link = "https://internshala.com" + relative_link if relative_link else url

        # Extract title and company cleanly
        title_tag = listing.find("div", class_="heading_4_5")
        company_tag = listing.find("a", class_="link_display_like_text")

        # Description as backup info
        desc = listing.get_text(separator=" ").strip()

        internships.append({
            "title": title_tag.text.strip() if title_tag else "No title",
            "company": company_tag.text.strip() if company_tag else "No company",
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


