import streamlit as st
import os
from models.similarity import load_data, get_similarity_model, recommend_item_based

st.set_page_config(page_title="Item Engine", page_icon="📦", layout="wide")
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📦 Item-Based Filtering")

matrix, items, _ = load_data()

if matrix is not None:
    # Create a mapping for Dropdown
    item_ids = list(matrix.columns)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_item = st.selectbox("Select Source Product ID", item_ids[:50])
        n_recs = st.slider("Similar Items", 1, 10, 5)
        
    if st.button("Find Similar Products"):
        with st.spinner("Scanning Vector Space..."):
            item_sim = get_similarity_model(matrix, 'item')
            recs = recommend_item_based(selected_item, item_sim, items, n_recs)
            
        st.write(f"**Customers who bought Item #{selected_item} also bought:**")
        st.dataframe(recs, use_container_width=True, hide_index=True)
