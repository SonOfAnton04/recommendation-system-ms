import numpy as np
import pandas as pd
import scipy.spatial
import random

def similarity_matrix_user_to_user(data: np.array, keyword: str) -> None:
    
    print("in similarity_matrix_user_to_user")
    
    USERS = len(data)
    similarity = np.zeros((USERS, USERS))
    for user1 in range(USERS):
        for user2 in range(USERS):
            if np.count_nonzero(data[user1]) and np.count_nonzero(data[user2]):
                if keyword == 'cosine':
                    similarity[user1][user2] = 1 - scipy.spatial.distance.cosine(data[user1], data[user2])
                elif keyword == 'jaccard':
                    similarity[user1][user2] = 1 - scipy.spatial.distance.jaccard(data[user1], data[user2])
                elif keyword == 'pearson':
                    try:
                        if not math.isnan(scipy.stats.pearsonr(data[user1],data[user2])[0]):
                            similarity[user1][user2] = scipy.stats.pearsonr(data[user1], data[user2])[0]
                        else:
                            similarity[user1][user2] = 0
                    except:
                        similarity[user1][user2] = 0
    return similarity


def similarity_matrix_item_to_item(data: np.array, keyword: str, N:int = 50) -> None:
    
    print("in similarity_matrix_item_to_item")
    
    ITEMS = len(data)
    similarity = np.zeros((ITEMS, ITEMS))
    data = user_item_data.T.to_numpy()
    
    for item1 in range(ITEMS):
        for item2 in range(ITEMS):
            if np.count_nonzero(data[item1]) and np.count_nonzero(data[item2]):
                if keyword == 'cosine':
                    similarity[item1][item2] = 1 - scipy.spatial.distance.cosine(data[item1], data[item2])
                elif keyword == 'jaccard':
                    similarity[item1][item2] = 1 - scipy.spatial.distance.jaccard(data[item1], data[item2])
                elif keyword == 'pearson':
                    try:
                        if not math.isnan(scipy.stats.pearsonr(data[item1],data[item2])[0]):
                            similarity[item1][item2] = scipy.stats.pearsonr(data[item1], data[item2])[0]
                        else:
                            similarity[item1][item2] = 0
                    except:
                        similarity[item1][item2] = 0
    return similarity


def user_based_prediction(user_item_data: pd.DataFrame, distance: str):
    print("in user_based_prediction")
    data = user_item_data.to_numpy()
    USERS, ITEMS = data.shape
    
    sim_user = similarity_matrix_user_to_user(data, distance)
    sim_user_df = pd.DataFrame(sim_user, index=user_item_data.index, columns=user_item_data.index)
    
    # selecting random user
    user = sim_user_df.index[random.randrange(len(sim_user_df))]
    user_sim = sim_user_df.iloc[user]
    
    # sort these user similarity values by similarity 
    user_sim.sort_values(ascending=False, inplace=True)
    
    # dropping na
    user_sim.dropna(inplace=True)
    
    # selecting top N users according to similarity 
    top_users = users_sim[1:N]

    # calculating user's ratings for all the movies
    ratings = []
    for movie in user_item_data.columns:
        count = 0
        users_who_voted = list()
        for user in top_users.keys():
            if user_item_data.loc[user, movie]:
                count += 1
                users_who_voted.append(user)
                
        sum_similarity = 0
        weighted_ratings = 0
        for user in users_who_voted:
            weighted_ratings += top_users[user] * user_item_data.loc[user, movie]
            sum_similarity += top_users[user]
            
        ratings.append(weighted_ratings / sum_similarity)
        
    ratings_df = pd.Series(ratings, index=user_item_data.columns)

    # sorting values according to ratings
    ratings_df.sort_values(ascending=False, inplace=True)
    
    # returning top N * 2 movies
    return ratings.index[:N * 2]


def item_based_prediction(user_item_data: pd.DataFrame, distance: str):
    print("in item_based_prediction")
    # selecting random user
    user = sim_user_df.index[random.randrange(len(sim_user_df))]
    
    # getting movies user rated
    movies = pd.DataFrame('./ml-latest-small/movies.csv')
    ratings = pd.DataFrame('./ml-latest-small/ratings.csv')
    main = pd.merge(ratings, movies, on="movieId")
    
    movies_user_rated = main[main['userId'] == user][['movieId', 'rating']]
    movies_to_rate = pd.Series(data=movies_user_rated['rating'], index=movies_user_rated['movieId'])
    
    # final container to hold the data
    rated_movies = {}
    
    data = user_item_data.to_numpy()
    USERS, ITEMS = data.shape
    
    items_to_rate = data.loc[data.index.get_loc(user)]
    
    sim_movies = similarity_matrix_user_to_user(data.T, distance)
    sim_movies_df = pd.DataFrame(sim_movies, index=user_item_data.columns, columns=user_item_data.columns)
    
    
    for movie in movies_to_rate.index:
        
        similar_movies = sim_movies_df.loc[movie]

        # sort these user similarity values by similarity 
        similar_movies.sort_values(ascending=False, inplace=True)

        # dropping na
        similar_movies.dropna(inplace=True)

        # selecting top N movies according to similarity 
        top_movies = similar_movies[1 : N]
        
        for movie, rating in top_movies.items():
            if movie in rated_movies:
                rated_movies[movie] = max(rating, rated_movies[movie])
            else:
                rated_movies[movie] = rating
        
        rated_movies_df = pd.Series(data=rated_movies.values(), index=rated_movies.keys())
        rated_movies_df.sort_values(ascending=False, inplace=True)

    # returning top N * 2 movies
    return rated_movies_df.index[:N * 2]



if __name__ == "__main__":
    # prestoring the similarties for all the cases
    user_item_df = pd.read_csv('./ml-latest-small/user_item.csv')
    for distance in ('cosine', 'jaccard', 'pearson'):
        print("getting user similarity for distance: ", distance)
        similarity = similarity_matrix_user_to_user(user_item_df.to_numpy(), distance)
        
        print("saving the user similarity csv for distance: ", distance)
        df = pd.DataFrame(similarity, index=user_item_df.index, columns=user_item_df.index)
        name = 'user-' + distance + '.csv' 
        df.to_csv(f'./ml-latest-small/{name}')
    
    
    for distance in ('cosine', 'jaccard', 'pearson'):
        print("getting items similarity for distance: ", distance)
        similarity = similarity_matrix_item_to_item(user_item_df.T.to_numpy(), distance)
        
        print("saving the items similarity csv for distance: ", distance)
        df = pd.DataFrame(similarity, index=user_item_df.columns, columns=user_item_df.columns)
        name = 'item-' + distance + '.csv' 
        df.to_csv(f'./ml-latest-small/{name}')
    
    
