import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Wellbeing Dashboard", layout="wide")

# =========================
# CORPORATE UI STYLE V2
# =========================
st.markdown("""
<style>

/* GLOBAL BACKGROUND */
.stApp {
    background: linear-gradient(180deg, #eef2f7 0%, #f8fafc 100%);
    font-family: "Inter", sans-serif;
}

/* PAGE PADDING (compact dashboard feel) */
.block-container {
    padding: 1rem 1.4rem;
}

/* TYPOGRAPHY SMALL BUSINESS STYLE */
h1 {
    font-size: 18px !important;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 4px;
}

h2 {
    font-size: 13px !important;
    color: #334155;
}

h3 {
    font-size: 12px !important;
}

/* SIDEBAR */
/* =========================
   SIDEBAR (CORPORATE LIGHT)
========================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border-right: 1px solid #e2e8f0;
}

/* sidebar text fix */
section[data-testid="stSidebar"] * {
    color: #0f172a !important;
    font-size: 13px;
}

/* sidebar header */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #0f172a !important;
    font-weight: 600;
}

/* dropdown/selectbox clean */
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stMultiSelect {
    background: white;
}

/* =========================
   KPI CARD SYSTEM
========================= */
.kpi-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 12px 14px;
    box-shadow: 0 6px 14px rgba(15, 23, 42, 0.06);
    transition: all 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.10);
}

.kpi-title {
    font-size: 11px;
    color: #64748b;
    margin-bottom: 4px;
}

.kpi-value {
    font-size: 18px;
    font-weight: 700;
    color: #0f172a;
}

/* KPI COLORS */
.kpi-blue { border-left: 4px solid #3b82f6; }
.kpi-green { border-left: 4px solid #22c55e; }
.kpi-orange { border-left: 4px solid #f97316; }
.kpi-purple { border-left: 4px solid #a855f7; }

/* CHART CARD */
.chart-card {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 10px;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.05);
}

/* DATAFRAME */
div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* CHART GAP FIX */
div.stPlotlyChart {
    margin-top: -6px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================
st.title("Wellbeing Dashboard")
st.caption("Corporate Employee Analytics Overview")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    file = "wellbeing.xlsx"

    users = pd.read_excel(file, sheet_name="users")
    activity = pd.read_excel(file, sheet_name="activity_logs")
    mcu = pd.read_excel(file, sheet_name="mcu_records")

    df = activity.merge(users, on="user_id", how="left")
    df = df.merge(mcu, on="user_id", how="left")

    df["start_date_local"] = pd.to_datetime(df["start_date_local"])
    df["moving_time"] = pd.to_timedelta(df["moving_time"].astype(str)).dt.total_seconds() / 60

    return df

df = load_data()

# =========================
# SIDEBAR FILTER
# =========================
with st.sidebar:
    st.header("FILTER PANEL")

    selected_user = st.selectbox("Employee", ["All"] + list(df["fullname"].dropna().unique()))
    selected_type = st.selectbox("Activity", ["All"] + list(df["type"].dropna().unique()))

filtered_df = df.copy()

if selected_user != "All":
    filtered_df = filtered_df[filtered_df["fullname"] == selected_user]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]

# =========================
# KPI CARDS (FINAL VERSION)
# =========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card kpi-blue">
        <div class="kpi-title">Total Distance</div>
        <div class="kpi-value">{filtered_df['distance'].sum():.1f} km</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card kpi-green">
        <div class="kpi-title">Avg Heart Rate</div>
        <div class="kpi-value">{filtered_df['average_heartrate'].mean():.0f} bpm</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card kpi-orange">
        <div class="kpi-title">BMI Average</div>
        <div class="kpi-value">{filtered_df['BMI'].mean():.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card kpi-purple">
        <div class="kpi-title">Activities</div>
        <div class="kpi-value">{len(filtered_df)}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# INSIGHT
# =========================
st.markdown("### Insight Summary")

if not filtered_df.empty:
    top = filtered_df.groupby("fullname")["distance"].sum().idxmax()
    st.success(f"Top performer: {top}")

st.divider()

# =========================
# CHARTS (2 COLUMN GRID)
# =========================
st.markdown("### Analytics Dashboard")

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig = px.line(filtered_df, x="start_date_local", y="distance", color="type")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig = px.pie(filtered_df, names="type", hole=0.55)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# LEADERBOARD
# =========================
st.markdown("### Performance Leaderboard")

leaderboard = filtered_df.groupby("fullname")["distance"].sum().reset_index()
leaderboard = leaderboard.sort_values("distance", ascending=False)

st.dataframe(leaderboard, use_container_width=True, height=260)