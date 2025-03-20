import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import streamlit as st
import json
from newspaper import Article
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

# Function to fetch news articles and summarize
def get_news_articles(company):
    url = f'https://news.google.com/search?q={company}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    for item in soup.find_all('article')[:10]:
        title = item.text
        link = item.find('a')['href']
        if link.startswith('/'):
            link = "https://news.google.com" + link

        # Fetch full article and summarize
        try:
            article = Article(link)
            article.download()
            article.parse()
            article.nlp()  # Summarization
            summary = article.summary
        except:
            summary = "Summary not available."

        articles.append({"title": title, "link": link, "summary": summary})
    return articles

# ✅ Fix: Proper indentation for function definition
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)['compound']
    return "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"

# Function to perform comparative sentiment analysis
def comparative_analysis(sentiments):
    total = len(sentiments)
    positive = sentiments.count("Positive")
    negative = sentiments.count("Negative")
    neutral = sentiments.count("Neutral")
    
    summary = f"Out of {total} articles, {positive} are Positive, {negative} are Negative, and {neutral} are Neutral."
    return summary

# Function to extract topics
def extract_topics(text):
    words = word_tokenize(text)
    keywords = [word for word in words if word.lower() not in stopwords.words('english') and word.isalpha()]
    return list(set(keywords[:5]))  # Return top 5 keywords

# Function to generate Hindi speech
def generate_tts(text, filename="output.mp3"):
    tts = gTTS(text, lang='hi')
    tts.save(filename)
    return filename

# Streamlit UI
def main():
    st.title("News Summarization & Sentiment Analysis")
    company = st.text_input("Enter company name:")
    if st.button("Fetch News"):
        articles = get_news_articles(company)
        sentiment_count = {"Positive": 0, "Negative": 0, "Neutral": 0}
        results = []
        sentiments_list = []  # ✅ Store sentiments for comparative analysis

        for article in articles:
            sentiment = analyze_sentiment(article['summary'])
            topics = extract_topics(article['summary'])
            sentiment_count[sentiment] += 1
            sentiments_list.append(sentiment)  # ✅ Collect sentiments
            results.append({"Title": article['title'], "Summary": article['summary'], "Sentiment": sentiment, "Topics": topics})

        # ✅ Perform Comparative Analysis
        comparison_result = comparative_analysis(sentiments_list)

        st.subheader("Sentiment Distribution")
        st.json(sentiment_count)

        st.subheader("Comparative Analysis Summary")
        st.text(comparison_result)  # ✅ Show comparison results

        report = json.dumps(results, indent=4, ensure_ascii=False)
        st.text_area("Sentiment Report", report, height=200)
        speech_file = generate_tts(report)
        st.audio(speech_file)

if __name__ == "__main__":
    main()
