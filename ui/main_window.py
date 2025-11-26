import tkinter as tk
from tkinter import ttk
from .author_window import VentanaAutores
from .cuisines_window import VentanaCuisines
from .ingredients_window import VentanaIngredientes
from .recipes_window import VentanaRecetas

# ============================
# Ventana Principal (Tk)
# ============================
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Recetas")
        self.geometry("400x300")

        ttk.Label(self, text="Panel Principal", font=("Arial", 16)).pack(pady=10)

        # Botones para abrir subventanas
        ttk.Button(self, text="Autores", command=self.abrir_autores).pack(pady=5)
        ttk.Button(self, text="Cocinas (Cuisines)", command=self.abrir_cuisines).pack(pady=5)
        ttk.Button(self, text="Ingredientes", command=self.abrir_ingredientes).pack(pady=5)
        ttk.Button(self, text="Recetas", command=self.abrir_recetas).pack(pady=5)

    # Métodos para abrir ventanas
    def abrir_autores(self):
        VentanaAutores(self)

    def abrir_cuisines(self):
        VentanaCuisines(self)

    def abrir_ingredientes(self):
        VentanaIngredientes(self)

    def abrir_recetas(self):
        VentanaRecetas(self)