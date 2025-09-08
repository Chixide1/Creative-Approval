from typing import Awaitable, Callable
from fastapi import Request, Response, FastAPI
from src.routers.main_router import router
from starlette.responses import Response
    

app = FastAPI(title="Creative Approval Service", version="1.0.0")
app.state.metrics = {
    "total_requests": 0,
    "APPROVED": 0,
    "REJECTED": 0,
    "REQUIRES_REVIEW": 0
}


app.include_router(router)

@app.middleware("http")
async def log_requests(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    app.state.metrics["total_requests"] += 1
    response = await call_next(request)
    return response