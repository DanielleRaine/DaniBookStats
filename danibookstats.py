import os
from dotenv import load_dotenv
import requests
from math import ceil
import mariadb


# load .env file that contains api key and database connection information
load_dotenv()

# get api key to authenticate with Google Books api
API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
# enable gzip compression and state user agent for api
headers = {'Accept-Encoding': 'gzip',
           'User-Agent': 'DaniBookStats/0.1 (https://github.com/DanielleHassanieh/DaniBookStats)'}

# list of genres to get data from
genres = ['Horror', 'Mystery', 'Fantasy', 'Science Fiction', 'Biography', 'Language', 'Math', 'Science']

# create connection to database
connection = mariadb.connect(user=os.getenv('DB_USER'),
                          password=os.getenv('DB_PASSWORD'),
                          host=os.getenv('DB_HOST'),     
                          database=os.getenv('DB_NAME'))

# create database cursor to input sql commands
cursor = connection.cursor()

#print(db_cursor.fetchall())


def get_subject_total_items(subject):
    return requests.get('https://www.googleapis.com/books/v1/volumes',
                        params={'q': f'subject:"{subject}"',
                                 'key': API_KEY,
                                 'fields': 'totalItems',
                                 'printType': 'books'},
                         headers=headers).json()['totalItems']

# create central table for all the books if it doesn't already exist
cursor.execute(f'CREATE TABLE IF NOT EXISTS books(id CHAR(12) unique, title CHAR(255), genre CHAR(32))')

for g in genres:
    # calculate number of queries based on how many total items can be acquired
    num_queries = ceil(get_subject_total_items(g) / 40)

    for i in range(num_queries):
        r = requests.get('https://www.googleapis.com/books/v1/volumes',
                         params={'q': f'subject:"{g}"',
                                 'key': API_KEY,
                                 'fields': 'items(id,volumeInfo(title,authors,publishedDate,pageCount,categories,'
                                           'averageRating,ratingsCount))',
                                 'startIndex': i * 40,
                                 'maxResults': 40},
                         headers=headers)

        for b in dict(r.json())['items']:
            print(f'INSERT IGNORE books VALUES("{b['id']}", "{b['volumeInfo']['title'].replace('\"', '\'')}", "{g}")')
            cursor.execute(f'INSERT IGNORE books VALUES("{b['id']}", "{b['volumeInfo']['title'].replace('\"', '\'')}", "{g}")')

connection.commit()
connection.close()

