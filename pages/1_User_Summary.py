import streamlit as st
from utils import load_data

st.set_page_config(page_title="User Summary", layout="wide")

df = load_data()

# =========================
# STYLE (CLEAN SMALL DASHBOARD)
# =========================
st.markdown("""
<style>
.block-container {padding: 1rem;}
h1 {font-size: 20px !important;}
h2 {font-size: 14px !important;}

div[data-testid="metric-container"]{
    background:white;
    border:1px solid #e2e8f0;
    padding:8px !important;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.title("User Summary")

# =========================
# KPI (SMALL & COMPACT)
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Employees", df["user_id"].nunique())
c2.metric("Avg Age", round(df["age"].mean(), 1))
c3.metric("Male %", round((df["gender"].value_counts(normalize=True).get("Male",0))*100, 1))
c4.metric("Departments", df["department"].nunique())

st.divider()

# =========================
# MINI CHART
# =========================
st.subheader("Department Distribution")

st.bar_chart(df["department"].value_counts())