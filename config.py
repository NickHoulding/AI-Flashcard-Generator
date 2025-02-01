import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

def get_env_var(key: str):
    """
    Get an environment variable value.
    
    Args:
        key (str): The key of the environment variable.
    Returns:
        str: Environment variable value if it exists, else None.
    """
    return os.getenv(key)