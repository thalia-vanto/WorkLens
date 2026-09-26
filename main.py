from agents import (
    create_client,
    run_engineering_agent,
    run_manager_agent,
    run_product_agent,
    run_research_agent,
)

from config import load_config


def print_header():
    print("=" * 48)
    print("Your Multi-Agent AI Hackathon Planning Team.")
    print("=" * 48)


def ask_multiline(prompt):
    print(prompt)
    print("Type your answer. Press Enter twice when done.\n")

    lines = []

    while True:
        line = input("> ")

        if line == "":
            break

        lines.append(line)

    return "\n".join(lines).strip()


def ask_for_idea():

    while True:

        idea = ask_multiline(
            "What's your hackathon idea?"
        )

        if idea:
            return idea

        print(
            "Please enter an idea so the agents "
            "have something to work with.\n"
        )


def build_blueprint():

    api_key, model = load_config()

    client = create_client(
        api_key=api_key
    )

    idea = ask_for_idea()

    context = ask_multiline(
        "Anything else we should know? Team size, skills, "
        "timeline, constraints, or goals are helpful."
    )

    print("\nBuilding your AI team...\n")

    print(
        "[Researcher] Searching the hackathon resource catalog..."
    )

    research = run_research_agent(
        client,
        model,
        idea,
        context,
        reporter=print
    )

    print(
        "\n[Product] Designing a focused MVP..."
    )

    product = run_product_agent(
        client,
        model,
        idea,
        context
    )

    print(
        "\n[Engineer] Planning the simplest workable architecture..."
    )

    engineer = run_engineering_agent(
        client,
        model,
        idea,
        context,
        research_results=research
    )

    print(
        "\n[Manager] Building your final hackathon blueprint..."
    )

    blueprint = run_manager_agent(
        client=client,
        model=model,
        idea=idea,
        context=context,
        research_results=research,
        product_plan=product,
        engineering_plan=engineer
    )

    return blueprint


def run_app():

    print_header()

    try:

        blueprint = build_blueprint()

        print("\n" + "=" * 48)
        print("             YOUR HACKATHON PLAN")
        print("=" * 48)

        print(blueprint)

    except Exception as error:

        print("\nSomething went wrong.")
        print(f"Error: {error}")


if __name__ == "__main__":
    run_app()
