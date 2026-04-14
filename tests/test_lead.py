import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

CUSTOMER = {"id": "c1", "name": "Alice", "industry": "Tech", "company_size": "50"}
ORDERS = [{"product": "Enterprise", "amount": 500, "status": "paid"}]
ACTIVITIES = [{"type": "call", "description": "Discussed renewal"}]


@pytest.mark.asyncio
async def test_score_lead_success():
    mock_response = json.dumps({
        "score": 85,
        "priority": "high",
        "reason": "Multiple high-value orders and recent activity",
    })
    with patch("app.api.lead.cache_get", new=AsyncMock(return_value=None)), \
         patch("app.api.lead.cache_set", new=AsyncMock()), \
         patch("app.api.lead.context_builder.fetch_customer", new=AsyncMock(return_value=CUSTOMER)), \
         patch("app.api.lead.context_builder.fetch_orders", new=AsyncMock(return_value=ORDERS)), \
         patch("app.api.lead.context_builder.fetch_activities", new=AsyncMock(return_value=ACTIVITIES)), \
         patch("app.api.lead.chat_completion", new=AsyncMock(return_value=mock_response)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post("/ai/lead/score", json={"customer_id": "c1"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["score"] == 85
    assert data["priority"] == "high"
    assert "reason" in data
