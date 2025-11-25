from multiprocessing import connection
from winreg import QueryInfoKey
from config.db import conectar_db
from utils.console import error, success


#AUTORES
def obtener_author():
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT *FROM author ORDER BY name")
            autores = cursor.fetchall()
            cursor.close()
            connection.close()
            return autores
        except Exception as e:
            print(error(f" Error al obtener autores: {e}"))
            return []
    return []


def agregar_author(name,  email, password_hash, avatar_url="", biography=""):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO author (name, email, password_hash, avatar_url, biography)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, password_hash, avatar_url, biography))
            connection.commit()
            author_id = cursor.lastrowid
            cursor.close()
            connection.close()
            print(success(" Autor agregado exitosamente."))
            return author_id
        except Exception as e:
            print(error(f" Error al agregar autor: {e}"))
            return None
    return None


def obtener_author_por_id(author_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM author WHERE id = %s", (author_id,))
            author = cursor.fetchone()
            cursor.close()
            connection.close()
            return author
        except Exception as e:
            print(error(f" Error al obtener autor por ID: {e}"))
            return None
    return None


def eliminar_author(author_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM author WHERE id = %s", (author_id,))
            connection.commit()
            cursor.close()
            connection.close()
            print(success(" Autor eliminado exitosamente."))
        except Exception as e:
            print(error(f" Error al eliminar autor: {e}"))
    return

def actualizar_author(author_id, name, email, password_hash, avatar_url="", biography=""):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                UPDATE author
                SET name = %s, email = %s, password_hash = %s, avatar_url = %s, biography = %s
                WHERE id = %s
            """
            cursor.execute(query, (name, email, password_hash, avatar_url, biography, author_id))
            connection.commit()
            cursor.close()
            connection.close()
            print(success(" Autor actualizado exitosamente."))
        except Exception as e:
            print(error(f" Error al actualizar autor: {e}"))
    return






#CUISINES
def obtener_cuisines():
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cuisines ORDER BY name")
            cuisines = cursor.fetchall()
            cursor.close()
            connection.close()
            return cuisines
        except Exception as e:
            print(error(f" Error al obtener cuisines: {e}"))
            return []
    return []

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
            cursor.close()
            connection.close()
            print(success(" Cuisines '{name}' agregada exitosamente."))
            return cuisine_id
        except Exception as e:
            print(error(f" Error al agregar cuisines: {e}"))
            return None
    return None

def obtener_cuisines_por_id(cuisine_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cuisines WHERE id = %s", (cuisine_id,))
            cuisines = cursor.fetchone()
            cursor.close()
            connection.close()
            return cuisines
        except Exception as e:
            print(error(f" Error al obtener cuisines por ID: {e}"))
            return None
    return None


def eliminar_cuisines(cuisine_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM cuisines WHERE id = %s", (cuisine_id,))
            connection.commit()
            cursor.close()
            connection.close()
            print(success(" Cuisine eliminada exitosamente."))
        except Exception as e:
            print(error(f" Error al eliminar cuisine: {e}"))
    return None

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
            cursor.close()
            connection.close()
            print(success(" Cuisine actualizada exitosamente."))
        except Exception as e:
            print(error(f" Error al actualizar cuisine: {e}"))
    return None






#INGREDIENTES
def obtener_ingrediente():
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ingredients ORDER BY name")
            ingredients = cursor.fetchall()
            cursor.close()
            connection.close()
            return ingredients
        except Exception as e:
            print(error(f" Error al obtener ingredientes: {e}"))
            return []
    return []

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
            cursor.close()
            connection.close()
            print(success(" Ingrediente agregado exitosamente."))
            return ingrediente_id
        except Exception as e:
            print(error(f" Error al agregar ingrediente: {e}"))
            return None
    return None


def obtener_ingrediente_por_id(ingrediente_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ingredients WHERE id = %s", (ingrediente_id,))
            ingredients = cursor.fetchone()
            cursor.close()
            connection.close()
            return ingredients
        except Exception as e:
            print(error(f" Error al obtener ingrediente por ID: {e}"))
            return None
    return None

def obtener_ingrediente_por_nombre(name):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ingredients WHERE name = %s", (name,))
            ingredients = cursor.fetchone()
            cursor.close()
            connection.close()
            return ingredients
        except Exception as e:
            print(error(f" Error al obtener ingrediente por nombre: {e}"))
            return None
    return None


def eliminar_ingrediente_por_id(ingrediente_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM ingredients WHERE id = %s", (ingrediente_id,))
            connection.commit()
            cursor.close()
            connection.close()
            print(success(" Ingrediente eliminado exitosamente."))
        except Exception as e:
            print(error(f" Error al eliminar ingrediente: {e}"))
    return None

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
            cursor.close()
            connection.close()
            print(success(" Ingrediente actualizado exitosamente."))
        except Exception as e:
            print(error(f" Error al actualizar ingrediente: {e}"))
    return None







#RECETAS
def obtener_recetas():
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM recipes ORDER BY title")
            recetas = cursor.fetchall()
            cursor.close()
            connection.close()
            return recetas
        except Exception as e:
            print(error(f" Error al obtener recetas: {e}"))
            return []
    return []

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
            cursor.close()
            connection.close()
            print(success(" Receta agregada exitosamente."))
            return receta_id
        except Exception as e:
            print(error(f" Error al agregar receta: {e}"))
            return None
    return None

def obtener_receta_por_id(receta_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM recipes WHERE id = %s", (receta_id,))
            receta = cursor.fetchone()
            cursor.close()
            connection.close()
            return receta
        except Exception as e:
            print(error(f" Error al obtener receta por ID: {e}"))
            return None
    return None

def obtener_receta_por_nombre(title):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM recipes WHERE title = %s", (title,))
            receta = cursor.fetchone()
            cursor.close()
            connection.close()
            return receta
        except Exception as e:
            print(error(f" Error al obtener receta por nombre: {e}"))
            return None
    return None

def eliminar_receta_por_id(receta_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM recipes WHERE id = %s", (receta_id,))
            connection.commit()
            cursor.close()
            connection.close()
            print(success(" Receta eliminada exitosamente."))
        except Exception as e:
            print(error(f" Error al eliminar receta: {e}"))
    return None

def obtener_receta_por_autor(author_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM recipes WHERE author_id = %s", (author_id,))
            recetas = cursor.fetchall()
            cursor.close()  
            connection.close()
            return recetas
        except Exception as e:
            print(error(f" Error al obtener recetas por autor: {e}"))
            return []
    return []

def obtener_receta_por_cuisine(cuisine_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM recipes WHERE cuisine_id = %s", (cuisine_id,))
            recetas = cursor.fetchall()
            cursor.close()  
            connection.close()
            return recetas
        except Exception as e:
            print(error(f" Error al obtener recetas por cuisine: {e}"))
            return []
    return []


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
            cursor.close()
            connection.close()
            print(success(" Receta actualizada exitosamente."))
        except Exception as e:
            print(error(f" Error al actualizar receta: {e}"))
    return None





#RECETAS - INGREDIENTEDS (TABLA PIVOTE)
def obtener_ingredientes_receta(recipe_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT i.*
                FROM ingrediente i
                JOIN recipe_ingredients ri ON i.id = ri.ingrediente_id
                WHERE ri.receta_id = %s
            """
            cursor.execute(query, (recipe_id,))
            ingredientes = cursor.fetchall()
            cursor.close()
            connection.close()
            return ingredientes
        except Exception as e:
            print(error(f" Error al obtener ingredientes de la receta: {e}"))
            return []
    return []


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
            cursor.close()
            connection.close()
            print(success(" Ingrediente agregado a la receta exitosamente."))
        except Exception as e:
            print(error(f" Error al agregar ingrediente a la receta: {e}"))
    return None


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
            cursor.close()
            connection.close()
            print(success(" Ingrediente eliminado de la receta exitosamente."))
        except Exception as e:
            print(error(f" Error al eliminar ingrediente de la receta: {e}"))
    return None


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
            cursor.close()
            connection.close()
            print(success(" Cantidad de ingrediente en la receta actualizada exitosamente."))
        except Exception as e:
            print(error(f" Error al actualizar cantidad de ingrediente en la receta: {e}"))
    return None



