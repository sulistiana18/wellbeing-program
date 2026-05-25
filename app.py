import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")


st.set_page_config(page_title="Wellbeing Dashboard", layout="wide")

# =========================
# ENTERPRISE UI STYLE (POWER BI INSPIRED)
# =========================
st.markdown(
    """
<style>

:root {
    --primary: #2563eb;
    --success: #16a34a;
    --warning: #f59e0b;
    --purple: #7c3aed;
}

/* GLOBAL BACKGROUND */
.stApp {
    background: #f5f7fb;
    font-family: "Inter", sans-serif;
}

/* DASHBOARD CANVAS (POWER BI FEEL) */
.block-container {
    background: #ffffff;
    border-radius: 20px;
    padding: 2.2rem 1.6rem 1.2rem 1.6rem !important;
    box-shadow: 0 10px 40px rgba(15, 23, 42, 0.08);
    margin-top: 1rem;
}

/* TYPOGRAPHY */
h1 {
    font-size: 22px !important;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}

h2 {
    font-size: 14px !important;
    color: #334155;
}

h3 {
    font-size: 15px !important;
    font-weight: 700;
    color: #111827;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border-right: 1px solid #e2e8f0;
}

section[data-testid="stSidebar"] * {
    color: #0f172a !important;
    font-size: 13px;
}

/* KPI CARD */
.kpi-card {
    background: linear-gradient(180deg, #ffffff 0%, #fbfbfd 100%);
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    position: relative;
    overflow: hidden;
    border-left: 6px solid var(--accent);
    transition: all 0.25s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.12);
}

.kpi-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 4px;
    width: 100%;
    background: var(--accent);
    opacity: 0.8;
}

.kpi-title {
    font-size: 11px;
    color: #64748b;
    margin-bottom: 4px;
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

/* DATA TABLE */
div[data-testid="stDataFrame"] table {
    font-size: 13px;
    border-radius: 12px;
    overflow: hidden;
}

/* DIVIDER SPACING */
hr {
    margin: 12px 0px;
    border: none;
    border-top: 1px solid #eef2f7;
}

</style>
""",
    unsafe_allow_html=True,
)

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
    df["moving_time"] = (
        pd.to_timedelta(df["moving_time"].astype(str)).dt.total_seconds() / 60
    )

    return df


df = load_data()

# =========================
# SIDEBAR FILTER
# =========================
with st.sidebar:
    st.header("FILTER PANEL")

    selected_user = st.selectbox(
        "Employee", ["All"] + list(df["fullname"].dropna().unique())
    )
    selected_type = st.selectbox(
        "Activity", ["All"] + list(df["type"].dropna().unique())
    )

filtered_df = df.copy()

if selected_user != "All":
    filtered_df = filtered_df[filtered_df["fullname"] == selected_user]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]

# =========================
# KPI SECTION
# =========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
    <div class="kpi-card kpi-blue">
        <div class="kpi-title">Total Distance</div>
        <div class="kpi-value">{filtered_df['distance'].sum():.1f} km</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
    <div class="kpi-card kpi-green">
        <div class="kpi-title">Avg Heart Rate</div>
        <div class="kpi-value">{filtered_df['average_heartrate'].mean():.0f} bpm</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
    <div class="kpi-card kpi-orange">
        <div class="kpi-title">BMI Average</div>
        <div class="kpi-value">{filtered_df['BMI'].mean():.1f}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""
    <div class="kpi-card kpi-purple">
        <div class="kpi-title">Activities</div>
        <div class="kpi-value">{len(filtered_df)}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# INSIGHT
# =========================
st.markdown("### Insight Summary")

if not filtered_df.empty:
    top = filtered_df.groupby("fullname")["distance"].sum().idxmax()
    st.success(f"Top performer: {top}")

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# CHARTS
# =========================
st.markdown("### Analytics Dashboard")

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig = px.line(filtered_df, x="start_date_local", y="distance", color="type")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig = px.pie(filtered_df, names="type", hole=0.55)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# LEADERBOARD
# =========================
st.markdown("### Performance Leaderboard")
st.caption("Top performance based on total distance covered.")

leaderboard = (
    filtered_df.groupby("fullname")["distance"]
    .sum()
    .reset_index()
    .sort_values("distance", ascending=False)
    .reset_index(drop=True)
)

# ADD RANKING
leaderboard.insert(0, "Rank", leaderboard.index + 1)

# FORMAT DISTANCE
leaderboard["distance"] = leaderboard["distance"].round(1)

# DISPLAY STYLING TABLE
st.dataframe(leaderboard, use_container_width=True, height=260, hide_index=True)
