import json
import time
import random
from app.utils.config import NEWS_SOURCE_FILE

# Sample news templates to generate dynamic content
TEMPLATES = [
    "Breaking: {topic} market sees a {trend} of {value}% today.",
    "Update: New policies regarding {topic} have been announced.",
    "Live Report: {topic} creates a buzz in the tech world.",
    "Analysis: Why {topic} is the next big thing.",
    "Global News: {topic} impacts international relations."
]

TOPICS = ["AI", "Crypto", "Stock Market", "Climate Change", "Space Exploration"]
TRENDS = ["surge", "drop", "stabilization", "fluctuation"]

def append_news_article(topic=None):
    """
    Simulates a new news article arriving in the stream.
    Appends a line of JSON to the file watched by Pathway.
    """
    if not topic:
        topic = random.choice(TOPICS)
    
    trend = random.choice(TRENDS)
    value = random.randint(1, 100)
    
    headline = random.choice(TEMPLATES).format(topic=topic, trend=trend, value=value)
    article = {
        "text": f"{headline} Details: This is a live report about {topic} showing significant {trend}. Experts suggest monitoring the situation.",
        "timestamp": time.time(),
        "source": "LiveSim"
    }
    
    with open(NEWS_SOURCE_FILE, "a") as f:
        f.write(json.dumps(article) + "\n")
    
    return article

if __name__ == "__main__":
    # Test the appending
    print(f"Appending to {NEWS_SOURCE_FILE}...")
    item = append_news_article()
    print(f"Added: {item}")
