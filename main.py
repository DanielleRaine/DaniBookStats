import os
from dotenv import load_dotenv
import requests

# load .env file
load_dotenv()
# get api key
API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
# headers
headers = {"Accept-Encoding": "gzip", "User-Agent": "DaniBookStats/0.1 (https://github.com/DanielleHassanieh/DaniBookStats)"}

# request
r = requests.get('https://www.googleapis.com/books/v1/volumes',
                 params={'q': 'subject:"Romance"', 'key': API_KEY, "startIndex": "0", "maxResults": "10"},
                 headers=headers)


with open("bob.txt", "w") as f:
    f.write(r.text)
