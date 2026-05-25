import pandas as pd
import streamlit as st

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