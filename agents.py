from google import genai


def create_client(api_key: str) -> genai.Client:
    """Create a Google Genai client with the provided API key."""
    return genai.Client(api_key=api_key)


def call_gemini(client, model, system_instruction, user_prompt):
    """Call Gemini using the Interactions API (recommended by Google)."""
    # Ensure model name has the proper prefix
    if not model.startswith("models/"):
        model = f"models/{model}"
    
    response = client.chats.create(
        model=model,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction
        ),
    )
    
    response = response.send_message(user_prompt)
    return response.text


def build_job_analysis_prompt(job_title: str, salary: float, context: str) -> str:
    """Build a formatted prompt for analyzing job replacement risk."""
    extra_context = context.strip() or 'No additional context provided.'
    return f"""
Job Title: {job_title}
Annual Salary: ${salary:,.2f}
Additional Context: {extra_context}
""".strip()


def run_research_agent(client, model, job_title, salary, context="", reporter=None):
    """Research agent that analyzes job tasks and AI replacement potential."""
    system_instruction = """You are a job analysis specialist. Analyze the job and provide a brief assessment (2-3 paragraphs max) covering:
1. Top 5-6 core tasks for this role
2. Which tasks are most automatable by AI
3. Overall automation potential as a percentage

Be concise and direct."""

    prompt = f"{build_job_analysis_prompt(job_title, salary, context)}\n\nProvide a brief task analysis and automation assessment."
    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )


def run_product_agent(
    client: genai.Client,
    model: str,
    job_title: str,
    salary: float,
    context: str = '',
    research_results: str = '',
) -> str:
    """Business agent that determines risk level and replacement cost."""
    system_instruction = """You are a business analyst. Keep response to 2-3 paragraphs max.
Assess:
1. Overall AI replacement risk (Low/Medium/High)
2. What percentage of the job can be automated
3. Estimated monthly cost to automate this role

Be specific but concise."""

    prompt = f"{build_job_analysis_prompt(job_title, salary, context)}\n\nTask Analysis:\n{research_results[:500]}\n\nProvide a business risk assessment."
    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )


def run_engineering_agent(
    client: genai.Client,
    model: str,
    job_title: str,
    salary: float,
    context: str = '',
    research_results: str = '',
    business_analysis: str = '',
) -> str:
    """Technical agent that maps AI tools to job tasks."""
    system_instruction = """You are a technical architect. Keep response to 2-3 paragraphs max.
Provide:
1. Top 3-4 AI tools/services that could automate this job
2. Implementation difficulty (Easy/Medium/Hard)
3. Key technical challenges

Be practical and concise."""

    prompt = f"{build_job_analysis_prompt(job_title, salary, context)}\n\nTask Analysis (summary):\n{research_results[:300]}\n\nProvide a technical implementation plan."
    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )


def run_manager_agent(
    client: genai.Client,
    model: str,
    job_title: str,
    salary: float,
    context: str,
    research_results: str,
    business_analysis: str,
    technical_plan: str,
) -> str:
    """Executive agent that synthesizes everything into a final risk report."""
    system_instruction = """You are an executive advisor. Keep response to 3-4 paragraphs max.
Synthesize:
1. Final risk assessment (Low/Medium/High)
2. Top 2-3 recommendations for the worker
3. Timeline for realistic automation (1-2 years, 3-5 years, 5+ years)

Be actionable and concise."""

    prompt = f"""Job Risk Assessment Summary

Job Title: {job_title}
Salary: ${salary:,.2f}
Context: {context or 'Standard role'}

Research: {research_results[:300]}
Business Analysis: {business_analysis[:300]}
Technical Plan: {technical_plan[:300]}

Provide a final executive summary and recommendations."""

    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )
