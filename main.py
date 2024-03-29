import os
from dotenv import load_dotenv
import requests
from math import ceil

# load .env file that contains api key
load_dotenv()
# get api key to authenticate with google books api
API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
# enable gzip compression and state user agent
headers = {"Accept-Encoding": "gzip",
           "User-Agent": "DaniBookStats/0.1 (https://github.com/DanielleHassanieh/DaniBookStats)"}
# list of genres to get data from
genres = ["Horror", "Mystery"]
#genres = ["Romance", "Mystery", "Fantasy", "Science Fiction", ""]


def get_num_books_subject(subject):
    return requests.get('https://www.googleapis.com/books/v1/volumes',
                        params={'q': f'subject:"{subject}"',
                                'key': API_KEY,
                                'fields': "totalItems",
                                'printType': 'books'},
                        headers=headers).json()["totalItems"]


# "startIndex": "0", "maxResults": "1"
r = requests.get('https://www.googleapis.com/books/v1/volumes',
                 params={'q': 'subject:"Mystery"+inauthor:"Kenneth H. Rosen"', 'key': API_KEY},
                 headers=headers)

print(40)

for g in genres:

    num_queries = ceil(get_num_books_subject(g) / 40)

    for i in range(num_queries):
         r = requests.get('https://www.googleapis.com/books/v1/volumes', params={'q': 'subject:"Mystery"+inauthor:"Kenneth H. Rosen"', 'key': API_KEY}, headers=headers)


    if r.ok:
        pass

   # pass


#r = requests.get("https://www.google.com/search?q=subject:%22Fiction%22&sca_esv=09842260a7ca25e4&sca_upv=1&tbm=bks&sxsrf=ACQVn08DDS_c0GBQ_837Xe0dRnh0c-Qmtw:1711732756530&ei=FPgGZuuFIJbKkPIPsqO52A8&start=0&sa=N&ved=2ahUKEwjr35y3_ZmFAxUWJUQIHbJRDvs4WhDy0wN6BAgPEAQ&biw=1920&bih=932&dpr=1", params={'key': API_KEY}, headers=headers)

#d = dict(r.json())

#d.update()

#print(get_num_books_subject("Fiction"))

with open("bob.json", "w") as f:
    f.write(r.text)
