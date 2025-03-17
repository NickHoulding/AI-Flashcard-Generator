import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv(dotenv_path='.env')

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