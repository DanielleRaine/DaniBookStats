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
bookdata <- dbGetQuery(con, "SELECT * FROM booksbygenre2024_5_3_15_0_3")

#View(bookdata)

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

# calculate summary stats for number of authors  
author_summary_stats <- bookdata %>%
  group_by(genre) %>%
  summarise(mean_authors = mean(num_authors),
            sd_authors = sd(num_authors),
  )

print(author_summary_stats)

# Group the data by genre
bookdata_grouped <- bookdata %>%
  group_by(genre)

# create boxplots
ggplot(bookdata_grouped, aes(x = genre, y = num_authors)) +
  geom_boxplot(outlier.shape = "circle", outlier.alpha = 0.25, outlier.size = 2, outlier.color = "purple") +
  geom_jitter(width = 0.25, height = 0.25, alpha = 0.5) +
  labs(title = "Boxplot Comparison of Number of Authors per Book by Genre",
       x = "Genre",
       y = "Number of Authors")

# create density curves
ggplot(bookdata_grouped, aes(x = num_authors, fill = genre)) +
  geom_density(alpha = 0.2) +
  labs(title = "Density Plot of Number of Authors per Book by Genre",
       x = "Number of Authors",
       y = "Density"
  )