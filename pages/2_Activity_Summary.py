import plotly.express as px
import streamlit as st

from utils import load_data

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Activity Summary", layout="wide")

df = load_data()

# =========================
# ENTERPRISE CSS (SAMA DENGAN app.py)
# =========================
st.markdown(
    """
<style>

/* GLOBAL */
.stApp {
    background: #f5f7fb;
    font-family: "Inter", sans-serif;
}

/* CONTAINER */
.block-container {
    background: #ffffff;
    border-radius: 20px;
    padding: 2rem 1.5rem !important;
    box-shadow: 0 10px 40px rgba(15, 23, 42, 0.08);
}

/* TITLE */
h1 {
    font-size: 22px !important;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
}

/* KPI CARD STYLE (CUSTOM METRIC REPLACEMENT) */
.kpi-card {
    background: linear-gradient(180deg, #ffffff 0%, #fbfbfd 100%);
    border-radius: 16px;
    padding: 14px 16px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    border-left: 5px solid #2563eb;
    transition: 0.2s;
}

.kpi-card:hover {
    transform: translateY(-2px);
}

.kpi-title {
    font-size: 11px;
    color: #64748b;
}

.kpi-value {
    font-size: 18px;
    font-weight: 800;
    color: #0f172a;
}

/* CHART CARD */
.chart-card {
    background: white;
    border-radius: 18px;
    padding: 12px;
    border: 1px solid #e8ecf4;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
}

/* DIVIDER */
hr {
    border: none;
    border-top: 1px solid #eef2f7;
    margin: 12px 0;
}

</style>
""",
    unsafe_allow_html=True,
)

# =========================
# HEADER
# =========================
st.title("Activity Summary")

# =========================
# KPI SECTION (UPGRADED UI, NOT st.metric DEFAULT)
# =========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-title">Activities</div>
        <div class="kpi-value">{df["activity_id"].count()}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-title">Distance</div>
        <div class="kpi-value">{round(df["distance"].sum(), 2)} km</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-title">Avg Heart Rate</div>
        <div class="kpi-value">{round(df["average_heartrate"].mean(), 1)} bpm</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-title">Types</div>
        <div class="kpi-value">{df["type"].nunique()}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# CHARTS
# =========================
st.markdown("### Analytics")

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig = px.line(df, x="start_date_local", y="distance", color="type")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig = px.pie(df, names="type", hole=0.5)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
