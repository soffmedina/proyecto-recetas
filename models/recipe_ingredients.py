from config.db import conectar_db
from utils.console import error, success

#RECETAS - INGREDIENTES (TABLA PIVOTE)
def obtener_ingredientes_receta(recipe_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT i.id, i.name, ri.quantity, ri.unit, ri.notes
                FROM ingredients i
                JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
                WHERE ri.recipe_id = %s
            """
            cursor.execute(query, (recipe_id,))
            ingredientes = cursor.fetchall()
            return ingredientes
        except Exception as e:
            print(error(f" Error al obtener ingredientes de la receta: {e}"))
            return []
        finally:
            cursor.close()
            connection.close()


def agregar_ingrediente_a_receta(recipe_id, ingredient_id, quantity="", unit="", notes=""):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit, notes)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (recipe_id, ingredient_id, quantity, unit, notes))
            connection.commit()
            lastrowid = cursor.lastrowid
            print(success(" Ingrediente agregado a la receta exitosamente."))
            return lastrowid
        except Exception as e:
            print(error(f" Error al agregar ingrediente a la receta: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()

def eliminar_ingrediente_de_receta(recipe_id, ingredient_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                DELETE FROM recipe_ingredients
                WHERE recipe_id = %s AND ingredient_id = %s
            """
            cursor.execute(query, (recipe_id, ingredient_id))
            connection.commit()
            print(success(" Ingrediente eliminado de la receta exitosamente."))
            return True
        except Exception as e:
            print(error(f" Error al eliminar ingrediente de la receta: {e}"))
            return False
        finally:
            cursor.close()
            connection.close()

def actualizar_cantidad_ingrediente_en_receta(recipe_id, ingredient_id, quantity, unit="", notes=""):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                UPDATE recipe_ingredients
                SET quantity = %s, unit = %s, notes = %s
                WHERE recipe_id = %s AND ingredient_id = %s
            """
            cursor.execute(query, (quantity, unit, notes, recipe_id, ingredient_id))
            connection.commit()
            print(success(" Cantidad de ingrediente en la receta actualizada exitosamente."))
        except Exception as e:
            print(error(f" Error al actualizar cantidad de ingrediente en la receta: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()


