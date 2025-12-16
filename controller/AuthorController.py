from models.author import agregar_author
from utils.hash import hash_password


class AuthorController:

    @staticmethod
    def create_author(name,  email, password_hash, avatar_url="", biography=""):
        """Crear un nuevo autor"""
        password_hasheado = hash_password(password_hash)
        response = agregar_author(name, email, password_hasheado, avatar_url, biography)
        return response

    @staticmethod
    def get_author_by_id(author_id):
        """Obtener un autor por ID"""
        pass

    @staticmethod
    def get_author_by_email(email):
        """Obtener un autor por correo"""
        pass

    @staticmethod
    def get_all_authors():
        """Obtener todos los autores"""
        pass

    @staticmethod
    def update_author(author_id):
        """Modificar un autor existente"""
        pass

    @staticmethod
    def delete_author(author_id):
        """Eliminar un autor"""
        pass