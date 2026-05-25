import plotly.express as px
import streamlit as st

from utils import load_data

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="MCU Summary", layout="wide")

df = load_data()

# =========================
# ENTERPRISE CSS (SAMA STYLE APP)
# =========================
st.markdown(
    """
<style>

/* GLOBAL BACKGROUND */
.stApp {
    background: #f5f7fb;
    font-family: "Inter", sans-serif;
}

/* MAIN CONTAINER */
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

/* KPI CARD */
.kpi-card {
    background: linear-gradient(180deg, #ffffff 0%, #fbfbfd 100%);
    border-radius: 16px;
    padding: 14px 16px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    border-left: 5px solid var(--accent);
    transition: 0.2s ease;
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

/* KPI COLORS */
.kpi-blue { --accent: #2563eb; }
.kpi-green { --accent: #16a34a; }
.kpi-orange { --accent: #f59e0b; }
.kpi-purple { --accent: #7c3aed; }

/* CHART CARD */
.chart-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 14px;
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
st.title("MCU Summary")

# =========================
# KPI SECTION (CUSTOM STYLE, NOT st.metric)
# =========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
    <div class="kpi-card kpi-blue">
        <div class="kpi-title">Avg BMI</div>
        <div class="kpi-value">{round(df["BMI"].mean(), 2)}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
    <div class="kpi-card kpi-orange">
        <div class="kpi-title">High BMI (>25)</div>
        <div class="kpi-value">{(df["BMI"] > 25).sum()}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
    <div class="kpi-card kpi-purple">
        <div class="kpi-title">Avg Cholesterol</div>
        <div class="kpi-value">{round(df["cholesterol"].mean(), 1)}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""
    <div class="kpi-card kpi-green">
        <div class="kpi-title">Avg Glucose</div>
        <div class="kpi-value">{round(df["gluc"].mean(), 1)}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# CHART SECTION
# =========================
st.markdown("### BMI Distribution")

chart_df = df["BMICat"].value_counts().reset_index()
chart_df.columns = ["BMICat", "Count"]

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
fig = px.bar(chart_df, x="BMICat", y="Count")
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
