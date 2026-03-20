import requests
from bs4 import BeautifulSoup
import feedparser
import json

def fetch_google_news(query):
    """Fetches news from Google News RSS feed for a specific query."""
    encoded_query = requests.utils.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    results = []
    for entry in feed.entries[:10]:
        results.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "source": "Google News"
        })
    return results

def fetch_major_portals():
    """Fetches headlines from major Indian portals (simplified for stability)."""
    # Using RSS feeds where possible for reliability
    feeds = {
        "TOI": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
        "NDTV": "http://feeds.feedburner.com/ndtvnews-top-stories",
        "Indian Express": "https://indianexpress.com/section/india/feed/"
    }
    
    results = []
    for name, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                results.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": name
                })
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    return results

def fetch_reddit_india():
    """Fetches hot posts from r/india (simplified)."""
    # Note: For production, use PRAW with valid credentials.
    # For now, we simulate or use a public JSON endpoint if available.
    # Reddit often blocks simple requests, so PRAW is recommended.
    # Mocking for implementation structure.
    return [
        {"title": "[Serious] What are the biggest problems you face daily in India?", "source": "Reddit r/india"},
        {"title": "Unemployment among engineers in 2024", "source": "Reddit r/india"}
    ]

def scan_all():
    print("Starting Scan...")
    queries = [
        "India news today problems issues",
        "India common man problems 2024",
        "Delhi Mumbai Bangalore Chennai Kolkata issues today"
    ]
    
    all_data = []
    for q in queries:
        all_data.extend(fetch_google_news(q))
    
    all_data.extend(fetch_major_portals())
    # all_data.extend(fetch_reddit_india()) # Add when PRAW configured
    
    return all_data

if __name__ == "__main__":
    data = scan_all()
    print(f"Scanned {len(data)} items.")
    for d in data[:5]:
        print(f"- {d['title']} ({d['source']})")
