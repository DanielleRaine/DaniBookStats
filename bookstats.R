# install packages
install.packages("dotenv")
install.packages("RMariaDB")
install.packages("DBI")
installed.packages("ggplot2")

# load packages
library(dotenv)
library(RMariaDB)
library(DBI)
library(ggplot2)


# load all the secret data
load_dot_env()

# connect to database
con <- dbConnect(
  MariaDB(),
  user=Sys.getenv('DB_USER'),
  password=Sys.getenv('DB_PASSWORD'),
  host=Sys.getenv('DB_HOST'),
  dbname=Sys.getenv('DB_NAME')
)

# retrieve data from table
bookdata <- dbGetQuery(con, "SELECT * FROM booksbygenre2024_4_27_12_20_27")

# disconnect
dbDisconnect(con)

# count occurrences of each genre and convert to frame
genre_count <- as.data.frame(table(c(bookdata$genre)))
# rename the columns
names(genre_count) <- c("genre", "count")

ggplot(genre_count, aes(x=genre, y=count)) +
  geom_bar(stat = "identity")
