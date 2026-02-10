import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from models.similarity import load_data, get_similarity_model
import numpy as np
import os

st.set_page_config(page_title="Model Performance", page_icon="📈", layout="wide")
style_path = os.path.join(os.path.dirname(__file__), "../assets/style.css")
with open(style_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📈 Model Performance Dashboard")
st.markdown("Evaluate the performance of our collaborative filtering recommendation models.")

matrix, items, interactions = load_data()

if matrix is not None and interactions is not None:
    # Compute similarity models
    user_sim = get_similarity_model(matrix, kind='user')
    item_sim = get_similarity_model(matrix, kind='item')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Matrix Statistics")
        sparsity = (matrix == 0).sum().sum() / (matrix.shape[0] * matrix.shape[1]) * 100
        st.metric("Matrix Sparsity", f"{sparsity:.1f}%")
        st.metric("Active Users", f"{(matrix > 0).any(axis=1).sum()}")
        st.metric("Active Items", f"{(matrix > 0).any(axis=0).sum()}")
    
    with col2:
        st.subheader("User Similarity Distribution")
        user_sim_values = user_sim.values[np.triu_indices_from(user_sim.values, k=1)]
        fig = px.histogram(user_sim_values, nbins=50, title="User-User Similarity Scores")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.subheader("Item Similarity Distribution")
        item_sim_values = item_sim.values[np.triu_indices_from(item_sim.values, k=1)]
        fig = px.histogram(item_sim_values, nbins=50, title="Item-Item Similarity Scores")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Top Similar Pairs")
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("**Top User Pairs**")
        # Get top similar user pairs
        user_sim.index.name = 'User 1'
        user_sim.columns.name = 'User 2'
        user_sim_flat = user_sim.where(np.triu(np.ones_like(user_sim), k=1).astype(bool))
        top_users = user_sim_flat.stack().nlargest(5).reset_index(name='Similarity')
        st.dataframe(top_users)
    
    with col5:
        st.markdown("**Top Item Pairs**")
        # Get top similar item pairs
        item_sim.index.name = 'Item 1'
        item_sim.columns.name = 'Item 2'
        item_sim_flat = item_sim.where(np.triu(np.ones_like(item_sim), k=1).astype(bool))
        top_items = item_sim_flat.stack().nlargest(5).reset_index(name='Similarity')
        st.dataframe(top_items)
    
    st.subheader("Recommendation Coverage Analysis")
    # Simulate coverage: for a sample of users, check how many recommendations we can generate
    sample_users = matrix.index[:min(100, len(matrix.index))]
    coverage = 0
    total_possible = 0
    
    for user in sample_users:
        user_recs = (matrix.loc[user] == 0).sum()  # Items not interacted
        total_possible += user_recs
        # In practice, we'd check if sim users exist, but for simplicity
        if user in user_sim.index:
            coverage += user_recs
    
    coverage_pct = (coverage / total_possible * 100) if total_possible > 0 else 0
    st.metric("Recommendation Coverage", f"{coverage_pct:.1f}%")
    
    st.info("**Note:** This dashboard shows descriptive statistics of the similarity models. For full evaluation, a test set with ground truth ratings would be needed.")
else:
    st.error("⚠️ Data Not Found! Please run `setup_data.py` and ensure CSVs are in `data/` folder.")
