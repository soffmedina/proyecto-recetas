from ast import main
from config import operaciones
from config.db import conectar_db
from config.operaciones import *
from utils.console import title, info, success, warn, error

connection= conectar_db()

def menu_principal():
    print(title("\n-------GESTOR DE RECETAS DE COCINA-------"))
    print("1. Gestionar Recetas")
    print("2. Gestionar tipos de Cocina")
    print("3. Gestionar Autores")
    print("4. Gestionar ingredientes")
    print("5. Salir")
    
   # opcion = input(info("Seleccione una opción: "))
    
#---------------------------------------------------------RECETA

def menu_recetas():
    while True:
        
        print(title("\n-------GESTIÓN DE RECETAS-------"))
        print("1. Agregar Receta")
        print("2. Obtener Recetas")
        print("3. Obtener Recetas por ID")
        print("4. Obtener Receta por nombre")
        print("5. Obtener Receta por tipo de cocina")
        print("6. Obtener Receta por autor")
        print("7. Actualizar Receta")
        print("8. Eliminar Receta por ID")
        print("9. Volver al Menú Principal")
    
        opcion = input(info("\n Seleccione una opción: ")).strip()

        if opcion == '1':
            agregar_receta(connection)
        elif opcion == '2':
            obtener_recetas(connection)
        elif opcion == '3':
            obtener_receta_por_id(connection)
        elif opcion == '4':
            obtener_receta_por_nombre(connection)
        elif opcion == '5':
            obtener_receta_por_cuisine(connection)
        elif opcion == '6':
            obtener_receta_por_autor(connection)
        elif opcion == '7':
            actualizar_receta(connection)   
        elif opcion == '8':
            eliminar_receta_por_id(connection)
        elif opcion == '9':
            return
        else:
            print(error("Opción inválida. Por favor, intente de nuevo."))
        return opcion






#---------------------------------------------------------CUISINE

def menu_cuisines():
    while True:
        print(title("\n---------GESTION DE TIPOS DE COCINA---------"))
        print("1. Obtener tipos de cocina")
        print("2. Agregar tipo de cocina")
        print("3. Obtener tipo de cocina por ID")
        print("4. Actualizar tipo de cocina")
        print("5. Eliminar tipo de cocina por ID")
        print("6. Volver al Menú Principal")
        
        opcion = input(info("\n Seleccione una opción: ")).strip()
        
        if opcion == '1':
            obtener_cuisines(connection)
        elif opcion == '2':
            agregar_cuisines(connection)
        elif opcion == '3':
            obtener_cuisines_por_id(connection)
        elif opcion == '4':
            actualizar_cuisines(connection)
        elif opcion == '5':
            eliminar_cuisines(connection)
        elif opcion == '6':
            return
        else:
            print(error("Opción inválida. Por favor, intente de nuevo."))   
        return opcion





#---------------------------------------------------------AUTOR
def menu_autores():
    while True:
        print(title("\n---------GESTION DE AUTORES---------"))
        print("1. Obtener autores")
        print("2. Agregar autor")
        print("3. Obtener autor por ID")
        print("4. Actualizar autor")
        print("5. Eliminar autor por ID")
        print("6. Volver al Menú Principal")
        
        opcion = input(info("\n Seleccione una opción: ")).strip()
        
        if opcion == '1':
            obtener_author(connection)
        elif opcion == '2':
            agregar_author(connection)
        elif opcion == '3':
            obtener_author_por_id(connection)
        elif opcion == '4':
            actualizar_author(connection)
        elif opcion == '5':
            eliminar_author(connection)
        elif opcion == '6':
            return
        else:
            print(error("Opción inválida. Por favor, intente de nuevo."))
        return opcion





#---------------------------------------------------------INGREDIENTE
def menu_ingredientes():
    while True:
        print(title("\n-----------------GESTION DE INGREDIENTES---------"))
        print("1. Obtener ingredientes")
        print("2. Agregar ingrediente")
        print("3. Obtener ingrediente por ID")
        print("4. Obtener ingrediente por nombre")
        print("5. Actualizar ingrediente")
        print("6. Eliminar ingrediente por ID")
        print("7. Volver al Menú Principal")
        
        opcion = input(info("\n Seleccione una opción: ")).strip()
        
        if opcion == '1':
            obtener_ingrediente(connection)
        elif opcion == '2':
            agregar_ingrediente(connection)
        elif opcion == '3':
            obtener_ingrediente_por_id(connection)
        elif opcion == '4':
            obtener_ingrediente_por_nombre(connection)
        elif opcion == '5':
            actualizar_ingrediente(connection)
        elif opcion == '6':
            eliminar_ingrediente_por_id(connection)
        elif opcion == '7':
            return
        else:
            print(error("Opción inválida. Por favor, intente de nuevo."))
        return opcion
    

if __name__ == "__main__":
    while True:
        menu_principal()
        opcion = input(info("\n Seleccione una opción: ")).strip()
        
        if opcion == '1':
            menu_recetas()
        elif opcion == '2':
            menu_cuisines()
        elif opcion == '3':
            menu_autores()
        elif opcion == '4':
            menu_ingredientes()
        elif opcion == '5':
            print(success("Saliendo del gestor de recetas. ¡Hasta luego!"))
            break
        else:
            print(error("Opción inválida. Por favor, intente de nuevo."))
def menu_principal():
    print(title("\n-------GESTOR DE RECETAS DE COCINA-------"))
    print("1. Gestionar Recetas")
    print("2. Gestionar tipos de Cocina")
    print("3. Gestionar Autores")
    print("4. Gestionar ingredientes")
    print("5. Salir")
    
main()