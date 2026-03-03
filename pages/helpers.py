import os

def get_env_var(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Required environment variable '{key}' is not set!")
    return value