import streamlit as st

from risk_model import JOB_CATALOG, calculate_job_risk, list_jobs

st.set_page_config(page_title="WorkLens", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        .stApp {
            background: linear-gradient(135deg, #07111f 0%, #0d1b2a 52%, #111827 100%);
            color: #e5eefb;
            font-family: 'Inter', sans-serif;
        }

        h1, h2, h3, h4 {
            color: #f8fbff !important;
            font-family: 'Inter', sans-serif !important;
        }

        .header-wrap {
            padding: 1.5rem 0 1rem 0;
        }

        .eyebrow {
            display: inline-block;
            padding: 0.4rem 0.8rem;
            border-radius: 999px;
            background: rgba(143, 198, 255, 0.12);
            border: 1px solid rgba(143, 198, 255, 0.28);
            color: #9cc9ff;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-size: 0.72rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        .title {
            font-size: 3rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.06em !important;
            margin-bottom: 0.2rem !important;
        }

        .subhead {
            color: #bfd2ec !important;
            font-size: 1.05rem !important;
            margin-bottom: 1rem !important;
        }

        [data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricLabel"] {
            color: #bfd2ec !important;
            font-size: 0.8rem !important;
        }

        .metric-card {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 25px rgba(2, 6, 23, 0.28);
        }

        .section-title {
            margin-top: 1.5rem;
            font-size: 1.35rem;
            font-weight: 700;
            color: #f5f9ff;
        }

        .task-card {
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 16px;
            padding: 1rem 1rem 0.75rem 1rem;
            margin-bottom: 0.8rem;
        }

        .task-name {
            font-weight: 700;
            color: #edf5ff;
            margin-bottom: 0.35rem;
            display: block;
        }

        .task-meta {
            color: #9bb7d6;
            font-size: 0.8rem;
            margin-top: 0.35rem;
        }

        .recommendation-box {
            background: linear-gradient(135deg, rgba(36, 88, 160, 0.18), rgba(59, 130, 246, 0.08));
            border: 1px solid rgba(96, 165, 250, 0.35);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            color: #e9f2ff;
        }

        .pill {
            display: inline-block;
            padding: 0.38rem 0.7rem;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.3);
            color: #a7f3d0;
            font-weight: 700;
        }

        .pill.warning {
            background: rgba(249, 115, 22, 0.12);
            border-color: rgba(249, 115, 22, 0.3);
            color: #fdba74;
        }

        .pill.danger {
            background: rgba(239, 68, 68, 0.12);
            border-color: rgba(239, 68, 68, 0.3);
            color: #fca5a5;
        }

        .footer-note {
            color: #93a9c7;
            text-align: center;
            margin-top: 1.7rem;
            padding-bottom: 1rem;
        }

        div[data-testid="stProgressBar"] > div {
            background: linear-gradient(90deg, #4f9cf9 0%, #7c3aed 100%);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="header-wrap">
        <div class="eyebrow">ShellHacks 2026</div>
        <div class="title">WorkLens</div>
        <div class="subhead">AI workforce intelligence for job risk, task-level automation, and business cost impact.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

job_title = st.selectbox("Select an occupation", list_jobs(), index=0)
annual_salary = st.number_input(
    "Estimated annual salary",
    min_value=20000,
    max_value=500000,
    value=85000,
    step=5000,
)

result = calculate_job_risk(job_title, annual_salary)

risk_color = {
    "Low": "pill",
    "Moderate": "pill warning",
    "High": "pill danger",
}

st.markdown(
    f"""
    <div class="section-title">{result['job_title']} at a glance</div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Overall AI risk", f"{result['overall_probability']:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Risk level", result["job_risk"])
    st.markdown(f'<div class="{risk_color[result["job_risk"]]}">{result["job_risk"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("AI replacement cost / mo", f"${result['cost_to_replace_with_ai']:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Task breakdown</div>', unsafe_allow_html=True)
for task in JOB_CATALOG[job_title]:
    label = task["task"]
    value = task["automation_probability"]
    st.markdown(
        f"""
        <div class="task-card">
            <div class="task-name">{label}</div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.2rem;">
                <span style="color:#dfeeff; font-size:0.85rem;">Automation chance</span>
                <span style="color:#8dc3ff; font-weight:700;">{value}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(value / 100)

st.markdown('<div class="section-title">Recommendation</div>', unsafe_allow_html=True)
st.markdown(f'<div class="recommendation-box">{result["recommendation"]}</div>', unsafe_allow_html=True)

if result["high_risk_tasks"]:
    st.markdown('<div class="section-title">High-risk tasks</div>', unsafe_allow_html=True)
    for task in result["high_risk_tasks"]:
        st.markdown(f"- **{task}**")

st.markdown('<div class="footer-note">Built at ShellHacks 2026 by Thalia Vanto.</div>', unsafe_allow_html=True)
