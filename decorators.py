def handle_exceptions(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Exception occurred in {func.__name__}: {e}")
                return None
        return wrapper
    return decorator