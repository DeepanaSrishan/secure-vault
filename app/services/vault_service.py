from sqlalchemy.orm import Session

from app.models.vault import Vault
from app.schemas.vault import (
    VaultCreate,
    VaultUpdate
)

from app.utils.encryption import encrypt_password


# ==========================
# CREATE PASSWORD
# ==========================

def create_password(
    data: VaultCreate,
    user_id: int,
    db: Session
):

    vault = Vault(
        website=data.website,
        username=data.username,
        password=encrypt_password(data.password),
        user_id=user_id
    )

    db.add(vault)
    db.commit()
    db.refresh(vault)

    return vault



# ==========================
# GET ALL PASSWORDS
# ==========================

def get_user_passwords(
    user_id: int,
    db: Session
):

    return db.query(Vault).filter(
        Vault.user_id == user_id
    ).all()



# ==========================
# UPDATE PASSWORD
# ==========================

def update_password(
    vault_id: int,
    data: VaultUpdate,
    user_id: int,
    db: Session
):

    vault = db.query(Vault).filter(
        Vault.id == vault_id,
        Vault.user_id == user_id
    ).first()


    if not vault:
        return None


    vault.website = data.website
    vault.username = data.username
    vault.password = encrypt_password(
        data.password
    )


    db.commit()
    db.refresh(vault)

    return vault



# ==========================
# DELETE PASSWORD
# ==========================

def delete_password(
    vault_id: int,
    user_id: int,
    db: Session
):

    vault = db.query(Vault).filter(
        Vault.id == vault_id,
        Vault.user_id == user_id
    ).first()


    if not vault:
        return False


    db.delete(vault)
    db.commit()

    return True

def delete_password(
    vault_id: int,
    user_id: int,
    db: Session
):

    vault = db.query(Vault).filter(
        Vault.id == vault_id,
        Vault.user_id == user_id
    ).first()


    if not vault:
        return False


    db.delete(vault)
    db.commit()

    return True