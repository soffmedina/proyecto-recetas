import tkinter as tk
from tkinter import ttk

class VentanaIngredientes(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Ingredientes")
        self.geometry("500x400")

        ttk.Label(self, text="Ingredientes", font=("Arial", 14)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("id", "name"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nombre")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        frame = ttk.Frame(self)
        frame.pack(pady=10)

        ttk.Button(frame, text="Agregar", command=self.agregar).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Editar", command=self.editar).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Eliminar", command=self.eliminar).grid(row=0, column=2, padx=5)
        ttk.Button(frame, text="Actualizar lista", command=self.cargar_datos).grid(row=0, column=3, padx=5)

    def cargar_datos(self):
        pass

    def agregar(self):
        pass

    def editar(self):
        pass

    def eliminar(self):
        pass
