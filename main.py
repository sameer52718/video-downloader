from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes.video_downloader_route import video_downloader_router
from routes.jobs_route import jobs_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()


# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount static files directory for serving static content
app.mount("/videos", StaticFiles(directory="downloads"), name="videos")

# home route
@app.get("/")
async def home():
    return {"message": "Welcome to the FastAPI application!"}

# include the video downloader router
app.include_router(video_downloader_router, prefix="/tools", tags=["tools"])
# include the jobs router
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)