import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_summary_success():
    mock_response = json.dumps({
        "summary": "Q3 planning meeting",
        "action_items": ["Send report by Friday"],
        "key_points": ["Budget approved"],
    })
    with patch("app.api.summary.chat_completion", new=AsyncMock(return_value=mock_response)), \
         patch("app.api.summary.cache_get", new=AsyncMock(return_value=None)), \
         patch("app.api.summary.cache_set", new=AsyncMock()):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post("/ai/summary", json={"text": "We discussed Q3 budget."})
    assert resp.status_code == 200
    data = resp.json()
    assert data["summary"] == "Q3 planning meeting"
    assert len(data["action_items"]) == 1
    assert len(data["key_points"]) == 1


@pytest.mark.asyncio
async def test_summary_cache_hit():
    cached = {
        "summary": "cached summary",
        "action_items": [],
        "key_points": [],
    }
    with patch("app.api.summary.cache_get", new=AsyncMock(return_value=cached)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post("/ai/summary", json={"text": "anything"})
    assert resp.status_code == 200
    assert resp.json()["summary"] == "cached summary"
