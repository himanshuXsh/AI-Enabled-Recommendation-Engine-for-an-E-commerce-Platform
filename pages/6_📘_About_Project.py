import streamlit as st
import os

st.set_page_config(page_title="About", page_icon="📘")
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📘 Project Documentation")

st.markdown("""
### 🧠 Architecture Overview
This system uses **Collaborative Filtering** to predict user preferences.

1.  **Data Ingestion**: Raw interaction logs are processed into a User-Item Matrix.
2.  **Vectorization**: Users and Items are represented as high-dimensional vectors.
3.  **Similarity Search**: Cosine Similarity is used to find nearest neighbors.
4.  **Ranking**: Recommendations are ranked by confidence scores.

### 🛠️ Tech Stack
-   **Frontend**: Streamlit (Python)
-   **Backend Logic**: Scikit-Learn, Pandas
-   **Visualization**: Plotly Express
""")
