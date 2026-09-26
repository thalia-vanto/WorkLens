import os

from dotenv import load_dotenv


def load_config() -> tuple[str, str]:
    """Load the Gemini API configuration from a local .env file."""
    load_dotenv()

    api_key = os.getenv('GEMINI_API_KEY', '').strip()
    if not api_key or api_key == 'your_api_key_here':
        raise ValueError(
            'Missing GEMINI_API_KEY. Create a .env file in the project root and add:\n'
            'GEMINI_API_KEY=your_key_here\n'
            'GEMINI_MODEL=gemini-2.0-flash'
        )

    model = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    return api_key, model
