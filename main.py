from agents import (
    create_client,
    run_engineering_agent,
    run_manager_agent,
    run_product_agent,
    run_research_agent,
)
from config import load_config


def print_header() -> None:
    print('=' * 60)
    print('WorkLens: AI Job Replacement Risk Analysis')
    print('=' * 60)


def ask_input(prompt: str) -> str:
    while True:
        value = input(f"\n{prompt}\n> ").strip()
        if value:
            return value
        print('Please enter a value.')


def ask_for_job() -> tuple[str, float]:
    job_title = ask_input('What job title do you want to analyze?')
    while True:
        try:
            salary = float(ask_input('What is the annual salary for this role? (example: 85000)'))
            if salary > 0:
                return job_title, salary
            print('Salary must be greater than 0.')
        except ValueError:
            print('Please enter a valid number.')


def build_risk_assessment() -> str:
    api_key, model = load_config()
    client = create_client(api_key)

    job_title, salary = ask_for_job()
    context = ask_input('Any extra context? (press enter if not needed)')

    print('\nBuilding your AI risk assessment...\n')

    print('[Researcher] Analyzing job tasks...')
    research_results = run_research_agent(client, model, job_title, salary, context, reporter=lambda msg: print(msg))
    print('✓ Research complete\n')

    print('[Business] Estimating automation impact...')
    business_analysis = run_product_agent(client, model, job_title, salary, context, research_results)
    print('✓ Business analysis complete\n')

    print('[Technical] Mapping AI tools to job tasks...')
    technical_plan = run_engineering_agent(client, model, job_title, salary, context, research_results, business_analysis)
    print('✓ Technical plan complete\n')

    print('[Executive] Writing final risk report...')
    final_report = run_manager_agent(
        client,
        model,
        job_title,
        salary,
        context,
        research_results,
        business_analysis,
        technical_plan,
    )
    print('✓ Final report complete\n')

    return final_report


def run_app() -> None:
    print_header()
    assessment = build_risk_assessment()
    print('=' * 60)
    print('AI JOB REPLACEMENT RISK ASSESSMENT')
    print('=' * 60)
    print(assessment)


if __name__ == '__main__':
    run_app()
