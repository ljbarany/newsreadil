pip install textstat
pip install python-dotenv

#Importing modules
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import json
from json import dumps, loads
from pandas import json_normalize
import textstat
from nltk.tokenize import sent_tokenize, word_tokenize
from textstat.textstat import textstatistics
from bs4 import BeautifulSoup
import re
import nltk
nltk.download('punkt')

#Setting API key into variable
load_dotenv()
key = os.getenv('API_KEY')

#Function to get readibility category of news based on topic

def linkcategory(topic, key):
    """
        This function obtain table for headline article of specific topic and calculate how easy-to-read each article for users.
        Readibility score calculation is inspired by `Flesch Kincaid Grade readibility score <https://readable.com/readability/flesch-reading-ease flesch-kincaid-grade-level/>`_
        
        Returns
        -------
        pandas.core.frame.DataFrame
          A dataframe containing complete information of title, link to the article, and readibility category of each writing.    
        
        Examples
        --------
        >>> from newsreadil import linkcategory
        >>> linkcategory("world cup", key)
        
        	title	url	read_category
        0	World Cup 2022: Sign up to Jürgen Klinsmann's ...	https://www.bbc.co.uk/sport/football/63607873	Basic
        1	A Destabilizing Hack-and-Leak Operation Hits M...	https://www.wired.com/story/moldova-leaks-goog...	Advanced
        2	Google’s Year in Search 2022 was dominated by ...	https://www.engadget.com/google-year-in-search...	Advanced
        3	World Cup 2022: Welsh anthem praised around th...	https://www.bbc.co.uk/news/uk-wales-63729674	Skilled
        4	World Cup: Shuttle flights cast doubts on carb...	https://www.bbc.co.uk/news/world-63796634	Skilled 
        """
    
    url = f'https://newsapi.org/v2/everything?q={topic}&apiKey={key}'
    r = requests.get(url)
    status = r.status_code
    if status==404:
            raise Exception("404 : error (failed to make request)")
    if status==500:
            raise Exception("500 : successfully made request but had internal error")
    if status == 200:
        data = r.json()
        df = pd.json_normalize(data, "articles")
        title = df['title']
        content = df['content'].to_string()
        df['sentences'] = df.apply(lambda row: nltk.sent_tokenize(row['content']), axis=1)
        df['sentences_count'] = df['content'].str.count('\\..').clip(lower=1)
        df['words'] = df.apply(lambda row: nltk.word_tokenize(row['content']), axis=1)
        df['words_count'] = df.apply(lambda row: len(row['words']), axis=1)
        df['average_sentence_length'] = df['words_count'] / df['sentences_count']
        df['syllable'] = textstatistics().syllable_count(content)
        df['ASPW'] = df['syllable']/df['words_count']
        df['FRE'] = 0.39 * df['average_sentence_length'] + 11.8 * df['ASPW'] - 15.59
        df['readibilityscore'] = round(df['FRE'],2)
        df['read_category'] = pd.cut(df['readibilityscore'], bins=[1, 270, 309, 339, 400],
                                         labels=['Basic', 'Average', 'Skilled', 'Advanced'])
        return df[['title', 'url', 'read_category']]
    else:
        error

    def newarticle(topic, key):
         """
        This function obtain table for headline article about specific topic and return the most recent news
        
        Returns
        -------
          List of the most recent news globally with complete information of title, link to the article, and source    
        
        Examples
        --------
        >>> from newsreadil import newarticle
        >>> newarticle("indonesia", key)
        
        'Avatar' star Sam Worthington reveals alcohol addiction: 'Drinking helped me get through the day' - Yahoo Entertainment  https://www.yahoo.com/entertainment/avatar-sam-worthington-alcohol-addiction-sober-fame-205541200.html                                           Yahoo Entertainment         2022-12-15 20:55:41+00:00
        49ers vs. Seahawks odds, line, spread Thursday Night Football picks, NFL predictions from dialed-in model - CBS Sports   https://www.cbssports.com/nfl/news/49ers-vs-seahawks-odds-line-spread-thursday-night-football-picks-nfl-predictions-from-dialed-in-model/        CBS Sports                  2022-12-15 23:51:28+00:00
        Congress votes to remove bust of chief justice who authored Dred Scott decision - Fox News                               https://www.foxnews.com/politics/congress-votes-remove-bust-chief-justice-authored-dred-scott-decision                                           Fox News                    2022-12-15 20:16:19+00:00 
        """
        url = f'https://newsapi.org/v2/everything?q={topic}&apiKey={key}'
        r = requests.get(url)
        data = r.json()
        df = pd.json_normalize(data, "articles")
        df['release'] = pd.to_datetime(df['publishedAt'])
        release =  df['release']
            return df.groupby(['title','url', 'source.name']).release.max()