# Here we're preprocessing the data provided by http://movielens.org and making a 
# few more csv files to easy handle the data at recommendation time

# files present in ./ml-latest-small
# 'links.csv', 'movies.csv', 'ratings.csv', 'README.txt', 'tags.csv'

import numpy as np
import pandas as pd

"""
Dataset info:

Tags Data File Structure (tags.csv)
-----------------------------------

All tags are contained in the file `tags.csv`. Each line of this file after the header row represents 
one tag applied to one movie by one user, and has the following format:

    userId,movieId,tag,timestamp

The lines within this file are ordered first by userId, then, within user, by movieId.

Tags are user-generated metadata about movies. Each tag is typically a single word or short phrase.
The meaning, value, and purpose of a particular tag is determined by each user.

=================================================================================================

Ratings Data File Structure (ratings.csv)
-----------------------------------------

All ratings are contained in the file `ratings.csv`. Each line of this file after the header row
represents one rating of one movie by one user, and has the following format:

    userId,movieId,rating,timestamp

The lines within this file are ordered first by userId, then, within user, by movieId.

Ratings are made on a 5-star scale, with half-star increments (0.5 stars - 5.0 stars).

=================================================================================================

Movies Data File Structure (movies.csv)
---------------------------------------

Movie information is contained in the file `movies.csv`. Each line of this file after the header row 
represents one movie, and has the following format:

    movieId,title,genres

Movie titles are entered manually or imported from https://www.themoviedb.org/, and include the year of 
release in parentheses. Errors and inconsistencies may exist in these titles.

=================================================================================================

Links Data File Structure (links.csv)
-------------------------------------

Identifiers that can be used to link to other sources of movie data are contained in the file `links.csv`.
Each line of this file after the header row represents one movie, and has the following format:

    movieId,imdbId,tmdbId

"""


# Initially we're combining movies.csv and ratings.csv
movies_df = pd.read_csv(r"./ml-latest-small/movies.csv")
ratings_df = pd.read_csv(r'./ml-latest-small/ratings.csv')

# Dropping timestamp as we don't need it
ratings_df.drop(['timestamp'], axis=1, inplace=True)

# Combining both DFs on movieId & saving it as main.csv
main_df = pd.merge(ratings_df, movies_df, on = 'movieId')
main_df.to_csv('./ml-latest-small/main.csv', index=False, columns=main_df.columns)

# getting all the genres
genres = np.unique(np.concatenate(movies_df.genres.str.split('|')))
genres_list = list(genres)
genres_list.remove('(no genres listed)')

# making a movie to genres boolean chart for content based filtering & saving it
movies = movies_df.copy()
movies.drop(['title'], axis=1, inplace=True)
for genre in genres_list:
    movies[genre] = movies.apply(lambda x: genre in x['genres'], axis=1)
    
movies.to_csv('./ml-latest-small/genres.csv', index=False, columns=movies.columns)


# Pivoting the combined df to create an user-movie pivot table
user_item_df = main_df.pivot_table(index=['userId'], columns=['movieId'], values='rating')

# Changing null with mean for Pearson correlation
user_item_df = user_item_df.apply(lambda row: row.fillna(row.mean()), axis=1)
user_item_df.to_csv('./ml-latest-small/user_item.csv', index=False)

