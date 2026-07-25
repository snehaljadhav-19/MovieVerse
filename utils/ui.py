import streamlit as st
from utils.tmdb import get_movie_details


def movie_card(movie):

    match = min(movie["match"], 100)

    with st.container(border=True):

        if movie.get("poster"):
            st.image(
                movie["poster"],
                width="stretch"
            )
        else:
            st.image(
                "https://via.placeholder.com/500x750?text=No+Poster",
                width="stretch"
            )

        st.markdown(
            f"""
            <h4 style="text-align:center;">
            {movie['title']}
            </h4>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "⭐ Rating",
                f"{movie['rating']:.1f}"
            )

        with col2:
            st.metric(
                "📅 Year",
                movie["year"]
            )

        st.caption("🎯 Recommendation Match")
        st.progress(match / 100)
        st.caption(f"{match:.1f}% Match")

        if st.button(
            "🎬 View Details",
            key=f"movie_{movie['movie_id']}"
        ):

            st.session_state.selected_movie_id = movie["movie_id"]
            st.switch_page("pages/1_Movie_Details.py")