from utils.tmdb import fetch_poster


def recommend(movie_title, movies, similarity):
    try:
        movie_index = movies[
            movies["title"] == movie_title
        ].index[0]

    except IndexError:
        return []

    distances = list(
        enumerate(similarity[movie_index])
    )

    distances = sorted(
        distances,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for movie_id, score in distances[1:21]:

        movie = movies.iloc[movie_id]

        poster = fetch_poster(
            movie["movie_id"]
        )

        recommendations.append(
            {
                "movie_id": movie["movie_id"],
                "title": movie["title"],
                "poster": poster,
                "rating": float(
                    movie.get(
                        "vote_average",
                        0
                    )
                ),
                "year": (
                    str(
                        movie.get(
                            "release_date",
                            ""
                        )
                    )[:4]
                    if movie.get(
                        "release_date"
                    )
                    else "N/A"
                ),
                "match": round(
                    score * 100,
                    1
                )
            }
        )

    return recommendations