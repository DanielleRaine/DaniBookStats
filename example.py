import requests
import os
from dotenv import load_dotenv


# pull in environment variables from .env file
load_dotenv()

# get google books api key from environment variables
API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')

# set headers for requests
headers = {'Accept-Encoding': 'gzip', 'User-Agent': 'DaniBookStats/0.1 (https://github.com/DanielleHassanieh/DaniBookStats)'}

r = requests.get('https://www.googleapis.com/books/v1/volumes',
             params={'q': 'subject:Fantasy',
                     'key': API_KEY},
             headers=headers)

with open('example.json', 'w') as f:
    f.write(r.text)
