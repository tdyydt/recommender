# Recommender

Anime recommender by k-nearest neighbors algorithm (KNN).

## Usage

Download `rating.csv` and `anime.csv`
from [Anime Recommendations Database](https://www.kaggle.com/CooperUnion/anime-recommendations-database) in kaggle.

- `python3 recommender.py`
  + Find the animes similar to the given anime.
  + (It takes a few minutes to train the model.)
- `python3 anime.py`
  + Find the ids of animes that contain the given keyword in the title.
  + (This is meant to help you find anime ids.)

Alternatively, see [sample.md](sample.md) for sample usage.

## Links

Inspired by [this post](https://www.codexa.net/collaborative-filtering-k-nearest-neighbor/). (I made several changes from this.)
