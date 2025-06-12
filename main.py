from fastapi import FastAPI
import uvicorn
from routes.video_downloader_route import video_downloader_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files directory for serving static content
app.mount("/videos", StaticFiles(directory="downloads"), name="videos")

# home route
@app.get("/")
async def home():
    return {"message": "Welcome to the FastAPI application!"}

# include the video downloader router
app.include_router(video_downloader_router, prefix="/tools", tags=["tools"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="unix:/root/video-downloader/app.sock", port=0)