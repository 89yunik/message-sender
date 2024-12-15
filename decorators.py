from traceback import format_exc
from sys import exit

def handle_exceptions(logger, exit_program=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Exception occurred in {func.__name__}: {e}\n{format_exc()}")
                if exit_program: exit(1)
        return wrapper
    return decorator