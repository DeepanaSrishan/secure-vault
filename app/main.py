from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.database.base import Base
from app.database.database import engine

# Import Models
from app.models import User, Vault, AuditLog

# Import Routers
from app.api.v1.auth import router as auth_router
from app.api.v1.vault import router as vault_router
from app.api.v1.security import router as security_router

# Import Security
from app.core.rate_limit import limiter
from app.core.security_headers import SecurityHeadersMiddleware

# Import Exception Handlers
from app.core.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)

app = FastAPI(
    title="SecureVault API",
    version="1.0.0"
)

# -------------------------------
# Rate Limiter
# -------------------------------
app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

# -------------------------------
# Global Exception Handlers
# -------------------------------
app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)

# -------------------------------
# CORS
# -------------------------------
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Security Headers
# -------------------------------
app.add_middleware(SecurityHeadersMiddleware)

# -------------------------------
# Create Database Tables
# -------------------------------
Base.metadata.create_all(bind=engine)

# -------------------------------
# Register Routers
# -------------------------------
app.include_router(auth_router)
app.include_router(vault_router)
app.include_router(security_router)

# -------------------------------
# Home Route
# -------------------------------
@app.get("/")
def home():
    return {
        "success": True,
        "message": "SecureVault API Running"
    }