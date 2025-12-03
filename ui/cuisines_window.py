import tkinter as tk
from tkinter import ttk, messagebox

from models.cuisines import actualizar_cuisines, agregar_cuisines, eliminar_cuisines, obtener_cuisines, obtener_cuisines_por_id


class VentanaCuisines(tk.Toplevel):  
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.crear_interfaz()
        self.cargar_cuisines()
    
    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.parent, bg=self.main_window.COLOR_SECUNDARIO, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🌎 Gestión de Tipos de Cocina", font=('Arial', 16, 'bold'), bg=self.main_window.COLOR_SECUNDARIO, fg='white').pack(side=tk.LEFT, padx=30, pady=15)
        
        tk.Button(header, text="➕ Nueva Cocina", command=self.abrir_formulario_nuevo, bg=self.main_window.COLOR_PRIMARIO, fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8, cursor='hand2', bd=0).pack(side=tk.RIGHT, padx=30)
        
        # Frame principal
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Treeview
        tree_frame = tk.Frame(main_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('ID', 'Nombre', 'País de Origen', 'Descripción')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        #Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('País de Origen', text='País de Origen')
        self.tree.heading('Descripción', text='Descripción')
        
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Nombre', width=200)
        self.tree.column('País de Origen', width=200)
        self.tree.column('Descripción', width=400)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=15, padx=10)
        
        tk.Button(btn_frame, text="✏️ Editar", command=self.editar_cuisine, bg=self.main_window.COLOR_NARANJA, fg='white', font=('Arial', 10), padx=15, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar_cuisine, bg=self.main_window.COLOR_ROJO, fg='white', font=('Arial', 10), padx=15, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
    
    def cargar_cuisines(self):
        """Carga todos los tipos de cocina"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        #Obtener cuisines
        cuisines = obtener_cuisines()
        for c in cuisines:
            desc = c['description'][:50] + '...' if c['description'] and len(c['description']) > 50 else (c['description'] or '')
            self.tree.insert('', tk.END, values=(c['id'], c['name'], c['country_origin'] or 'N/A', desc))
    
    def abrir_formulario_nuevo(self):
        """Abre formulario para nueva cuisine"""
        VentanaFormularioCuisine(self.main_window.root, self, modo='nuevo')
    
    def editar_cuisine(self):
        """Editar cuisine seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un tipo de cocina")
            return
        item = self.tree.item(seleccion[0])
        cuisine_id = item['values'][0]
        VentanaFormularioCuisine(self.main_window.root, self, modo='editar', cuisine_id=cuisine_id)
    
    def eliminar_cuisine(self):
        """Eliminar cuisine seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un tipo de cocina")
            return
        item = self.tree.item(seleccion[0])
        cuisine_id = item['values'][0]
        cuisine_nombre = item['values'][1]
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar '{cuisine_nombre}'?")
        if confirmar:
            eliminar_cuisines(cuisine_id)
            messagebox.showinfo("Éxito", "Tipo de cocina eliminado")
            self.cargar_cuisines()


# ==================== FORMULARIO CUISINE ====================

class VentanaFormularioCuisine:
    """Formulario para crear/editar cuisine"""
    
    def __init__(self, parent, ventana_cuisines, modo='nuevo', cuisine_id=None):
        self.ventana_cuisines = ventana_cuisines
        self.modo = modo
        self.cuisine_id = cuisine_id
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("➕ Nueva Cocina" if modo == 'nuevo' else "✏️ Editar Cocina")
        self.ventana.geometry("500x400")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        
        self.crear_interfaz()
        if modo == 'editar' and cuisine_id:
            self.cargar_datos()
    
    def crear_interfaz(self):
        """Crea el formulario"""
        frame = tk.Frame(self.ventana, bg='white', padx=30, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        #Titulo
        titulo_texto = "Tipos de Cocinas" if self.modo == 'nuevo' else "Editar Receta"
        tk.Label(frame, text=titulo_texto, font=('Arial', 18, 'bold'), bg='white', fg='#2E7D32').pack(pady=(0, 20))
        
        #Nombre
        tk.Label(frame, text="Nombre:*", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        self.entry_nombre = ttk.Entry(frame, font=('Arial', 11), width=50)
        self.entry_nombre.pack(fill=tk.X)
        
        #Pais
        tk.Label(frame, text="País de Origen:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        self.entry_pais = ttk.Entry(frame, font=('Arial', 11), width=50)
        self.entry_pais.pack(fill=tk.X)
        
        #Descripcion
        tk.Label(frame, text="Descripción:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        self.text_descripcion = tk.Text(frame, height=5, font=('Arial', 10), wrap=tk.WORD)
        self.text_descripcion.pack(fill=tk.X)
        
        # Botones
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="💾 Guardar", command=self.guardar, bg='#2E7D32', fg='white', font=('Arial', 11, 'bold'), padx=20, pady=10, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.ventana.destroy, bg='#757575', fg='white', font=('Arial', 11), padx=20, pady=10, cursor='hand2', bd=0).pack(side=tk.LEFT)
    
    
    def cargar_datos(self):
        """Carga datos para editar"""
        cuisine = obtener_cuisines_por_id(self.cuisine_id)
        if cuisine:
            self.entry_nombre.insert(0, cuisine['name'])
            if cuisine['country_origin']:
                self.entry_pais.insert(0, cuisine['country_origin'])
            if cuisine['description']:
                self.text_descripcion.insert('1.0', cuisine['description'])
    
    def guardar(self):
        """Guarda o actualiza"""
        #Valida campos
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return
        
        pais = self.entry_pais.get().strip()
        descripcion = self.text_descripcion.get('1.0', tk.END).strip()
        
        #Guardar o actualizar
        if self.modo == 'nuevo':
            if agregar_cuisines(nombre, descripcion, pais):
                messagebox.showinfo("Éxito", "Tipo de cocina creado")
                self.ventana_cuisines.cargar_cuisines()
                self.ventana.destroy()
        else:
            actualizar_cuisines(self.cuisine_id, nombre, descripcion, pais)
            messagebox.showinfo("Éxito", "Tipo de cocina actualizado")
            self.ventana_cuisines.cargar_cuisines()
            self.ventana.destroy()
