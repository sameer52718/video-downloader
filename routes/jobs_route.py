from fastapi import APIRouter, Query, HTTPException
from careerjet_api_client import CareerjetAPIClient
from dotenv import load_dotenv
import os, hashlib

load_dotenv()
AFFILIATE_ID = os.getenv("AFFILIATE_ID")

jobs_router = APIRouter()
cj = CareerjetAPIClient("en_GB")

# In-memory cache for jobs
JOB_CACHE = {}

def generate_job_id(job_url: str) -> str:
    """Generate a short unique ID from job URL."""
    return hashlib.sha256(job_url.encode()).hexdigest()[:12]


@jobs_router.get("/")
def get_jobs(
    keywords: str = Query(..., description="Keywords for job search"),
    location: str = Query("Karachi", description="Location for job search"),
    pagesize: int = Query(5, description="Number of results per page"),
    page: int = Query(1, description="Page number for job search results"),
):
    try:
        result_json = cj.search({
            "location": location,
            "keywords": keywords,
            "affid": AFFILIATE_ID,
            "pagesize": pagesize,
            "page": page,
            "user_ip": "11.22.33.44",
            "url": f"https://downloader.informreaders.com/jobs?q={keywords}&l={location}",
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0"
        })

        jobs = []
        for job in result_json.get("jobs", []):
            job_id = generate_job_id(job["url"])
            job_with_id = {**job, "job_id": job_id}
            JOB_CACHE[job_id] = job_with_id  # store in cache
            jobs.append(job_with_id)

        return {
            "page": page,
            "pagesize": pagesize,
            "total_hits": result_json.get("hits"),
            "pages": result_json.get("pages"),
            "jobs": jobs,
        }

    except Exception as e:
        return {"error": str(e)}


@jobs_router.get("/info/{job_id}")
def get_job_info(job_id: str):
    """
    Returns the full job object based on the job_id generated in the search results.
    """
    job = JOB_CACHE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or expired from cache.")
    return job
