import requests
from bs4 import BeautifulSoup
from utils import get_summarized_news

def confidence_check(query):
    """Use basic confidence scoring to decide if the input looks like a company."""
    search_url = f"https://www.bing.com/search?q={query}+stock"
    response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    score = 0

    # 1. Trusted financial domains
    trusted_domains = ["investing.com", "marketwatch.com", "reuters.com", "moneycontrol.com", "bloomberg.com"]
    links = soup.find_all("a", href=True)
    if any(domain in link["href"] for link in links for domain in trusted_domains):
        score += 1

    # 2. Page content contains finance-related keywords
    finance_keywords = ["stock", "share price", "financials", "market cap", "valuation", "company"]
    text_blobs = soup.find_all(["h2", "p", "title"])
    if any(word in tag.get_text().lower() for tag in text_blobs for word in finance_keywords):
        score += 1

    # 3. URL structure has hints
    if any(path in link["href"] for link in links for path in ["/stock", "/company", "/quote", "/share"]):
        score += 1

    return score

# --------------------- MAIN ---------------------

if __name__ == "__main__":
    company_name = input("Enter a company name: ")

    # Confidence check
    score = confidence_check(company_name)
    if score < 1:
        print("\n⚠️ This might not be a recognized company.")
        proceed = input("Do you still want to search news for this topic? (y/n): ").strip().lower()
        if proceed != "y":
            print("✅ Cancelled by user.")
            exit()

    result = get_summarized_news(company_name)

    if "error" in result:
        print(f"\n{result['error']}")

    print("\n🔹 Showing Available Summaries for:", result["company"])

    for i, news in enumerate(result["news_summaries"], 1):
        print(f"\n🔹 News {i}:")
        print(f"🔗 URL: {news['source']}")
        print(f"📝 Summary: {news['summary']}")
        print(f"📊 Sentiment: {news['sentiment']}")
        print(f"📌 Key Topics: {', '.join(news['topics'])}")

    if result.get("comparative_analysis"):
        print("\n📊 Comparative Analysis:")
        analysis = result["comparative_analysis"]

        print(f"🟢 Sentiment Distribution: {analysis['sentiment_distribution']}")
        print(f"🧠 Top Topics: {', '.join(analysis['top_topics'])}")
        print(f"🌐 Top News Sources: {', '.join(analysis['top_sources'])}")

        if "example_negative_summary" in analysis:
            print("\n🚨 Sample Negative Coverage:")
            print(analysis["example_negative_summary"])

        print("\n📝 Overall Summary:")
        print(analysis["overall_summary"])
