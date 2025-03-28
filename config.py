import os
from dotenv import load_dotenv
from typing import Optional

PROG_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(PROG_PATH, '.env'))

def get_env_var(
        key: str
    ) -> Optional[str]:
    """
    Gets an environment variable value, 
    or None if it doesn't exist.
    
    Args:
        key (str): Environment variable's key.
    
    Returns:
        str: The key's value if it exists, else None.
    
    Raises:
        None
    """
    return os.getenv(key)

def get_absolute_path(
        env_key: str
    ) -> str:
    """
    Gets an absolute path from an environment variable.
    If the path is relative, it will be resolved relative to PROG_PATH.
    
    Args:
        env_key (str): Environment variable key for the path.
    
    Returns:
        str: The absolute path.
    
    Raises:
        ValueError: If the environment variable doesn't exist.
    """
    path = get_env_var(env_key)
    if path is None:
        raise ValueError(f"Environment variable {env_key} not found")

    if os.path.isabs(path):
        return path
    
    return os.path.join(PROG_PATH, path)