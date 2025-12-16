from models.recipe_ingredients import (
    obtener_ingredientes_receta, agregar_ingrediente_a_receta,
    eliminar_ingrediente_de_receta, actualizar_cantidad_ingrediente_en_receta
)
from models.recipes import obtener_receta_por_id
from models.ingredients import obtener_ingrediente_por_id
from utils.validators import validate_required_text
from utils.formatters import clean_text
from typing import Optional, Dict, Any, List


class RecipeIngredientController:

    @staticmethod
    def get_ingredients_for_recipe(recipe_id: int) -> List[Dict[str, Any]]:
        """Obtener ingredientes de una receta"""
        return obtener_ingredientes_receta(recipe_id)

    @staticmethod
    def add_ingredient_to_recipe(recipe_id: int, ingredient_id: int, quantity: str = "",
                               unit: str = "", notes: str = "") -> Optional[int]:
        """
        Agregar un ingrediente a una receta con validación básica
        """
        # Verificar que receta existe
        if not obtener_receta_por_id(recipe_id):
            print("La receta no existe")
            return None

        # Verificar que ingrediente existe
        if not obtener_ingrediente_por_id(ingredient_id):
            print("El ingrediente no existe")
            return None

        # Limpiar datos
        cleaned_quantity = quantity.strip() if quantity else ""
        cleaned_unit = clean_text(unit) if unit else ""
        cleaned_notes = clean_text(notes) if notes else ""

        # Agregar ingrediente
        return agregar_ingrediente_a_receta(
            recipe_id, ingredient_id, cleaned_quantity, cleaned_unit, cleaned_notes
        )

    @staticmethod
    def remove_ingredient_from_recipe(recipe_id: int, ingredient_id: int) -> bool:
        """Eliminar un ingrediente de una receta"""
        return eliminar_ingrediente_de_receta(recipe_id, ingredient_id)

    @staticmethod
    def update_ingredient_in_recipe(recipe_id: int, ingredient_id: int, quantity: str,
                                  unit: str = "", notes: str = "") -> bool:
        """
        Actualizar cantidad de ingrediente en una receta
        """
        # Verificar que receta existe
        if not obtener_receta_por_id(recipe_id):
            print("La receta no existe")
            return False

        # Verificar que ingrediente existe
        if not obtener_ingrediente_por_id(ingredient_id):
            print("El ingrediente no existe")
            return False

        # Limpiar datos
        cleaned_quantity = quantity.strip() if quantity else ""
        cleaned_unit = clean_text(unit) if unit else ""
        cleaned_notes = clean_text(notes) if notes else ""

        # Actualizar
        try:
            actualizar_cantidad_ingrediente_en_receta(
                recipe_id, ingredient_id, cleaned_quantity, cleaned_unit, cleaned_notes
            )
            return True
        except:
            return False

    @staticmethod
    def bulk_update_recipe_ingredients(recipe_id: int, ingredients_data: List[Dict[str, Any]]) -> bool:
        """
        Actualizar múltiples ingredientes de una receta de forma atómica
        ingredients_data: lista de dicts con keys: ingredient_id, quantity, unit, notes
        """
        try:
            # Verificar que receta existe
            if not obtener_receta_por_id(recipe_id):
                print("La receta no existe")
                return False

            # Obtener ingredientes actuales
            current_ingredients = obtener_ingredientes_receta(recipe_id)

            # Crear set de IDs actuales y nuevos
            current_ids = {ing['id'] for ing in current_ingredients}
            new_ids = {data['ingredient_id'] for data in ingredients_data}

            # Eliminar ingredientes que ya no están
            for ing in current_ingredients:
                if ing['id'] not in new_ids:
                    eliminar_ingrediente_de_receta(recipe_id, ing['id'])

            # Agregar o actualizar ingredientes
            for data in ingredients_data:
                # Verificar que ingrediente existe
                if not obtener_ingrediente_por_id(data['ingredient_id']):
                    print(f"El ingrediente {data['ingredient_id']} no existe")
                    continue

                # Limpiar datos
                cleaned_quantity = data.get('quantity', '').strip()
                cleaned_unit = clean_text(data.get('unit', ''))
                cleaned_notes = clean_text(data.get('notes', ''))

                if data['ingredient_id'] in current_ids:
                    # Actualizar existente
                    actualizar_cantidad_ingrediente_en_receta(
                        recipe_id, data['ingredient_id'],
                        cleaned_quantity, cleaned_unit, cleaned_notes
                    )
                else:
                    # Agregar nuevo
                    agregar_ingrediente_a_receta(
                        recipe_id, data['ingredient_id'],
                        cleaned_quantity, cleaned_unit, cleaned_notes
                    )

            return True
        except Exception as e:
            print(f"Error en bulk update: {e}")
            return False