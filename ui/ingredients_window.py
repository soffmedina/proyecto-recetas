import tkinter as tk
from tkinter import ttk, messagebox

from controller.IngredientController import IngredientController

class VentanaIngredientes(tk.Toplevel):
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.crear_interfaz()
        self.cargar_ingredientes()
    
    def crear_interfaz(self):
        #Header
        header = tk.Frame(self.parent, bg=self.main_window.COLOR_SECUNDARIO, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🥕 Catálogo de Ingredientes", font=('Arial', 16, 'bold'), bg=self.main_window.COLOR_SECUNDARIO, fg='white').pack(side=tk.LEFT, padx=30, pady=15)
        tk.Button(header, text="➕ Nuevo Ingrediente", command=self.abrir_formulario_nuevo, bg=self.main_window.COLOR_PRIMARIO, fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8, cursor='hand2', bd=0).pack(side=tk.RIGHT, padx=30)
        
        #Frame Principal
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        #Treeview
        tree_frame = tk.Frame(main_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('ID', 'Nombre', 'Fecha')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        #Configurar columnas 
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Fecha', text='Fecha Registro')
        
        self.tree.column('ID', width=100, anchor=tk.CENTER)
        self.tree.column('Nombre', width=500)
        self.tree.column('Fecha', width=300, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Botones de accion
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=15, padx=10)
        
        tk.Button(btn_frame, text="✏️ Editar", command=self.editar_ingrediente, bg=self.main_window.COLOR_NARANJA, fg='white', font=('Arial', 10), padx=15, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar_ingrediente, bg=self.main_window.COLOR_ROJO, fg='white', font=('Arial', 10), padx=15, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
   
    
    def cargar_ingredientes(self):
        """Carga ingredientes"""
        #Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        #Obtener ingredientes
        ingredientes = IngredientController.get_all_ingredients()
        for ing in ingredientes:
            self.tree.insert('', tk.END, values=(ing['id'], ing['name'], str(ing['created_at'])[:19]))
    
    def abrir_formulario_nuevo(self):
        """Abre formulario"""
        VentanaFormularioIngrediente(self.main_window, self, modo='nuevo')
    
    def editar_ingrediente(self):
        """Editar"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un ingrediente")
            return
        item = self.tree.item(seleccion[0])
        ing_id = item['values'][0]
        VentanaFormularioIngrediente(self.main_window, self, modo='editar', ingrediente_id=ing_id)
    
    def eliminar_ingrediente(self):
        """Eliminar"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un ingrediente")
            return
        item = self.tree.item(seleccion[0])
        ing_id = item['values'][0]
        ing_nombre = item['values'][1]
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar '{ing_nombre}'?")
        if confirmar:
            if IngredientController.delete_ingredient(ing_id):
                messagebox.showinfo("Éxito", "Ingrediente eliminado")
                self.cargar_ingredientes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el ingrediente")


# ==================== FORMULARIO INGREDIENTE ====================

class VentanaFormularioIngrediente:
    """Formulario ingrediente"""
    
    def __init__(self, parent, ventana_ingredientes, modo='nuevo', ingrediente_id=None):
        self.ventana_ingredientes = ventana_ingredientes
        self.modo = modo
        self.ingrediente_id = ingrediente_id
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("➕ Nuevo Ingrediente" if modo == 'nuevo' else "✏️ Editar Ingrediente")
        self.ventana.geometry("450x200")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        
        self.crear_interfaz()
        if modo == 'editar' and ingrediente_id:
            self.cargar_datos()
    
    def crear_interfaz(self):
        """Crea formulario"""
        frame = tk.Frame(self.ventana, bg='white', padx=30, pady=20)
        frame.pack(fill=tk.BOTH, expand=True) 

        
        #Titulo - Nombre
        tk.Label(frame, text="🥕 Ingrediente:*", font=('Arial', 11, 'bold'), bg='white', fg='#2E7D32').grid(row=0, column=0, sticky=tk.W, pady=10)
        self.entry_nombre = tk.Entry(frame, font=('Arial', 11), width=30)
        self.entry_nombre.grid(row=0, column=1, pady=10)
        self.entry_nombre.focus()
       
        # Botones
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="💾 Guardar", command=self.guardar_ingrediente, bg='#4CAF50', fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.ventana.destroy, bg='#757575', fg='white', font=('Arial', 11), padx=20, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
    
    
    def cargar_datos(self):
        """Cargar datos para editar"""
        ingrediente = IngredientController.get_ingredient_by_id(self.ingrediente_id)
        if ingrediente:
            self.entry_nombre.insert(0, ingrediente['name'])
            
    def guardar_ingrediente(self):
        """Guardar ingrediente"""
        #Validar campo
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre no puede estar vacío")
            return
        
        #Guardar o actualizar
        if self.modo == 'nuevo':
            ingrediente_id = IngredientController.create_ingredient(nombre)
            if ingrediente_id:
                messagebox.showinfo("Éxito", "Ingrediente creado")
                self.ventana_ingredientes.cargar_ingredientes()
                self.ventana.destroy()
        else:
            if IngredientController.update_ingredient(self.ingrediente_id, nombre):
                messagebox.showinfo("Éxito", "Ingrediente actualizado")
                self.ventana_ingredientes.cargar_ingredientes()
                self.ventana.destroy()
                
          