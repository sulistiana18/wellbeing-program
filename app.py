import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Wellbeing Dashboard", layout="wide")

# =========================
# STYLE (clean minimal)
# =========================
st.markdown("""
<style>
.stApp {
    background: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1 {
    color: #1e3a8a;
    margin-bottom: 0px;
}

h2 {
    color: #334155;
    margin-top: 2rem;
}

/* KPI spacing fix */
div[data-testid="metric-container"] {
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    padding: 14px;
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* section spacing */
section {
    padding-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("💙 Employee Wellbeing Dashboard")
st.caption("Analytics overview of employee health & activity")

st.divider()

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
# FILTER
# =========================
st.sidebar.header("Filter")

selected_user = st.sidebar.selectbox("User", ["All"] + list(df["fullname"].dropna().unique()))
selected_type = st.sidebar.selectbox("Activity Type", ["All"] + list(df["type"].dropna().unique()))

filtered_df = df.copy()

if selected_user != "All":
    filtered_df = filtered_df[filtered_df["fullname"] == selected_user]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]

# =========================
# KPI (GROUPED SECTION)
# =========================
st.subheader("📊 Overview")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Distance", f"{filtered_df['distance'].sum():.2f} km")
k2.metric("Avg HR", f"{filtered_df['average_heartrate'].mean():.0f} bpm")
k3.metric("BMI", f"{filtered_df['BMI'].mean():.2f}")
k4.metric("Activities", int(filtered_df["activity_id"].count()))

st.divider()

# =========================
# INSIGHT (SEPARATE CARD)
# =========================
st.subheader("🧠 Insight Story")

if not filtered_df.empty:

    top_user = (
        filtered_df.groupby("fullname")["moving_time"]
        .sum()
        .sort_values(ascending=False)
    )

    most_active_type = filtered_df["type"].value_counts().idxmax()

    st.info(
        f"🏆 **{top_user.index[0]}** is the most active employee with "
        f"**{top_user.values[0]:.0f} minutes** total activity.\n\n"
        f"🏃 Most frequent activity type is **{most_active_type}**."
    )

st.divider()

# =========================
# CHART GRID (IMPORTANT FIX)
# =========================
st.subheader("📈 Analytics")

c1, c2 = st.columns(2)

with c1:
    fig1 = px.line(
        filtered_df,
        x="start_date_local",
        y="distance",
        color="type",
        markers=True,
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.pie(
        filtered_df,
        names="type",
        hole=0.4,
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(
    filtered_df,
    x="distance",
    y="average_heartrate",
    color="type",
    template="plotly_white"
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# =========================
# LEADERBOARD (CLEAR SECTION)
# =========================
st.subheader("🏆 Leaderboard")

if not filtered_df.empty:

    leaderboard = (
        filtered_df.groupby("fullname")["moving_time"]
        .sum()
        .reset_index()
        .sort_values("moving_time", ascending=False)
    )

    leaderboard["Rank"] = leaderboard.index + 1
    leaderboard["Hours"] = (leaderboard["moving_time"] / 60).round(2)

    leaderboard = leaderboard[["Rank", "fullname", "Hours"]]

    st.dataframe(leaderboard, use_container_width=True)

st.divider()

# =========================
# RAW DATA
# =========================
st.subheader("📋 Raw Data")
st.dataframe(filtered_df)