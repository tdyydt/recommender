import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# Global variables

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


def find_neighbors(aid):
    # 近いアニメを探す
    the_anime = anime_user_mat.loc[aid].values.reshape(1,-1)  # 2dにする必要あり
    xss, yss = model_knn.kneighbors(the_anime, n_neighbors=11)  # 距離/index

    # loop over kneighbors
    for j, (dist, ind) in enumerate(zip(xss.flatten(), yss.flatten())):
        # nearest anime should be itself
        if j == 0: assert(anime_index_to_id(ind) == aid)
        else:
            aid_ngigh = anime_index_to_id(ind)
            print(aid_neigh, anime_id_to_name(aid_neigh))

# anime_user行列のindex(行番号)に対応するanime_idを返す
def anime_index_to_id(ind):
    # ここではnameがanime_idに対応
    return anime_user_mat.iloc[ind].name

# anime_idに対応する，アニメのタイトル(ローマ字)を返す
def anime_id_to_name(aid):
    return df_anime[df_anime.anime_id==aid].name.values[0]

if __name__ == '__main__':
    # TODO: input anime id
    find_neighbors(27989)
