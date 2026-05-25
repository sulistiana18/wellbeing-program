import pandas as pd
import streamlit as st

st.set_page_config(page_title="User Profile", layout="wide")

st.markdown(
    """
<style>

.kpi-card {
    background: linear-gradient(180deg, #ffffff 0%, #fbfbfd 100%);
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    position: relative;
    overflow: hidden;
    border-left: 6px solid var(--accent);
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

.kpi-blue { --accent: #2563eb; }
.kpi-green { --accent: #16a34a; }
.kpi-orange { --accent: #f59e0b; }
.kpi-purple { --accent: #7c3aed; }

</style>
""",
    unsafe_allow_html=True,
)


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

    return df, users, activity, mcu


df, users, activity, mcu = load_data()

# =========================
# RANKING SYSTEM (GLOBAL)
# =========================
user_rank = (
    df.groupby("fullname")
    .agg(
        total_activity=("fullname", "count"),
        total_distance=("distance", "sum")
    )
    .reset_index()
)

user_rank = user_rank.sort_values("total_activity", ascending=False)
user_rank["rank"] = user_rank["total_activity"].rank(method="dense", ascending=False).astype(int)

sorted_users = user_rank.sort_values("rank")["fullname"].tolist()

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Employee Selector")

selected_user = st.sidebar.selectbox(
    "Choose Employee (Ranked)",
    sorted_users
)

# =========================
# FILTER USER DATA
# =========================
user_df = df[df["fullname"] == selected_user].copy()
user_info = users[users["fullname"] == selected_user].iloc[0]
user_position = user_rank[user_rank["fullname"] == selected_user].iloc[0]["rank"]

# =========================
# KPI CALCULATION
# =========================
total_activity = len(user_df)
total_distance = user_df["distance"].sum()

user_df["week"] = user_df["start_date_local"].dt.isocalendar().week
weekly = user_df.groupby("week").size()
avg_per_week = weekly.mean() if not weekly.empty else 0

# BMI CATEGORY
def bmi_category(bmi):
    if pd.isna(bmi):
        return "Unknown"
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obese"

bmi_val = user_df["BMI"].mean() if "BMI" in user_df.columns else None
bmi_cat = bmi_category(bmi_val)

# =========================
# HEADER
# =========================
st.title(f"Employee Health Profile - Rank #{user_position}")
st.caption("Individual wellbeing, activity, and medical overview")

st.markdown("---")

# =========================
# KPI ROW (EXECUTIVE SUMMARY)
# =========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="kpi-card kpi-blue">
            <div class="kpi-title">Total Activities</div>
            <div class="kpi-value">{total_activity}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="kpi-card kpi-green">
            <div class="kpi-title">Total Distance (km)</div>
            <div class="kpi-value">{total_distance:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="kpi-card kpi-orange">
            <div class="kpi-title">Avg / Week</div>
            <div class="kpi-value">{avg_per_week:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""
        <div class="kpi-card kpi-purple">
            <div class="kpi-title">BMI Category</div>
            <div class="kpi-value">{bmi_cat}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# =========================
# MAIN LAYOUT
# =========================
left, right = st.columns([1, 2])

# =========================
# LEFT PANEL (PROFILE)
# =========================
with left:
    st.subheader("Employee Profile")

    st.markdown(f"""
### {user_info['fullname']}

**Global Rank:** #{user_position}  

- **Age:** {user_info.get('age', '-') }  
- **Department:** {user_info.get('department', '-') }  
- **Gender:** {user_info.get('gender', '-') }  
""")

    st.markdown("---")

    st.subheader("Health Snapshot")

    st.write("**BMI Value:**", round(bmi_val, 2) if bmi_val else "-")
    st.write("**Category:**", bmi_cat)

    if "blood_pressure" in user_df.columns:
        bp = user_df["blood_pressure"].dropna()
        latest_bp = bp.iloc[-1] if not bp.empty else "N/A"

        st.write("**Latest Blood Pressure:**")
        st.code(latest_bp)

# =========================
# RIGHT PANEL (TABS)
# =========================
with right:
    tab1, tab2 = st.tabs(["📊 Activity History", "🧪 MCU Records"])

    # ACTIVITY TAB
    with tab1:
        st.subheader("Activity Timeline (Latest First)")

        activity_sorted = user_df.sort_values("start_date_local", ascending=False)

        st.dataframe(
            activity_sorted[[
                "start_date_local",
                "type",
                "distance",
                "moving_time"
            ]],
            use_container_width=True,
            height=400
        )

    # MCU TAB
    with tab2:
        st.subheader("Medical Check-Up Records")

        mcu_user = mcu[mcu["user_id"] == user_info["user_id"]]

        if not mcu_user.empty:
            st.dataframe(mcu_user, use_container_width=True, height=400)
        else:
            st.info("No MCU record found for this employee")