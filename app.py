import streamlit as st

from risk_model import JOB_CATALOG, calculate_job_risk, list_jobs

st.set_page_config(page_title="WorkLens", page_icon="📊", layout="wide")

st.title("WorkLens")
st.caption("AI job replacement risk, broken down by task and business cost.")

job_title = st.selectbox("Select an occupation", list_jobs())
annual_salary = st.number_input(
    "Estimated annual salary for this role",
    min_value=20000,
    max_value=500000,
    value=85000,
    step=5000,
)

result = calculate_job_risk(job_title, annual_salary)

st.subheader(f"{result['job_title']} overview")

col1, col2, col3 = st.columns(3)
col1.metric("Overall AI risk", f"{result['overall_probability']:.1f}%")
col2.metric("Risk level", result["job_risk"])
col3.metric("AI replacement cost / month", f"${result['cost_to_replace_with_ai']:.2f}")

st.markdown("### Task breakdown")
for task in JOB_CATALOG[job_title]:
    label = task["task"]
    value = task["automation_probability"]
    st.write(f"**{label}**")
    st.progress(value / 100)
    st.caption(f"AI automation likelihood: {value}%")

st.markdown("### Recommendation")
st.info(result["recommendation"])

if result["high_risk_tasks"]:
    st.markdown("### High-risk tasks")
    for task in result["high_risk_tasks"]:
        st.markdown(f"- {task}")

st.markdown("---")
st.caption("Built at ShellHacks 2026 by Thalia Vanto.")
