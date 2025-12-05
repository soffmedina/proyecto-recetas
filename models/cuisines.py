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
            # Normalizar clave: algunos esquemas pueden tener 'county_origin' (typo)
            for c in cuisines:
                if 'county_origin' in c and 'country_origin' not in c:
                    c['country_origin'] = c.get('county_origin')
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
            # Usar 'county_origin' por compatibilidad con esquemas existentes
            query = """
                INSERT INTO cuisines (name, description, county_origin)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (name, description, country_origin))
            connection.commit()
            cuisine_id = cursor.lastrowid
            print(success(f" Cuisine '{name}' agregada exitosamente."))
            return True
        except Exception as e:
            print(error(f" Error al agregar cuisines: {e}"))
            return False
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
            # Normalizar clave si existe el typo en la BD
            if cuisines and 'county_origin' in cuisines and 'country_origin' not in cuisines:
                cuisines['country_origin'] = cuisines.get('county_origin')
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
            # Usar 'county_origin' por compatibilidad con esquemas existentes
            query = """
                UPDATE cuisines
                SET name = %s, description = %s, county_origin = %s
                WHERE id = %s
            """
            cursor.execute(query, (name, description, country_origin, cuisine_id))
            connection.commit()
            print(success(" Cuisine actualizada exitosamente."))
            return True
        except Exception as e:
            print(error(f" Error al actualizar cuisine: {e}"))
            return False
        finally:
            cursor.close()
            connection.close()