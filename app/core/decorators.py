from app.core.functions import handle_error


def handle_exception_decorator(error_message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handle_error(f"{error_message}: {e}")
        return wrapper
    return decorator
