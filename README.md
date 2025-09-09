# CECAPTI-PERU - Sistema de Gestión Web

Panel administrativo profesional para la gestión de usuarios, cursos, maquinaria e inscripciones en CECAPTI-PERU.

## Tecnologías principales
- **Python 3.10+**
- **Flask** (Blueprints, Flask-Login, Flask-WTF, SQLAlchemy)
- **MySQL** (o MariaDB)
- **Bootstrap 5** (UI/UX responsivo y moderno)
- **Font Awesome** (iconos)
- **Chart.js** (gráficos de estado)
- **bcrypt** (hash de contraseñas)
- **Jinja2** (plantillas)
- **Git** (control de versiones)

## Estructura principal
- `app/` - Código fuente Flask
  - `main/` - Blueprints, rutas y formularios
  - `models.py` - Modelos SQLAlchemy
  - `templates/` - Plantillas HTML (admin, login, dashboards, CRUD)
  - `static/` - Archivos estáticos (CSS, imágenes, JS)
- `run.py` - Script de arranque

## Instalación y ejecución
1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/Palaciosjc/sistemacecapti_web.git
   cd sistemacecapti_web/app
   ```
2. **Crea un entorno virtual y actívalo:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   # source venv/bin/activate  # En Linux/Mac
   ```
3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configura la base de datos:**
   - Crea una base de datos MySQL y ajusta la cadena de conexión en `app/__init__.py` o en tu archivo de configuración.
   - Ejecuta las migraciones si usas Flask-Migrate, o crea las tablas manualmente según los modelos.
5. **Ejecuta la aplicación:**
   ```bash
   python run.py
   ```
   Accede a [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Funcionalidades principales
- Dashboard con KPIs y gráfico de maquinaria
- CRUD completo de Usuarios, Cursos, Maquinaria e Inscripciones
- Exportación a CSV en cada módulo
- Login seguro y gestión de roles (administrador, instructor, alumno)
- UI/UX profesional, responsiva y corporativa

## Personalización
- Cambia el logo en `app/static/img/logocecapti.jpg`
- Ajusta colores en `app/static/css/style.css`

## Colaboración
- Haz fork, crea ramas y pull requests para contribuir.
- Usa issues para reportar bugs o sugerir mejoras.

---

**Desarrollado por el equipo CECAPTI-PERU.**
