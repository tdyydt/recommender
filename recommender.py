import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from anime import anime_id_to_name

# Global variables:

df_rating = pd.read_csv('rating.csv')
# Ignore rating=-1 (watched, but didn't rate)
df_rating = df_rating[df_rating.rating >= 0].drop_duplicates(['user_id','anime_id'], keep=False)

# Make (anime, user-rating) matrix
# rating=0 if the user didn't watch the anime.
anime_user_mat = df_rating.pivot(index='anime_id',columns='user_id',values='rating').fillna(0)
# scipy sparse matrix
anime_user_csr = csr_matrix(anime_user_mat)

# Train KNN model
neigh = NearestNeighbors(n_neighbors=9, algorithm='brute', metric='cosine')
model_knn = neigh.fit(anime_user_csr)


# Given anime_id (aid), print relevant animes.
def find_neighbors(aid):
    # 近いアニメを探す
    the_anime = anime_user_mat.loc[aid].values.reshape(1,-1)  # 2dにする必要あり
    xss, yss = model_knn.kneighbors(the_anime, n_neighbors=11)  # 距離/index

    print(f'The users who like "{anime_id_to_name(aid)}" also like...')

    # loop over kneighbors
    for j, (dist, ind) in enumerate(zip(xss.flatten(), yss.flatten())):
        # nearest anime should be itself
        if j == 0: assert(anime_index_to_id(ind) == aid)
        else:
            aid_neigh = anime_index_to_id(ind)
            print(f'{aid_neigh} => {anime_id_to_name(aid_neigh)}')
    print()

# anime_user行列のindex(行番号)に対応するanime_idを返す
def anime_index_to_id(ind):
    # ここではnameがanime_idに対応
    return anime_user_mat.iloc[ind].name


if __name__ == '__main__':
    while True:
        try:
            anime_id = int(input('Enter anime id: '))
            find_neighbors(anime_id)
        except ValueError:
            print('Invalid input.')
        except KeyError:
            print('KeyError (e.g. the given id was not found)')
