import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

CUSTOMER = {"id": "c1", "name": "John Doe", "email": "john@example.com"}
ORDERS = [{"product": "Pro Plan", "amount": 99, "status": "paid"}]


@pytest.mark.asyncio
async def test_generate_email_success():
    mock_response = json.dumps({
        "subject": "Following up on your Pro Plan",
        "body": "Hi John, just checking in...",
    })
    with patch("app.api.email.cache_get", new=AsyncMock(return_value=None)), \
         patch("app.api.email.cache_set", new=AsyncMock()), \
         patch("app.api.email._gather_context", new=AsyncMock(return_value=(CUSTOMER, ORDERS))), \
         patch("app.api.email.chat_completion", new=AsyncMock(return_value=mock_response)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/ai/email/generate",
                json={"customer_id": "c1", "tone": "formal", "language": "en"},
            )
    assert resp.status_code == 200
    data = resp.json()
    assert "subject" in data
    assert "body" in data


@pytest.mark.asyncio
async def test_generate_email_cache_hit():
    cached = {"subject": "Cached subject", "body": "Cached body"}
    with patch("app.api.email.cache_get", new=AsyncMock(return_value=cached)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/ai/email/generate",
                json={"customer_id": "c1", "tone": "friendly", "language": "en"},
            )
    assert resp.status_code == 200
    assert resp.json()["subject"] == "Cached subject"
