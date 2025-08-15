from datetime import datetime, timedelta
import os
from agents.tool import function_tool
from models import News, NewsApiResponse, NewsList
import requests


@function_tool
async def fetch_news(query: str) -> NewsList:
    """Fetch news from the News API
    
    Args:
        query: The query to search for.
               You can use the AND / OR / NOT keywords, and optionally group these with parenthesis. Eg: crypto AND (ethereum OR litecoin) NOT bitcoin.
        from_date: The date to search from in ISO 8601 date format. (Defaults to 30 days ago)

    Returns:
        A list of news articles
    """
    from_date = None
    if from_date is None:
        from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    # Set the API key and endpoint
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"

    # Make the API request
    raw_response = requests.get(NEWS_API_ENDPOINT, params={"q": query, "apiKey": NEWS_API_KEY, "from": from_date})
    data = raw_response.json()
    print(f"Response from the News API: {data}")
    response = NewsApiResponse.model_validate(data)
    print(f"Validated response: {response}")
    if response.status != "ok":
        raise ValueError(f"Error fetching news: {response.status}")

    # Extract the articles from the response
    news_list = NewsList(articles=[
        News(
            title=article.title,
            description=article.description,
            url=article.url,
            source=article.source.name,
            publishedAt=article.publishedAt
        ) for article in response.articles
    ])
    return news_list