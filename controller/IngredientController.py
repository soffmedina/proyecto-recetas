from models.ingredients import (
    obtener_ingrediente, agregar_ingrediente, obtener_ingrediente_por_id,
    obtener_ingrediente_por_nombre, eliminar_ingrediente_por_id, actualizar_ingrediente
)
from utils.validators import validate_required_text
from utils.formatters import format_title
from typing import Optional, Dict, Any, List


class IngredientController:

    @staticmethod
    def get_all_ingredients() -> List[Dict[str, Any]]:
        """Obtener todos los ingredientes"""
        return obtener_ingrediente()

    @staticmethod
    def create_ingredient(name: str) -> Optional[int]:
        """
        Crear un nuevo ingrediente con validación básica
        """
        # Validar nombre
        valid, error = validate_required_text(name, "Nombre del ingrediente", 2)
        if not valid:
            print(f"Error de validación: {error}")
            return None

        # Verificar unicidad
        formatted_name = format_title(name)
        if not IngredientController._check_name_uniqueness(formatted_name):
            print("Ya existe un ingrediente con ese nombre")
            return None

        # Crear ingrediente
        return agregar_ingrediente(formatted_name)

    @staticmethod
    def get_ingredient_by_id(ingredient_id: int) -> Optional[Dict[str, Any]]:
        """Obtener un ingrediente por ID"""
        return obtener_ingrediente_por_id(ingredient_id)

    @staticmethod
    def get_ingredient_by_name(name: str) -> Optional[Dict[str, Any]]:
        """Obtener un ingrediente por nombre"""
        return obtener_ingrediente_por_nombre(name)

    @staticmethod
    def update_ingredient(ingredient_id: int, name: str) -> bool:
        """
        Actualizar un ingrediente existente
        """
        # Verificar que existe
        current_ingredient = obtener_ingrediente_por_id(ingredient_id)
        if not current_ingredient:
            return False

        # Validar nombre
        valid, error = validate_required_text(name, "Nombre del ingrediente", 2)
        if not valid:
            print(f"Error de validación: {error}")
            return False

        # Verificar unicidad (excluyendo el ingrediente actual)
        formatted_name = format_title(name)
        if not IngredientController._check_name_uniqueness(formatted_name, ingredient_id):
            print("Ya existe otro ingrediente con ese nombre")
            return False

        # Actualizar ingrediente
        return actualizar_ingrediente(ingredient_id, formatted_name)

    @staticmethod
    def delete_ingredient(ingredient_id: int) -> bool:
        """Eliminar un ingrediente"""
        # Verificar que existe
        if not obtener_ingrediente_por_id(ingredient_id):
            return False

        return eliminar_ingrediente_por_id(ingredient_id)

    @staticmethod
    def _check_name_uniqueness(name: str, exclude_id: int = None) -> bool:
        """Verificar si el nombre es único"""
        ingredients = obtener_ingrediente()
        for ingredient in ingredients:
            if ingredient['name'].lower() == name.lower():
                if exclude_id is None or ingredient['id'] != exclude_id:
                    return False
        return True