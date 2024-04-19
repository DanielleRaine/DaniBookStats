# Author: Danielle Hassanieh
# Created: 2024-03-26
# Last Modified: 2024-04-19
# Description: This script pulls in book data from the Google Books API and stores it in a MySQL database.

import os
import requests
from math import ceil
import mariadb
from datetime import datetime


# get google books api key from environment variables
API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
# set headers for requests
headers = {'Accept-Encoding': 'gzip', 'User-Agent': 'DaniBookStats/0.1 (https://github.com/DanielleHassanieh/DaniBookStats)'}

# list of genres to search for
genres = ['Horror', 'Mystery', 'Fantasy', 'Science Fiction', 'Biography', 'Language', 'History', 'Science']

# connect to database
connection = mariadb.connect(user=os.getenv('DB_USER'),
                             password=os.getenv('DB_PASSWORD'),
                             host=os.getenv('DB_HOST'),
                             database=os.getenv('DB_NAME'))

# create cursor for database
cursor = connection.cursor()


# function to get number of queries to make
# ceil is used to round up to the nearest whole number
# totalItems is the total number of books in the genre
# each query returns 40 books
# so totalItems / 40 is the number of queries to make
def get_num_queries(subject):
    return ceil(requests.get('https://www.googleapis.com/books/v1/volumes',
                        params={'q': f'subject:"{subject}"',
                                'key': API_KEY,
                                'fields': 'totalItems',
                                'printType': 'books'},
                        headers=headers).json()['totalItems'] / 40)

# name of table to store books
table_name = f'booksbygenre{datetime.now().year}_{datetime.now().month}_{datetime.now().day}_{datetime.now().hour}_{datetime.now().minute}_{datetime.now().second}'

# write table name to file
with open('table_names.txt', 'a') as f:
    f.write(f'{table_name}\n')

# create table if it doesn't exist
cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name}(id CHAR(12) unique, title CHAR(255), authors CHAR(255), publisher CHAR(64), publishedDate DATE, pageCount INT, averageRating DECIMAL(2,1), ratingsCount INT, genre CHAR(32))')

# loop through genres and get books
for g in genres:
    # get number of queries to make
    num_queries = get_num_queries(g)

    # create a list to store book data
    books = []

    # loop through queries and get books
    for i in range(num_queries):
        # get books for genre
        r = requests.get('https://www.googleapis.com/books/v1/volumes',
                         params={'q': f'subject:"{g}"',
                                 'key': API_KEY,
                                 'fields': 'items(id,volumeInfo(title,authors,publisher,publishedDate,pageCount,averageRating,ratingsCount))',
                                 'startIndex': i * 40,
                                 'maxResults': 40},
                         headers=headers)

        # loop through books and add to list
        for b in dict(r.json())['items']:
            # add book to list
            books.append((b['id'],
                          b['volumeInfo']['title'].replace('\"', '\'') if 'title' in b['volumeInfo'] else 'Unknown',
                          ", ".join(b['volumeInfo']['authors']) if 'authors' in b['volumeInfo'] else 'Unknown',
                          b['volumeInfo']['publisher'] if 'publisher' in b['volumeInfo'] else 'Unknown',
                          b['volumeInfo']['publishedDate'] if 'publishedDate' in b['volumeInfo'] else 'Unknown',
                          b['volumeInfo']['pageCount'] if 'pageCount' in b['volumeInfo'] else 0,
                          float(b['volumeInfo']['averageRating'] if 'averageRating' in b['volumeInfo'] else 0),
                          b['volumeInfo']['ratingsCount'] if 'ratingsCount' in b['volumeInfo'] else 0,
                          g))

    # insert books into database
    # use IGNORE to prevent duplicate entries
    # use executemany to insert multiple rows at once
    # use %s as a placeholder for values
    # pass in list of tuples with values to insert
    cursor.executemany(f'INSERT IGNORE INTO {table_name} (id, title, authors, publisher, publishedDate, pageCount, averageRating, ratingsCount, genre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', books) 

# commit changes and close connection
connection.commit()
connection.close()
