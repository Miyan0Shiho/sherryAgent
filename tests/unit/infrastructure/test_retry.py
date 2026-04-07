import asyncio
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

import aiohttp

from src.sherry_agent.infrastructure.retry import (
    with_retry,
    check_http_status,
    RetryableError,
)


class TestWithRetry:
    @pytest.mark.asyncio
    async def test_success_on_first_attempt(self):
        call_count = 0
        
        @with_retry(max_retries=3)
        async def successful_func():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = await successful_func()
        
        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_retry_on_client_error(self):
        call_count = 0
        
        @with_retry(max_retries=3, base_delay=0.01, max_delay=0.1)
        async def failing_then_success():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise aiohttp.ClientError("Connection failed")
            return "success"
        
        result = await failing_then_success()
        
        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_retry_on_timeout_error(self):
        call_count = 0
        
        @with_retry(max_retries=2, base_delay=0.01, max_delay=0.1)
        async def timeout_then_success():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise asyncio.TimeoutError("Request timed out")
            return "success"
        
        result = await timeout_then_success()
        
        assert result == "success"
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_retry_on_retryable_error(self):
        call_count = 0
        
        @with_retry(max_retries=3, base_delay=0.01, max_delay=0.1)
        async def retryable_error_then_success():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise RetryableError("Server error", status_code=503)
            return "success"
        
        result = await retryable_error_then_success()
        
        assert result == "success"
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_max_retries_exceeded(self):
        call_count = 0
        
        @with_retry(max_retries=2, base_delay=0.01, max_delay=0.1)
        async def always_fail():
            nonlocal call_count
            call_count += 1
            raise aiohttp.ClientError("Always fails")
        
        with pytest.raises(aiohttp.ClientError, match="Always fails"):
            await always_fail()
        
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_non_retryable_exception_reraised(self):
        call_count = 0
        
        @with_retry(max_retries=3)
        async def raise_value_error():
            nonlocal call_count
            call_count += 1
            raise ValueError("Not retryable")
        
        with pytest.raises(ValueError, match="Not retryable"):
            await raise_value_error()
        
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_exponential_backoff(self):
        delays = []
        original_sleep = asyncio.sleep
        
        async def mock_sleep(delay):
            delays.append(delay)
            await original_sleep(0.001)
        
        call_count = 0
        
        @with_retry(max_retries=3, base_delay=1.0, max_delay=30.0, exponential_base=2.0)
        async def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 4:
                raise aiohttp.ClientError("Fail")
            return "success"
        
        with patch('asyncio.sleep', mock_sleep):
            result = await failing_func()
        
        assert result == "success"
        assert len(delays) == 3
        assert delays[0] == 1.0
        assert delays[1] == 2.0
        assert delays[2] == 4.0

    @pytest.mark.asyncio
    async def test_max_delay_cap(self):
        delays = []
        original_sleep = asyncio.sleep
        
        async def mock_sleep(delay):
            delays.append(delay)
            await original_sleep(0.001)
        
        call_count = 0
        
        @with_retry(max_retries=5, base_delay=10.0, max_delay=15.0, exponential_base=2.0)
        async def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 5:
                raise aiohttp.ClientError("Fail")
            return "success"
        
        with patch('asyncio.sleep', mock_sleep):
            result = await failing_func()
        
        assert result == "success"
        for delay in delays:
            assert delay <= 15.0

    @pytest.mark.asyncio
    async def test_custom_retryable_exceptions(self):
        call_count = 0
        
        @with_retry(
            max_retries=2,
            base_delay=0.01,
            max_delay=0.1,
            retryable_exceptions=(ValueError,)
        )
        async def raise_value_error():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Retryable")
            return "success"
        
        result = await raise_value_error()
        
        assert result == "success"
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_preserves_function_metadata(self):
        @with_retry(max_retries=3)
        async def my_function():
            """This is my function."""
            return "result"
        
        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "This is my function."

    @pytest.mark.asyncio
    async def test_passes_arguments_correctly(self):
        @with_retry(max_retries=3)
        async def func_with_args(a, b, c=None):
            return f"{a}-{b}-{c}"
        
        result = await func_with_args("x", "y", c="z")
        
        assert result == "x-y-z"


class TestCheckHttpStatus:
    def test_success_status(self):
        check_http_status(200, "OK")
        check_http_status(201, "Created")
        check_http_status(204, "No Content")

    def test_retryable_status_500(self):
        with pytest.raises(RetryableError, match="HTTP 500"):
            check_http_status(500, "Internal Server Error")

    def test_retryable_status_502(self):
        with pytest.raises(RetryableError, match="HTTP 502"):
            check_http_status(502, "Bad Gateway")

    def test_retryable_status_503(self):
        with pytest.raises(RetryableError, match="HTTP 503"):
            check_http_status(503, "Service Unavailable")

    def test_retryable_status_504(self):
        with pytest.raises(RetryableError, match="HTTP 504"):
            check_http_status(504, "Gateway Timeout")

    def test_client_error_status_400(self):
        with pytest.raises(aiohttp.ClientResponseError):
            check_http_status(400, "Bad Request")

    def test_client_error_status_401(self):
        with pytest.raises(aiohttp.ClientResponseError):
            check_http_status(401, "Unauthorized")

    def test_client_error_status_404(self):
        with pytest.raises(aiohttp.ClientResponseError):
            check_http_status(404, "Not Found")

    def test_client_error_status_429(self):
        with pytest.raises(aiohttp.ClientResponseError):
            check_http_status(429, "Too Many Requests")


class TestRetryableError:
    def test_creation_with_message(self):
        error = RetryableError("Something went wrong")
        
        assert str(error) == "Something went wrong"
        assert error.status_code is None

    def test_creation_with_status_code(self):
        error = RetryableError("Server error", status_code=503)
        
        assert str(error) == "Server error"
        assert error.status_code == 503

    def test_is_exception(self):
        error = RetryableError("Test error")
        
        assert isinstance(error, Exception)
