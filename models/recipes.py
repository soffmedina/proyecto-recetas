from config.db import conectar_db
from utils.console import error, success

#RECETAS
def obtener_recetas():
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM recipes ORDER BY title")
            recetas = cursor.fetchall()
            return recetas
        except Exception as e:
            print(error(f" Error al obtener recetas: {e}"))
            return []
        finally:
            cursor.close()
            connection.close()

def agregar_receta(title, description, preparation, author_id=None, cuisine_id=None):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO recipes (title, description, preparation, author_id, cuisine_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (title, description, preparation, author_id, cuisine_id))
            connection.commit()
            receta_id = cursor.lastrowid
            print(success(" Receta agregada exitosamente."))
            return receta_id
        except Exception as e:
            print(error(f" Error al agregar receta: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()

def obtener_receta_por_id(receta_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM recipes WHERE id = %s", (receta_id,))
            receta = cursor.fetchone()
            return receta
        except Exception as e:
            print(error(f" Error al obtener receta por ID: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()

def obtener_receta_por_nombre(title):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM recipes WHERE title = %s", (title,))
            receta = cursor.fetchone()
            return receta
        except Exception as e:
            print(error(f" Error al obtener receta por nombre: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()

def eliminar_receta_por_id(receta_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM recipes WHERE id = %s", (receta_id,))
            connection.commit()
            print(success(" Receta eliminada exitosamente."))
            return True
        except Exception as e:
            print(error(f" Error al eliminar receta: {e}"))
            return False
        finally:
            cursor.close()
            connection.close()
            
def obtener_receta_por_autor(author_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM recipes WHERE author_id = %s", (author_id,))
            recetas = cursor.fetchall()
            return recetas
        except Exception as e:
            print(error(f" Error al obtener recetas por autor: {e}"))
            return []
        finally:
            cursor.close()
            connection.close()

def obtener_receta_por_cuisine(cuisine_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM recipes WHERE cuisine_id = %s", (cuisine_id,))
            recetas = cursor.fetchall()
            return recetas
        except Exception as e:
            print(error(f" Error al obtener recetas por cuisine: {e}"))
            return []
        finally:
            cursor.close()
            connection.close()


def actualizar_receta(receta_id, title, description, preparation, author_id=None, cuisine_id=None):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                UPDATE recipes
                SET title = %s, description = %s, preparation = %s, author_id = %s, cuisine_id = %s
                WHERE id = %s
            """
            cursor.execute(query, (title, description, preparation, author_id, cuisine_id, receta_id))
            connection.commit()
            print(success(" Receta actualizada exitosamente."))
            return True
        except Exception as e:
            print(error(f" Error al actualizar receta: {e}"))
            return False
        finally:
            cursor.close()
            connection.close()