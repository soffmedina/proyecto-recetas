import bcrypt


def hash_password(password: str) -> str:
    """
    Hashea una contraseña en texto plano.
    Retorna el hash como string.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Compara una contraseña en texto plano con su hash.
    Retorna True si coinciden, False si no.
    """
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )