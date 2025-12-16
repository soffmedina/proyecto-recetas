from utils.validators import validate_email, validate_password, validate_required_text


class AuthorBusinessRules:
    """Reglas básicas para autores"""

    @staticmethod
    def validate_create_data(name: str, email: str, password: str) -> tuple[bool, str]:
        """Valida datos para crear autor"""
        # Validar campos requeridos
        valid, error = validate_required_text(name, "Nombre", 2)
        if not valid:
            return False, error

        valid, error = validate_email(email)
        if not valid:
            return False, error

        valid, error = validate_password(password)
        if not valid:
            return False, error

        return True, ""

    @staticmethod
    def validate_update_data(name: str, email: str) -> tuple[bool, str]:
        """Valida datos para actualizar autor"""
        valid, error = validate_required_text(name, "Nombre", 2)
        if not valid:
            return False, error

        valid, error = validate_email(email)
        if not valid:
            return False, error

        return True, ""

    @staticmethod
    def check_email_uniqueness(email: str, exclude_id: int = None) -> bool:
        """Verifica si email es único"""
        from models.author import obtener_author
        authors = obtener_author()
        for author in authors:
            if author['email'].lower() == email.lower():
                if exclude_id is None or author['id'] != exclude_id:
                    return False
        return True


class RecipeBusinessRules:
    """Reglas básicas para recetas"""

    @staticmethod
    def validate_basic_data(title: str, preparation: str) -> tuple[bool, str]:
        """Valida datos básicos de receta"""
        valid, error = validate_required_text(title, "Título", 3)
        if not valid:
            return False, error

        valid, error = validate_required_text(preparation, "Preparación", 10)
        if not valid:
            return False, error

        return True, ""