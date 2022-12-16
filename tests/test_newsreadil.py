from newsreadil import newsreadil
import json
import pandas as pd
import requests
from nltk.tokenize import sent_tokenize, word_tokenize
from textstat.textstat import textstatistics,legacy_round
from bs4 import BeautifulSoup
import re
import pytest

def test_linkcategory():
    act = newsreadil.linkcategory()
    expected = pd.read_pickle(df[['title', 'url', 'read_category']])
    assert expected.equals(act), "no result found"

def test_newarticle():
    act = newsreadil.newarticle()
    expected = pd.read_pickle(df.groupby(['title','url', 'source.name']).release.max())
    assert expected.equals(act), "no result found"