import pandas as pd
import numpy as np

df_anime = pd.read_csv('anime.csv')

# anime_idに対応する，アニメのタイトル(ローマ字)を返す
def anime_id_to_name(aid):
    return df_anime[df_anime.anime_id==aid].name.values[0]

# queryをタイトルに含むようなアニメを探す
def find_anime_contains(query):
    df_narrowed = df_anime[df_anime.name.str.contains(query, case=False)]
    print(f'There are {len(df_narrowed)} results.')
    for i, (_, row) in enumerate(df_narrowed.iterrows()):
        if i >= 10: break
        print(f"{row['anime_id']} => {row['name']}")


if __name__ == '__main__':
    while True:
        query = input('Enter query: ')
        find_anime_contains(query)
