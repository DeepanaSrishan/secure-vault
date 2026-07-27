from fastapi import FastAPI

from app.database.database import engine
from app.database.base import Base
from app.models import User, Vault
from app.api.v1.vault import router as vault_router

# Import models
from app.models import User
from app.api.v1.auth import router as auth_router
app = FastAPI(
    title="SecureVault API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(vault_router)

@app.get("/")
def home():
    return {
        "message": "SecureVault API Running"
    }