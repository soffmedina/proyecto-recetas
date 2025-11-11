import mysql.connector
from mysql.connector import Error
from utils.console import error, success 

def conectar_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="gestion_recetas"
        )
        if connection.is_connected():
            print(success(" Conexion a MySQL exitosa..."))
            return connection
    except Error as e:
        print(error(f" Error al conectar a MySQL: {e}"))
        return None 