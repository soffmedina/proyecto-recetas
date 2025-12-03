import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from models.author import eliminar_author, obtener_author, obtener_author_por_id
from models.cuisines import obtener_cuisines_por_id
from models.ingredients import actualizar_ingrediente, agregar_ingrediente, obtener_ingrediente_por_id
from models.recipes import obtener_receta_por_autor


class VentanaAutores(tk.Toplevel):
    """Gestión de autores"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.crear_interfaz()
        self.cargar_autores()
    
    def crear_interfaz(self):
        #Header
        header = tk.Frame(self.parent, bg=self.main_window.COLOR_SECUNDARIO, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="👨‍🍳 Gestión de Autores", font=('Arial', 16, 'bold'), bg=self.main_window.COLOR_SECUNDARIO, fg='white').pack(side=tk.LEFT, padx=30, pady=15)
        tk.Button(header, text="➕ Nuevo Autor", command=self.abrir_formulario_nuevo, bg=self.main_window.COLOR_PRIMARIO, fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8, cursor='hand2', bd=0).pack(side=tk.RIGHT, padx=30)
        
        #frame principal
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        #treeview
        tree_frame = tk.Frame(main_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('ID', 'Nombre', 'Email', 'Biografía')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        #Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Biografía', text='Biografía')
        
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Nombre', width=250)
        self.tree.column('Email', width=300)
        self.tree.column('Biografía', width=400)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        #Botones de accion
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=15, padx=10)
        
        tk.Button(btn_frame, text="👁️ Ver Detalles", command=self.ver_detalles, bg=self.main_window.COLOR_AZUL, fg='white', font=('Arial', 10), padx=15, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Editar", command=self.editar_autor, bg=self.main_window.COLOR_NARANJA, fg='white', font=('Arial', 10), padx=15, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar_autor, bg=self.main_window.COLOR_ROJO, fg='white', font=('Arial', 10), padx=15, pady=8, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
    
    def cargar_autores(self):
        """Carga autores"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        autores = obtener_author()
        for a in autores:
            bio = a['biography'][:50] + '...' if a['biography'] and len(a['biography']) > 50 else (a['biography'] or '')
            self.tree.insert('', tk.END, values=(a['id'], a['name'], a['email'], bio))
    
    def abrir_formulario_nuevo(self):
        """Abre formulario nuevo"""
        VentanaFormularioAutor(self.main_window, self, modo='nuevo')
    
    def ver_detalles(self):
        """Ver detalles de la receta seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una receta")
            return
        
        item = self.tree.item(seleccion[0])
        receta_id = item['values'][0]
        VentanaDetallesAutor(self.main_window, receta_id)
    
    def editar_autor(self):
        """Editar autor"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un autor")
            return
        item = self.tree.item(seleccion[0])
        autor_id = item['values'][0]
        VentanaFormularioAutor(self.main_window, self, modo='editar', autor_id=autor_id)
    
    def eliminar_autor(self):
        """Eliminar autor"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un autor")
            return
        item = self.tree.item(seleccion[0])
        autor_id = item['values'][0]
        autor_nombre = item['values'][1]
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar '{autor_nombre}'?")
        if confirmar:
            if eliminar_author(autor_id):
                messagebox.showinfo("Éxito", "Autor eliminado")
                self.cargar_autores()

            
            
# ==================== VENTANA DETALLES AUTOR ====================

class VentanaDetallesAutor:
    """Muestra los detalles completos de un autor"""
    
    def __init__(self, parent, autor_id):
        self.autor_id = autor_id
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("👨‍🍳 Detalles del Autor")
        self.ventana.geometry("800x750")
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
        """Carga y muestra los detalles del autor"""
        autor = obtener_author_por_id(self.autor_id)
        if not autor:
            messagebox.showerror("Error", "No se pudo cargar el autor")
            self.ventana.destroy()
            return
        
        frame = self.scrollable_frame
        
        # Header con foto de perfil (simulada)
        header_frame = tk.Frame(frame, bg='#FF9800', relief=tk.RAISED, borderwidth=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Avatar (círculo simulado con emoji)
        avatar_frame = tk.Frame(header_frame, bg='#FF9800')
        avatar_frame.pack(pady=20)
        
        tk.Label(avatar_frame,
                text="👨‍🍳",
                font=('Arial', 60),
                bg='#FF9800').pack()
        
        # Nombre del autor
        tk.Label(header_frame,
                text=autor['name'].upper(),
                font=('Arial', 24, 'bold'),
                bg='#FF9800',
                fg='white').pack(pady=(0, 10))
        
        tk.Label(header_frame,
                text=f"📧 {autor['email']}",
                font=('Arial', 12),
                bg='#FF9800',
                fg='white').pack(pady=(0, 20))
        
        # Información básica
        info_frame = tk.Frame(frame, bg='#FFF3E0', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(info_frame,
                text="📋 Información Básica",
                font=('Arial', 14, 'bold'),
                bg='#FFF3E0',
                fg='#E65100').pack(anchor='w', padx=15, pady=(10, 5))
        
        info_data = [
            ("🆔 ID:", str(autor['id'])),
            ("📅 Fecha de Registro:", str(autor['created_at'])[:19]),
            ("🔗 Avatar URL:", autor['avatar_url'] if autor['avatar_url'] else 'No configurado')
        ]
        
        for label, value in info_data:
            row = tk.Frame(info_frame, bg='#FFF3E0')
            row.pack(fill=tk.X, padx=20, pady=8)
            tk.Label(row, text=label, font=('Arial', 11, 'bold'), bg='#FFF3E0').pack(side=tk.LEFT)
            tk.Label(row, text=value, font=('Arial', 11), bg='#FFF3E0').pack(side=tk.LEFT, padx=10)
        
        # Biografía
        if autor['biography']:
            tk.Label(frame,
                    text="📖 Biografía",
                    font=('Arial', 14, 'bold'),
                    bg='white',
                    fg='#E65100').pack(anchor='w', pady=(20, 5))
            
            bio_frame = tk.Frame(frame, bg='#FAFAFA', relief=tk.SOLID, borderwidth=1)
            bio_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(bio_frame,
                    text=autor['biography'],
                    font=('Arial', 11),
                    bg='#FAFAFA',
                    wraplength=700,
                    justify=tk.LEFT).pack(padx=15, pady=15)
        else:
            tk.Label(frame,
                    text="📖 Biografía",
                    font=('Arial', 14, 'bold'),
                    bg='white',
                    fg='#E65100').pack(anchor='w', pady=(20, 5))
            
            tk.Label(frame,
                    text="Este autor no tiene biografía registrada.",
                    font=('Arial', 11, 'italic'),
                    bg='white',
                    fg='#757575').pack(anchor='w', pady=5)
        
        # Recetas del autor
        tk.Label(frame,
                text="📚 Recetas de este Autor",
                font=('Arial', 14, 'bold'),
                bg='white',
                fg='#E65100').pack(anchor='w', pady=(20, 10))
        
        recetas_frame = tk.Frame(frame, bg='white')
        recetas_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Obtener recetas del autor
        recetas = obtener_receta_por_autor(self.autor_id)
        
        if recetas:
            # Crear mini-tabla de recetas
            recetas_container = tk.Frame(recetas_frame, bg='#E3F2FD', relief=tk.SOLID, borderwidth=1)
            recetas_container.pack(fill=tk.BOTH, expand=True)
            
            # Header de la tabla
            header_recetas = tk.Frame(recetas_container, bg='#2196F3')
            header_recetas.pack(fill=tk.X)
            
            tk.Label(header_recetas, text="Título", font=('Arial', 11, 'bold'), bg='#2196F3', fg='white', width=40, anchor='w').pack(side=tk.LEFT, padx=10, pady=8)
            tk.Label(header_recetas, text="Fecha", font=('Arial', 11, 'bold'), bg='#2196F3', fg='white', width=20, anchor='w').pack(side=tk.LEFT, padx=10, pady=8)
            
            # Lista de recetas
            for receta in recetas[:10]:  # Mostrar máximo 10 recetas
                receta_row = tk.Frame(recetas_container, bg='white', relief=tk.SOLID, borderwidth=1)
                receta_row.pack(fill=tk.X, pady=1)
                
                tk.Label(receta_row, text=f"🍽️ {receta['title']}", font=('Arial', 10), bg='white', width=40, anchor='w').pack(side=tk.LEFT, padx=10, pady=8)
                tk.Label(receta_row, text=str(receta['created_at'])[:10], font=('Arial', 10), bg='white', width=20, anchor='w').pack(side=tk.LEFT, padx=10, pady=8)
            
            # Total de recetas
            tk.Label(recetas_container,
                    text=f"📊 Total de recetas: {len(recetas)}",
                    font=('Arial', 11, 'bold'),
                    bg='#E3F2FD',
                    fg='#1565C0').pack(anchor='w', padx=15, pady=10)
        else:
            tk.Label(recetas_frame,
                    text="Este autor aún no tiene recetas registradas.",
                    font=('Arial', 11, 'italic'),
                    bg='white',
                    fg='#757575').pack(pady=10)
        
        # Estadísticas adicionales
        stats_frame = tk.Frame(frame, bg='#E8F5E9', relief=tk.SOLID, borderwidth=1)
        stats_frame.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(stats_frame,
                text="📊 Estadísticas",
                font=('Arial', 14, 'bold'),
                bg='#E8F5E9',
                fg='#2E7D32').pack(anchor='w', padx=15, pady=(10, 5))
        
        # Calcular estadísticas
        total_recetas = len(recetas)
        
        # Obtener tipos de cocina únicos en las recetas del autor
        cuisines_autor = set()
        for receta in recetas:
            if receta['cuisine_id']:
                cuisine = obtener_cuisines_por_id(receta['cuisine_id'])
                if cuisine:
                    cuisines_autor.add(cuisine['name'])
        
        stats_data = [
            ("📖 Total de recetas publicadas:", str(total_recetas)),
            ("🌎 Tipos de cocina que domina:", str(len(cuisines_autor)) if cuisines_autor else "0"),
            ("🏆 Estado:", "Autor Activo" if total_recetas > 0 else "Sin recetas")
        ]
        
        for label, value in stats_data:
            row = tk.Frame(stats_frame, bg='#E8F5E9')
            row.pack(fill=tk.X, padx=20, pady=8)
            tk.Label(row, text=label, font=('Arial', 11, 'bold'), bg='#E8F5E9').pack(side=tk.LEFT)
            tk.Label(row, text=value, font=('Arial', 11), bg='#E8F5E9', fg='#2E7D32').pack(side=tk.LEFT, padx=10)
        
        # Lista de tipos de cocina
        if cuisines_autor:
            tk.Label(stats_frame,
                    text="Especialidades:",
                    font=('Arial', 10, 'bold'),
                    bg='#E8F5E9').pack(anchor='w', padx=20, pady=(5, 0))
            
            cuisines_text = ", ".join(cuisines_autor)
            tk.Label(stats_frame,
                    text=cuisines_text,
                    font=('Arial', 10),
                    bg='#E8F5E9',
                    fg='#4CAF50',
                    wraplength=700,
                    justify=tk.LEFT).pack(anchor='w', padx=20, pady=(0, 10))
        
        # Botones de acción
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame,
                 text="📖 Ver todas sus recetas",
                 command=lambda: self.ver_recetas_autor(recetas),
                 bg='#2196F3',
                 fg='white',
                 font=('Arial', 11, 'bold'),
                 padx=20,
                 pady=10,
                 cursor='hand2',
                 bd=0).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame,
                 text="❌ Cerrar",
                 command=self.ventana.destroy,
                 bg='#757575',
                 fg='white',
                 font=('Arial', 11),
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 bd=0).pack(side=tk.LEFT, padx=5)
    
    def ver_recetas_autor(self, recetas):
        """Muestra una ventana con todas las recetas del autor"""
        if not recetas:
            messagebox.showinfo("Información", "Este autor no tiene recetas")
            return
        
        VentanaListaRecetasAutor(self.ventana, recetas)


# ==================== VENTANA LISTA RECETAS DE AUTOR ====================

class VentanaListaRecetasAutor:
    """Muestra todas las recetas de un autor específico"""
    
    def __init__(self, parent, recetas):
        self.recetas = recetas
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"📖 Recetas del Autor ({len(recetas)} total)")
        self.ventana.geometry("900x600")
        self.ventana.resizable(False, False)
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz"""
        # Header
        header = tk.Frame(self.ventana, bg='#2196F3', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header,
                text=f"📚 Todas las Recetas ({len(self.recetas)})",
                font=('Arial', 16, 'bold'),
                bg='#2196F3',
                fg='white').pack(side=tk.LEFT, padx=30, pady=15)
        
        # Frame principal
        main_frame = tk.Frame(self.ventana, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        tree_frame = tk.Frame(main_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('ID', 'Título', 'Descripción', 'Fecha')
        tree = ttk.Treeview(tree_frame,
                           columns=columns,
                           show='headings',
                           yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Título', text='Título')
        tree.heading('Descripción', text='Descripción')
        tree.heading('Fecha', text='Fecha Creación')
        
        tree.column('ID', width=50, anchor=tk.CENTER)
        tree.column('Título', width=300)
        tree.column('Descripción', width=400)
        tree.column('Fecha', width=120, anchor=tk.CENTER)
        
        # Insertar recetas
        for receta in self.recetas:
            desc = receta['description'][:50] + '...' if receta['description'] and len(receta['description']) > 50 else (receta['description'] or '')
            tree.insert('', tk.END, values=(
                receta['id'],
                receta['title'],
                desc,
                str(receta['created_at'])[:10]
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Botón cerrar
        tk.Button(main_frame,
                 text="❌ Cerrar",
                 command=self.ventana.destroy,
                 bg='#757575',
                 fg='white',
                 font=('Arial', 11),
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 bd=0).pack(pady=15)


# ==================== FORMULARIO AUTOR ====================

class VentanaFormularioAutor:
    """Formulario autor"""
    
    def __init__(self, parent, ventana_autores, modo='nuevo', autor_id=None):
        self.ventana_autores = ventana_autores
        self.modo = modo
        self.autor_id = autor_id
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Nuevo Autor" if modo == 'nuevo' else "Editar Autor")
        self.ventana.geometry("550x500")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        
        self.crear_interfaz()
        if modo == 'editar' and autor_id:
            self.cargar_datos()
    
    def crear_interfaz(self):
        """Crea formulario"""
        frame = tk.Frame(self.ventana, bg='white', padx=30, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo_texto = "Crear Nuevo Autor" if self.modo == 'nuevo' else "Editar Receta"
        tk.Label(frame, text=titulo_texto, font=('Arial', 18, 'bold'), bg='white', fg='#2E7D32').pack(pady=(0, 20))
        
        # Formulario con scroll
        canvas = tk.Canvas(frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Campos del formulario
        form = scrollable_frame
        
        # Nombre
        tk.Label(form, text="Nombre:*", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        self.entry_titulo = ttk.Entry(form, font=('Arial', 11), width=60)
        self.entry_titulo.pack(fill=tk.X, pady=(0, 10))
        
        # Email
        tk.Label(form, text="Email:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        self.text_descripcion = tk.Text(form, height=4, font=('Arial', 10), wrap=tk.WORD)
        self.text_descripcion.pack(fill=tk.X, pady=(0, 10))
        
        #Avatar URL
        tk.Label(form, text="URL del Avatar:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        self.entry_avatar_url = ttk.Entry(form, font=('Arial', 11), width=60)
        self.entry_avatar_url.pack(fill=tk.X, pady=(0, 10))
        
        
        # Biografia
        tk.Label(form, text="Biografia:*", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(10, 5))
        self.text_preparacion = scrolledtext.ScrolledText(form, height=8, font=('Arial', 10), wrap=tk.WORD)
        self.text_preparacion.pack(fill=tk.X, pady=(0, 10))
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="💾 Guardar", command=self.guardar, bg='#2E7D32', fg='white', font=('Arial', 11, 'bold'), padx=20, pady=10, cursor='hand2', bd=0).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.ventana.destroy, bg='#757575', fg='white', font=('Arial', 11), padx=20, pady=10, cursor='hand2', bd=0).pack(side=tk.LEFT)
    
    def cargar_datos(self):
        """Carga datos para editar"""
        ingrediente = obtener_ingrediente_por_id(self.ingrediente_id)
        if ingrediente:
            self.entry_nombre.insert(0, ingrediente['name'])
    
    def guardar(self):
        """Guarda o actualiza ingrediente"""
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return
        
        if self.modo == 'nuevo':
            if agregar_ingrediente(nombre):
                messagebox.showinfo("Éxito", "Ingrediente creado")
                self.ventana_ingredientes.cargar_ingredientes()
                self.ventana.destroy()
        else:
            actualizar_ingrediente(self.ingrediente_id, nombre)
            messagebox.showinfo("Éxito", "Ingrediente actualizado")
            self.ventana_ingredientes.cargar_ingredientes()
            self.ventana.destroy()

