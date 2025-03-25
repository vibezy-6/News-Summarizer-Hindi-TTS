import requests
import re
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
from urllib.parse import urlparse
from collections import Counter
import nltk

nltk.download("vader_lexicon")
nltk.download("punkt")

from nltk.tokenize import sent_tokenize

HEADERS = {"User-Agent": "Mozilla/5.0"}
BING_SEARCH_URL = "https://www.bing.com/search?q={query}"
BING_NEWS_URL = "https://www.bing.com/news/search?q={query}"
sia = SentimentIntensityAnalyzer()


def is_company_name(query):
    """Verify if input is a company by checking Bing Search results for financial sources."""
    search_url = f"https://www.bing.com/search?q={query} stock site:investing.com OR site:marketwatch.com OR site:reuters.com"
    response = requests.get(search_url, headers=HEADERS)
    if response.status_code != 200:
        return False
    soup = BeautifulSoup(response.text, "html.parser")
    return any(
        "investing.com" in link["href"]
        or "marketwatch.com" in link["href"]
        or "reuters.com" in link["href"]
        for link in soup.find_all("a", href=True)
    )


def fetch_news_links(query):
    search_url = BING_NEWS_URL.format(query=query)
    response = requests.get(search_url, headers=HEADERS)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True) if "http" in a["href"]]
    return list(set(links))


def extract_summary(url, company_name):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        full_text = " ".join(p.get_text().strip() for p in paragraphs if len(p.get_text().split()) > 10)
        if not full_text or company_name.lower() not in full_text.lower():
            return None  # Reject if company name not in summary
        sentences = re.split(r'(?<=[.!?])\s+', full_text)
        summary = ""
        word_count = 0
        for sentence in sentences:
            words = sentence.split()
            if word_count + len(words) > 75:
                break
            summary += sentence + " "
            word_count += len(words)
        return summary.strip()
    except:
        return None


def analyze_sentiment(text):
    score = sia.polarity_scores(text)["compound"]
    return "Positive" if score >= 0.05 else "Negative" if score <= -0.05 else "Neutral"


def extract_topics(text):
    words = [word.lower() for word in text.split() if len(word) > 3]
    return list(set(words))[:5]


def comparative_analysis(summaries, company_name):
    sentiments = [s['sentiment'] for s in summaries]
    sentiment_counts = Counter(sentiments)
    all_topics = [topic for s in summaries for topic in s['topics']]
    topic_counts = Counter(all_topics).most_common(5)
    sources = [s["source"] for s in summaries]
    domains = [urlparse(link).netloc for link in sources]
    domain_counts = Counter(domains).most_common(3)
    most_negative_article = next((s for s in summaries if s['sentiment'] == "Negative"), None)
    full_text = " ".join(s["summary"] for s in summaries if company_name.lower() in s["summary"].lower())
    sentences = re.split(r'(?<=[.!?])\s+', full_text)
    limited_summary = " ".join(sentences[:5]) if sentences else full_text
    if not limited_summary.endswith(('.', '!', '?')):
        limited_summary += "."
    analysis = {
        "sentiment_distribution": dict(sentiment_counts),
        "top_topics": [t[0] for t in topic_counts],
        "top_sources": [d[0] for d in domain_counts],
        "overall_summary": limited_summary,
    }
    if most_negative_article:
        analysis["example_negative_summary"] = most_negative_article["summary"]
    return analysis


def get_summarized_news(query):
    if not is_company_name(query):
        return {"error": "❌ This might not be a valid company name."}

    summaries = []
    checked_links = set()
    max_rounds = 7
    round_counter = 0

    search_variants = [
        f"{query} news",
        f"{query} latest updates",
        f"{query} recent headlines",
        f"{query} industry news",
        f"{query} company updates"
    ]

    while len(summaries) < 10 and round_counter < max_rounds:
        search_query = search_variants[round_counter % len(search_variants)]
        links = fetch_news_links(search_query)
        round_counter += 1

        for link in links:
            if link in checked_links:
                continue
            checked_links.add(link)

            summary = extract_summary(link, query)
            if summary:
                summaries.append({
                    "summary": summary,
                    "sentiment": analyze_sentiment(summary),
                    "topics": extract_topics(summary),
                    "source": link,
                })

            if len(summaries) >= 10:
                break

    if len(summaries) < 10:
        return {
            "error": "❌ Could not find 10 valid summaries.",
            "available_count": len(summaries),
            "total_links_checked": len(checked_links),
            "company": query,
            "news_summaries": summaries,
            "comparative_analysis": comparative_analysis(summaries, query) if summaries else {},
        }

    return {
        "company": query,
        "news_summaries": summaries,
        "comparative_analysis": comparative_analysis(summaries, query),
    }
