import re


def validate_email(email: str) -> tuple[bool, str]:
    """Valida email básico"""
    if not email or not email.strip():
        return False, "Email es obligatorio"
    if "@" not in email or "." not in email:
        return False, "Email inválido"
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """Valida password básico"""
    if not password or len(password) < 6:
        return False, "Password debe tener al menos 6 caracteres"
    return True, ""


def validate_required_text(text: str, field_name: str, min_length: int = 1) -> tuple[bool, str]:
    """Valida texto requerido"""
    if not text or not text.strip():
        return False, f"{field_name} es obligatorio"
    if len(text.strip()) < min_length:
        return False, f"{field_name} debe tener al menos {min_length} caracteres"
    return True, ""