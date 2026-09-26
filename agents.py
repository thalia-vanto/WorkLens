from google import genai
from google.genai import types


def create_client(api_key: str) -> genai.Client:
    """Create a Google Genai client with the provided API key."""
    return genai.Client(api_key=api_key)


def request_gemini(client, model, instruction, prompt, tools=None):
    """Make a request to Gemini API using the current Google GenAI SDK."""
    # Ensure model name has the proper prefix
    if not model.startswith("models/"):
        model = f"models/{model}"
    
    config = types.GenerateContentConfig(system_instruction=instruction)
    return client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )


def call_gemini(client, model, system_instruction, user_prompt):
    """Call Gemini and return just the text response."""
    response = request_gemini(client, model, system_instruction, user_prompt)
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
    system_instruction = """You are a job analysis specialist. Your job is to:
1. Understand the job title and its typical responsibilities
2. Break down the job into 5-8 specific, measurable tasks
3. For each task, evaluate how automatable it is
4. Consider current AI capabilities in 2024-2026
5. Generate structured analysis of what parts of the job AI can do

Be specific and realistic. Consider both the technical feasibility and business impact."""

    prompt = build_job_analysis_prompt(job_title, salary, context)
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
    system_instruction = """You are a business analyst specializing in AI automation impact. Your job is to:
1. Review the job analysis and task breakdown
2. Determine the overall AI replacement risk (Low/Medium/High)
3. Calculate what percentage of the job can be automated
4. Estimate the monthly cost to replace this job with AI solutions
5. Identify which AI tools would be most effective
6. Consider partial automation vs full replacement

Be data-driven but realistic about implementation challenges."""

    prompt = f"{build_job_analysis_prompt(job_title, salary, context)}\n\nTask Analysis:\n{research_results}"
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
    system_instruction = """You are a technical architect specializing in AI automation. Your job is to:
1. Review the job analysis and business assessment
2. Identify the specific AI tools and APIs that can automate each task
3. Design a technical architecture for job automation
4. Break down implementation into feasible pieces
5. List required integrations (LLMs, databases, workflow tools, etc.)
6. Estimate complexity and implementation time

Focus on practical, available AI solutions in 2024-2026."""

    prompt = f"""{build_job_analysis_prompt(job_title, salary, context)}

Task Analysis:
{research_results}

Business Analysis:
{business_analysis}"""
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
    system_instruction = """You are an executive advisor on AI automation impact. Your job is to:
1. Synthesize all technical, business, and task analysis
2. Create a clear, actionable risk assessment (Low/Medium/High)
3. Provide specific recommendations for workers in this role
4. Suggest skills to learn or pivot to avoid automation
5. Estimate timeframe for realistic AI replacement
6. Present both opportunities and risks

Format your response as a professional report suitable for executives and workers."""

    prompt = f"""EXECUTIVE JOB RISK ASSESSMENT REPORT

Job Title: {job_title}
Annual Salary: ${salary:,.2f}
Additional Context: {context or 'Standard role'}

=== RESEARCH FINDINGS ===
{research_results}

=== BUSINESS IMPACT ANALYSIS ===
{business_analysis}

=== TECHNICAL AUTOMATION ROADMAP ===
{technical_plan}

Please provide a comprehensive risk assessment and recommendations."""

    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )
