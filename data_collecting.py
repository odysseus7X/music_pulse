import requests
import pandas as pd
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

tracked = pd.read_csv("tracked_songs.csv")

song_ids = tracked["song_id"].tolist()

def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

rows = []

timestamp = datetime.now(timezone.utc).isoformat()

for batch in chunk(song_ids, 50):

    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {"part": "snippet,statistics", "id": ",".join(batch), "key": API_KEY}

    response = requests.get(url, params=params).json()

    for item in response.get("items", []):

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
            "comments": int(stats.get("commentCount", 0))
        })

snapshot = pd.DataFrame(rows)

if os.path.exists("snapshots.csv"):
    old = pd.read_csv("snapshots.csv")
    snapshot = pd.concat([old, snapshot], ignore_index=True)

snapshot.to_csv("snapshots.csv", index=False)
