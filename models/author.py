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
            return autores
        except Exception as e:
            print(error(f" Error al obtener autores: {e}"))
            return []
        finally:
            cursor.close()
            connection.close()


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
            return True
        except Exception as e:
            print(error(f" Error al agregar autor: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()



def obtener_author_por_id(author_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM author WHERE id = %s", (author_id,))
            author = cursor.fetchone()
            return author
        except Exception as e:
            print(error(f" Error al obtener autor por ID: {e}"))
            return None
        
        finally:
            cursor.close()
            connection.close()


def eliminar_author(author_id):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM author WHERE id = %s", (author_id,))
            connection.commit()
            return True
        except Exception as e:
            print(error(f" Error al eliminar autor: {e}"))   
            return None
        finally:
            cursor.close()
            connection.close()


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
            return True
        except Exception as e:
            print(error(f" Error al actualizar autor: {e}"))
            return None
        finally:
            cursor.close()
            connection.close()