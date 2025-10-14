import time
import asyncio
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def timed(label: str | None = None):
    """Measure and log how long a function takes to run."""
    def decorator(func):
        # figure out whether the function is async or not
        is_async = asyncio.iscoroutinefunction(func)
        if is_async:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    result = await func(*args, **kwargs)
                except Exception:
                    elapsed = (time.perf_counter() - start) * 1000
                    name = label or func.__name__
                    logger.exception(f"timed({name}): {elapsed:.2f} ms [ERROR]")
                    raise
                else:
                    elapsed = (time.perf_counter() - start) * 1000
                    name = label or func.__name__
                    logger.info(f"timed({name}): {elapsed:.2f} ms")
                    return result
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                except Exception:
                    elapsed = (time.perf_counter() - start) * 1000
                    name = label or func.__name__
                    logger.exception(f"timed({name}): {elapsed:.2f} ms [ERROR]")
                    raise
                else:
                    elapsed = (time.perf_counter() - start) * 1000
                    name = label or func.__name__
                    logger.info(f"timed({name}): {elapsed:.2f} ms")
                    return result
            return sync_wrapper
    return decorator