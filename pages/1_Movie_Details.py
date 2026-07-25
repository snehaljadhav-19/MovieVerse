import streamlit as st

from utils.tmdb import (
    get_movie_details,
    get_trailer,
    get_similar_movies,
    get_cast_and_director,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="🎬 Movie Details",
    page_icon="🎬",
    layout="wide",
)

# ==========================================================
# LOAD CSS
# ==========================================================

try:
    with open("css/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# ==========================================================
# SESSION CHECK
# ==========================================================

if "selected_movie_id" not in st.session_state:
    st.warning("Please select a movie first.")

    if st.button("⬅ Back Home"):
        st.switch_page("app.py")

    st.stop()

movie_id = st.session_state.selected_movie_id

movie = get_movie_details(movie_id)

if not movie:
    st.error("Movie details could not be loaded.")

    if st.button("⬅ Back Home"):
        st.switch_page("app.py")

    st.stop()

# ==========================================================
# BACK BUTTON
# ==========================================================

if st.button("⬅ Back to Recommendations"):
    st.switch_page("app.py")

# ==========================================================
# HERO BACKDROP
# ==========================================================

backdrop = movie.get("backdrop_path")

if backdrop:
    st.image(
        f"https://image.tmdb.org/t/p/original{backdrop}",
        width="stretch",
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# MAIN LAYOUT
# ==========================================================

poster_col, details_col = st.columns([1, 2])

with poster_col:

    poster = movie.get("poster_path")

    if poster:
        st.image(
            f"https://image.tmdb.org/t/p/w500{poster}",
            width="stretch",
        )
with details_col:

    # ==========================================================
    # TITLE
    # ==========================================================

    st.title(movie.get("title", "Unknown Movie"))

    tagline = movie.get("tagline")

    if tagline:
        st.caption(tagline)

    st.markdown("### 📝 Overview")

    st.write(
        movie.get(
            "overview",
            "Overview not available."
        )
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # MOVIE STATS
    # ==========================================================

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "⭐ Rating",
            f"{movie.get('vote_average', 0):.1f}"
        )

    with c2:

        release = movie.get(
            "release_date",
            "N/A"
        )

        year = release[:4] if release else "N/A"

        st.metric(
            "📅 Year",
            year
        )

    with c3:

        runtime = movie.get("runtime")

        runtime_text = (
            f"{runtime} min"
            if runtime
            else "N/A"
        )

        st.metric(
            "⏱ Runtime",
            runtime_text
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # GENRES
    # ==========================================================

    genres = movie.get("genres", [])

    if genres:

        st.markdown("### 🎭 Genres")

        genre_cols = st.columns(len(genres))

        for col, genre in zip(genre_cols, genres):

            with col:

                st.markdown(
                    f"""
<div style="
background:#E50914;
padding:10px;
border-radius:25px;
text-align:center;
font-weight:bold;
color:white;
margin-bottom:10px;
">
{genre['name']}
</div>
""",
                    unsafe_allow_html=True
                )

    # ==========================================================
    # LANGUAGE
    # ==========================================================

    st.markdown("### 🌍 Original Language")

    st.success(
        movie.get(
            "original_language",
            "N/A"
        ).upper()
    )

    # ==========================================================
    # DIRECTOR
    # ==========================================================

    credits = get_cast_and_director(movie["id"])

    if credits:

        st.markdown("### 🎬 Director")

        st.success(
            credits.get(
                "director",
                "Unknown"
            )
        )

# ==========================================================
# CAST
# ==========================================================

if credits:

    st.markdown("### 👨‍👩‍👧‍👦 Cast")

    cast = credits.get("cast", [])

    if cast:

        cols = st.columns(4)

        for index, actor in enumerate(cast):

            with cols[index % 4]:

                # Actor Photo
                if actor.get("photo"):

                    st.image(
                        actor["photo"],
                        width="stretch"
                    )

                else:

                    st.image(
                        "https://via.placeholder.com/300x450?text=No+Photo",
                        width="stretch"
                    )

                # Actor Name
                st.markdown(
                    f"""
<div style="
text-align:center;
font-weight:bold;
font-size:16px;
padding-top:8px;
">
{actor['name']}
</div>
""",
                    unsafe_allow_html=True
                )

                # Character
                character = actor.get("character")

                if character:

                    st.caption(
                        f"as {character}"
                    )

# ==========================================================
# PRODUCTION
# ==========================================================

companies = movie.get(
    "production_companies",
    []
)

if companies:

    st.markdown("---")

    st.markdown("### 🏢 Production Companies")

    for company in companies:

        st.success(company["name"])

# ==========================================================
# TRAILER
# ==========================================================

st.markdown("---")

st.header("🎥 Official Trailer")

trailer = get_trailer(movie["id"])

if trailer:
    st.video(trailer)
else:
    st.info("Trailer not available.")

# ==========================================================
# SIMILAR MOVIES
# ==========================================================

st.markdown("---")

st.header("🍿 Similar Movies")

similar_movies = get_similar_movies(movie["id"])

if similar_movies:

    cols = st.columns(5)

    for index, similar in enumerate(similar_movies[:10]):

        with cols[index % 5]:

            if similar.get("poster"):

                st.image(
                    similar["poster"],
                    width="stretch"
                )

            st.markdown(
                f"#### {similar['title']}"
            )

            if similar.get("rating") is not None:

                st.caption(
                    f"⭐ {similar['rating']}"
                )

            if st.button(
                "View Details",
                key=f"similar_{similar['id']}"
            ):

                st.session_state.selected_movie_id = similar["id"]
                st.rerun()

else:

    st.info("No similar movies found.")

# ==========================================================
# MOVIE INFORMATION
# ==========================================================

st.markdown("---")

st.header("📊 Movie Information")

col1, col2 = st.columns(2)

with col1:

    st.write(
        "**Status:**",
        movie.get("status", "N/A")
    )

    st.write(
        "**Release Date:**",
        movie.get("release_date", "N/A")
    )

    st.write(
        "**Original Title:**",
        movie.get("original_title", "N/A")
    )

with col2:

    budget = movie.get("budget", 0)

    revenue = movie.get("revenue", 0)

    if budget:
        st.write(
            "**Budget:**",
            f"${budget:,.0f}"
        )

    if revenue:
        st.write(
            "**Revenue:**",
            f"${revenue:,.0f}"
        )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    """
<div style="
text-align:center;
padding:20px;
color:#888;
">

<h2>🎬 MovieVerse</h2>

<p>
Powered by TMDB API • Streamlit • Python
</p>

<p style="font-size:14px;">
Made with ❤️ by Snehal Jadhav
</p>

</div>
""",
    unsafe_allow_html=True
)