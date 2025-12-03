import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from models.author import obtener_author, obtener_author_por_id
from models.cuisines import obtener_cuisines, obtener_cuisines_por_id
from models.recipes import actualizar_receta, agregar_receta, eliminar_receta_por_id, obtener_receta_por_id, obtener_recetas

class VentanaRecetas(tk.Toplevel):
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.crear_interfaz()
        self.cargar_recetas()
    
    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.parent, bg=self.main_window.COLOR_SECUNDARIO, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="📖 Gestión de Recetas", font=('Arial', 16, 'bold'), bg=self.main_window.COLOR_SECUNDARIO, fg='white').pack(side=tk.LEFT, padx=30, pady=15)
        tk.Button(header, text="➕ Nueva Receta", command=self.abrir_ventana_nueva_receta, bg=self.main_window.COLOR_PRIMARIO, fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8, cursor='hand2', bd=0).pack(side=tk.RIGHT, padx=30)
        
        # Frame principal
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Barra de búsqueda
        search_frame = tk.Frame(main_frame, bg='white')
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(search_frame, text="🔍 Buscar:", font=('Arial', 11), bg='white').pack(side=tk.LEFT, padx=(10, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame,
                                textvariable=self.search_var,
                                font=('Arial', 11),
                                width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(search_frame,
                 text="Buscar",
                 command=self.buscar_recetas,
                 bg=self.main_window.COLOR_AZUL,
                 fg='white',
                 font=('Arial', 10),
                 padx=15,
                 pady=5,
                 cursor='hand2',
                 bd=0).pack(side=tk.LEFT, padx=5)
        
        tk.Button(search_frame,
                 text="↻ Recargar",
                 command=self.cargar_recetas,
                 bg=self.main_window.COLOR_SECUNDARIO,
                 fg='white',
                 font=('Arial', 10),
                 padx=15,
                 pady=5,
                 cursor='hand2',
                 bd=0).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        tree_frame = tk.Frame(main_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        columns = ('ID', 'Título', 'Descripción', 'Autor', 'Cocina')
        self.tree = ttk.Treeview(tree_frame,
                                columns=columns,
                                show='headings',
                                yscrollcommand=scrollbar_y.set,
                                xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Título', text='Título')
        self.tree.heading('Descripción', text='Descripción')
        self.tree.heading('Autor', text='Autor')
        self.tree.heading('Cocina', text='Tipo de Cocina')
        
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Título', width=250)
        self.tree.column('Descripción', width=350)
        self.tree.column('Autor', width=150)
        self.tree.column('Cocina', width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Botones de acción
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=15, padx=10)
        
        tk.Button(btn_frame, text="👁️ Ver Detalles", command=self.ver_detalles, bg=self.main_window.COLOR_AZUL, fg='white', font=('Arial', 10), padx=15, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Editar", command=self.editar_receta, bg=self.main_window.COLOR_NARANJA, fg='white', font=('Arial', 10), padx=15, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar_receta, bg=self.main_window.COLOR_ROJO, fg='white', font=('Arial', 10), padx=15, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
    
    
    def cargar_recetas(self):
        """Carga todas las recetas en el Treeview"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener recetas
        recetas = obtener_recetas()
        autores = {a['id']: a['name'] for a in obtener_author()}
        cuisines = {c['id']: c['name'] for c in obtener_cuisines()}
        
        # Insertar en el Treeview
        for receta in recetas:
            autor_nombre = autores.get(receta['author_id'], 'Sin autor')
            cuisine_nombre = cuisines.get(receta['cuisine_id'], 'Sin cocina')
            descripcion = receta['description'][:50] + '...' if receta['description'] and len(receta['description']) > 50 else (receta['description'] or '')
            
            self.tree.insert('', tk.END, values=(
                receta['id'],
                receta['title'],
                descripcion,
                autor_nombre,
                cuisine_nombre 
            ))
    
    def buscar_recetas(self):
        """Busca recetas por término"""
        termino = self.search_var.get().strip()
        if not termino:
            self.cargar_recetas()
            return
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar recetas
        recetas = obtener_recetas()
        autores = {a['id']: a['name'] for a in obtener_author()}
        cuisines = {c['id']: c['name'] for c in obtener_cuisines()}
        
        # Filtrar por término
        for receta in recetas:
            if (termino.lower() in receta['title'].lower() or 
                (receta['description'] and termino.lower() in receta['description'].lower())):
                
                autor_nombre = autores.get(receta['author_id'], 'Sin autor')
                cuisine_nombre = cuisines.get(receta['cuisine_id'], 'Sin cocina')
                descripcion = receta['description'][:50] + '...' if receta['description'] and len(receta['description']) > 50 else (receta['description'] or '')
                
                self.tree.insert('', tk.END, values=(
                    receta['id'],
                    receta['title'],
                    descripcion,
                    autor_nombre,
                    cuisine_nombre
                ))
    
    def abrir_ventana_nueva_receta(self):
        """Abre ventana para crear nueva receta"""
        VentanaFormularioReceta(self.main_window, self, modo='nuevo')
    
    def ver_detalles(self):
        """Ver detalles de la receta seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una receta")
            return
        
        item = self.tree.item(seleccion[0])
        receta_id = item['values'][0]
        VentanaDetallesReceta(self.main_window, receta_id)
    
    def editar_receta(self):
        """Editar receta seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una receta")
            return
        
        item = self.tree.item(seleccion[0])
        receta_id = item['values'][0]
        VentanaFormularioReceta(self.main_window, self, modo='editar', receta_id=receta_id)
    
    def eliminar_receta(self):
        """Eliminar receta seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una receta")
            return
        
        item = self.tree.item(seleccion[0])
        receta_id = item['values'][0]
        receta_titulo = item['values'][1]
        
        confirmar = messagebox.askyesno("Confirmar Eliminación",
                                        f"¿Eliminar la receta '{receta_titulo}'?\n\nEsta acción no se puede deshacer.")
        
        if confirmar:
            if eliminar_receta_por_id(receta_id):
                messagebox.showinfo("Éxito", "Receta eliminada correctamente")
                self.cargar_recetas()


# ==================== VENTANA FORMULARIO RECETA ====================

class VentanaFormularioReceta:
    """Ventana para crear/editar recetas"""
    
    def __init__(self, parent, ventana_recetas, modo='nuevo', receta_id=None):
        self.ventana_recetas = ventana_recetas
        self.modo = modo
        self.receta_id = receta_id
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("➕ Nueva Receta" if modo == 'nuevo' else "✏️ Editar Receta")
        self.ventana.geometry("700x750")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        
        self.crear_interfaz()
        if modo == 'editar' and receta_id:
            self.cargar_datos_receta()
    
    def crear_interfaz(self):
        """Crea el formulario de receta"""
        main_frame = tk.Frame(self.ventana, bg='white', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo_texto = "Crear Nueva Receta" if self.modo == 'nuevo' else "Editar Receta"
        tk.Label(main_frame, text=titulo_texto, font=('Arial', 18, 'bold'), bg='white', fg='#2E7D32').pack(pady=(0, 20))
        
        # Formulario con scroll
        canvas = tk.Canvas(main_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Campos del formulario
        form = scrollable_frame
        
        # Título
        tk.Label(form, text="Título:*", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        self.entry_titulo = ttk.Entry(form, font=('Arial', 11), width=60)
        self.entry_titulo.pack(fill=tk.X, pady=(0, 10))
        
        # Descripción
        tk.Label(form, text="Descripción:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        self.text_descripcion = tk.Text(form, height=4, font=('Arial', 10), wrap=tk.WORD)
        self.text_descripcion.pack(fill=tk.X, pady=(0, 10))
        
        # Autor
        tk.Label(form, text="Autor:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        autores = obtener_author()
        autor_valores = [f"{a['id']} - {a['name']}" for a in autores]
        autor_valores.insert(0, "Sin autor")
        self.combo_autor = ttk.Combobox(form, values=autor_valores, state='readonly', font=('Arial', 10), width=57)
        self.combo_autor.current(0)
        self.combo_autor.pack(fill=tk.X, pady=(0, 10))
        
        # Tipo de cocina
        tk.Label(form, text="Tipo de Cocina:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        cuisines = obtener_cuisines()
        cuisine_valores = [f"{c['id']} - {c['name']}" for c in cuisines]
        cuisine_valores.insert(0, "Sin tipo de cocina")
        self.combo_cuisine = ttk.Combobox(form, values=cuisine_valores, state='readonly', font=('Arial', 10), width=57)
        self.combo_cuisine.current(0)
        self.combo_cuisine.pack(fill=tk.X, pady=(0, 10))
        
        # Preparación
        tk.Label(form, text="Instrucciones de Preparación:*", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        self.text_preparacion = scrolledtext.ScrolledText(form, height=8, font=('Arial', 10), wrap=tk.WORD)
        self.text_preparacion.pack(fill=tk.X, pady=(0, 10))
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(btn_frame, text="💾 Guardar", command=self.guardar_receta, bg='#2E7D32', fg='white', font=('Arial', 11, 'bold'), padx=30, pady=10, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.ventana.destroy, bg='#757575', fg='white', font=('Arial', 11), padx=30, pady=10, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
    
    def cargar_datos_receta(self):
        """Carga los datos de la receta para editar"""
        receta = obtener_receta_por_id(self.receta_id)
        if not receta:
            messagebox.showerror("Error", "No se pudo cargar la receta")
            self.ventana.destroy()
            return
        
        self.entry_titulo.insert(0, receta['title'])
        
        if receta['description']:
            self.text_descripcion.insert('1.0', receta['description'])
        
        if receta['author_id']:
            for i, valor in enumerate(self.combo_autor['values']):
                if valor.startswith(str(receta['author_id'])):
                    self.combo_autor.current(i)
                    break
        
        if receta['cuisine_id']:
            for i, valor in enumerate(self.combo_cuisine['values']):
                if valor.startswith(str(receta['cuisine_id'])):
                    self.combo_cuisine.current(i)
                    break
        
        if receta['preparation']:
            self.text_preparacion.insert('1.0', receta['preparation'])
    
    def guardar_receta(self):
        """Guarda o actualiza la receta"""
        # Validar campos
        titulo = self.entry_titulo.get().strip()
        if not titulo:
            messagebox.showwarning("Advertencia", "El título es obligatorio")
            return
        
        descripcion = self.text_descripcion.get('1.0', tk.END).strip()
        preparacion = self.text_preparacion.get('1.0', tk.END).strip()
        
        if not preparacion:
            messagebox.showwarning("Advertencia", "Las instrucciones de preparación son obligatorias")
            return
        
        # Obtener IDs
        autor_seleccion = self.combo_autor.get()
        author_id = None if autor_seleccion == "Sin autor" else int(autor_seleccion.split(' - ')[0])
        
        cuisine_seleccion = self.combo_cuisine.get()
        cuisine_id = None if cuisine_seleccion == "Sin tipo de cocina" else int(cuisine_seleccion.split(' - ')[0])
        
        # Guardar o actualizar
        if self.modo == 'nuevo':
            receta_id = agregar_receta(titulo, descripcion, preparacion, author_id, cuisine_id)
            if receta_id:
                messagebox.showinfo("Éxito", "Receta creada correctamente")
                self.ventana_recetas.cargar_recetas()
                self.ventana.destroy()
        else:
            if actualizar_receta(self.receta_id, titulo, descripcion, preparacion, author_id, cuisine_id):
                messagebox.showinfo("Éxito", "Receta actualizada correctamente")
                self.ventana_recetas.cargar_recetas()
                self.ventana.destroy()
                
                

# ==================== VENTANA DETALLES RECETA ====================

class VentanaDetallesReceta:
    """Muestra los detalles completos de una receta"""
    
    def __init__(self, parent, receta_id):
        self.receta_id = receta_id
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("📖 Detalles de Receta")
        self.ventana.geometry("700x800")
        self.ventana.resizable(False, False)
        
        self.crear_interfaz()
        self.cargar_detalles()
    
    def crear_interfaz(self):
        """Crea la interfaz de detalles"""
        # Canvas con scroll
        canvas = tk.Canvas(self.ventana, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.ventana, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white', padx=30, pady=20)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def cargar_detalles(self):
        """Carga y muestra los detalles de la receta"""
        receta = obtener_receta_por_id(self.receta_id)
        if not receta:
            messagebox.showerror("Error", "No se pudo cargar la receta")
            self.ventana.destroy()
            return
        
        frame = self.scrollable_frame
        
        # Título
        tk.Label(frame,
                text=f"🍽️ {receta['title'].upper()}",
                font=('Arial', 20, 'bold'),
                bg='white',
                fg='#2E7D32').pack(pady=(0, 20))
        
        # Información básica
        info_frame = tk.Frame(frame, bg='#E8F5E9', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=10)
        
        # Obtener autor y cuisine
        autor = obtener_author_por_id(receta['author_id']) if receta['author_id'] else None
        cuisine = obtener_cuisines_por_id(receta['cuisine_id']) if receta['cuisine_id'] else None
        
        info_data = [
            ("👨‍🍳 Autor:", autor['name'] if autor else 'Sin autor'),
            ("🌎 Tipo de Cocina:", cuisine['name'] if cuisine else 'Sin tipo'),
            ("📅 Creada:", str(receta['created_at'])[:19]),
            ("🔄 Actualizada:", str(receta['updated_at'])[:19])
        ]
        
        for label, value in info_data:
            row = tk.Frame(info_frame, bg='#E8F5E9')
            row.pack(fill=tk.X, padx=15, pady=8)
            tk.Label(row, text=label, font=('Arial', 11, 'bold'), bg='#E8F5E9').pack(side=tk.LEFT)
            tk.Label(row, text=value, font=('Arial', 11), bg='#E8F5E9').pack(side=tk.LEFT, padx=10)
        
        # Descripción
        if receta['description']:
            tk.Label(frame, text="📝 Descripción:", font=('Arial', 13, 'bold'), bg='white', fg='#2E7D32').pack(anchor='w', pady=(20, 5))
            desc_frame = tk.Frame(frame, bg='#FAFAFA', relief=tk.SOLID, borderwidth=1)
            desc_frame.pack(fill=tk.X, pady=5)
            tk.Label(desc_frame, text=receta['description'], font=('Arial', 11), bg='#FAFAFA', wraplength=600, justify=tk.LEFT).pack(padx=15, pady=10)
        
        # Ingredientes
        tk.Label(frame, text="🥕 Ingredientes:", font=('Arial', 13, 'bold'), bg='white', fg='#2E7D32').pack(anchor='w', pady=(20, 5))
        ing_frame = tk.Frame(frame, bg='#FFF9C4', relief=tk.SOLID, borderwidth=1)
        ing_frame.pack(fill=tk.X, pady=5)
        
        # Aquí cargarías los ingredientes de la tabla recipe_ingredients
        tk.Label(ing_frame, text="(Ingredientes por implementar con tabla pivote)", font=('Arial', 10, 'italic'), bg='#FFF9C4').pack(padx=15, pady=10)
        
        # Preparación
        if receta['preparation']:
            tk.Label(frame, text="👨‍🍳 Instrucciones de Preparación:", font=('Arial', 13, 'bold'), bg='white', fg='#2E7D32').pack(anchor='w', pady=(20, 5))
            prep_frame = tk.Frame(frame, bg='#FAFAFA', relief=tk.SOLID, borderwidth=1)
            prep_frame.pack(fill=tk.X, pady=5)
            tk.Label(prep_frame, text=receta['preparation'], font=('Arial', 11), bg='#FAFAFA', wraplength=600, justify=tk.LEFT).pack(padx=15, pady=10)

