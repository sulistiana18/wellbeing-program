import streamlit as st
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Activity Summary", layout="wide")

df = load_data()

st.markdown("""
<style>
.block-container {padding: 1rem;}
h1 {font-size: 20px !important;}
div[data-testid="metric-container"]{
    background:white;
    border:1px solid #e2e8f0;
    padding:8px !important;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.title("Activity Summary")

# KPI
c1, c2, c3, c4 = st.columns(4)

c1.metric("Activities", df["activity_id"].count())
c2.metric("Distance", round(df["distance"].sum(), 2))
c3.metric("Avg HR", round(df["average_heartrate"].mean(), 1))
c4.metric("Types", df["type"].nunique())

st.divider()

# CHARTS
c1, c2 = st.columns(2)

with c1:
    fig = px.line(df, x="start_date_local", y="distance", color="type")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.plotly_chart(px.pie(df, names="type"), use_container_width=True)