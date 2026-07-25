import pandas as pd
import ast
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk.stem.porter import PorterStemmer

# ==========================================
# LOAD DATA
# ==========================================

movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# ==========================================
# MERGE DATASETS
# ==========================================

movies = movies.merge(credits, on="title")

# ==========================================
# SELECT REQUIRED COLUMNS
# ==========================================

movies = movies[
    [
        "movie_id",
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "crew",
        "vote_average",
        "release_date"
    ]
]

# ==========================================
# REMOVE MISSING VALUES
# ==========================================

movies.dropna(inplace=True)

# ==========================================
# FUNCTIONS
# ==========================================

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i["name"])
    return L


def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter != 3:
            L.append(i["name"])
            counter += 1
        else:
            break
    return L


def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i["job"] == "Director":
            L.append(i["name"])
            break
    return L


# ==========================================
# APPLY FUNCTIONS
# ==========================================

movies["genres"] = movies["genres"].apply(convert)

movies["keywords"] = movies["keywords"].apply(convert)

movies["cast"] = movies["cast"].apply(convert3)

movies["crew"] = movies["crew"].apply(fetch_director)

# ==========================================
# CLEAN OVERVIEW
# ==========================================

movies["overview"] = movies["overview"].apply(lambda x: x.split())

# ==========================================
# REMOVE SPACES
# ==========================================

movies["genres"] = movies["genres"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["keywords"] = movies["keywords"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["cast"] = movies["cast"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["crew"] = movies["crew"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

# ==========================================
# CREATE TAGS
# ==========================================

movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

# ==========================================
# CREATE NEW DATAFRAME
# ==========================================

new_df = movies[
    [
        "movie_id",
        "title",
        "overview",
        "vote_average",
        "release_date",
        "tags"
    ]
].copy()

# ==========================================
# CONVERT TAGS TO STRING
# ==========================================

new_df["tags"] = new_df["tags"].apply(
    lambda x: " ".join(x)
)

new_df["tags"] = new_df["tags"].apply(
    lambda x: x.lower()
)

# ==========================================
# STEMMING
# ==========================================

ps = PorterStemmer()


def stem(text):
    return " ".join(
        [ps.stem(word) for word in text.split()]
    )


new_df["tags"] = new_df["tags"].apply(stem)

# ==========================================
# VECTORIZATION
# ==========================================

cv = CountVectorizer(
    max_features=5000,
    stop_words="english"
)

vectors = cv.fit_transform(
    new_df["tags"]
).toarray()

# ==========================================
# COSINE SIMILARITY
# ==========================================

similarity = cosine_similarity(vectors)

# ==========================================
# SAVE FILES
# ==========================================

pickle.dump(
    new_df,
    open("models/movies.pkl", "wb")
)

pickle.dump(
    similarity,
    open("models/similarity.pkl", "wb")
)

print("✅ Model files saved successfully!")