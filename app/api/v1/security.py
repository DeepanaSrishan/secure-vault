from fastapi import APIRouter

from app.utils.password_generator import generate_password

from app.schemas.security import PasswordCheckRequest

from app.utils.password_checker import (
    check_password_strength
)


router = APIRouter(
    prefix="/api/v1/security",
    tags=["Security"]
)


# Generate Secure Password
@router.get("/generate-password")
def generate_new_password():

    password = generate_password()

    return {
        "password": password
    }



# Check Password Strength
@router.post("/check-password")
def check_password(
    data: PasswordCheckRequest
):

    result = check_password_strength(
        data.password
    )

    return result