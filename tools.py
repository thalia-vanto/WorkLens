"""Tools and utilities for job AI replacement risk analysis."""

# Job task catalog - maps job titles to their core tasks
JOB_TASK_CATALOG = {
    "Software Engineer": [
        {"task": "Code implementation and debugging", "automation_probability": 75},
        {"task": "Writing unit tests", "automation_probability": 80},
        {"task": "Code documentation", "automation_probability": 70},
        {"task": "System architecture design", "automation_probability": 45},
        {"task": "Debugging complex issues", "automation_probability": 50},
        {"task": "Code review and quality checks", "automation_probability": 65},
        {"task": "API integration", "automation_probability": 72},
    ],
    "Data Analyst": [
        {"task": "Data extraction and cleaning", "automation_probability": 85},
        {"task": "Creating reports and dashboards", "automation_probability": 70},
        {"task": "Statistical analysis", "automation_probability": 60},
        {"task": "Data visualization", "automation_probability": 75},
        {"task": "Database queries and SQL", "automation_probability": 80},
        {"task": "Identifying trends and patterns", "automation_probability": 55},
    ],
    "Marketing Manager": [
        {"task": "Social media posting and scheduling", "automation_probability": 85},
        {"task": "Email campaign creation", "automation_probability": 70},
        {"task": "Content writing", "automation_probability": 65},
        {"task": "Campaign performance analysis", "automation_probability": 75},
        {"task": "Strategic planning", "automation_probability": 30},
        {"task": "Creative concept development", "automation_probability": 25},
        {"task": "Customer segmentation analysis", "automation_probability": 80},
    ],
    "Customer Service Representative": [
        {"task": "Responding to common inquiries", "automation_probability": 90},
        {"task": "Troubleshooting standard issues", "automation_probability": 85},
        {"task": "Processing refunds and returns", "automation_probability": 75},
        {"task": "Handling complex complaints", "automation_probability": 35},
        {"task": "Escalation coordination", "automation_probability": 40},
        {"task": "Ticket documentation", "automation_probability": 80},
    ],
    "Financial Analyst": [
        {"task": "Financial statement analysis", "automation_probability": 70},
        {"task": "Variance analysis and reporting", "automation_probability": 75},
        {"task": "Forecasting and modeling", "automation_probability": 65},
        {"task": "Data compilation", "automation_probability": 85},
        {"task": "Investment research", "automation_probability": 55},
        {"task": "Risk assessment", "automation_probability": 50},
    ],
    "Project Manager": [
        {"task": "Status report creation", "automation_probability": 80},
        {"task": "Schedule management", "automation_probability": 70},
        {"task": "Budget tracking", "automation_probability": 75},
        {"task": "Risk identification", "automation_probability": 45},
        {"task": "Team coordination", "automation_probability": 30},
        {"task": "Stakeholder communication", "automation_probability": 40},
    ],
    "Graphic Designer": [
        {"task": "Photo editing and manipulation", "automation_probability": 65},
        {"task": "Creating social media graphics", "automation_probability": 50},
        {"task": "Banner and ad design", "automation_probability": 55},
        {"task": "Brand identity development", "automation_probability": 25},
        {"task": "UX/UI design", "automation_probability": 30},
        {"task": "Design revisions", "automation_probability": 45},
    ],
    "HR Specialist": [
        {"task": "Resume screening", "automation_probability": 85},
        {"task": "Scheduling interviews", "automation_probability": 90},
        {"task": "Employee onboarding", "automation_probability": 60},
        {"task": "Benefits administration", "automation_probability": 80},
        {"task": "Employee relations", "automation_probability": 25},
        {"task": "Payroll processing", "automation_probability": 85},
    ],
}

# Define the job analysis tools for Gemini
JOB_RISK_TOOLS = [
    {
        "name": "analyze_job_tasks",
        "description": "Analyze a job title and get its core tasks with automation probability scores",
        "input_schema": {
            "type": "object",
            "properties": {
                "job_title": {
                    "type": "string",
                    "description": "The job title to analyze (e.g., 'Software Engineer', 'Data Analyst')"
                }
            },
            "required": ["job_title"]
        }
    },
    {
        "name": "get_ai_capabilities",
        "description": "Get information about current AI capabilities and what they can automate",
        "input_schema": {
            "type": "object",
            "properties": {
                "capability_type": {
                    "type": "string",
                    "description": "Type of AI capability (e.g., 'text_generation', 'data_analysis', 'image_creation')"
                }
            },
            "required": ["capability_type"]
        }
    }
]

# AI capabilities reference
AI_CAPABILITIES = {
    "text_generation": {
        "examples": ["Email writing", "Report generation", "Content creation", "Documentation"],
        "maturity": "High",
        "cost_per_month": 20,
    },
    "data_analysis": {
        "examples": ["Data cleaning", "Statistical analysis", "Pattern detection", "Forecasting"],
        "maturity": "High",
        "cost_per_month": 50,
    },
    "image_creation": {
        "examples": ["Graphic design", "Photo editing", "Banner creation", "Social media graphics"],
        "maturity": "Medium",
        "cost_per_month": 30,
    },
    "code_generation": {
        "examples": ["Code writing", "Debugging", "Testing", "Documentation"],
        "maturity": "High",
        "cost_per_month": 25,
    },
    "customer_service": {
        "examples": ["FAQ handling", "Ticket routing", "Common issue resolution", "Chatbots"],
        "maturity": "High",
        "cost_per_month": 40,
    },
    "image_analysis": {
        "examples": ["Quality control", "Medical imaging", "Document processing", "Surveillance"],
        "maturity": "Medium",
        "cost_per_month": 35,
    },
}


def analyze_job_tasks(job_title: str) -> list:
    """
    Analyze a job and return its core tasks with AI automation probability.
    Returns task breakdown for the given job.
    """
    # Normalize job title for lookup
    job_title_lower = job_title.lower()
    
    # Try exact match first
    for job, tasks in JOB_TASK_CATALOG.items():
        if job.lower() == job_title_lower:
            return tasks
    
    # Try partial match
    for job, tasks in JOB_TASK_CATALOG.items():
        if job_title_lower in job.lower() or job.lower() in job_title_lower:
            return tasks
    
    # Default: generic task breakdown
    return [
        {"task": "Data processing and analysis", "automation_probability": 75},
        {"task": "Communication and reporting", "automation_probability": 65},
        {"task": "Routine administrative tasks", "automation_probability": 85},
        {"task": "Decision making and strategy", "automation_probability": 40},
        {"task": "Creative or specialized work", "automation_probability": 30},
    ]


def get_ai_capabilities(capability_type: str) -> dict:
    """
    Get information about a specific AI capability.
    Returns what the AI can do and associated costs.
    """
    capability_type_lower = capability_type.lower().replace(" ", "_")
    
    if capability_type_lower in AI_CAPABILITIES:
        return AI_CAPABILITIES[capability_type_lower]
    
    return {
        "examples": ["General AI assistance"],
        "maturity": "Medium",
        "cost_per_month": 30,
    }


def calculate_job_replacement_cost(tasks: list, salary: float) -> float:
    """
    Calculate the estimated monthly cost to replace a job with AI.
    Based on task automation costs.
    """
    base_cost = 100  # Base infrastructure cost
    
    # Calculate task-specific costs
    for task in tasks:
        automation_prob = task.get("automation_probability", 0) / 100
        task_monthly_cost = (salary / 12) * automation_prob * 0.3  # AI costs ~30% of salary for automatable portion
        base_cost += task_monthly_cost * 0.1  # Weight by actual implementation cost
    
    return round(base_cost, 2)


def calculate_overall_risk(tasks: list) -> float:
    """
    Calculate overall AI replacement risk as a percentage.
    Higher = more likely to be automated.
    """
    if not tasks:
        return 0
    
    total_probability = sum(task.get("automation_probability", 0) for task in tasks)
    return round(total_probability / len(tasks), 1)
