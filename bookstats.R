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
  mutate(num_authors = sapply(strsplit(ifelse(is.na(authors), "", authors), ", "), length))

# Group the data by genre, filtered removing null values
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

# LEARNING STUFF

# get the indices of book titles greater than 20 characters in length
indices_of_titles <- which(nchar(bookdata$title) > 20)
# you can do this I guess and it works real well (print the items specified by indices of numeric vector)
print(bookdata$title[indices_of_titles])

# you can put a column of items into a vector!
c(bookdata$id)
# frequency table!
publisher_frequency <- table(c(bookdata$publisher))
# access the table like this probably!
print(publisher_frequency["Cambridge University Press"])

common_publisher <- which(publisher_frequency > 10)
print(publisher_frequency[common_publisher])

# count occurrences of each genre and convert to frame
genre_count <- as.data.frame(table(c(bookdata$genre)))
# rename the columns
names(genre_count) <- c("Genre", "Count")
# construct bar graph that shows count of each book by genre
ggplot(genre_count, aes(x=Genre, y=Count)) +
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

# change column named genre to Genre in author summary stats
names(author_summary_stats)[names(author_summary_stats) == "genre"] <- 'Genre'
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
       y = "Density")
