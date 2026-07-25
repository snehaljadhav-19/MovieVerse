import pandas as pd

# Load datasets
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Display first 5 rows
print("=" * 60)
print("MOVIES DATASET")
print("=" * 60)
print(movies.head())

print("\nMovies Shape:", movies.shape)

print("\nMovies Columns:")
print(movies.columns)

print("\n" + "=" * 60)
print("CREDITS DATASET")
print("=" * 60)
print(credits.head())

print("\nCredits Shape:", credits.shape)

print("\nCredits Columns:")
print(credits.columns)