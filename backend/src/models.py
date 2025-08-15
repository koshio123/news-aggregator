from datetime import datetime
from pydantic.fields import Field
from pydantic.main import BaseModel


class NewsApiSource(BaseModel):
    """A news source from the News API"""
    id: str | None
    name: str


class NewsApiArticle(BaseModel):
    """A single news article from the News API"""
    source: NewsApiSource
    author: str | None
    title: str
    description: str
    url: str
    urlToImage: str | None
    publishedAt: datetime


class NewsApiResponse(BaseModel):
    """Response from the News API"""
    status: str
    totalResults: int
    articles: list[NewsApiArticle]


class News(BaseModel):
    """A single news article"""
    title: str
    description: str
    url: str
    source: str
    publishedAt: datetime

class NewsList(BaseModel):
    """A list of news articles"""
    articles: list[News]


class RelevanceScore(BaseModel):
    """Relevance score and reason for a news article"""
    score: float = Field(
        description="Relevance score of the news article based on the user's interest."
    )
    reason: str = Field(
        description="Reason for the relevance score, explaining why this article is relevant to the user's interest."
    )


class ScoredNews(News):
    """A single news article with a relevance score"""
    relevance_score: float = Field(
        description="Relevance score of the news article based on the user's interest."
    )
    relevance_reason: str = Field(
        description="Reason for the relevance score, explaining why this article is relevant to the user's interest."
    )


class ScoredNewsList(NewsList):
    """A list of news articles with relevance score"""
    articles: list[ScoredNews]


class UserInfo(BaseModel):
    """User information for news retrieval"""
    interest_topic: str = Field(
        description="The topic of interest for the user, e.g., 'AI in healthcare'."
    )
    job_title: str = Field(
        description="The job title of the user, e.g., 'Data Scientist'."
    )
    job_description: str | None = Field(
        default=None,
        description="The job description of the user, e.g., 'Responsible for analyzing data and building machine learning models'."
    )


class NewsSummary(BaseModel):
    """Summary of a news article"""
    summary: str = Field(
        description="A concise summary of the news article, focusing on the key points that are useful for the user."
    )
    contents: str = Field(
        description="The full contents of the news article."
    )
    supplementary_info: str | None = Field(
        default=None,
        description="Any additional information that might be useful for the user, such as related articles or background information."
    )