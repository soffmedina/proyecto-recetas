from config.db import conectar_db
from utils.console import error, success, warning


# CRUD RECETAS 

def obtener_recetas():
    """Obtiene todas las recetas con su categoría"""
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT r.*, c.nombre as categoria_nombre 
                FROM recetas r 
                LEFT JOIN categorias c ON r.categoria_id = c.id
                ORDER BY r.fecha_creacion DESC
            """
            cursor.execute(query)
            recetas = cursor.fetchall()
            cursor.close()
            connection.close()
            return recetas
        except Exception as e:
            print(error(f"Error al obtener recetas: {e}"))
            return []
    return []




