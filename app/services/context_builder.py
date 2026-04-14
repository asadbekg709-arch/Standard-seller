import httpx

from app.core.config import get_settings
from app.core.logger import get_logger

logger = get_logger(__name__)


async def fetch_customer(customer_id: str) -> dict:
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=settings.timeout) as client:
            resp = await client.get(
                f"{settings.user_service_url}/users/{customer_id}"
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.warning(f"Failed to fetch customer {customer_id}: {e}")
        return {"id": customer_id, "name": "Unknown", "email": ""}


async def fetch_orders(customer_id: str) -> list:
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=settings.timeout) as client:
            resp = await client.get(
                f"{settings.order_service_url}/orders",
                params={"customer_id": customer_id},
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.warning(f"Failed to fetch orders for {customer_id}: {e}")
        return []


async def fetch_activities(customer_id: str) -> list:
    settings = get_settings()
    crm_url = settings.crm_service_url
    if not crm_url:
        return []
    try:
        async with httpx.AsyncClient(timeout=settings.timeout) as client:
            resp = await client.get(
                f"{crm_url}/activities",
                params={"customer_id": customer_id},
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.warning(f"Failed to fetch activities for {customer_id}: {e}")
        return []
