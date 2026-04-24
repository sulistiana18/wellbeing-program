
import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Wellbeing Dashboard", layout="wide")

st.title("💙 Employee Wellbeing Dashboard")
st.markdown("Monitor employee activity, health metrics, and wellbeing insights")

# =========================
# HELPER FUNCTION
# =========================
def safe_int(val):
    return int(val) if pd.notna(val) else 0

def safe_float(val, digits=2):
    return round(val, digits) if pd.notna(val) else 0

def safe_display(val, suffix="", digits=2):
    return f"{round(val, digits)}{suffix}" if pd.notna(val) else "-"

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    file = "wellbeing.xlsx"

    users = pd.read_excel(file, sheet_name="users")
    activity = pd.read_excel(file, sheet_name="activity_logs")
    mcu = pd.read_excel(file, sheet_name="mcu_records")

    # JOIN DATA
    df = activity.merge(users, on="user_id", how="left")
    df = df.merge(mcu, on="user_id", how="left")

    # Convert date
    df["start_date_local"] = pd.to_datetime(df["start_date_local"])

    # Convert moving_time ke menit
    df["moving_time"] = pd.to_timedelta(df["moving_time"].astype(str)).dt.total_seconds() / 60

    return df

df = load_data()

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("Filter")

selected_user = st.sidebar.selectbox(
    "Select User", ["All"] + list(df["fullname"].dropna().unique())
)

selected_type = st.sidebar.selectbox(
    "Activity Type", ["All"] + list(df["type"].dropna().unique())
)

# FILTER
filtered_df = df.copy()

if selected_user != "All":
    filtered_df = filtered_df[filtered_df["fullname"] == selected_user]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]

# =========================
# KPI
# =========================
col1, col2, col3, col4 = st.columns(4)

total_distance = filtered_df["distance"].sum()
avg_hr = filtered_df["average_heartrate"].mean()
avg_bmi = filtered_df["BMI"].mean()
total_activity = filtered_df["activity_id"].count()

col1.metric("Total Distance (km)", safe_float(total_distance))
col2.metric("Avg Heart Rate", safe_display(avg_hr, " bpm", 0))
col3.metric("Avg BMI", safe_display(avg_bmi))
col4.metric("Total Activities", total_activity)

# =========================
# INSIGHT
# =========================
st.subheader("🧠 Key Insights")

if not filtered_df.empty:
    top_user = (
        filtered_df.groupby("fullname")["moving_time"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    most_active_type = filtered_df["type"].value_counts()

    st.markdown(f"""
    - 🏆 **Most active user**: **{top_user.index[0]}** with total moving time **{safe_int(top_user.values[0])} minutes**
    - 🏃 **Most common activity**: **{most_active_type.idxmax() if not most_active_type.empty else "-"}**
    - 💓 **Average heart rate**: **{safe_display(avg_hr, " bpm", 0)}**
    - ⚖️ **Average BMI**: **{safe_display(avg_bmi)}**
    """)
else:
    st.warning("No data available")

# =========================
# CHARTS
# =========================
st.subheader("📈 Activity Over Time")

if not filtered_df.empty:
    fig1 = px.line(
        filtered_df,
        x="start_date_local",
        y="distance",
        color="type",
        markers=True
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No data for chart")

st.subheader("🏃 Activity Distribution")

if not filtered_df.empty:
    fig2 = px.pie(
        filtered_df,
        names="type",
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("💓 Heart Rate vs Distance")

if not filtered_df.empty:
    fig3 = px.scatter(
        filtered_df,
        x="distance",
        y="average_heartrate",
        color="type",
        hover_data=["fullname"]
    )
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# MCU ANALYSIS
# =========================
st.subheader("🧬 BMI Category Distribution")

if "BMICat" in filtered_df.columns and not filtered_df.empty:
    fig4 = px.histogram(
        filtered_df,
        x="BMICat",
        color="BMICat"
    )
    st.plotly_chart(fig4, use_container_width=True)

# =========================
# LEADERBOARD
# =========================
st.subheader("🏆 Leaderboard (Most Active Users)")

if not filtered_df.empty:
    leaderboard = (
        filtered_df.groupby(["fullname", "user_id"])["moving_time"]
        .sum()
        .reset_index()
        .sort_values(by="moving_time", ascending=False)
        .reset_index(drop=True)
    )

    leaderboard["Rank"] = leaderboard.index + 1
    leaderboard["moving_time_hours"] = (leaderboard["moving_time"] / 60).round(2)

    leaderboard = leaderboard[["Rank", "fullname", "user_id", "moving_time_hours"]]

    # TOP 3
    top3 = leaderboard.head(3)
    medals = ["🥇", "🥈", "🥉"]

    cols = st.columns(3)

    for i in range(min(3, len(top3))):
        cols[i].metric(
            f"{medals[i]} {top3.iloc[i]['fullname']}",
            f"{top3.iloc[i]['moving_time_hours']:.2f} hrs"
        )

    st.dataframe(leaderboard, use_container_width=True)
else:
    st.warning("No leaderboard data")

# =========================
# TABLE
# =========================
st.subheader("📋 Data Preview")
st.dataframe(filtered_df)
