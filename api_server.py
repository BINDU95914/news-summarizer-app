from fastapi import FastAPI
import json
from api import get_news_articles, analyze_sentiment, comparative_analysis  # Import your functions

app = FastAPI()

@app.get("/news/{company}")
def fetch_news(company: str):
    articles = get_news_articles(company)
    sentiments = [analyze_sentiment(article['summary']) for article in articles]
    sentiment_summary = comparative_analysis(sentiments)
    
    return {
        "company": company,
        "articles": articles,
        "sentiment_distribution": sentiment_summary
    }

if __name__ == "__main__":
    import uvicorn
    #uvicorn.run(app, host="0.0.0.0", port=8001)
