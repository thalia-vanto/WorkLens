import json
from google import genai
from tools import RESOURCE_SEARCH_TOOL, search_hackathon_resources


def create_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def request_gemini(client, model, instruction, prompt, tools=None):
    return client.interactions.create(
        model=model,
        input=prompt,
        system_instruction=instruction,
        tools=tools or [],
        store=False,
    )


def call_gemini(client, model, system_instruction, user_prompt):
    response = request_gemini(
        client=client,
        model=model,
        instruction=system_instruction,
        prompt=user_prompt,
    )

    return response.output_text


def build_project_prompt(idea: str, context: str) -> str:
    return f"""
Hackathon idea:
{idea}

Extra context:
{context or "No extra context was provided."}
""".strip()


def run_research_agent(
    client,
    model,
    idea,
    context="",
    reporter=None
):
    system_instruction = """
You are the Research Agent for a hackathon team.

Find useful services and coding documentation from the supplied resource
catalog.

Use the search tool when useful. Keep the research practical and relevant
to the hackathon idea.

Explain which resources are useful and mention important limitations or
cost considerations.

Do not invent resources.
""".strip()

    prompt = build_project_prompt(idea, context)

    response = request_gemini(
        client=client,
        model=model,
        instruction=system_instruction,
        prompt=prompt,
        tools=[RESOURCE_SEARCH_TOOL],
    )

    resources = []

    for step in response.steps:
        if getattr(step, "type", None) == "function_call":
            query = getattr(step, "arguments", {}).get("query", "")

            if query:
                matches = search_hackathon_resources(query)

                resources.extend(matches)

                if reporter:
                    reporter(f"[Researcher -> Tool] Search: {query}")

                    names = ", ".join(
                        item["name"] for item in matches
                    )

                    reporter(
                        f"[Tool -> Researcher] {names or 'No matches'}"
                    )

    unique_resources = []

    for resource in resources:
        if resource not in unique_resources:
            unique_resources.append(resource)

    resource_text = json.dumps(
        unique_resources,
        indent=2
    )

    final_prompt = f"""
Hackathon idea:
{idea}

Extra context:
{context or "No extra context was provided."}

Resources found:
{resource_text}

Write a short research summary explaining:
- useful resources
- why they are useful
- limitations
- cost or billing considerations

Do not invent information.
""".strip()

    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=final_prompt,
    )


def run_product_agent(
    client,
    model,
    idea,
    context=""
):
    system_instruction = """
You are the Product Agent for a hackathon team.

Create a simple and realistic MVP based on the hackathon idea.

Focus on:
- what the product does
- the main features
- what should be built first
- what can be left out

Keep the plan realistic for a hackathon.
""".strip()

    prompt = build_project_prompt(idea, context)

    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )


def run_engineering_agent(
    client,
    model,
    idea,
    context="",
    research_results=""
):
    system_instruction = """
You are the Engineering Agent for a hackathon team.

Create a simple technical plan for building the MVP.

Explain:
- main technologies
- basic architecture
- important components
- how the pieces connect

Keep the solution simple enough for a hackathon.
""".strip()

    prompt = build_project_prompt(idea, context)

    if research_results:
        prompt += f"""

Research findings:
{research_results}
"""

    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )


def run_manager_agent(
    client,
    model,
    idea,
    context,
    research_results,
    product_plan,
    engineering_plan
):
    system_instruction = """
You are the Manager Agent for a hackathon team.

Combine the research, product plan, and engineering plan into one clear
hackathon blueprint.

The final plan should include:
- project idea
- recommended resources
- MVP features
- technical architecture
- implementation steps
- demo plan

Keep the plan realistic and focused.
""".strip()

    prompt = f"""
Original hackathon idea:
{idea}

Extra context:
{context or "No extra context was provided."}

Research Agent:
{research_results}

Product Agent:
{product_plan}

Engineering Agent:
{engineering_plan}

Create the final hackathon blueprint.
""".strip()

    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )
