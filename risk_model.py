from __future__ import annotations

from typing import Any, Dict, List

JOB_CATALOG: Dict[str, List[Dict[str, Any]]] = {
    "Data Analyst": [
        {"task": "Data cleaning", "automation_probability": 88, "salary_impact": 0.18},
        {"task": "Dashboard reporting", "automation_probability": 72, "salary_impact": 0.12},
        {"task": "Statistical analysis", "automation_probability": 61, "salary_impact": 0.2},
        {"task": "Stakeholder communication", "automation_probability": 34, "salary_impact": 0.1},
    ],
    "Customer Support Representative": [
        {"task": "Answering FAQs", "automation_probability": 81, "salary_impact": 0.14},
        {"task": "Ticket triage", "automation_probability": 74, "salary_impact": 0.12},
        {"task": "Escalation handling", "automation_probability": 49, "salary_impact": 0.1},
        {"task": "Empathy and relationship management", "automation_probability": 22, "salary_impact": 0.18},
    ],
    "Software Engineer": [
        {"task": "Code generation", "automation_probability": 66, "salary_impact": 0.2},
        {"task": "Testing and debugging", "automation_probability": 58, "salary_impact": 0.15},
        {"task": "System design", "automation_probability": 43, "salary_impact": 0.18},
        {"task": "Client communication", "automation_probability": 26, "salary_impact": 0.12},
    ],
    "Graphic Designer": [
        {"task": "Template-based design", "automation_probability": 77, "salary_impact": 0.18},
        {"task": "Brand adaptation", "automation_probability": 53, "salary_impact": 0.12},
        {"task": "Creative concepting", "automation_probability": 31, "salary_impact": 0.16},
        {"task": "Client revision cycles", "automation_probability": 29, "salary_impact": 0.12},
    ],
    "Legal Assistant": [
        {"task": "Document review", "automation_probability": 76, "salary_impact": 0.18},
        {"task": "Contract drafting", "automation_probability": 62, "salary_impact": 0.17},
        {"task": "Client intake", "automation_probability": 41, "salary_impact": 0.1},
        {"task": "Case strategy understanding", "automation_probability": 28, "salary_impact": 0.15},
    ],
}


def calculate_job_risk(job_title: str, annual_salary: float = 70000.0) -> Dict[str, Any]:
    tasks = JOB_CATALOG.get(job_title)
    if not tasks:
        return {
            "job_title": job_title,
            "job_risk": 0.0,
            "overall_probability": 0.0,
            "task_count": 0,
            "high_risk_tasks": [],
            "cost_to_replace_with_ai": 0.0,
            "recommendation": "No data available for this occupation yet.",
        }

    avg_probability = sum(task["automation_probability"] for task in tasks) / len(tasks)
    high_risk_tasks = [
        task["task"] for task in tasks if task["automation_probability"] >= 60
    ]

    ai_cost = annual_salary * (0.42 + (avg_probability / 100) * 0.58)
    ai_cost_monthly = ai_cost / 12

    if avg_probability >= 70:
        risk_level = "High"
        recommendation = "This role is highly exposed to automation; retraining into oversight, strategy, or human-centric tasks is recommended."
    elif avg_probability >= 45:
        risk_level = "Moderate"
        recommendation = "The job is partially automatable; hybrid human-AI workflows may be the strongest strategy."
    else:
        risk_level = "Low"
        recommendation = "This role has strong human-centered components and is less likely to be fully automated."

    return {
        "job_title": job_title,
        "job_risk": risk_level,
        "overall_probability": round(avg_probability, 1),
        "task_count": len(tasks),
        "high_risk_tasks": high_risk_tasks,
        "cost_to_replace_with_ai": round(ai_cost_monthly, 2),
        "recommendation": recommendation,
    }


def list_jobs() -> List[str]:
    return list(JOB_CATALOG.keys())
