import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv(dotenv_path='.env')

def get_env_var(key: str) -> Optional[str]:
    """
    Gets an environment variable value, or None if it doesn't exist.
    
    Args:
        key (str): The key of the environment variable.
    Returns:
        str: Environment variable value if it exists, else None.
    """
    return os.getenv(key)