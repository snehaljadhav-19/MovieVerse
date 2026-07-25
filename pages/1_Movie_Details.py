import streamlit as st

from utils.tmdb import (
    get_movie_details,
    get_trailer,
    get_similar_movies,
    get_cast_and_director
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="🎬 Movie Details",
    page_icon="🎬",
    layout="wide"
)

# ==========================================================
# LOAD CSS
# ==========================================================

try:
    with open("css/style.css") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

# ==========================================================
# CHECK SESSION
# ==========================================================

if "selected_movie_id" not in st.session_state:

    st.warning("No movie selected.")

    if st.button("⬅ Back Home"):

        st.switch_page("app.py")

    st.stop()

movie_id = st.session_state.selected_movie_id

movie = get_movie_details(movie_id)

if movie is None:

    st.error("Movie details not found.")

    if st.button("⬅ Back Home"):

        st.switch_page("app.py")

    st.stop()

# ==========================================================
# BACK BUTTON
# ==========================================================

if st.button(
    "⬅ Back to Recommendations",
    width="stretch"
):

    st.switch_page("app.py")

# ==========================================================
# HERO BANNER
# ==========================================================

backdrop = movie.get("backdrop_path")

if backdrop:

    st.image(
        f"https://image.tmdb.org/t/p/original{backdrop}",
        width="stretch"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# MAIN DETAILS
# ==========================================================

left, right = st.columns([1, 2])

with left:

    poster = movie.get("poster_path")

    if poster:

        st.image(
            f"https://image.tmdb.org/t/p/w500{poster}",
            width="stretch"
        )

with right:

    st.title(movie.get("title", "Unknown Movie"))

    tagline = movie.get("tagline")

    if tagline:
        st.caption(tagline)

    st.write(
        movie.get(
            "overview",
            "Overview not available."
        )
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "⭐ Rating",
            f"{movie.get('vote_average',0):.1f}"
        )

    with c2:

        release = movie.get(
            "release_date",
            "N/A"
        )

        if release:
            release = release[:4]

        st.metric(
            "📅 Year",
            release
        )

    with c3:

        runtime = movie.get("runtime")

        if runtime:
            runtime = f"{runtime} min"
        else:
            runtime = "N/A"

        st.metric(
            "⏱ Runtime",
            runtime
        )

    # --------------------------------------------

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
padding:8px;
border-radius:20px;
text-align:center;
font-weight:bold;
color:white;
">
{genre['name']}
</div>
""",
                    unsafe_allow_html=True
                )

    # --------------------------------------------

    st.markdown("### 🌍 Language")

    st.write(
        movie.get(
            "original_language",
            "N/A"
        ).upper()
    )

    credits = get_cast_and_director(movie["id"])

    if credits:

        st.markdown("### 🎬 Director")

        st.success(
            credits["director"]
        )

        st.markdown("### 👨‍👩‍👧‍👦 Cast")

        cast_cols = st.columns(4)

        for i, actor in enumerate(credits["cast"]):

            with cast_cols[i % 4]:

                st.info(actor)

    companies = movie.get(
        "production_companies",
        []
    )

    if companies:

        st.markdown("### 🏢 Production")

        st.write(
            ", ".join(
                company["name"]
                for company in companies
            )
        )

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

    for i, similar in enumerate(similar_movies[:10]):

        with cols[i % 5]:

            poster = similar.get("poster")

            if poster:

                st.image(
                    poster,
                    width="stretch"
                )

            st.markdown(
                f"**{similar['title']}**"
            )

            rating = similar.get("rating")

            if rating:

                st.caption(f"⭐ {rating}")

else:

    st.info("No similar movies found.")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    """
<div style="text-align:center;padding:20px;color:#888;">

<h3>🎬 MovieVerse</h3>

<p>
Powered by TMDB API • Streamlit • Python
</p>

</div>
""",
    unsafe_allow_html=True
)
