import os
import requests
import json
import time 
import datetime as dt
from zoneinfo import ZoneInfo
from email.utils import parsedate_to_datetime

from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display

# Load environment variables
load_dotenv(override=True)

twitterapi_io_key = os.getenv("TWITTERAPI_IO_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not twitterapi_io_key:
    raise ValueError("Missing 'TWITTERAPI_IO_KEY' in your .env file")

if not openai_api_key:
    raise ValueError("Missing 'OPENAI_API_KEY' in your .env file.")

openai_client = OpenAI()

base_url = "https://api.twitterapi.io"
TZ = ZoneInfo("America/Chicago")

print("Setup Complete.")

# ----------------------------------------------------------------------
# Fetch tweets from twitterapi.io
# Free-tier: 1 request every 5 seconds, includes 429 backoff handling

def fetch_user_last_tweets(username: str, limit: int = 80) -> list[dict]:
    """
    Fetch recent tweets for a username via twitterapi.io
    """

    url = f"{base_url}/twitter/user/last_tweets"
    headers = {'X-API_KEY': twitterapi_io_key}
    params = {'username': username, 'count': limit, 'limit': limit}

    r = requests.get(url, headers=headers, params=params)

    # Retry once if rate-limited
    if r.status_code == 429:
        time.sleep(6)
        r = requests.get(url, headers=headers, params=params, timeout=30)

    if not r.ok:
        raise RuntimeError(f"TwitterAPI error {r.status_code}: {r.text[:800]}")
    
    data = r.json()

    # Handles various response shapes from the API
    tweets = (
        data.get("data", {}).get("tweets")
        or data.get("tweets")
        or data.get("data", {}).get("items")
        or data.get("data")
        or []
    )

    if isinstance(tweets, dict):
        tweets = tweets.get("tweets") or tweets.get("items") or []

    return tweets[:limit]

# ----------------------------- Tweet Parsing Helpers -----------------------------


def _parse_created_at(tweet: dict) -> dt.datetime | None:
    """
    Parse tweet timestamp and convert to local timezone.
    """

    s = tweet.get("CreatedAt") or tweet.get("created_at")

    if not s:
        return None
    
    try:
        return parsedate_to_datetime(s).astimezone(TZ)
    
    except Exception:
        return None
    

def is_retweet(tweet: dict) -> bool:
    return tweet.get("retweeted_tweet") is not None


def tweet_url(tweet: dict) -> str:
    return (tweet.get("url") or tweet.get("twitterUrl") or "").strip()


def split_today_vs_yesterday(tweets: list[dict], include_retweets: bool = True) -> tuple[list[dict], list[dict]]:
    """
    Separate tweets into todays and yesterday's buckets
    """

    now = dt.datetime.now(TZ)
    today, yesterday = now.date(), (now - dt.timedelta(days=1)).date()

    todays, yesterdays = [], []

    for tw in tweets:
        if not include_retweets and is_retweet(tw):
            continue

        t = _parse_created_at(tw)

        if not t:
            continue

        if t.date() == today:
            todays.append(tw)
        elif t.date() == yesterday:
            yesterdays.append(tw)

    sort_key = lambda tw: (_parse_created_at(tw) or dt.datetime.min.replace(tzinfo=TZ)).timestamp()

    return sorted(todays, key=sort_key), sorted(yesterday, key=sort_key)

# --------------------------  Format tweets for LLM Consumption ----------------------------

def format_tweets_for_LLM(tweets: list[dict], max_items: int = 50) -> str:
    """
    Convert tweet list into a compact text format for the LLM
    """

    if not tweets:
        return "(No tweets found.)"
    
    lines = []

    for tw in tweets[:max_items]:
        t = _parse_created_at(tw)
        ts = t.strftime("%Y-%m-%d %H:%M %Z") if t else "UNKNOWN_TIME"
        prefix = "RT: " if is_retweet(tw) else ""
        text = tweet_text(tw)
        url = tweet_url(tw)
        lines.append(f"- [{ts}] {prefix}{text} ({url})".strip())
        
    return "\n".join(lines)


# System Prompt - Defines the AI's role and output format
system_prompt = """
You are an sassy snarky intelligent analyst.
You will be given two sets of tweets from the same account.
(1) today's tweet
(2) yesterday's tweet

Produce a crisp daily brief with these sections:

1) What changed vs yesterday?
2) What's new product /market signal?
3) Anything controversial/risky?
4) Actionable items:
    - Investigate (max 3)
    - Monitor (max 3)
    - Ignore (max 3)

Rules:
- Ground everything in the provided tweets.
- If today's tweets are empty, say so and base "changed vs yesterday" on that
- Output Markdown only (no code block)
""".strip()


# ----------------------------- Core Summarization Function ------------------------------------

def summarize_daily(username: str = "elonmusk", include_retweets: bool = True) -> str:
    """
    Fetch tweets and generate AI-powered daily summary.
    """

    # Step 1: Fetch recent tweets
    raw = fetch_user_last_tweets(username, limit=80)

    # Step 2: Split into today vs yesterday
    todays, yesterdays = split_today_vs_yesterday(raw, include_retweets=include_retweets)

    # Step 3: Format for LLM
    today_block = format_tweets_for_LLM(todays)
    yesterday_block = format_tweets_for_LLM(yesterdays)

    # Step 4: Build user prompt
    user_prompt = f"""
Here are the details of the users twitter account.
Please provide a detailed summary.

Account: @{username}
Timezone: America/Chicago
Include retweets: {include_retweets}

Today's Tweets:
{today_block}

Yesterday's Tweets:
{yesterday_block}
""".strip()
    
    # Step 5: Call OpenAI
    response = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages= [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
    )

    return response.choices[0].message.content

def display_summary(username: str = "elonmusk", include_retweets: bool = True):
    """
    Display the summary as formatted Markdown
    """
    
    md = summarize_daily(username=username, include_retweets= include_retweets)
    display(Markdown(md))

# ------------------------------------------------------

# Run the Daily Summary
# Change username to analyze any Twitter/X account

display_summary("elonmusk", include_retweets= True)