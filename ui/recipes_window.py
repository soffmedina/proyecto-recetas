import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from controller.AuthorController import AuthorController
from controller.CuisineController import CuisineController
from controller.RecipeController import RecipeController
from controller.IngredientController import IngredientController
from controller.RecipeIngredientController import RecipeIngredientController

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
        recetas = RecipeController.get_all_recipes()
        autores = {a['id']: a['name'] for a in AuthorController.get_all_authors()}
        cuisines = {c['id']: c['name'] for c in CuisineController.get_all_cuisines()}
        
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
        recetas = RecipeController.get_all_recipes()
        autores = {a['id']: a['name'] for a in AuthorController.get_all_authors()}
        cuisines = {c['id']: c['name'] for c in CuisineController.get_all_cuisines()}
        
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
            if RecipeController.delete_recipe(receta_id):
                messagebox.showinfo("Éxito", "Receta eliminada correctamente")
                self.cargar_recetas()


# ==================== VENTANA FORMULARIO RECETA ====================

class VentanaFormularioReceta:
    """Ventana para crear/editar recetas con validaciones y diseño mejorado"""
    
    def __init__(self, parent, ventana_recetas, modo='nuevo', receta_id=None):
        self.ventana_recetas = ventana_recetas
        self.modo = modo
        self.receta_id = receta_id
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("➕ Nueva Receta" if modo == 'nuevo' else "✏️ Editar Receta")
        self.ventana.geometry("700x800")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        
        self.crear_interfaz()
        if modo == 'editar' and receta_id:
            self.cargar_datos_receta()
    
    def crear_interfaz(self):
        """Crea el formulario de receta con scroll y validaciones"""
        # Header
        header = tk.Frame(self.ventana, bg='#2196F3', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        titulo_texto = "➕ Crear Nueva Receta" if self.modo == 'nuevo' else "✏️ Editar Receta"
        tk.Label(header, text=titulo_texto, font=('Arial', 16, 'bold'), bg='#2196F3', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
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
        
        # Crear campos
        self._crear_campos()
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones
        btn_frame = tk.Frame(self.ventana, bg='white', pady=15)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="💾 Guardar", command=self.guardar_receta, bg='#2196F3', fg='white', 
                 font=('Arial', 11, 'bold'), padx=25, pady=10, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.ventana.destroy, bg='#757575', fg='white', 
                 font=('Arial', 11), padx=25, pady=10, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
    
    def _crear_campos(self):
        """Crea los campos del formulario con iconos y validaciones"""
        form = self.scrollable_frame
        
        # ===== TÍTULO =====
        titulo_frame = tk.Frame(form, bg='white')
        titulo_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(titulo_frame, text="🍽️ Título:*", font=('Arial', 11, 'bold'), bg='white', fg='#2196F3').pack(anchor='w', pady=(0, 5))
        self.entry_titulo = ttk.Entry(titulo_frame, font=('Arial', 11), width=65)
        self.entry_titulo.pack(fill=tk.X)
        self.label_titulo_error = tk.Label(titulo_frame, text="", font=('Arial', 9), bg='white', fg='#F44336')
        self.label_titulo_error.pack(anchor='w', pady=(3, 0))
        
        # ===== DESCRIPCIÓN =====
        descripcion_frame = tk.Frame(form, bg='white')
        descripcion_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(descripcion_frame, text="📝 Descripción:", font=('Arial', 11, 'bold'), bg='white', fg='#2196F3').pack(anchor='w', pady=(0, 5))
        self.text_descripcion = tk.Text(descripcion_frame, height=4, font=('Arial', 10), wrap=tk.WORD)
        self.text_descripcion.pack(fill=tk.X)
        tk.Label(descripcion_frame, text="ℹ️ Opcional - Resumen o introducción de la receta", font=('Arial', 9, 'italic'), bg='white', fg='#757575').pack(anchor='w', pady=(3, 0))
        
        # ===== AUTOR =====
        autor_frame = tk.Frame(form, bg='white')
        autor_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(autor_frame, text="👨‍🍳 Autor:", font=('Arial', 11, 'bold'), bg='white', fg='#2196F3').pack(anchor='w', pady=(0, 5))
        autores = AuthorController.get_all_authors()
        autor_valores = [f"{a['id']} - {a['name']}" for a in autores]
        autor_valores.insert(0, "Sin autor")
        self.combo_autor = ttk.Combobox(autor_frame, values=autor_valores, state='readonly', font=('Arial', 10), width=62)
        self.combo_autor.current(0)
        self.combo_autor.pack(fill=tk.X)
        tk.Label(autor_frame, text="ℹ️ Opcional - Selecciona el autor de la receta", font=('Arial', 9, 'italic'), bg='white', fg='#757575').pack(anchor='w', pady=(3, 0))
        
        # ===== TIPO DE COCINA =====
        cuisine_frame = tk.Frame(form, bg='white')
        cuisine_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(cuisine_frame, text="🌎 Tipo de Cocina:", font=('Arial', 11, 'bold'), bg='white', fg='#2196F3').pack(anchor='w', pady=(0, 5))
        cuisines = CuisineController.get_all_cuisines()
        cuisine_valores = [f"{c['id']} - {c['name']}" for c in cuisines]
        cuisine_valores.insert(0, "Sin tipo de cocina")
        self.combo_cuisine = ttk.Combobox(cuisine_frame, values=cuisine_valores, state='readonly', font=('Arial', 10), width=62)
        self.combo_cuisine.current(0)
        self.combo_cuisine.pack(fill=tk.X)
        tk.Label(cuisine_frame, text="ℹ️ Opcional - Selecciona el tipo de cocina", font=('Arial', 9, 'italic'), bg='white', fg='#757575').pack(anchor='w', pady=(3, 0))
        
        # ===== INGREDIENTES =====
        ingredientes_frame = tk.Frame(form, bg='white')
        ingredientes_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(ingredientes_frame, text="🥕 Ingredientes:", font=('Arial', 11, 'bold'), bg='white', fg='#2196F3').pack(anchor='w', pady=(0, 5))
        
        # Frame para selector de ingredientes
        selector_frame = tk.Frame(ingredientes_frame, bg='white')
        selector_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(selector_frame, text="Ingrediente:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=(0, 5))
        ingredientes_lista = IngredientController.get_all_ingredients()
        self.ingredientes_disponibles = {ing['id']: ing['name'] for ing in ingredientes_lista}
        print(f"DEBUG: Ingredientes cargados en formulario: {len(self.ingredientes_disponibles)} ({list(self.ingredientes_disponibles.items())[:3]}...)")
        self.combo_ingrediente = ttk.Combobox(selector_frame, 
                                               values=[ing['name'] for ing in ingredientes_lista],
                                               state='readonly', font=('Arial', 10), width=20)
        self.combo_ingrediente.pack(side=tk.LEFT, padx=5)
        
        tk.Label(selector_frame, text="Cantidad:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=(10, 5))
        self.entry_cantidad = ttk.Entry(selector_frame, font=('Arial', 10), width=10)
        self.entry_cantidad.pack(side=tk.LEFT, padx=5)
        
        tk.Label(selector_frame, text="Unidad:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=(10, 5))
        self.combo_unidad = ttk.Combobox(selector_frame, 
                                          values=['g', 'kg', 'ml', 'l', 'taza', 'cuchara', 'cucharita', 'unidad'],
                                          state='readonly', font=('Arial', 10), width=10)
        self.combo_unidad.pack(side=tk.LEFT, padx=5)
        
        tk.Button(selector_frame, text="➕ Agregar", command=self._agregar_ingrediente, 
                 bg='#4CAF50', fg='white', font=('Arial', 9), padx=10, pady=3, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
        
        # Treeview con ingredientes agregados - con etiqueta visual del contador
        tree_label_frame = tk.Frame(ingredientes_frame, bg='white')
        tree_label_frame.pack(fill=tk.X, pady=(0, 3))
        tk.Label(tree_label_frame, text="Ingredientes agregados:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.label_cant_ingredientes = tk.Label(tree_label_frame, text="(0)", font=('Arial', 10, 'italic'), bg='white', fg='#2196F3')
        self.label_cant_ingredientes.pack(anchor='w')
        
        self.tree_ingredientes = ttk.Treeview(ingredientes_frame, columns=('Ingrediente', 'Cantidad', 'Unidad'), show='headings', height=4)
        self.tree_ingredientes.heading('Ingrediente', text='Ingrediente')
        self.tree_ingredientes.heading('Cantidad', text='Cantidad')
        self.tree_ingredientes.heading('Unidad', text='Unidad')
        self.tree_ingredientes.column('Ingrediente', width=150)
        self.tree_ingredientes.column('Cantidad', width=80)
        self.tree_ingredientes.column('Unidad', width=80)
        # bind event para actualizar contador cuando se agregan/elimina ingredientes
        self.tree_ingredientes.bind('<<TreeviewSelect>>', self._actualizar_contador_ingredientes)
        self.tree_ingredientes.pack(fill=tk.X, pady=(0, 8))
        
        # Botón para eliminar ingrediente seleccionado
        tk.Button(ingredientes_frame, text="❌ Eliminar Ingrediente Seleccionado", command=self._eliminar_ingrediente,
                 bg='#F44336', fg='white', font=('Arial', 9), padx=10, pady=3, cursor='hand2', bd=0).pack(anchor='w', pady=(0, 8))
        
        tk.Label(ingredientes_frame, text="ℹ️ Opcional - Agrega los ingredientes que contiene esta receta", font=('Arial', 9, 'italic'), bg='white', fg='#757575').pack(anchor='w', pady=(0, 15))
        
        # ===== PREPARACIÓN =====
        preparacion_frame = tk.Frame(form, bg='white')
        preparacion_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(preparacion_frame, text="👨‍🍳 Instrucciones de Preparación:*", font=('Arial', 11, 'bold'), bg='white', fg='#2196F3').pack(anchor='w', pady=(0, 5))
        self.text_preparacion = scrolledtext.ScrolledText(preparacion_frame, height=8, font=('Arial', 10), wrap=tk.WORD)
        self.text_preparacion.pack(fill=tk.BOTH, expand=True)
        self.label_prep_error = tk.Label(preparacion_frame, text="", font=('Arial', 9), bg='white', fg='#F44336')
        self.label_prep_error.pack(anchor='w', pady=(3, 0))
        tk.Label(preparacion_frame, text="ℹ️ Obligatorio - Detalla paso a paso cómo preparar la receta", font=('Arial', 9, 'italic'), bg='white', fg='#757575').pack(anchor='w', pady=(3, 0))
    
    def _actualizar_contador_ingredientes(self, event=None):
        """Actualiza el contador visual de ingredientes en el formulario"""
        cantidad = len(self.tree_ingredientes.get_children())
        self.label_cant_ingredientes.config(text=f"({cantidad})")
    
    def _agregar_ingrediente(self):
        """Agrega un ingrediente al treeview"""
        ingrediente_nombre = self.combo_ingrediente.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        unidad = self.combo_unidad.get().strip()
        
        if not ingrediente_nombre:
            messagebox.showwarning("Validación", "Selecciona un ingrediente")
            return
        
        # Encontrar el ID del ingrediente seleccionado
        ingrediente_id = None
        for ing_id, ing_name in self.ingredientes_disponibles.items():
            if ing_name == ingrediente_nombre:
                ingrediente_id = ing_id
                break
        
        if ingrediente_id is None:
            messagebox.showerror("Error", "No se encontró el ingrediente")
            return
        
        # Verificar si ya está agregado
        for item in self.tree_ingredientes.get_children():
            if self.tree_ingredientes.item(item)['values'][0] == ingrediente_nombre:
                messagebox.showinfo("Aviso", "Este ingrediente ya está agregado a la receta")
                return
        
        # Agregar al treeview
        self.tree_ingredientes.insert('', tk.END, values=(ingrediente_nombre, cantidad, unidad), tags=(ingrediente_id,))
        
        # Limpiar campos
        self.combo_ingrediente.set('')
        self.entry_cantidad.delete(0, tk.END)
        self.combo_unidad.set('')
        
        # Actualizar contador
        self._actualizar_contador_ingredientes()
    
    def _eliminar_ingrediente(self):
        """Elimina el ingrediente seleccionado del treeview"""
        seleccion = self.tree_ingredientes.selection()
        if not seleccion:
            messagebox.showinfo("Aviso", "Selecciona un ingrediente para eliminar")
            return
        
        self.tree_ingredientes.delete(seleccion[0])
        # Actualizar contador
        self._actualizar_contador_ingredientes()
    
    def _validar_titulo(self):
        """Valida el título"""
        titulo = self.entry_titulo.get().strip()
        if not titulo:
            self.label_titulo_error.config(text="⚠️ El título es obligatorio")
            return False
        if len(titulo) < 3:
            self.label_titulo_error.config(text="⚠️ El título debe tener al menos 3 caracteres")
            return False
        self.label_titulo_error.config(text="")
        return True
    
    def _validar_preparacion(self):
        """Valida la preparación"""
        prep = self.text_preparacion.get('1.0', tk.END).strip()
        if not prep:
            self.label_prep_error.config(text="⚠️ Las instrucciones son obligatorias")
            return False
        if len(prep) < 10:
            self.label_prep_error.config(text="⚠️ Las instrucciones deben tener al menos 10 caracteres")
            return False
        self.label_prep_error.config(text="")
        return True
    
    def cargar_datos_receta(self):
        """Carga los datos de la receta para editar"""
        receta = RecipeController.get_recipe_by_id(self.receta_id)
        if not receta:
            messagebox.showerror("❌ Error", "No se pudo cargar la receta")
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
        
        # Cargar ingredientes existentes
        ingredientes_receta = RecipeIngredientController.get_ingredients_for_recipe(self.receta_id)
        for ing in ingredientes_receta:
            self.tree_ingredientes.insert('', tk.END, values=(ing['name'], ing.get('quantity', ''), ing.get('unit', '')), tags=(ing['id'],))
        
        # Actualizar contador inicial
        self._actualizar_contador_ingredientes()
    
    def guardar_receta(self):
        """Guarda o actualiza la receta con validaciones"""
        if not self._validar_titulo():
            messagebox.showwarning("Validación", "Por favor corrige el título")
            return
        
        if not self._validar_preparacion():
            messagebox.showwarning("Validación", "Por favor corrige las instrucciones")
            return
        
        # Obtener valores
        titulo = self.entry_titulo.get().strip()
        descripcion = self.text_descripcion.get('1.0', tk.END).strip()
        preparacion = self.text_preparacion.get('1.0', tk.END).strip()
        
        # convertir selección de combobox a ID, cuidando posibles valores
        # inesperados para que no rompamos la ventana con un ValueError.
        autor_seleccion = self.combo_autor.get()
        author_id = None
        if autor_seleccion and autor_seleccion != "Sin autor":
            try:
                author_id = int(autor_seleccion.split(' - ')[0])
            except Exception:
                # si no se puede convertir, dejamos None pero avisamos en
                # consola para depuración
                print(f"Advertencia: formato de autor no válido '{autor_seleccion}'")

        cuisine_seleccion = self.combo_cuisine.get()
        cuisine_id = None
        if cuisine_seleccion and cuisine_seleccion != "Sin tipo de cocina":
            try:
                cuisine_id = int(cuisine_seleccion.split(' - ')[0])
            except Exception:
                print(f"Advertencia: formato de tipo de cocina no válido '{cuisine_seleccion}'")
        
        # Guardar o actualizar
        # los métodos del controlador esperan los parámetros en el orden
        # (title, description, preparation, author_id, cuisine_id). En versiones
        # anteriores se estaba pasando la preparación donde debería ir la
        # descripción, lo que provocaba que al editar no se ejecutara ningún
        # cambio (y en ocasiones se lanzaba una excepción silenciada por tkinter).
        # Además, el update también presentaba el mismo desajuste.
        try:
            if self.modo == 'nuevo':
                receta_id = RecipeController.create_recipe(
                    titulo,
                    descripcion,
                    preparacion,
                    author_id,
                    cuisine_id,
                )
                if receta_id:
                    # Guardar ingredientes recién añadidos
                    try:
                        self._guardar_ingredientes(receta_id)
                    except Exception as ing_exc:
                        print(f"Error al guardar ingredientes nuevos: {ing_exc}")
                    messagebox.showinfo("✅ Éxito", f"Receta '{titulo}' creada correctamente")
                    self.ventana_recetas.cargar_recetas()
                    self.ventana.destroy()
                else:
                    messagebox.showerror("❌ Error", "No se pudo crear la receta")
            else:
                actualizado = RecipeController.update_recipe(
                    self.receta_id,
                    titulo,
                    descripcion,
                    preparacion,
                    author_id,
                    cuisine_id,
                )
                if actualizado:
                    # Actualizar lista de ingredientes si la receta ya existía
                    try:
                        self._actualizar_ingredientes(self.receta_id)
                    except Exception as ing_exc:
                        print(f"Error al actualizar ingredientes: {ing_exc}")
                    messagebox.showinfo("✅ Éxito", f"Receta '{titulo}' actualizada correctamente")
                    self.ventana_recetas.cargar_recetas()
                    self.ventana.destroy()
                else:
                    messagebox.showerror("❌ Error", "No se pudo actualizar la receta")
        except Exception as exc:
            # registrar la excepción completa en consola para análisis futuro
            import traceback
            traceback.print_exc()

            # algunos errores son por conversión de IDs, otros pueden ser
            # inesperados (p.ej. problemas con la DB). Presentamos el mensaje
            # completo en el diálogo para que el usuario pueda copiarlo.
            if isinstance(exc, ValueError):
                messagebox.showerror(
                    "❌ Error",
                    "Ocurrió un problema con los datos ingresados. Revisa autor y tipo de cocina."
                )
            else:
                messagebox.showerror(
                    "❌ Error",
                    f"Ocurrió un error al guardar la receta:\n{exc}"
                )
    
    def _guardar_ingredientes(self, receta_id):
        """Guarda los ingredientes agregados a la receta"""
        errores = []
        for item in self.tree_ingredientes.get_children():
            try:
                valores = self.tree_ingredientes.item(item)['values']
                tags = self.tree_ingredientes.item(item)['tags']
                
                # extraer ingredient_id del tag, siendo defensivo
                ingrediente_id = None
                if tags and len(tags) > 0:
                    try:
                        ingrediente_id = int(tags[0])
                    except (ValueError, TypeError) as e:
                        print(f"Error extrayendo ID de tag {tags}: {e}")
                        errores.append(f"Error procesando ID de ingrediente: {e}")
                        continue
                
                if not ingrediente_id:
                    errores.append("Ingrediente sin ID válido")
                    continue
                
                # convertir a texto siempre para evitar errores de tipos (Decimal, int, etc.)
                cantidad = str(valores[1]) if len(valores) > 1 and valores[1] is not None else ''
                unidad = str(valores[2]) if len(valores) > 2 and valores[2] is not None else ''
                
                # debuging: print what we're about to save
                print(f"Guardando: receta={receta_id}, ingrediente_id={ingrediente_id}, cantidad={cantidad}, unidad={unidad}")
                
                result = RecipeIngredientController.add_ingredient_to_recipe(receta_id, ingrediente_id, cantidad, unidad, "")
                if result is None:
                    errores.append(f"No se pudo guardar ingrediente ID {ingrediente_id}")
                else:
                    print(f"Ingrediente {ingrediente_id} guardado exitosamente (ID:{result})")
            except Exception as exc:
                print(f"Error procesando ingrediente: {exc}")
                import traceback
                traceback.print_exc()
                errores.append(str(exc))
        
        if errores:
            msg = "\n".join(errores)
            print(f"Errores al guardar ingredientes: {msg}")
            messagebox.showwarning("Advertencia", f"Algunos ingredientes no se guardaron:\n{msg}")
    
    def _actualizar_ingredientes(self, receta_id):
        """Actualiza los ingredientes de la receta (elimina actuales y agrega nuevos)"""
        try:
            ingredientes_actuales = RecipeIngredientController.get_ingredients_for_recipe(receta_id)
            
            for ing in ingredientes_actuales:
                try:
                    RecipeIngredientController.remove_ingredient_from_recipe(receta_id, ing['id'])
                except Exception as exc:
                    print(f"Error eliminando ingrediente {ing['id']}: {exc}")
            
            self._guardar_ingredientes(receta_id)
        except Exception as exc:
            print(f"Error en _actualizar_ingredientes: {exc}")
            messagebox.showerror("Error", f"Error al actualizar ingredientes: {exc}")
                
                

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
        receta = RecipeController.get_recipe_by_id(self.receta_id)
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
        autor = AuthorController.get_author_by_id(receta['author_id']) if receta['author_id'] else None
        cuisine = CuisineController.get_cuisine_by_id(receta['cuisine_id']) if receta['cuisine_id'] else None
        
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
        
        # Cargar ingredientes de la tabla pivote
        ingredientes = RecipeIngredientController.get_ingredients_for_recipe(self.receta_id)
        if ingredientes:
            for ing in ingredientes:
                ing_text = f"• {ing['name']}"
                if ing.get('quantity'):
                    ing_text += f" ({ing['quantity']}"
                    if ing.get('unit'):
                        ing_text += f" {ing['unit']}"
                    ing_text += ")"
                tk.Label(ing_frame, text=ing_text, font=('Arial', 11), bg='#FFF9C4', justify=tk.LEFT).pack(anchor='w', padx=15, pady=3)
        else:
            tk.Label(ing_frame, text="Sin ingredientes especificados", font=('Arial', 10, 'italic'), bg='#FFF9C4').pack(padx=15, pady=10)
        
        # Preparación
        if receta['preparation']:
            tk.Label(frame, text="👨‍🍳 Instrucciones de Preparación:", font=('Arial', 13, 'bold'), bg='white', fg='#2E7D32').pack(anchor='w', pady=(20, 5))
            prep_frame = tk.Frame(frame, bg='#FAFAFA', relief=tk.SOLID, borderwidth=1)
            prep_frame.pack(fill=tk.X, pady=5)
            tk.Label(prep_frame, text=receta['preparation'], font=('Arial', 11), bg='#FAFAFA', wraplength=600, justify=tk.LEFT).pack(padx=15, pady=10)

