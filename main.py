import os
from dotenv import load_dotenv
import requests
from math import ceil
import mysql.connector as mariadb

# load .env file that contains api key
load_dotenv()
# get api key to authenticate with Google Books api
API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
# enable gzip compression and state user agent
headers = {'Accept-Encoding': 'gzip',
           'User-Agent': 'DaniBookStats/0.1 (https://github.com/DanielleHassanieh/DaniBookStats)'}
# list of genres to get data from
genres = ['Horror', 'Mystery']

# create connection to database
db_conn = mariadb.connect(user=os.getenv('MARIADB_USER'),
                          password=os.getenv('MARIADB_PASSWORD'),
                          host=os.getenv('MARIADB_HOST'),
                          port=os.getenv('MARIADB_PORT'),
                          database=os.getenv('MARIADB_DATABASE'))

mariadb_cursor = db_conn.cursor()

mariadb_cursor.execute("SHOW DATABASES")

for x in mariadb_cursor:
    print(x)

# genres = ["Romance", "Mystery", "Fantasy", "Science Fiction", ""]


# def get_subject_total_items(subject):
#     return requests.get('https://www.googleapis.com/books/v1/volumes',
#                         params={'q': f'subject:"{subject}"',
#                                 'key': API_KEY,
#                                 'fields': 'totalItems',
#                                 'printType': 'books'},
#                         headers=headers).json()['totalItems']
#
#
# for g in genres:
#     num_queries = ceil(get_subject_total_items(g) / 40)
#
#     for i in range(num_queries):
#         r = requests.get('https://www.googleapis.com/books/v1/volumes',
#                          params={'q': f'subject:"{g}"',
#                                  'key': API_KEY,
#                                  'fields': 'items(id,volumeInfo(title,authors,publishedDate,pageCount,categories,'
#                                            'averageRating,ratingsCount))',
#                                  'startIndex': i * 40,
#                                  'maxResults': 40},
#                          headers=headers)
