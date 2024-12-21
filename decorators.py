
from traceback import format_exc
from logging_config import setup_logging

def log_exceptions (logger=None):
    logger = logger or setup_logging()
    def decorator (func):
        def wrapper (*args, **kwargs):
            try: 
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Exception occurred in {func.__name__}: {e}\n{format_exc()}")
                raise
        return wrapper
    return decorator