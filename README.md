# 🍳 Gestor de Recetas de Cocina

Un sistema completo de gestión de recetas culinarias desarrollado en Python con interfaz gráfica Tkinter y base de datos MySQL. Permite gestionar autores, tipos de cocina, ingredientes y recetas de manera intuitiva.

## 📋 Características

### ✨ Funcionalidades Principales
- **👨‍🍳 Gestión de Autores**: Crear, editar y eliminar autores con información detallada
- **📖 Gestión de Recetas**: Crear y gestionar recetas completas con ingredientes y preparaciones
- **🌎 Tipos de Cocina**: Administrar diferentes estilos culinarios
- **🥕 Gestión de Ingredientes**: Mantener un catálogo de ingredientes
- **🔍 Búsqueda Avanzada**: Buscar recetas, autores e ingredientes
- **📊 Dashboard**: Vista general con estadísticas del sistema

### 🛠️ Arquitectura
- **MVC Pattern**: Separación clara entre modelos, vistas y controladores
- **Interfaz Gráfica**: Tkinter con diseño moderno y responsivo
- **Base de Datos**: MySQL con relaciones normalizadas
- **Validaciones**: Sistema robusto de validaciones de datos
- **Hashing Seguro**: Contraseñas encriptadas con bcrypt

## 🚀 Instalación

### Prerrequisitos
- Python 3.8 o superior
- MySQL Server
- pip (gestor de paquetes de Python)

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd proyecto-recetas
```

### 2. Crear entorno virtual (Opcional pero recomendado)
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos
1. Iniciar MySQL Server
2. Crear la base de datos ejecutando el script SQL:
```bash
mysql -u root -p < sql/create_table.sql
```

### 5. Configurar conexión a la base de datos (opcional)
Editar `config/db.py` si es necesario cambiar las credenciales:
```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",          # Cambiar si es necesario
    password="root",      # Cambiar si es necesario
    database="gestion_recetas"
)
```

## 🎯 Uso

### Versión Gráfica (Recomendada)
```bash
python app.py
```

### Versión de Consola
```bash
python main.py
```

## 📁 Estructura del Proyecto

```
proyecto-recetas/
├── app.py                      # Punto de entrada aplicación gráfica
├── main.py                     # Punto de entrada aplicación consola
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
├── config/
│   └── db.py                   # Configuración de base de datos
├── controller/                 # Controladores (lógica de negocio)
│   ├── AuthorController.py
│   ├── CuisineController.py
│   ├── IngredientController.py
│   ├── RecipeController.py
│   └── RecipeIngredientController.py
├── models/                     # Modelos de datos
│   ├── author.py
│   ├── cuisines.py
│   ├── ingredients.py
│   ├── recipes.py
│   └── recipe_ingredients.py
├── sql/
│   └── create_table.sql        # Script de creación de BD
├── ui/                         # Interfaz de usuario
│   ├── main_window.py          # Ventana principal
│   ├── author_window.py        # Gestión de autores
│   ├── cuisines_window.py      # Gestión de tipos de cocina
│   ├── ingredients_window.py   # Gestión de ingredientes
│   └── recipes_window.py       # Gestión de recetas
└── utils/                      # Utilidades
    ├── business_rules.py       # Reglas de negocio
    ├── console.py              # Utilidades de consola
    ├── formatters.py           # Formateadores de texto
    ├── hash.py                 # Encriptación de contraseñas
    └── validators.py           # Validadores de datos
```

## 🗄️ Base de Datos

### Tablas Principales

#### `author`
- Información de los autores de recetas
- Campos: id, name, email, password_hash, avatar_url, biography, created_at

#### `cuisines`
- Tipos de cocina/estilos culinarios
- Campos: id, name, description, country_origin, created_at

#### `ingredients`
- Catálogo de ingredientes
- Campos: id, name, created_at

#### `recipes`
- Recetas principales
- Campos: id, author_id, cuisine_id, title, description, preparation, created_at, updated_at

#### `recipe_ingredients`
- Relación muchos a muchos entre recetas e ingredientes
- Campos: id, recipe_id, ingredient_id, quantity, unit, notes

## 🔧 Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **Tkinter**: Interfaz gráfica nativa
- **MySQL**: Base de datos relacional
- **mysql-connector-python**: Conector de base de datos
- **bcrypt**: Encriptación de contraseñas
- **colorama**: Colores en consola

## 📊 Funcionalidades Detalladas

### 👨‍🍳 Gestión de Autores
- Crear autores con email único
- Contraseñas encriptadas con bcrypt
- Biografía opcional para información adicional
- Validación completa de datos
- Búsqueda por nombre, email o contenido de biografía

### 📖 Gestión de Recetas
- Crear recetas completas con título y preparación
- Asociación opcional con autor y tipo de cocina
- Lista detallada de ingredientes con cantidades y unidades
- Instrucciones de preparación extensas
- Validaciones de campos obligatorios y formatos

### 🌎 Tipos de Cocina
- Crear y gestionar estilos culinarios
- País de origen opcional
- Descripción detallada de cada estilo
- Asociación con múltiples recetas

### 🥕 Ingredientes
- Catálogo centralizado de ingredientes
- Nombres únicos para evitar duplicados
- Asociación múltiple con diferentes recetas
- Cantidades y unidades personalizables por receta

## 🔒 Validaciones y Seguridad

- **Email único** para autores con verificación de formato
- **Contraseñas encriptadas** con algoritmo bcrypt
- **Validación de campos obligatorios** (título, preparación, nombre)
- **Longitud máxima** en textos para optimización de BD
- **Relaciones referenciales** íntegras en base de datos
- **Validación de existencia** de entidades relacionadas

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request


## 👥 Autor

**Sofia Medina**
**Lourdes Figueroa**
**Gonzalo Moreno**
- Proyecto desarrollado como parte de aprendizaje en Python y desarrollo de aplicaciones de escritorio


⭐ Si este proyecto te resulta útil, ¡dale una estrella en GitHub!


## 🔄 Versiones

### v1.0.0
- ✅ Arquitectura MVC completa
- ✅ Interfaz gráfica moderna con Tkinter
- ✅ Base de datos MySQL con relaciones normalizadas
- ✅ Sistema de validaciones robusto
- ✅ Gestión completa de autores, recetas, ingredientes y tipos de cocina
- ✅ Encriptación de contraseñas
- ✅ Búsqueda avanzada
- ✅ Dashboard con estadísticas
