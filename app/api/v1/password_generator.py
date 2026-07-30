print("✅ password_tools.py loaded")
from fastapi import APIRouter

from app.utils.password_generator import generate_password


router = APIRouter(
    prefix="/api/v1/tools",
    tags=["Security Tools"]
)


@router.get("/generate-password")
def password_generator():

    return {
        "password": generate_password()
    }