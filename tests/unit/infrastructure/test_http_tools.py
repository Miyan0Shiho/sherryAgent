from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from src.sherry_agent.infrastructure.tools.http_tools import http_request


@pytest.fixture
def mock_aiohttp():
    with patch("src.sherry_agent.infrastructure.tools.http_tools.aiohttp") as mock:
        yield mock


@pytest.mark.asyncio
async def test_http_request_success(mock_aiohttp):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "text/plain"}
    mock_response.url = "https://example.com"
    mock_response.text = AsyncMock(return_value="Hello, World!")

    mock_context_manager = MagicMock()
    mock_context_manager.__aenter__.return_value = mock_response

    mock_session = MagicMock()
    mock_session.request.return_value = mock_context_manager

    mock_client_session = MagicMock()
    mock_client_session.__aenter__.return_value = mock_session

    mock_aiohttp.ClientSession.return_value = mock_client_session

    result = await http_request("https://example.com", "GET")

    assert result.success is True
    assert result.content == "Hello, World!"
    assert result.metadata["status_code"] == 200


@pytest.mark.asyncio
async def test_http_request_client_error(mock_aiohttp):
    mock_aiohttp.ClientSession.side_effect = Exception("Connection error")

    result = await http_request("https://example.com", "GET")

    assert result.success is False
    assert "HTTP request failed" in result.content


@pytest.mark.asyncio
async def test_http_request_server_error(mock_aiohttp):
    mock_response = MagicMock()
    mock_response.status = 500
    mock_response.headers = {}
    mock_response.url = "https://example.com"
    mock_response.text = AsyncMock(return_value="Internal Server Error")

    mock_context_manager = MagicMock()
    mock_context_manager.__aenter__.return_value = mock_response

    mock_session = MagicMock()
    mock_session.request.return_value = mock_context_manager

    mock_client_session = MagicMock()
    mock_client_session.__aenter__.return_value = mock_session

    mock_aiohttp.ClientSession.return_value = mock_client_session

    result = await http_request("https://example.com", "GET")

    assert result.success is False
    assert result.content == "Internal Server Error"
    assert result.metadata["status_code"] == 500


@pytest.mark.asyncio
async def test_http_request_with_headers_and_body(mock_aiohttp):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.headers = {}
    mock_response.url = "https://example.com"
    mock_response.text = AsyncMock(return_value="OK")

    mock_context_manager = MagicMock()
    mock_context_manager.__aenter__.return_value = mock_response

    mock_session = MagicMock()
    mock_session.request.return_value = mock_context_manager

    mock_client_session = MagicMock()
    mock_client_session.__aenter__.return_value = mock_session

    mock_aiohttp.ClientSession.return_value = mock_client_session

    headers = {"X-Test": "value"}
    body = "test body"

    result = await http_request(
        "https://example.com",
        "POST",
        headers=headers,
        body=body,
    )

    assert result.success is True
    mock_session.request.assert_called_once_with(
        method="POST",
        url="https://example.com",
        headers=headers,
        data=body,
    )
