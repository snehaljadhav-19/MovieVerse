import pickle
import streamlit as st


@st.cache_resource
def load_models():
    try:
        with open("models/movies.pkl", "rb") as file:
            movies = pickle.load(file)

        with open("models/similarity.pkl", "rb") as file:
            similarity = pickle.load(file)

        return movies, similarity

    except FileNotFoundError:
        st.error(
            "Model files not found. Please run train_model.py first."
        )
        st.stop()

    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()