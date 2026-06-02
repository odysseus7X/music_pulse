# Music Pulse – RecoBee ML Intern Assignment

## Platform Chosen

I used the YouTube Data API because it provides publicly available statistics such as views, likes, comments, upload date, and allows tracking videos over time.

The songs were collected from major Indian music channels such as T-Series, Sony Music India, Zee Music Company, and Saregama.

## Approach

The goal was to rank songs based on momentum rather than total popularity.

First, I collected song statistics periodically and stored snapshots over time. Using consecutive snapshots, I calculated signals that capture growth, engagement, and freshness of a song.

## Signals Used

### 1. View Velocity

Calculated using the increase in views between two snapshots.

### 2. Engagement Quality

Measures engagement based on new likes and comments relative to new views.

### 3. Recency

Gives a higher score to newer songs and reduces the impact of old songs.

## Momentum Score

Instead of using only total views, I combined growth, engagement, and recency into a single momentum score.

I normalized all three signals using min-max scaling and then combined them in a simple linear combination.

## Limitations

* the data collection period is limited, longer-term trend may not be captured.
* The momentum formula is heuristic-based and not learned from historical data.

## What I Would Improve With More Time

* Collect data for a longer time period.
* Include more platforms and social signals.
* Experiment with learning the momentum score from historical trends instead of manually defining it.
* Add features such as growth acceleration, etc.

## How to Run

1. Add your YouTube API key to a `.env` file.
2. Run `discover_videos.py` to create the initial list of songs.
3. Run `collect_snapshots.py` periodically to collect statistics.
4. Run `compute_momentum.py` to generate the final ranking.
