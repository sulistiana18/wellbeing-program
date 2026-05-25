import streamlit as st
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="MCU Summary", layout="wide")

df = load_data()

st.title("MCU Summary")

# KPI
c1, c2, c3, c4 = st.columns(4)

c1.metric("Avg BMI", round(df["BMI"].mean(), 2))
c2.metric("High BMI", (df["BMI"] > 25).sum())
c3.metric("Avg Cholesterol", round(df["cholesterol"].mean(), 1))
c4.metric("Avg Glucose", round(df["gluc"].mean(), 1))

st.divider()

# CHART
st.subheader("BMI Distribution")
st.bar_chart(df["BMICat"].value_counts())