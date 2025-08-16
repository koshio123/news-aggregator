import os
import json
import asyncio

from agents.run import Runner
from agents.tracing.create import trace
from models import News, NewsList, NewsSummary, UserInfo
from custom_agents import news_retriever_agent, news_scorer_agent, news_summarizer_agent
from utils import SESClient


async def async_handler(event, context):
    interest_topic = event["interest_topic"]
    job_title = event["job_title"]
    job_description = event.get("job_description", None)

    user_info = UserInfo(
        interest_topic=interest_topic,
        job_title=job_title,
        job_description=job_description
    )

    relevant_articles: list[News] = []
    summaries: list[NewsSummary] = []
    with trace("News Retriever"):
        print(f"Running news retriever agent with user info: {user_info.model_dump_json()}")
        result = await Runner.run(news_retriever_agent, user_info.model_dump_json())
        articles: list[News] = result.final_output.articles
        print(f"Retrieved {len(articles)} articles.")
        for article in articles:
            print(f"Article: {article.model_dump_json()}")
            message = f"""
            ## User Information
            - Interest Topic: {user_info.interest_topic}
            - Job Title: {user_info.job_title}
            - Job Description: {user_info.job_description}

            ## News Article
            - Title: {article.title}
            - Description: {article.description}
            """
            print(f"Running news scorer agent for article: {article.title}")
            result = await Runner.run(news_scorer_agent, message)
            score = result.final_output
            print(f"Relevance Score: {score.model_dump_json()}")
            if score.score >= 0.7:
                relevant_articles.append(article)
                print(f"Runnig news summarizer agent for article: {article.title}")
                result = await Runner.run(news_summarizer_agent, message)
                summary: NewsSummary = result.final_output
                summaries.append(summary)
                print(f"Summary: {summary.model_dump_json()}")


def lambda_handler(event, context):
    print(f"Recieved event: {json.dumps(event)}")

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_handler(event, context))
