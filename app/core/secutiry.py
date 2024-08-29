import bcrypt
from passlib.context import CryptContext

password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_salt() -> str:
    return bcrypt.gensalt().decode()


def get_password_hash(password: str) -> str:
    return password_ctx.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_ctx.verify(plain_password, hashed_password)
