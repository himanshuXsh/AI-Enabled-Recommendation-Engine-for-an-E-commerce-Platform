import streamlit as st
import os
from models.similarity import load_data, get_similarity_model, recommend_user_based

st.set_page_config(page_title="User Engine", page_icon="👤", layout="wide")
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("👤 User-Based Collaborative Filtering")

matrix, items, _ = load_data()

if matrix is not None:
    with st.sidebar:
        st.header("Control Panel")
        user_list = list(matrix.index)
        selected_user = st.selectbox("Select User ID", user_list[:50])
        n_recs = st.slider("Recommendations", 1, 20, 5)

    if st.button("Generate Suggestions"):
        with st.spinner("Computing User Similarity Vectors..."):
            user_sim = get_similarity_model(matrix, 'user')
            recs = recommend_user_based(selected_user, matrix, user_sim, items, n_recs)
            
        if not recs.empty:
            st.success(f"Top {n_recs} Recommendations for User {selected_user}")
            st.dataframe(recs, use_container_width=True, hide_index=True)
        else:
            st.warning("No recommendations available (User may have seen all items or has no history).")
