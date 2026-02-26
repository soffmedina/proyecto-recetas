import tkinter as tk
from tkinter import ttk, messagebox

# se reutiliza el validador central para mantener la lógica idéntica a la capa de
# controlador. De esta manera no habrá discrepancias entre lo que acepta la
# interfaz y lo que acepta el backend (por ejemplo, antes el formulario
# exigía 3 caracteres en el nombre mientras que el controlador permitía 2).
from utils.validators import validate_required_text

from controller.CuisineController import CuisineController


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
        cuisines = CuisineController.get_all_cuisines()
        for c in cuisines:
            desc = c['description'][:50] + '...' if c['description'] and len(c['description']) > 50 else (c['description'] or '')
            self.tree.insert('', tk.END, values=(c['id'], c['name'], c['country_origin'] or 'N/A', desc))
    
    def abrir_formulario_nuevo(self):
        """Abre formulario para nueva cuisine"""
        VentanaFormularioCuisine(self.main_window, self, modo='nuevo')
    
    def editar_cuisine(self):
        """Editar cuisine seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un tipo de cocina")
            return
        item = self.tree.item(seleccion[0])
        cuisine_id = item['values'][0]
        VentanaFormularioCuisine(self.main_window, self, modo='editar', cuisine_id=cuisine_id)
    
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
            if CuisineController.delete_cuisine(cuisine_id):
                messagebox.showinfo("Éxito", "Tipo de cocina eliminado")
                self.cargar_cuisines()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la cocina")


# ==================== FORMULARIO CUISINE ====================

class VentanaFormularioCuisine:
    """Formulario para crear/editar cuisine con validaciones y diseño mejorado"""
    
    def __init__(self, parent, ventana_cuisines, modo='nuevo', cuisine_id=None):
        self.ventana_cuisines = ventana_cuisines
        self.modo = modo
        self.cuisine_id = cuisine_id
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("➕ Nueva Cocina" if modo == 'nuevo' else "✏️ Editar Cocina")
        self.ventana.geometry("600x650")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        
        self.crear_interfaz()
        if modo == 'editar' and cuisine_id:
            self.cargar_datos()
    
    def crear_interfaz(self):
        """Crea el formulario con scroll y validaciones"""
        # Header
        header = tk.Frame(self.ventana, bg='#FF6F00', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        titulo_texto = "➕ Crear Nuevo Tipo de Cocina" if self.modo == 'nuevo' else "✏️ Editar Tipo de Cocina"
        tk.Label(header, text=titulo_texto, font=('Arial', 16, 'bold'), bg='#FF6F00', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        # Main frame con scroll
        main_frame = tk.Frame(self.ventana, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        canvas = tk.Canvas(main_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Crear campos en el frame scrollable
        self._crear_campos()
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones al final
        btn_frame = tk.Frame(self.ventana, bg='white', pady=15)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="💾 Guardar", command=self.guardar, bg='#FF6F00', fg='white', 
                 font=('Arial', 11, 'bold'), padx=25, pady=10, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.ventana.destroy, bg='#757575', fg='white', 
                 font=('Arial', 11), padx=25, pady=10, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
    
    def _crear_campos(self):
        """Crea los campos del formulario con iconos y validaciones"""
        form = self.scrollable_frame
        
        # ===== NOMBRE =====
        nombre_frame = tk.Frame(form, bg='white')
        nombre_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(nombre_frame, text="🌎 Nombre:*", font=('Arial', 11, 'bold'), bg='white', fg='#FF6F00').pack(anchor='w', pady=(0, 5))
        self.entry_nombre = ttk.Entry(nombre_frame, font=('Arial', 11), width=65)
        self.entry_nombre.pack(fill=tk.X)
        self.label_nombre_error = tk.Label(nombre_frame, text="", font=('Arial', 9), bg='white', fg='#F44336')
        self.label_nombre_error.pack(anchor='w', pady=(3, 0))
        
        # ===== PAÍS DE ORIGEN =====
        pais_frame = tk.Frame(form, bg='white')
        pais_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(pais_frame, text="🗺️ País de Origen:", font=('Arial', 11, 'bold'), bg='white', fg='#FF6F00').pack(anchor='w', pady=(0, 5))
        self.entry_pais = ttk.Entry(pais_frame, font=('Arial', 11), width=65)
        self.entry_pais.pack(fill=tk.X)
        tk.Label(pais_frame, text="ℹ️ Opcional - Ingresa el país de origen de esta cocina", font=('Arial', 9, 'italic'), bg='white', fg='#757575').pack(anchor='w', pady=(3, 0))
        
        # ===== DESCRIPCIÓN =====
        descripcion_frame = tk.Frame(form, bg='white')
        descripcion_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(descripcion_frame, text="📝 Descripción:", font=('Arial', 11, 'bold'), bg='white', fg='#FF6F00').pack(anchor='w', pady=(0, 5))
        self.text_descripcion = tk.Text(descripcion_frame, height=6, font=('Arial', 10), wrap=tk.WORD)
        self.text_descripcion.pack(fill=tk.BOTH, expand=True)
        tk.Label(descripcion_frame, text="ℹ️ Opcional - Describe características, platos típicos, técnicas culinarias, etc.", font=('Arial', 9, 'italic'), bg='white', fg='#757575').pack(anchor='w', pady=(3, 0))
    
    def _validar_nombre(self):
        """Valida el campo nombre"""
        # aprovechamos el validador común para no repetir condiciones y poder
        # cambiar el mínimo en un solo lugar si fuera necesario. El valor 2 es el
        # que utiliza la capa de negocio/servicio.
        nombre = self.entry_nombre.get().strip()
        valid, err = validate_required_text(nombre, "Nombre de la cocina", 2)
        if not valid:
            # el validador devuelve el mensaje apropiado, sólo lo mostramos
            self.label_nombre_error.config(text=f"⚠️ {err}")
            return False
        self.label_nombre_error.config(text="")
        return True
    
    def cargar_datos(self):
        """Carga datos para editar"""
        cuisine = CuisineController.get_cuisine_by_id(self.cuisine_id)
        if cuisine:
            self.entry_nombre.insert(0, cuisine['name'])
            if cuisine['country_origin']:
                self.entry_pais.insert(0, cuisine['country_origin'])
            if cuisine['description']:
                self.text_descripcion.insert('1.0', cuisine['description'])
    
    def guardar(self):
        """Guarda o actualiza con validaciones"""
        if not self._validar_nombre():
            messagebox.showwarning("Validación", "Por favor corrige el nombre")
            return
        
        nombre = self.entry_nombre.get().strip()
        pais = self.entry_pais.get().strip()
        descripcion = self.text_descripcion.get('1.0', tk.END).strip()
        
        if self.modo == 'nuevo':
            if CuisineController.create_cuisine(nombre, descripcion, pais):
                messagebox.showinfo("✅ Éxito", f"Tipo de cocina '{nombre}' creado correctamente")
                self.ventana_cuisines.cargar_cuisines()
                self.ventana.destroy()
            else:
                messagebox.showerror("❌ Error", "No se pudo crear el tipo de cocina")
        else:
            if CuisineController.update_cuisine(self.cuisine_id, nombre, descripcion, pais):
                messagebox.showinfo("✅ Éxito", f"Tipo de cocina '{nombre}' actualizado correctamente")
                self.ventana_cuisines.cargar_cuisines()
                self.ventana.destroy()
            else:
                messagebox.showerror("❌ Error", "No se pudo actualizar el tipo de cocina")
