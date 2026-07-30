from fastapi import APIRouter, Depends, HTTPException, status,Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.services.audit_service import create_log
from app.database.database import get_db

from app.models.user import User
from app.core.rate_limit import limiter

from app.schemas.user import (
    UserRegister,
    UserResponse,
    UserLogin,
)

from app.services.auth_service import (
    register_user,
    login_user,
)

from app.core.security import (
    create_access_token,
    verify_token,
)


# JWT Token Reader
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


# ==========================
# Register User
# ==========================
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    created_user = register_user(
        user,
        db
    )

    if created_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    return created_user



# ==========================
# Login User
# ==========================
@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = login_user(
        user.email,
        user.password,
        db
    )


    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    


    access_token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    create_log(
    db_user.id,
    "LOGIN",
    db
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ==========================
# OAuth2 Token Login (Swagger)
# ==========================
@router.post("/token")
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = login_user(
        form_data.username,
        form_data.password,
        db
    )

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



# ==========================
# Get Current User
# ==========================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    print("TOKEN RECEIVED:", token)


    email = verify_token(token)


    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )


    user = db.query(User).filter(
        User.email == email
    ).first()


    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )


    return user



# ==========================
# My Profile
# ==========================
@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):

    return current_user