# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 21:54:56 2025

@author: USER
"""
import requests
# NewsAPI setup # get supplier related news from api




import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWS_URL = 'https://newsapi.org/v2/everything'

def get_news(search_string):
    params = {
        'q': search_string,  # Search for supplier-related news
        'apiKey': NEWS_API_KEY,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 5
    }

    response = requests.get(NEWS_URL, params=params)
    news_data = response.json()

    articles = []
    for article in news_data.get('articles', []):
        articles.append(f"Title: {article['title']}\n"
                        f"Description: {article['description']}\n"
                        f"URL: {article['url']}\n")

    return "\n".join(articles)
