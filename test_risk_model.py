from risk_model import calculate_job_risk


def test_calculate_job_risk_returns_expected_shape():
    result = calculate_job_risk("Data Analyst", annual_salary=90000)

    assert result["job_title"] == "Data Analyst"
    assert 0 <= result["overall_probability"] <= 100
    assert result["task_count"] > 0
    assert "recommendation" in result
    assert result["cost_to_replace_with_ai"] > 0


def test_calculate_job_risk_handles_unknown_job():
    result = calculate_job_risk("Unknown Role", annual_salary=60000)

    assert result["overall_probability"] == 0.0
    assert result["task_count"] == 0
    assert result["job_risk"] == 0.0
