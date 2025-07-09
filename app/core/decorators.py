from functools import wraps

import typer


def handle_exception_decorator(error_message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                from app.core.functions import handle_error
                handle_error(f"{error_message}: {e}")
                raise typer.Exit(code=1)
        return wrapper
    return decorator
