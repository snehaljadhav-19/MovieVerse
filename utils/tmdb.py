


import requests
import streamlit as st

# ==========================================================
# TMDB CONFIGURATION
# ==========================================================
API_KEY = st.secrets["TMDB_API_KEY"]

BASE_URL = "https://api.themoviedb.org/3"

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/original"


# ==========================================================
# MOVIE DETAILS
# ==========================================================

@st.cache_data(show_spinner=False)
def get_movie_details(movie_id):
    """
    Fetch complete movie details from TMDB.
    """

    try:

        url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}"

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return None


# ==========================================================
# MOVIE POSTER
# ==========================================================

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    """
    Returns poster URL.
    """

    movie = get_movie_details(movie_id)

    if movie and movie.get("poster_path"):

        return f"{IMAGE_BASE_URL}{movie['poster_path']}"

    return "https://via.placeholder.com/500x750?text=No+Poster"


# ==========================================================
# MOVIE BACKDROP
# ==========================================================

@st.cache_data(show_spinner=False)
def fetch_backdrop(movie_id):
    """
    Returns backdrop image URL.
    """

    movie = get_movie_details(movie_id)

    if movie and movie.get("backdrop_path"):

        return f"{BACKDROP_BASE_URL}{movie['backdrop_path']}"

    return None


# ==========================================================
# OFFICIAL TRAILER
# ==========================================================

@st.cache_data(show_spinner=False)
def get_trailer(movie_id):
    """
    Returns YouTube trailer URL.
    """

    try:

        url = f"{BASE_URL}/movie/{movie_id}/videos?api_key={API_KEY}"

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        videos = response.json().get("results", [])

        # Official Trailer

        for video in videos:

            if (
                video.get("site") == "YouTube"
                and video.get("type") == "Trailer"
                and video.get("official")
            ):

                return f"https://www.youtube.com/watch?v={video['key']}"

        # Any Trailer

        for video in videos:

            if (
                video.get("site") == "YouTube"
                and video.get("type") == "Trailer"
            ):

                return f"https://www.youtube.com/watch?v={video['key']}"

        # Any YouTube Video

        for video in videos:

            if video.get("site") == "YouTube":

                return f"https://www.youtube.com/watch?v={video['key']}"

    except requests.RequestException:

        return None

    return None


# ==========================================================
# CAST & DIRECTOR
# ==========================================================

@st.cache_data(show_spinner=False)
def get_cast_and_director(movie_id):
    """
    Returns director and top cast.
    """

    try:

        url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        director = "Not Available"

        for crew in data.get("crew", []):

            if crew.get("job") == "Director":

                director = crew.get("name")

                break

        cast = []

        for actor in data.get("cast", [])[:8]:

            cast.append(
                {
                    "name": actor.get("name"),
                    "character": actor.get("character", ""),
                    "photo": (
                        f"{IMAGE_BASE_URL}{actor['profile_path']}"
                        if actor.get("profile_path")
                        else None
                    )
                }
            )

        return {
            "director": director,
            "cast": cast
        }

    except requests.RequestException:

        return None


# ==========================================================
# SIMILAR MOVIES
# ==========================================================

@st.cache_data(show_spinner=False)
def get_similar_movies(movie_id):
    """
    Returns similar movies.
    """

    try:

        url = f"{BASE_URL}/movie/{movie_id}/similar?api_key={API_KEY}"

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        results = response.json().get("results", [])[:10]

        movies = []

        for movie in results:

            poster = None

            if movie.get("poster_path"):

                poster = f"{IMAGE_BASE_URL}{movie['poster_path']}"

            year = "N/A"

            if movie.get("release_date"):

                year = movie["release_date"][:4]

            movies.append(
                {
                    "id": movie.get("id"),
                    "title": movie.get("title"),
                    "poster": poster,
                    "rating": round(
                        movie.get("vote_average", 0),
                        1
                    ),
                    "year": year
                }
            )

        return movies

    except requests.RequestException:

        return []


# ==========================================================
# FORMAT RUNTIME
# ==========================================================

def format_runtime(runtime):
    """
    Converts minutes to '2h 15m'
    """

    if runtime is None:

        return "N/A"

    hours = runtime // 60

    minutes = runtime % 60

    return f"{hours}h {minutes}m"
