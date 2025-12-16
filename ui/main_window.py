import tkinter as tk
from tkinter import ttk, messagebox
from config.db import conectar_db
from controller.AuthorController import AuthorController
from controller.CuisineController import CuisineController
from controller.IngredientController import IngredientController
from controller.RecipeController import RecipeController
from .author_window import VentanaAutores
from .cuisines_window import VentanaCuisines
from .ingredients_window import VentanaIngredientes
from .recipes_window import VentanaRecetas


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.root = root
        self.title("🍳 Gestor de Recetas de Cocina")
        self.geometry("1400x800")
        #self.state('zoomed')  # Maximizar ventana
        
        # Colores del tema
        self.COLOR_PRIMARIO = "#688F0E"
        self.COLOR_SECUNDARIO = "#AEACAB"
        self.COLOR_FONDO = "#F5F5F5"
        self.COLOR_BLANCO = "#FFFFFF"
        self.COLOR_AZUL = "#2196F3"
        self.COLOR_NARANJA = "#FF9800"
        self.COLOR_ROJO = "#F44336"
        self.COLOR_VIOLETA = "#9C27B0"
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Verificar conexión
        if not self.verificar_conexion():
            messagebox.showerror("Error de Conexión", 
                               "No se pudo conectar a la base de datos.\nVerifica tu configuración.")
            self.destroy()
            return
        
        # Crear interfaz
        self.crear_header()
        self.crear_menu_lateral()
        self.crear_area_principal()
        
        # Mostrar dashboard por defecto
        self.mostrar_dashboard()
    
    def configurar_estilos(self):
        """Configura los estilos de ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones del menú
        style.configure('Menu.TButton',
                       background=self.COLOR_PRIMARIO,
                       foreground='white',
                       padding=(20, 15),
                       font=('Arial', 11),
                       borderwidth=0)
        
        style.map('Menu.TButton',
                 background=[('active', self.COLOR_SECUNDARIO)])
        
        # Estilo para botones de acción
        style.configure('Primary.TButton',
                       background=self.COLOR_PRIMARIO,
                       foreground='white',
                       padding=(15, 10),
                       font=('Arial', 10, 'bold'))
        
        style.configure('Danger.TButton',
                       background=self.COLOR_ROJO,
                       foreground='white',
                       padding=(15, 10),
                       font=('Arial', 10, 'bold'))
        
        style.configure('Info.TButton',
                       background=self.COLOR_AZUL,
                       foreground='white',
                       padding=(15, 10),
                       font=('Arial', 10, 'bold'))
        
        # Estilo para Treeview
        style.configure('Treeview',
                       background='white',
                       foreground='black',
                       rowheight=30,
                       fieldbackground='white',
                       font=('Arial', 10))
        
        style.configure('Treeview.Heading',
                       background=self.COLOR_PRIMARIO,
                       foreground='white',
                       font=('Arial', 11, 'bold'))
    
    def verificar_conexion(self):
        """Verifica la conexión a la base de datos"""
        connection = conectar_db()
        if connection:
            connection.close()
            return True
        return False
    
    def crear_header(self):
        """Crea el encabezado de la aplicación"""
        header = tk.Frame(self, bg=self.COLOR_PRIMARIO, height=80)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        # Título
        titulo = tk.Label(header,
                         text="🍳 GESTOR DE RECETAS DE COCINA",
                         font=('Arial', 24, 'bold'),
                         bg=self.COLOR_PRIMARIO,
                         fg='white')
        titulo.pack(side=tk.LEFT, padx=30, pady=20)
        
    
    def crear_menu_lateral(self):
        """Crea el menú lateral de navegación"""
        self.menu_frame = tk.Frame(self, bg=self.COLOR_PRIMARIO, width=250)
        self.menu_frame.pack(fill=tk.Y, side=tk.LEFT)
        self.menu_frame.pack_propagate(False)
        
        # Título del menú
        titulo_menu = tk.Label(self.menu_frame,
                              text="📋 MENÚ PRINCIPAL",
                              font=('Arial', 12, 'bold'),
                              bg=self.COLOR_SECUNDARIO,
                              fg='white',
                              pady=15)
        titulo_menu.pack(fill=tk.X, pady=(20, 10), padx=10)
        
        # Botones del menú
        botones = [
            ("🏠 Dashboard", self.mostrar_dashboard),
            ("📖 Recetas", self.mostrar_recetas),
            ("🌎 Tipos de Cocina", self.mostrar_cuisines),
            ("👨‍🍳 Autores", self.mostrar_autores),
            ("🥕 Ingredientes", self.mostrar_ingredientes),
        ]
        
        for texto, comando in botones:
            btn = tk.Button(self.menu_frame,
                          text=texto,
                          command=comando,
                          bg=self.COLOR_PRIMARIO,
                          fg='white',
                          font=('Arial', 11),
                          bd=0,
                          padx=20,
                          pady=15,
                          anchor='w',
                          cursor='hand2',
                          activebackground=self.COLOR_SECUNDARIO,
                          activeforeground='white')
            btn.pack(fill=tk.X, pady=2, padx=10)
    
    def crear_area_principal(self):
        """Crea el área principal donde se mostrará el contenido"""
        self.area_principal = tk.Frame(self, bg=self.COLOR_FONDO)
        self.area_principal.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
    
    def limpiar_area_principal(self):
        """Limpia el área principal"""
        for widget in self.area_principal.winfo_children():
            widget.destroy()
    
    def mostrar_dashboard(self):
        """Muestra el dashboard con estadísticas"""
        self.limpiar_area_principal()
        
        # Título
        titulo = tk.Label(self.area_principal,
                         text="📊 Dashboard - Estadísticas del Sistema",
                         font=('Arial', 20, 'bold'),
                         bg=self.COLOR_FONDO,
                         fg=self.COLOR_PRIMARIO)
        titulo.pack(pady=30)
        
        # Frame para las tarjetas
        cards_frame = tk.Frame(self.area_principal, bg=self.COLOR_FONDO)
        cards_frame.pack(pady=20, padx=40)
        
        # Obtener estadísticas
        total_recetas = len(RecipeController.get_all_recipes())
        total_autores = len(AuthorController.get_all_authors())
        total_cuisines = len(CuisineController.get_all_cuisines())
        total_ingredientes = len(IngredientController.get_all_ingredients())
        
        # Crear tarjetas
        estadisticas = [
            ("📖 Recetas", total_recetas, self.COLOR_AZUL),
            ("👨‍🍳 Autores", total_autores, self.COLOR_NARANJA),
            ("🌎 Tipos de Cocina", total_cuisines, self.COLOR_ROJO),
            ("🥕 Ingredientes", total_ingredientes, self.COLOR_VIOLETA)
        ]
        
        for i, (titulo, valor, color) in enumerate(estadisticas):
            self.crear_tarjeta_estadistica(cards_frame, titulo, valor, color, i)
    
    def crear_tarjeta_estadistica(self, parent, titulo, valor, color, columna):
        """Crea una tarjeta de estadística"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, borderwidth=2)
        card.grid(row=0, column=columna, padx=20, pady=10, ipadx=30, ipady=30)
        
        titulo_label = tk.Label(card,
                               text=titulo,
                               font=('Arial', 14, 'bold'),
                               bg=color,
                               fg='white')
        titulo_label.pack(pady=(10, 5))
        
        valor_label = tk.Label(card,
                              text=str(valor),
                              font=('Arial', 36, 'bold'),
                              bg=color,
                              fg='white')
        valor_label.pack(pady=(5, 10))
    
    
    
    
    
    
    
    
    #METODOS PARA ABRIR LAS VENTANAS DE GESTION
    def mostrar_recetas(self):
        """Muestra la gestión de recetas"""
        self.limpiar_area_principal()
        VentanaRecetas(self.area_principal, self)
    
    def mostrar_cuisines(self):
        """Muestra la gestión de tipos de cocina"""
        self.limpiar_area_principal()
        VentanaCuisines(self.area_principal, self)
    
    def mostrar_autores(self):
        """Muestra la gestión de autores"""
        self.limpiar_area_principal()
        VentanaAutores(self.area_principal, self)
    
    def mostrar_ingredientes(self):
        """Muestra la gestión de ingredientes"""
        self.limpiar_area_principal()
        VentanaIngredientes(self.area_principal, self)
