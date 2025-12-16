from models.author import agregar_author, obtener_author, obtener_author_por_id, eliminar_author, actualizar_author
from utils.hash import hash_password
from utils.business_rules import AuthorBusinessRules
from typing import Optional, Dict, Any


class AuthorController:

    @staticmethod
    def create_author(name: str, email: str, password: str, biography: str = "") -> Optional[int]:
        """
        Crear un nuevo autor con validaciones básicas
        Retorna el ID del autor creado o None si hay error
        """
        # Validar datos básicos
        valid, error = AuthorBusinessRules.validate_create_data(name, email, password)
        if not valid:
            print(f"Error de validación: {error}")
            return None

        # Verificar unicidad de email
        if not AuthorBusinessRules.check_email_uniqueness(email):
            print("Email ya existe")
            return None

        # Hashear password
        password_hasheado = hash_password(password)

        # Crear autor
        result = agregar_author(name.strip(), email.strip().lower(), password_hasheado, "", biography.strip())

        return result

    @staticmethod
    def get_author_by_id(author_id: int) -> Optional[Dict[str, Any]]:
        """Obtener un autor por ID"""
        return obtener_author_por_id(author_id)

    @staticmethod
    def get_author_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Obtener un autor por correo"""
        authors = obtener_author()
        for author in authors:
            if author['email'].lower() == email.lower():
                return author
        return None

    @staticmethod
    def get_all_authors() -> list:
        """Obtener todos los autores"""
        return obtener_author()

    @staticmethod
    def update_author(author_id: int, name: str, email: str, biography: str = "") -> bool:
        """
        Modificar un autor existente con validaciones básicas
        """
        # Obtener datos actuales
        current_author = obtener_author_por_id(author_id)
        if not current_author:
            return False

        # Validar datos básicos
        valid, error = AuthorBusinessRules.validate_update_data(name, email)
        if not valid:
            print(f"Error de validación: {error}")
            return False

        # Verificar unicidad de email (excluyendo el autor actual)
        if not AuthorBusinessRules.check_email_uniqueness(email, author_id):
            print("Email ya existe")
            return False

        # Actualizar autor (mantener password y avatar)
        return actualizar_author(
            author_id,
            name.strip(),
            email.strip().lower(),
            current_author['password_hash'],
            current_author.get('avatar_url', ''),
            biography.strip()
        )

    @staticmethod
    def delete_author(author_id: int) -> bool:
        """Eliminar un autor"""
        # Verificar que existe
        if not obtener_author_por_id(author_id):
            return False

        return eliminar_author(author_id) is not None