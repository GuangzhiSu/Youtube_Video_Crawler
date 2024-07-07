import yt_dlp
import json
import os

# 加载视频信息
try:
    with open('Youtube_video_Scrape/videos2.json', 'r') as videos_file:
        videos = json.load(videos_file)
        print("Loaded videos.json successfully")
except FileNotFoundError:
    print("videos.json not found")
    exit()

# 确保目标文件夹存在
download_folder = "/home/gs285/videos2"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print(f"Created download folder: {download_folder}")

# cookies 文件路径
cookies_file = 'Youtube_video_Scrape/cookies.txt'
if not os.path.exists(cookies_file):
    print(f"cookies.txt not found at {cookies_file}")
    exit()

print(f"Using cookies file: {cookies_file}")

# 下载视频
for video in videos:
    print(f"Downloading: {video['title']}")
    print(f"URL: {video['url']}")

    try:
        ydl_opts = {
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'cookiefile': cookies_file,
            'verbose': True,  # 增加详细日志
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video['url']])
        
        print(f"Downloaded: {video['title']}\n")
    except Exception as e:
        print(f"Failed to download video: {video['title']}")
        print(f"Error: {e}\n")
