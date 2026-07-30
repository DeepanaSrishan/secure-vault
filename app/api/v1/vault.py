from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.services.audit_service import create_log


from app.schemas.vault import (
    VaultCreate,
    VaultResponse,
    VaultUpdate
)

from app.services.vault_service import (
    create_password,
    get_user_passwords,
    delete_password
)

from app.api.v1.auth import get_current_user

from app.models.user import User
from app.models.vault import Vault

from app.utils.encryption import (
    encrypt_password,
    decrypt_password
)


router = APIRouter(
    prefix="/api/v1/vault",
    tags=["Vault"]
)


# =================================
# CREATE PASSWORD
# =================================

@router.post(
    "",
    response_model=VaultResponse,
    status_code=status.HTTP_201_CREATED
)
def create_vault(
    data: VaultCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_password(
        data,
        current_user.id,
        db
    )


# =================================
# GET ALL PASSWORDS
# =================================

@router.get(
    "",
    response_model=List[VaultResponse]
)
def get_passwords(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_user_passwords(
        current_user.id,
        db
    )


# =================================
# GET PASSWORD BY ID
# =================================

@router.get("/{vault_id}")
def get_vault(
    vault_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    vault = db.query(Vault).filter(
        Vault.id == vault_id,
        Vault.user_id == current_user.id
    ).first()


    if not vault:
        raise HTTPException(
            status_code=404,
            detail="Password not found"
        )
    
    create_log(
    current_user.id,
    "VIEW_PASSWORD",
    db
)




    return {
        "id": vault.id,
        "website": vault.website,
        "username": vault.username,
        "password": decrypt_password(
            vault.password
        )
    }



# =================================
# UPDATE PASSWORD
# =================================

@router.put("/{vault_id}")
def update_vault(
    vault_id: int,
    data: VaultUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    vault = db.query(Vault).filter(
        Vault.id == vault_id,
        Vault.user_id == current_user.id
    ).first()


    if not vault:
        raise HTTPException(
            status_code=404,
            detail="Password not found"
        )


    vault.website = data.website
    vault.username = data.username
    vault.password = encrypt_password(
        data.password
    )


    db.commit()
    db.refresh(vault)


    return {
        "message": "Password updated successfully"
    }



# =================================
# DELETE PASSWORD
# =================================

@router.delete("/{vault_id}")
def delete_vault(
    vault_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    deleted = delete_password(
        vault_id,
        current_user.id,
        db
    )


    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Password not found"
        )


    return {
        "message": "Password deleted successfully"
    }