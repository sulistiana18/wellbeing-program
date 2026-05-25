import streamlit as st

from utils import load_data

st.set_page_config(page_title="User Summary", layout="wide")

df = load_data()

# =========================
# ENTERPRISE STYLE (MATCH app.py)
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

/* GLOBAL BACKGROUND (MATCH APP.PY) */
.stApp {
    background: #f5f7fb;
    font-family: "Inter", sans-serif;
}

/* DASHBOARD CANVAS */
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
}

h3 {
    font-size: 15px !important;
    font-weight: 700;
    color: #111827;
}

/* =========================
   KPI CARD SYSTEM (COPY FROM APP.PY)
========================= */
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

/* KPI COLORS (SAME AS APP.PY) */
.kpi-blue { --accent: #2563eb; }
.kpi-green { --accent: #16a34a; }
.kpi-orange { --accent: #f59e0b; }
.kpi-purple { --accent: #7c3aed; }

/* CHART STYLE */
div[data-testid="stBarChart"] {
    background: #ffffff;
    padding: 12px;
    border-radius: 16px;
    border: 1px solid #e8ecf4;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
}

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
st.title("User Summary")
st.caption("Employee demographic and organizational overview")

# =========================
# KPI SECTION (MATCH APP.PY STYLE)
# =========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
    <div class="kpi-card kpi-blue">
        <div class="kpi-title">Total Employees</div>
        <div class="kpi-value">{df['user_id'].nunique()}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
    <div class="kpi-card kpi-green">
        <div class="kpi-title">Average Age</div>
        <div class="kpi-value">{df['age'].mean():.1f}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
    <div class="kpi-card kpi-orange">
        <div class="kpi-title">Male Percentage</div>
        <div class="kpi-value">{df['gender'].value_counts(normalize=True).get('Male',0)*100:.1f}%</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""
    <div class="kpi-card kpi-purple">
        <div class="kpi-title">Departments</div>
        <div class="kpi-value">{df['department'].nunique()}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# CHART
# =========================
st.markdown("### Department Distribution")

dept = df["department"].value_counts()

st.bar_chart(dept)
