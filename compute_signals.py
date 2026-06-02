import pandas as pd
from datetime import datetime, timezone

df = pd.read_csv("data/snapshots.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df["published_at"] = pd.to_datetime(df["published_at"], utc=True)

results = []

for song_id, group in df.groupby("song_id"):

    group = group.sort_values("timestamp")

    if len(group) < 2:
        continue

    prev = group.iloc[-2]
    curr = group.iloc[-1]

    hours_elapsed = (curr["timestamp"] - prev["timestamp"]).total_seconds() / 3600

    if hours_elapsed <= 0:
        continue

    delta_views = curr["views"] - prev["views"]
    delta_likes = curr["likes"] - prev["likes"]
    delta_comments = curr["comments"] - prev["comments"]

    view_velocity = delta_views / hours_elapsed

    engagement_rate = (curr["likes"]) / max(curr["views"], 1)

    comment_rate = (curr["comments"]) / max(curr["views"], 1)

    age_days = (datetime.now(timezone.utc) - curr["published_at"]).total_seconds() / (3600 * 24)

    recency_weight = 1 / (age_days + 1)

    results.append({
        "video_id": song_id,
        "title": curr["title"],
        "view_velocity": view_velocity,
        "engagement_rate": engagement_rate,
        "comment_rate": comment_rate,
        "recency_weight": recency_weight
    })

features = pd.DataFrame(results)

feature_cols = ["view_velocity", "engagement_rate", "comment_rate", "recency_weight"]

for col in feature_cols:

    mn = features[col].min()
    mx = features[col].max()

    if mx > mn:
        features[col] = (features[col] - mn) / (mx - mn)
    else:
        features[col] = 0

features["momentum_score"] = (0.40 * features["view_velocity"] +0.30 * features["engagement_rate"] +0.10 * features["comment_rate"] +0.20 * features["recency_weight"])

ranked = features.sort_values("momentum_score", ascending=False)

print("\nTOP 10 SONGS\n")
print(ranked[["title", "momentum_score", "view_velocity", "engagement_rate", "comment_rate", "recency_weight"]].head(10))

ranked.to_csv("momentum_ranking.csv", index=False)