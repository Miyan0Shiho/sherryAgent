import asyncio
import functools
import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

import aiohttp

T = TypeVar('T')

logger = logging.getLogger(__name__)


class RetryableError(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def with_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential_base: float = 2.0,
    retryable_exceptions: tuple[type[Exception], ...] = (
        aiohttp.ClientError,
        aiohttp.ClientConnectionError,
        asyncio.TimeoutError,
        RetryableError,
    ),
    retryable_status_codes: tuple[int, ...] = (500, 502, 503, 504),
):
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception: Exception | None = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e

                    if attempt < max_retries:
                        delay = min(base_delay * (exponential_base ** attempt), max_delay)

                        status_info = ""
                        if isinstance(e, RetryableError) and e.status_code:
                            status_info = f" (status: {e.status_code})"

                        logger.warning(
                            f"Retry attempt {attempt + 1}/{max_retries} for {func.__name__}: "
                            f"{type(e).__name__}{status_info}, waiting {delay:.1f}s"
                        )

                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_retries} retry attempts failed for {func.__name__}: "
                            f"{type(e).__name__}: {e}"
                        )
                except Exception:
                    raise

            if last_exception:
                raise last_exception

            raise RuntimeError("Unexpected state in retry logic")

        return wrapper

    return decorator


def check_http_status(status: int, response_text: str = "") -> None:
    retryable_codes = (500, 502, 503, 504)

    if status in retryable_codes:
        raise RetryableError(
            f"HTTP {status}: {response_text}",
            status_code=status
        )

    if status >= 400:
        raise aiohttp.ClientResponseError(
            request_info=None,
            history=(),
            status=status,
            message=response_text
        )
