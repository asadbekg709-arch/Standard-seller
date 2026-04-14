import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

CUSTOMER = {"id": "c1", "name": "Bob", "email": "bob@example.com", "status": "active"}


@pytest.mark.asyncio
async def test_chat_success():
    mock_response = json.dumps({"answer": "Bob has been a customer since 2022."})
    with patch("app.api.chat.context_builder.fetch_customer", new=AsyncMock(return_value=CUSTOMER)), \
         patch("app.api.chat.chat_completion", new=AsyncMock(return_value=mock_response)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/ai/chat",
                json={"customer_id": "c1", "question": "How long has this customer been with us?"},
            )
    assert resp.status_code == 200
    assert "answer" in resp.json()


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
