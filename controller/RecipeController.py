from models.recipes import (
    obtener_recetas, agregar_receta, obtener_receta_por_id, obtener_receta_por_nombre,
    eliminar_receta_por_id, obtener_receta_por_autor, obtener_receta_por_cuisine, actualizar_receta
)
from utils.business_rules import RecipeBusinessRules
from utils.formatters import format_title
from typing import Optional, Dict, Any, List


class RecipeController:

    @staticmethod
    def get_all_recipes() -> List[Dict[str, Any]]:
        """Obtener todas las recetas"""
        return obtener_recetas()

    @staticmethod
    def create_recipe(title: str, description: str, preparation: str,
                     author_id: Optional[int] = None, cuisine_id: Optional[int] = None) -> Optional[int]:
        """
        Crear una nueva receta con validaciones básicas
        """
        # Validar datos básicos
        valid, error = RecipeBusinessRules.validate_basic_data(title, preparation)
        if not valid:
            print(f"Error de validación en receta: {error}")
            return None

        # Crear receta
        return agregar_receta(
            format_title(title),
            description.strip() if description else "",
            preparation.strip(),
            author_id,
            cuisine_id
        )

    @staticmethod
    def get_recipe_by_id(recipe_id: int) -> Optional[Dict[str, Any]]:
        """Obtener una receta por ID"""
        return obtener_receta_por_id(recipe_id)

    @staticmethod
    def get_recipe_by_title(title: str) -> Optional[Dict[str, Any]]:
        """Obtener una receta por título"""
        return obtener_receta_por_nombre(title)

    @staticmethod
    def get_recipes_by_author(author_id: int) -> List[Dict[str, Any]]:
        """Obtener recetas por autor"""
        return obtener_receta_por_autor(author_id)

    @staticmethod
    def get_recipes_by_cuisine(cuisine_id: int) -> List[Dict[str, Any]]:
        """Obtener recetas por cocina"""
        return obtener_receta_por_cuisine(cuisine_id)

    @staticmethod
    def update_recipe(recipe_id: int, title: str, description: str, preparation: str,
                     author_id: Optional[int] = None, cuisine_id: Optional[int] = None) -> bool:
        """
        Actualizar una receta existente con validaciones básicas
        """
        # Verificar que la receta existe
        current_recipe = obtener_receta_por_id(recipe_id)
        if not current_recipe:
            return False

        # Validar datos básicos
        valid, error = RecipeBusinessRules.validate_basic_data(title, preparation)
        if not valid:
            print(f"Error de validación en receta: {error}")
            return False

        # Actualizar receta
        return actualizar_receta(
            recipe_id,
            format_title(title),
            description.strip() if description else "",
            preparation.strip(),
            author_id,
            cuisine_id
        )

    @staticmethod
    def delete_recipe(recipe_id: int) -> bool:
        """Eliminar una receta"""
        # Verificar que existe
        if not obtener_receta_por_id(recipe_id):
            return False

        return eliminar_receta_por_id(recipe_id)