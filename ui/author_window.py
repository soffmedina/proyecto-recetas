import tkinter as tk
from tkinter import ttk

# ============================
# Ventana de Autores
# ============================
class VentanaAutores(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Autores")
        self.geometry("500x400")

        ttk.Label(self, text="Autores", font=("Arial", 14)).pack(pady=10)

        # Tabla
        self.tree = ttk.Treeview(self, columns=("id", "name", "email"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("email", text="Email")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Botones CRUD
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        ttk.Button(frame, text="Agregar", command=self.agregar).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Editar", command=self.editar).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Eliminar", command=self.eliminar).grid(row=0, column=2, padx=5)
        ttk.Button(frame, text="Actualizar lista", command=self.cargar_datos).grid(row=0, column=3, padx=5)

    # Métodos vacíos para que completes
    def cargar_datos(self):
        pass

    def agregar(self):
        pass

    def editar(self):
        pass

    def eliminar(self):
        pass