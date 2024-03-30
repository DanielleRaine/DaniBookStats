import os
from dotenv import load_dotenv
import requests
from math import ceil
from time import sleep

# load .env file that contains api key
load_dotenv()
# get api key to authenticate with google books api
API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
# enable gzip compression and state user agent
headers = {"Accept-Encoding": "gzip",
           "User-Agent": "DaniBookStats/0.1 (https://github.com/DanielleHassanieh/DaniBookStats)"}
# list of genres to get data from
genres = ["Horror", "Mystery"]


# genres = ["Romance", "Mystery", "Fantasy", "Science Fiction", ""]


def get_subject_num_books(subject):
    return requests.get('https://www.googleapis.com/books/v1/volumes',
                        params={'q': f'subject:"{subject}"',
                                'key': API_KEY,
                                'fields': "totalItems",
                                'printType': 'books'},
                        headers=headers).json()["totalItems"]


r = requests.get('https://www.googleapis.com/books/v1/volumes',
                 params={'q': f'subject:"Mystery"',
                         'key': API_KEY,
                         'fields': 'items(id,volumeInfo(title,authors,publishedDate,pageCount,categories,averageRating,ratingsCount))',
                         'startIndex': 0,
                         'maxResults': 40},
                 headers=headers)

# for g in genres:
#
#     num_queries = ceil(get_subject_num_books(g) / 40)
#
#     for i in range(num_queries):
#         r = requests.get('https://www.googleapis.com/books/v1/volumes',
#                          params={'q': f'subject:"{g}"',
#                                  'key': API_KEY,
#                                  'fields': 'items(id,volumeInfo(title,authors,publishedDate,pageCount,categories,averageRating,ratingsCount))',
#                                  'startIndex': i * 40,
#                                  'maxResults': 40},
#                          headers=headers)
#         # if not r.ok:
#         #     continue
#


# d = dict(r.json())

# d.update()

# print(get_num_books_subject("Fiction"))

with open("bob.json", "w") as f:
    f.write(r.text)
