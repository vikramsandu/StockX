"""
Given Company Name, Fetch Latest News about the company.
"""
import httpx


def get_financial_news(query: str, news_api: str) -> str:
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={news_api}"
    response = httpx.get(url)
    articles = response.json().get("articles", [])
    news_items = [{
        "title": article["title"],
        "url": article["url"]
    } for article in articles[:10]]

    return "\n".join([f"- {item['title']}" for item in news_items])
