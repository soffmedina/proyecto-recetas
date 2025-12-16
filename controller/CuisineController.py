from models.cuisines import (
    obtener_cuisines, agregar_cuisines, obtener_cuisines_por_id,
    eliminar_cuisines, actualizar_cuisines
)
from utils.validators import validate_required_text
from utils.formatters import format_title
from typing import Optional, Dict, Any, List


class CuisineController:

    @staticmethod
    def get_all_cuisines() -> List[Dict[str, Any]]:
        """Obtener todas las cocinas"""
        return obtener_cuisines()

    @staticmethod
    def create_cuisine(name: str, description: str = "", country_origin: str = "") -> bool:
        """
        Crear una nueva cocina con validación básica
        """
        # Validar nombre
        valid, error = validate_required_text(name, "Nombre de la cocina", 2)
        if not valid:
            print(f"Error de validación: {error}")
            return False

        # Formatear datos
        cleaned_name = format_title(name)
        cleaned_description = description.strip() if description else ""
        cleaned_country = country_origin.strip() if country_origin else ""

        # Crear cocina
        return agregar_cuisines(cleaned_name, cleaned_description, cleaned_country)

    @staticmethod
    def get_cuisine_by_id(cuisine_id: int) -> Optional[Dict[str, Any]]:
        """Obtener una cocina por ID"""
        return obtener_cuisines_por_id(cuisine_id)

    @staticmethod
    def update_cuisine(cuisine_id: int, name: str, description: str = "", country_origin: str = "") -> bool:
        """
        Actualizar una cocina existente
        """
        # Verificar que existe
        current_cuisine = obtener_cuisines_por_id(cuisine_id)
        if not current_cuisine:
            return False

        # Validar nombre
        valid, error = validate_required_text(name, "Nombre de la cocina", 2)
        if not valid:
            print(f"Error de validación: {error}")
            return False

        # Formatear datos
        cleaned_name = format_title(name)
        cleaned_description = description.strip() if description else ""
        cleaned_country = country_origin.strip() if country_origin else ""

        # Actualizar cocina
        return actualizar_cuisines(cuisine_id, cleaned_name, cleaned_description, cleaned_country)

    @staticmethod
    def delete_cuisine(cuisine_id: int) -> bool:
        """Eliminar una cocina"""
        # Verificar que existe
        if not obtener_cuisines_por_id(cuisine_id):
            return False

        try:
            eliminar_cuisines(cuisine_id)
            return True
        except:
            return False