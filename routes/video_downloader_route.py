from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from utils.download_video import download_video

video_downloader_router = APIRouter()

# video download route
@video_downloader_router.get("/download_video")
def video_downloader(platform: str = Query(...), video_url: str = Query(...)):
    """
    Download a video from the specified platform using the provided video URL.
    
    Args:
        platform (str): The platform from which to download the video.
        video_url (str): The URL of the video to download.
        
    Returns:
        download video URL or error message.
    """
    
    supported_platforms = ["youtube", "facebook", "instagram", "tiktok"]
    if platform not in supported_platforms:
        return JSONResponse(
            status_code=400,
            content={"error": "Unsupported platform"}
        )
    
    try:
        download_url = download_video(video_url, platform)
        return JSONResponse(content={"video_url": download_url})
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error Aagya while downloading the video: {str(e)}"}
        )