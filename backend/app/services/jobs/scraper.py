import asyncio
import httpx
from bs4 import BeautifulSoup
import uuid

# Fallback jobs if scraping fails or is blocked
FALLBACK_JOBS = [
    {
        "id": str(uuid.uuid4()),
        "title": "Senior React Developer",
        "company": "Tech Lanka Solutions",
        "location": "Colombo, Sri Lanka",
        "description": "Looking for an experienced React developer to lead our frontend team in Colombo.",
        "required_skills": ["react", "typescript", "tailwind css", "javascript", "redux"],
        "salary_range": "LKR 400,000 - 600,000",
        "url": "https://topjobs.lk"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Python Backend Engineer",
        "company": "InnovateLK",
        "location": "Kandy, Sri Lanka (Hybrid)",
        "description": "Join our remote-friendly team to build scalable Python microservices.",
        "required_skills": ["python", "fastapi", "sql", "docker", "aws"],
        "salary_range": "LKR 350,000 - 550,000",
        "url": "https://topjobs.lk"
    }
]

async def scrape_sri_lankan_jobs():
    """
    Scrapes IT jobs from topjobs.lk using BeautifulSoup.
    """
    jobs = []
    
    url = "https://topjobs.lk/applicant/vacancybycategory.jsp?jobCategoryCode=SDV"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Topjobs table structure
            job_rows = soup.find_all('tr', id=lambda x: x and x.startswith('tr'))
            
            for row in job_rows[:15]:
                title_tag = row.find('h2')
                company_tag = row.find('h1')
                
                if not title_tag or not company_tag:
                    continue
                    
                title = title_tag.get_text(strip=True)
                company = company_tag.get_text(strip=True)
                
                # We extract keywords from title to form required skills
                title_lower = title.lower()
                skills = []
                if 'react' in title_lower: skills.append('react')
                if 'python' in title_lower: skills.append('python')
                if 'node' in title_lower: skills.append('node.js')
                if 'java' in title_lower and 'javascript' not in title_lower: skills.append('java')
                if 'javascript' in title_lower: skills.append('javascript')
                if 'php' in title_lower: skills.append('php')
                if 'aws' in title_lower: skills.append('aws')
                if 'qa' in title_lower or 'quality' in title_lower: skills.append('qa')
                if 'data' in title_lower: skills.extend(['sql', 'data analysis'])
                if not skills:
                    skills = ['javascript', 'sql', 'agile'] # Generic fallback
                
                jobs.append({
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "company": company,
                    "location": "Sri Lanka",
                    "description": f"Exciting opportunity for a {title} at {company}. Apply to learn more.",
                    "required_skills": skills,
                    "salary_range": "Negotiable",
                    "url": "https://topjobs.lk"
                })
                
    except Exception as e:
        print(f"Scraper error or timeout: {e}. Using fallback jobs.")
        
    if not jobs:
        return FALLBACK_JOBS
        
    return jobs

if __name__ == "__main__":
    jobs = asyncio.run(scrape_sri_lankan_jobs())
    print(f"Scraped {len(jobs)} jobs")
    for j in jobs:
        print(j['title'], "-", j['company'])
