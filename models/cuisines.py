from config.db import conectar_db
from utils.console import error, success

#CUISINES
def obtener_cuisines():
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cuisines ORDER BY name")
            cuisines = cursor.fetchall()
            return cuisines
        except Exception as e:
            print(error(f" Error al obtener cuisines: {e}"))
            return []
        finally:
            cursor.close()
            connection.close()

def agregar_cuisines(name, description="", country_origin=""):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO cuisines (name, description, country_origin)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (name, description, country_origin))
            connection.commit()
            cuisine_id = cursor.lastrowid
            print(success(" Cuisines '{name}' agregada exitosamente."))
            return cuisine_id
        except Exception as e:
            print(error(f" Error al agregar cuisines: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()

def obtener_cuisines_por_id(cuisine_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cuisines WHERE id = %s", (cuisine_id,))
            cuisines = cursor.fetchone()
            return cuisines
        except Exception as e:
            print(error(f" Error al obtener cuisines por ID: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()
    


def eliminar_cuisines(cuisine_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM cuisines WHERE id = %s", (cuisine_id,))
            connection.commit()
            print(success(" Cuisine eliminada exitosamente."))
        except Exception as e:
            print(error(f" Error al eliminar cuisine: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()

def actualizar_cuisines(cuisine_id, name, description="", country_origin=""):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                UPDATE cuisines
                SET name = %s, description = %s, country_origin = %s
                WHERE id = %s
            """
            cursor.execute(query, (name, description, country_origin, cuisine_id))
            connection.commit()
            print(success(" Cuisine actualizada exitosamente."))
        except Exception as e:
            print(error(f" Error al actualizar cuisine: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()