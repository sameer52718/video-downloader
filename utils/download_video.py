import os 
import uuid
import yt_dlp
import ffmpeg
from utils.get_cookies import get_cookie

def download_video(video_url:str, platform:str):


    DOWNLOAD_DIR = "downloads"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    # Base download options
    ydl_opts = {
    'outtmpl': filepath,
    'quiet': True,
    'merge_output_format': 'mp4',
    'format': 'best',
    # 'format': 'bestvideo[vcodec=avc1][height<=720]+bestaudio[acodec^=mp4a]/mp4',
    }

    if platform == "youtube":
        selenium_cookie = get_cookie(video_url)
        
        if selenium_cookie:
            print("Cookies found for YouTube video...")

            yt_dlp_cookies = []
            for cookie in selenium_cookie:
                yt_dlp_cookies.append({
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': cookie['domain'],
                })
            ydl_opts['cookies'] = yt_dlp_cookies
            print("Cookies added to yt-dlp options.")
        

    try:
        # Download file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Special processing for TikTok
        if platform == "tiktok":
            tiktok_filename = f"tiktok_{uuid.uuid4()}.mp4"
            tiktok_file = os.path.join(DOWNLOAD_DIR, tiktok_filename)

            ffmpeg.input(filepath).output(
                tiktok_file, 
                vcodec='libx264', 
                acodec='aac', 
                movflags='+faststart',
                preset='fast'
                ).run(overwrite_output=True)
            
            # Remove original downloaded file after conversion
            os.remove(filepath)

            return f"https://downloader.informreaders.com/videos/{tiktok_filename}"

        return f"https://downloader.informreaders.com/videos/{filename}"
    
    except Exception as e:
        # Cleanup on error
        if os.path.exists(filepath):
            os.remove(filepath)
        raise e