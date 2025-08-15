# News Aggregator Backend

This is the backend service for the News Aggregator application, deployed on AWS Lambda.  
The service uses multiple AI agents to fetch, score, and summarize news articles based on user interests and professional context.

## Features

- **News Retrieval**: Fetches relevant news articles based on user interests
- **Relevance Scoring**: AI-powered scoring of articles based on user's professional context
- **Article Summarization**: Intelligent summarization of news articles

## API

The service exposes a Lambda function that accepts the following input:

```json
{
  "interest_topic": "string",
  "job_title": "string",
  "job_description": "string" // optional
}
```

## How to deploy
See the documents of [uv](https://docs.astral.sh/uv/guides/integration/aws-lambda/#deploying-a-zip-archive) and [Lambda](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-dependencies) for more details.

1. Bundle application dependencies into a local directory `package`.
```bash
uv export --frozen --no-dev --no-editable -o requirements.txt
uv pip install \
   --python-platform x86_64-manylinux2014 \
   --python 3.12 \
   --target packages \
   --only-binary=:all: \
   -r requirements.txt
```
2. Following the AWS Lambda documentation, bundle these dependencies into a zip.
```bash
cd packages
zip -r ../package.zip .
cd ..
```
3. Finally, we can add the application code to the zip archive.
```bash
cd src
zip -r ../package.zip .
cd ..
```
4. We can then deploy the zip archive to AWS Lambda via the AWS Management Console or the AWS CLI.


## Development

1. Create a Python virtual environment (3.12+)
2. Install dependencies using UV:
   ```bash
   uv add openai-agents
   ```

## Configuration

The service requires appropriate API keys and configuration for:
- OpenAI API access
- News API integration

Please ensure all necessary environment variables are set before deploying.
