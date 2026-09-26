import time
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
    return f"Job: {job_title}, Salary: ${salary:,.0f}, Context: {extra_context}"


def run_research_agent(client, model, job_title, salary, context="", reporter=None):
    """Research agent that analyzes job tasks and AI replacement potential."""
    system_instruction = "You are a job analyst. In 1-2 sentences each, list 4 main tasks for this job and estimate automation risk (Low/Medium/High)."

    prompt = build_job_analysis_prompt(job_title, salary, context)
    result = call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )
    time.sleep(2)  # Rate limit protection
    return result


def run_product_agent(
    client: genai.Client,
    model: str,
    job_title: str,
    salary: float,
    context: str = '',
    research_results: str = '',
) -> str:
    """Business agent that determines risk level and replacement cost."""
    system_instruction = "You are a business analyst. In 1-2 sentences, rate this job's automation risk (Low/Medium/High) and estimate cost to automate (as % of salary)."

    prompt = f"{build_job_analysis_prompt(job_title, salary, context)}. Risk summary: {research_results[:200]}"
    result = call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )
    time.sleep(2)  # Rate limit protection
    return result


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
    system_instruction = "You are a technical architect. In 1-2 sentences, list 2-3 AI tools that could automate this job and difficulty level (Easy/Medium/Hard)."

    prompt = f"{build_job_analysis_prompt(job_title, salary, context)}"
    result = call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )
    time.sleep(2)  # Rate limit protection
    return result


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
    system_instruction = "You are an executive advisor. In 2-3 sentences, provide: final risk level (Low/Medium/High), one key recommendation, and timeline for automation (1-2 years / 3-5 years / 5+ years)."

    prompt = f"{build_job_analysis_prompt(job_title, salary, context)}"
    result = call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )
    return result
