from cryptography.fernet import Fernet

from app.core.config import ENCRYPTION_KEY


cipher = Fernet(
    ENCRYPTION_KEY.encode()
)


def encrypt_password(password: str):

    encrypted = cipher.encrypt(
        password.encode()
    )

    return encrypted.decode()



def decrypt_password(encrypted_password: str):

    decrypted = cipher.decrypt(
        encrypted_password.encode()
    )

    return decrypted.decode()