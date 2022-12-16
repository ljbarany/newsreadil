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
    expected = 'gdkkn'
    actual = linkcategory('indonesia', key)
    assert actual == expected