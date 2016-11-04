"""
The Google Web Search API is no longer available. Please migrate to the Google Custom Search API
https://developers.google.com/custom-search/
"""

import urllib
import json
from AnonBrowser import *

def google(search_term):
    anon = AnonBrowser()
    search_term = urllib.quote_plus(search_term)
    response = anon.open('http://ajax.googleapis.com/' + 'ajax/services/search/web?v=1.0&q=' + search_term)
    objects = json.load(response)
    print(objects)

google('Bruce Lee')