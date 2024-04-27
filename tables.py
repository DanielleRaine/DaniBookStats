import mariadb
import os


conn = mariadb.connect(user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    host=os.getenv('DB_HOST'),
                    database=os.getenv('DB_NAME'))

cursor = conn.cursor()
cursor.execute("SHOW TABLES")
print(cursor.fetchall())