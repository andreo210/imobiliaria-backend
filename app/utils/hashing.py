from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def codificar_senha(password: str) -> str:
    return pwd_context.hash(password)

def decodificar_senha(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
