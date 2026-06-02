import pandas as pd
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

timestamp = datetime.now(timezone.utc).isoformat()

#channels ids of t-series, sony music, zee music and saregama
Channel_ids = ["UCq-Fj5jknLsUf-MWSy4_brA", "UC56gTxNs4f9xZ7Pa2i5xNzg", "UCppHT7SZKKvar4Oc9J4oljQ", "UC_A7K2dXFsTMAciGmnNxy-Q",]

song_ids = []

for channel_id in Channel_ids:

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "key": API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "type": "video",
        "maxResults": 10
        }

    response = requests.get(url, params=params).json()

    for item in response["items"]:
        song_ids.append(item["id"]["videoId"])

def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i+size]

rows = []

for batch in chunk(song_ids, 10):

    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "key": API_KEY, "part": "snippet,statistics", "id": ",".join(batch)}

    response = requests.get(url, params=params).json()

    for item in response["items"]:
        stats = item.get("statistics", {})
        snippet = item["snippet"]

        rows.append({
            "timestamp": timestamp,
            "song_id": item["id"],
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "published_at": snippet["publishedAt"],
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0))})

df = pd.DataFrame(rows)

df = df.drop_duplicates(subset=["song_id"])
df.to_csv("tracked_songs.csv", index=False)
