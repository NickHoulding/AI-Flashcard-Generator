from dotenv import load_dotenv
import os

# Load the .env file.
load_dotenv(dotenv_path='.env')

def get_env_var(key: str):
    """
    Get an environment variable from the .env file.
    Args:
        key (str): The key of the environment variable.
    Returns:
        str: The value of the environment variable, or None if not found.
    """
    return os.getenv(key)