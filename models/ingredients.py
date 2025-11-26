from config.db import conectar_db
from utils.console import error, success

#INGREDIENTES
def obtener_ingrediente():
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ingredients ORDER BY name")
            ingredients = cursor.fetchall()
            return ingredients
        except Exception as e:
            print(error(f" Error al obtener ingredientes: {e}"))
            return []
        finally:
            cursor.close()
            connection.close()

def agregar_ingrediente(name):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO ingredients (name)
                VALUES (%s)
            """
            cursor.execute(query, (name,))
            connection.commit()
            ingrediente_id = cursor.lastrowid
            print(success(" Ingrediente agregado exitosamente."))
            return ingrediente_id
        except Exception as e:
            print(error(f" Error al agregar ingrediente: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()


def obtener_ingrediente_por_id(ingrediente_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ingredients WHERE id = %s", (ingrediente_id,))
            ingredients = cursor.fetchone()
            return ingredients
        except Exception as e:
            print(error(f" Error al obtener ingrediente por ID: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()

def obtener_ingrediente_por_nombre(name):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ingredients WHERE name = %s", (name,))
            ingredients = cursor.fetchone()
            return ingredients
        except Exception as e:
            print(error(f" Error al obtener ingrediente por nombre: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()


def eliminar_ingrediente_por_id(ingrediente_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM ingredients WHERE id = %s", (ingrediente_id,))
            connection.commit()
            print(success(" Ingrediente eliminado exitosamente."))
        except Exception as e:
            print(error(f" Error al eliminar ingrediente: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()

def actualizar_ingrediente(ingrediente_id, name):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                UPDATE ingredients
                SET name = %s
                WHERE id = %s
            """
            cursor.execute(query, (name, ingrediente_id))
            connection.commit()
            print(success(" Ingrediente actualizado exitosamente."))
        except Exception as e:
            print(error(f" Error al actualizar ingrediente: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()

