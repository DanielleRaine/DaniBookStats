# install packages
install.packages("dotenv")
install.packages("RMariaDB")
install.packages("DBI")
installed.packages("ggplot2")
install.packages("dplyr")
install.packages("crayon")

# load packages
library(dotenv)
library(RMariaDB)
library(DBI)
library(ggplot2)
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
# disconnect
dbDisconnect(con)


# add number of authors to each entry
bookdata <- bookdata %>%
  mutate(numAuthors = sapply(strsplit(ifelse(is.na(authors), "", authors), ", "), length))

# Group the data by genre, removing null values
bookdata_filtered <- bookdata %>%
  group_by(genre) %>%
  filter(!is.na(pageCount)) %>%
  filter(pageCount != 0)

View(bookdata_filtered)

# create a plot of box plot comparison showing page count for each genre
ggplot(bookdata_filtered, aes(x = genre, y = pageCount)) +
  geom_boxplot(outlier.shape = "circle", alpha = 0.75, outlier.size = 1, outlier.colour = "blue") +
  labs(title = "Box Plot Comparison of Page Count per Book by Genre",
       x = "Genre",
       y = "Page Count")

# count length of each title and add it to each entry
bookdata_filtered$titleLength <- nchar(bookdata_filtered$title)

# linear regression time!!
ggplot(bookdata_filtered, aes(x = titleLength, y = pageCount)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE) +
  labs(title = "Title Length vs Page Count Linear Model",
       x = "Title Length",
       y = "Page Count")

ggplot(bookdata_filtered, aes(x = titleLength, y = pageCount)) +
  geom_point(size = 0.5) +
  geom_smooth(method = "lm", se = FALSE) +
  facet_wrap(~ genre, scales = "free") +
  labs(title = "Title Length vs Page Count Linear Model by Genre",
       x = "Title Length",
       y = "Page Count")

# print the entries that were weird
print(bookdata_filtered[bookdata_filtered[["titleLength"]] > 150, ] )
# summary of linear model
summary(lm(pageCount ~ titleLength, data = bookdata_filtered))

# Fit linear regression models for each genre and obtain summaries
model_summaries <- by(bookdata_filtered, bookdata_filtered$genre, function(df) {
  lm_model <- lm(pageCount ~ titleLength, data = df)
  summary(lm_model)
})

# Print summaries for each genre
print(model_summaries)

# get frequency of each publisher
publisher_frequency <- as.data.frame(table(c(bookdata$publisher)))
# rename columns
names(publisher_frequency) <- c("Publisher", "Number of Books Published")

common_publishers <- publisher_frequency %>%
  filter(`Number of Books Published` > 15)

ggplot(as.data.frame(common_publishers), aes(x=Publisher, y=`Number of Books Published`)) +
  geom_bar(stat = "identity") +
  labs(title = "Number of Books Published by Publishers with > 15 Published Books")


# count occurrences of each genre and convert to frame
genre_count <- as.data.frame(table(c(bookdata$genre)))
# rename the columns
names(genre_count) <- c("Genre", "Count")
# construct bar graph that shows count of each book by genre
ggplot(genre_count, aes(x=Genre, y=Count)) +
  geom_bar(stat = "identity") +
  labs(title = "Count of Books per Genre")

# calculate summary stats for number of authors  
author_summary_stats <- bookdata %>%
  group_by(genre) %>%
  summarise(mean_authors = mean(numAuthors),
            sd_authors = sd(numAuthors),
  )

# change column named genre to Genre in author summary stats
names(author_summary_stats)[names(author_summary_stats) == "genre"] <- 'Genre'
print(author_summary_stats)

# Group the data by genre
bookdata_grouped <- bookdata %>%
  group_by(genre)

# create density curves
ggplot(bookdata_grouped, aes(x = numAuthors, fill = genre)) +
  geom_density(alpha = 0.2) +
  labs(title = "Density Plot of Number of Authors per Book by Genre",
       x = "Number of Authors",
       y = "Density")

ggplot(bookdata_grouped, aes(x = numAuthors, fill = genre)) +
  geom_density(alpha = 0.2) +
  facet_wrap(~ genre, scales = "free") +  
  labs(title = "Density Plot of Number of Authors per Book by Genre",
       x = "Number of Authors",
       y = "Density")

