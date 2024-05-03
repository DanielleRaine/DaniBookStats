# install packages
install.packages("dotenv")
install.packages("RMariaDB")
install.packages("DBI")
installed.packages("ggplot2")
install.packages("stringr")
install.packages("dplyr")
install.packages("crayon")


# load packages
library(dotenv)
library(RMariaDB)
library(DBI)
library(ggplot2)
library(stringr)
library(dplyr)
library(crayon)


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
# construct bar graph that shows count of each book by genre
ggplot(genre_count, aes(x=genre, y=count)) +
  geom_bar(stat = "identity")

# count the number if authors per entry using a pipe
bookdata <- bookdata %>%
  mutate(num_authors = sapply(strsplit(ifelse(is.na(authors), "", authors), ", "), length))

# calculate summary stats for num authors associated with genre
num_author_summary_stats <- bookdata %>%
  filter(num_authors != 0) %>%
  group_by(genre) %>%
  summarise(mean_authors = mean(num_authors, na.rm = TRUE),
            sd_authors = sd(num_authors, na.rm = TRUE))

dnorm(mean = num_author_summary_stats[1,2], sd = num_author_summary_stats[1,3])
