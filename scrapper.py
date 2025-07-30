import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# ---------- INTERN SHALA SCRAPER ----------
def scrape_internshala(query="machine learning"):
    url = f"https://internshala.com/internships/keywords-{quote(query)}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    internships = []
    listings = soup.find_all("div", class_="individual_internship")

    for listing in listings[:10]:  # Limit to first 10 for now
        title_tag = listing.find("div", class_="heading_4_5")
        company_tag = listing.find("a", class_="link_display_like_text")
        link_tag = listing.find("a", class_="view_detail_button")
        desc = listing.get_text(separator=" ").strip()

        internships.append({
            "title": title_tag.text.strip() if title_tag else "No title",
            "company": company_tag.text.strip() if company_tag else "No company",
            "desc": desc[:400] + "...",
            "link": "https://internshala.com" + link_tag["href"] if link_tag else url
        })
    return internships

# ---------- GOOGLE JOBS via SERPAPI ----------
def scrape_google_jobs(query="machine learning internship", location="Remote"):
    api_key = "a10476cc1cc9c98784152777c77e55c284ff41a566fcb5cc2099aa92ac017571" 
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": api_key
    }
    r = requests.get("https://serpapi.com/search", params=params)
    data = r.json()

    internships = []
    for job in data.get("jobs_results", [])[:10]:
        internships.append({
            "title": job.get("title", ""),
            "company": job.get("company_name", ""),
            "desc": job.get("description", "")[:400] + "...",
            "link": job.get("via", job.get("job_google_link", "#"))
        })

    return internships
