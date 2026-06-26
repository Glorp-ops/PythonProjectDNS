import bcrypt


def encrypt_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(hashed_password: bytes, password: bytes) -> bool:
    return bcrypt.checkpw(password, hashed_password)
