import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import email, lead, summary, chat
from app.core.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="radius-ai-service",
    version="1.0.0",
    description="AI-powered features for CRM system",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start = time.monotonic()
    response = await call_next(request)
    elapsed = round(time.monotonic() - start, 3)
    logger.info(
        f"rid={request_id} method={request.method} "
        f"path={request.url.path} status={response.status_code} time={elapsed}s"
    )
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "Internal server error"},
    )


app.include_router(email.router, prefix="/ai/email", tags=["email"])
app.include_router(lead.router, prefix="/ai/lead", tags=["lead"])
app.include_router(summary.router, prefix="/ai/summary", tags=["summary"])
app.include_router(chat.router, prefix="/ai/chat", tags=["chat"])


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
