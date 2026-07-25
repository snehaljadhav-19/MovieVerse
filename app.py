import streamlit as st
from streamlit_searchbox import st_searchbox

from utils.loader import load_models
from utils.recommender import recommend
from utils.ui import movie_card

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="🎬 MovieVerse",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
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
except FileNotFoundError:
    pass

# ==========================================================
# LOAD MODEL
# ==========================================================

movies, similarity = load_models()

# ==========================================================
# SESSION STATE
# ==========================================================

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

if "selected_movie_id" not in st.session_state:
    st.session_state.selected_movie_id = None

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🎬 MovieVerse")

    st.markdown("### About")

    st.write("""
MovieVerse is an AI-powered
Movie Recommendation System
using Content-Based Filtering.
""")

    st.markdown("---")

    st.markdown("### Features")

    st.markdown("""
🎬 Smart Recommendations

⭐ Ratings

🎥 Trailers

👨‍👩‍👧‍👦 Cast

🎭 Genres

🍿 Similar Movies
""")

# ==========================================================
# HERO
# ==========================================================

st.markdown("""
<div class="hero">

<h1>🎬 MovieVerse</h1>

<p>
Discover your next favourite movie
with AI-powered recommendations.
</p>

</div>
""",
unsafe_allow_html=True)

# ==========================================================
# SEARCH
# ==========================================================

def search_movies(searchterm):

    if not searchterm:
        return []

    filtered = movies[
        movies["title"].str.contains(
            searchterm,
            case=False,
            na=False
        )
    ]

    return (
        filtered["title"]
        .drop_duplicates()
        .sort_values()
        .head(15)
        .tolist()
    )

selected_movie = st_searchbox(
    search_function=search_movies,
    placeholder="🔍 Search for a movie...",
    label="",
    key="movie_search"
)

if not selected_movie:

    st.info("👆 Search for a movie to begin.")

    st.stop()

# ==========================================================
# RECOMMEND BUTTON
# ==========================================================

recommend_button = st.button(
    "✨ Find Similar Movies",
    width="stretch"
)

if recommend_button:

    with st.spinner("Finding recommendations..."):

        recommendations = recommend(
            selected_movie,
            movies,
            similarity
        )

        st.session_state.recommendations = recommendations

recommendations = st.session_state.recommendations

# ==========================================================
# RECOMMENDATIONS
# ==========================================================

if recommendations:

    st.success(
        f"🎯 Found {len(recommendations)} recommendations"
    )

    st.markdown("""
    <h2 style="margin-top:25px;">
    🍿 Recommended For You
    </h2>
    """,
    unsafe_allow_html=True)

    # --------------------------------------------------

    for i in range(0, len(recommendations), 5):

        cols = st.columns(5)

        for col, movie in zip(
            cols,
            recommendations[i:i+5]
        ):

            with col:

                movie_card(movie)

    # --------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <h2>
    📊 MovieVerse Statistics
    </h2>
    """,
    unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🎬 Movies",
            len(movies)
        )

    with c2:

        st.metric(
            "🍿 Recommendations",
            len(recommendations)
        )

    with c3:

        st.metric(
            "🤖 AI Engine",
            "Cosine Similarity"
        )

else:

    st.info(
        "Search for a movie and click 'Find Similar Movies' to get recommendations."
    )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    """
<div style="text-align:center;padding:25px;color:#999;">

<h2 style="color:white;">
🎬 MovieVerse
</h2>

<p>
AI-Powered Movie Recommendation System
</p>

<p>
Built with ❤️ using
<b>Python</b> •
<b>Streamlit</b> •
<b>Scikit-Learn</b> •
<b>TMDB API</b>
</p>

</div>
""",
    unsafe_allow_html=True
)