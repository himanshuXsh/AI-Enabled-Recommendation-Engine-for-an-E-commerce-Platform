import streamlit as st
import os
from models.similarity import load_data

st.set_page_config(page_title="AI Retail Engine", page_icon="🛍️", layout="wide")

# CSS Loader
css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🛍️ AI-Powered Retail Intelligence")
st.markdown("### Enterprise Recommendation System")
st.divider()

matrix, items, interactions = load_data()

if matrix is not None:
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Users", f"{matrix.shape[0]:,}")
    col2.metric("Inventory Size", f"{matrix.shape[1]:,}")
    col3.metric("Total Interactions", f"{interactions.shape[0]:,}")
    col4.metric("System Health", "🟢 Optimal")
    
    st.subheader("🚀 Quick Actions")
    c1, c2 = st.columns(2)
    with c1:
        st.info("**👤 User Recommendations**\n\nMimic specific user profiles and see what the AI suggests for them.")
    with c2:
        st.info("**📦 Item Similarity**\n\nFind 'Frequently Bought Together' items using product embeddings.")
else:
    st.error("⚠️ Data Not Found! Please run `setup_data.py` and ensure CSVs are in `data/` folder.")
