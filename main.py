import os
from dotenv import load_dotenv
import requests

# load .env file that contains api key
load_dotenv()
# get api key to authenticate with google books api
API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
# enable gzip compression and state user agent
headers = {"Accept-Encoding": "gzip",
           "User-Agent": "DaniBookStats/0.1 (https://github.com/DanielleHassanieh/DaniBookStats)"}
# list of genres to get data from
genres = ["Romance", "Mystery", "Textbook"]


def get_num_books_subject(subject):
    return requests.get('https://www.googleapis.com/books/v1/volumes',
                        params={'q': f'subject:"{subject}"',
                                'key': API_KEY,
                                'fields': "totalItems",
                                'printType': 'books'},
                        headers=headers).json()["totalItems"]


# "startIndex": "0", "maxResults": "1"
r = requests.get('https://www.googleapis.com/books/v1/volumes',
                 params={'q': 'subject:"Romance"', 'key': API_KEY},
                 headers=headers)

#d = dict(r.json())

#d.update()

print(get_num_books_subject("Romance"))

with open("bob.json", "w") as f:
    f.write(r.text)
