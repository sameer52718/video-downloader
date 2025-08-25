from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from careerjet_api_client import CareerjetAPIClient
from dotenv import load_dotenv
import os 

load_dotenv()
AFFILIATE_ID = os.getenv("AFFILIATE_ID")

jobs_router = APIRouter()

# initialize Careerjet API client for Pakistan
cj = CareerjetAPIClient("en_GB")

@jobs_router.get("/")
def get_jobs(
    keywords: str = Query(..., description="Keywords for job search"),
    location: str = Query("Karachi", description="Location for job search"),
    pagesize: int = Query(5, description="Number of results per page"),
    page: int = Query(1, description="Page number for job search results"),
):
    # fetch jobs from Careerjet API
    try:
        result_json = cj.search({
            'location'    : location,
            'keywords'    : keywords,
            'affid'       : AFFILIATE_ID,
            'pagesize'    : pagesize,
            'page'        : page,
            'user_ip'     : '11.22.33.44',
            'url'         : f'https://downloader.informreaders.com/jobs?q={keywords}&l={location}',
            'user_agent'  : 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
        })

        return {
            "page": page,
            "pagesize": pagesize,
            "total_hits": result_json.get("hits"),
            "pages": result_json.get("pages"),
            "jobs": result_json.get("jobs", []),
        }
    except Exception as e:
        return {"error": str(e)}