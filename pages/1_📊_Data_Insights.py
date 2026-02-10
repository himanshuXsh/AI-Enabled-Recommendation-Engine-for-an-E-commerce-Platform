import streamlit as st
import pandas as pd
import plotly.express as px
import os
from models.similarity import load_data

st.set_page_config(page_title="Data Insights", page_icon="📊", layout="wide")
style_path = os.path.join(os.path.dirname(__file__), "../assets/style.css")
with open(style_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📊 Data Analytics Dashboard")
matrix, items, interactions = load_data()

if interactions is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Event Distribution")
        event_counts = interactions['event'].value_counts().reset_index()
        event_counts.columns = ['Event Type', 'Count']
        fig = px.pie(event_counts, values='Count', names='Event Type', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Traffic Over Time")
        # Ensure timestamp is datetime
        interactions['timestamp'] = pd.to_datetime(interactions['timestamp'], unit='ms')
        daily_traffic = interactions.set_index('timestamp').resample('D').size()
        fig2 = px.line(daily_traffic, labels={'value': 'Interactions', 'timestamp': 'Date'})
        fig2.update_traces(line_color='#58a6ff')
        st.plotly_chart(fig2, use_container_width=True)
