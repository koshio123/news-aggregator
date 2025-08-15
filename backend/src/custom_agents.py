

from agents.agent import Agent
from agents.model_settings import ModelSettings
from models import NewsList, NewsSummary, RelevanceScore
from tools import fetch_news


INSTRUCTIONS = """
You are a news retriever. Given a user's interest in a topic, job title, and job description, 
you will fetch news articles using fetch_news and return 10 relevant news articles which user might be interested in.
If the relevant news articles are not found, update the query to be more general and try again.
Make sure to return all articles retrieved from the News API without modifying them.
"""

news_retriever_agent = Agent(
    name="News Retriever",
    instructions=INSTRUCTIONS,
    tools=[fetch_news],
    model="gpt-5-mini",
    model_settings=ModelSettings(tool_choice="fetch_news"),
    output_type=NewsList
)

INSTRUCTIONS = """
You are a news article relevance scorer. Given a user's interest (topic, job title, and job description) and the news article,
you will score the article based on their relevance to the user's interest.
The relevance score should be a float between 0 and 1, where 1 means the article is highly relevant to the user's interest and 0 means it is not relevant at all.
You should also provide a reason for the relevance score, explaining why this article is relevant to the user's interest.
"""

news_scorer_agent = Agent(
    name="News Scorer",
    instructions=INSTRUCTIONS,
    model="gpt-4o",
    output_type=RelevanceScore
)

INSTRUCTIONS = """
You are a news article summarizer. Given a user's interest (topic, job title, and job description) and the news article,
you will summarize the article focusing on the key points that are useful for the user.
The summary should be concise and highlight the most relevant information for the user.
Do not include any additional text or formatting in the summary.
"""

news_summarizer_agent = Agent(
    name="News Summarizer",
    instructions=INSTRUCTIONS,
    model="gpt-4o",
    output_type=NewsSummary
)