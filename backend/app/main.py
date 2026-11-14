from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.routers import auth, resources, users

settings = get_settings()

app = FastAPI(title="Campus Sports Booking API", version="0.1.0")
register_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base URL from the API contract on Confluence: http://localhost:8000/api/v1
api = APIRouter(prefix="/api/v1")
api.include_router(auth.router)
api.include_router(users.router)
api.include_router(resources.router)


@api.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api)
