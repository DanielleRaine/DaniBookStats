import os
import mariadb


# connect to database
connection = mariadb.connect(user=os.getenv('DB_USER'),
                             password=os.getenv('DB_PASSWORD'),
                             host=os.getenv('DB_HOST'),
                             database=os.getenv('DB_NAME'))

# create cursor for database
cursor = connection.cursor()

# execute SHOW TABLES command
cursor.execute("SHOW TABLES")

# fetch all tables
tables = cursor.fetchall()

# iterate over each table and drop it
for table in tables:
    cursor.execute(f"DROP TABLE {table[0]}")

# close the connection
connection.close()
