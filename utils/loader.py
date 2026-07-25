import pickle
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_resource
def load_models():
    try:
        with open("models/movies.pkl", "rb") as f:
            movies = pickle.load(f)

        with open("models/vectorizer.pkl", "rb") as f:
            cv = pickle.load(f)

        vectors = cv.transform(movies["tags"]).toarray()
        similarity = cosine_similarity(vectors)

        return movies, similarity

    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()