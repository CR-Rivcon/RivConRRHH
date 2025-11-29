# 🏢 Sistema de Onboarding de RRHH - Rivcon

Sistema completo de gestión de onboarding para Recursos Humanos construido con Django 5.x, Tailwind CSS y Alpine.js.

## 🚀 Características

### ✨ Funcionalidades Principales

- **Dashboard Interactivo**: KPIs en tiempo real, gráficos y estadísticas
- **Gestión de Empleados**: Alta, edición y seguimiento del proceso de onboarding
- **Vista Kanban**: Visualización del estado de onboarding (Pre-ingreso, En Proceso, Completado)
- **Sistema de Tareas**: Tareas automáticas generadas al crear un empleado
- **Gestión Documental**: Subida, revisión y aprobación de documentos
- **Sistema de Permisos**: Grupos predefinidos (RRHH, Supervisores, Empleados, IT)
- **Notificaciones por Email**: Emails de bienvenida con credenciales temporales
- **Interfaz Moderna**: UI/UX profesional con Tailwind CSS

### 🎯 Modelos Implementados

- **Departamento**: Gestión de departamentos de la empresa
- **Puesto**: Puestos de trabajo con niveles y rangos salariales
- **Empleado**: Perfil completo del empleado con seguimiento de progreso
- **Documento**: Sistema de gestión documental con estados de aprobación
- **TareaOnboarding**: Tareas automatizadas y manuales del proceso

### 🔐 Sistema de Permisos

#### RRHH
- Permisos totales sobre empleados, documentos y tareas
- Puede aprobar/rechazar documentos
- Acceso al dashboard completo

#### Supervisores
- Ver y editar tareas de subordinados
- Ver información de empleados
- Acceso limitado al dashboard

#### Empleados
- Ver su propio perfil y tareas
- Subir sus documentos personales
- Sin acceso administrativo

#### IT
- Ver empleados y documentos
- Gestionar tareas asignadas a IT
- Configuración de accesos técnicos

## 📋 Requisitos

- Python 3.10+
- Django 5.2.8
- SQLite (por defecto) o PostgreSQL

## 🛠️ Instalación

### 1. Clonar o verificar el proyecto

```bash
cd RivconRRHH
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Django

```bash
pip install django
```

### 4. Realizar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Configurar grupos y permisos

```bash
python manage.py setup_groups
```

Este comando creará automáticamente los grupos de usuarios con sus permisos correspondientes.

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu cuenta de administrador.

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

### 8. Acceder al sistema

1. Abre tu navegador en: **http://127.0.0.1:8000/**
2. Serás redirigido automáticamente a la página de login
3. Ingresa las credenciales del superusuario que creaste
4. ¡Listo! Accederás al dashboard principal

**URLs importantes:**
- **Login:** http://127.0.0.1:8000/login/
- **Dashboard:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

## 📁 Estructura del Proyecto

```
RivconRRHH/
├── gestor/                          # App principal
│   ├── management/
│   │   └── commands/
│   │       └── setup_groups.py      # Comando de configuración
│   ├── migrations/
│   ├── templates/
│   │   └── gestor/
│   │       ├── base.html            # Template base
│   │       ├── dashboard.html       # Dashboard principal
│   │       ├── empleado_*.html      # Templates de empleados
│   │       ├── documento_*.html     # Templates de documentos
│   │       ├── tarea_*.html         # Templates de tareas
│   │       └── ...
│   ├── admin.py                     # Configuración del admin
│   ├── forms.py                     # Formularios
│   ├── models.py                    # Modelos de datos
│   ├── urls.py                      # URLs de la app
│   └── views.py                     # Vistas (CBV)
├── RivconRRHH/
│   ├── settings.py                  # Configuración
│   └── urls.py                      # URLs del proyecto
├── media/                           # Archivos subidos
├── static/                          # Archivos estáticos
├── db.sqlite3                       # Base de datos
└── manage.py
```

## 🎨 Tecnologías Utilizadas

### Backend
- **Django 5.2.8**: Framework web
- **Python 3.x**: Lenguaje de programación
- **SQLite**: Base de datos (desarrollo)

### Frontend
- **Tailwind CSS 3.x**: Framework CSS (CDN)
- **Alpine.js 3.x**: Framework JS ligero
- **Font Awesome 6.x**: Iconos

## 📚 Uso del Sistema

### Crear un Nuevo Empleado

1. Accede al dashboard principal
2. Click en "Nuevo Empleado"
3. Completa el formulario con datos personales y laborales
4. Al guardar:
   - Se crea el usuario automáticamente
   - Se generan 10 tareas predeterminadas de onboarding
   - Se envía un email de bienvenida (visible en consola durante desarrollo)

### Gestionar Documentos

1. Accede a "Documentos" en el menú
2. Filtra por estado (Pendiente, En Revisión, Aprobado, Rechazado)
3. Click en "Revisar" para aprobar/rechazar
4. Los empleados pueden subir documentos desde su perfil

### Vista Kanban

- Visualiza el estado de todos los empleados
- Arrastra y suelta entre columnas (próximamente)
- Click en una tarjeta para ver detalles

### Panel de Administración

Accede a `/admin/` para:
- Gestión avanzada de todos los modelos
- Acciones en masa (aprobar documentos, completar tareas, etc.)
- Filtros y búsquedas avanzadas
- Asignación de usuarios a grupos

## 🔧 Configuración Adicional

### Cambiar a PostgreSQL

En `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rivcon_rrhh',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Configurar Email Real

En `settings.py`, reemplaza:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña'
DEFAULT_FROM_EMAIL = 'noreply@rivcon.com'
```

### Cambiar Zona Horaria

En `settings.py`:

```python
TIME_ZONE = 'America/Santo_Domingo'  # Ajusta según tu ubicación
```

## 🐛 Solución de Problemas

### Error: "No such table"
```bash
python manage.py migrate
```

### Error: "Permission denied"
```bash
python manage.py setup_groups
```

### Los estilos no cargan
Verifica que Tailwind CSS CDN esté cargando correctamente en `base.html`

## 🤝 Asignar Usuarios a Grupos

### Opción 1: Admin de Django

1. Accede a `/admin/auth/user/`
2. Selecciona un usuario
3. En "Groups", selecciona el grupo apropiado (RRHH, Supervisores, etc.)
4. Guarda

### Opción 2: Código Python

```python
from django.contrib.auth.models import User, Group

user = User.objects.get(username='nombre_usuario')
grupo = Group.objects.get(name='RRHH')
user.groups.add(grupo)
```

## 📊 Características de Automatización

### Signals Implementados

1. **Creación de Empleado**:
   - Genera 10 tareas automáticas de onboarding
   - Envía email de bienvenida con credenciales
   - Establece contraseña temporal segura

2. **Actualización de Tareas**:
   - Actualiza automáticamente el progreso del empleado
   - Registra fecha de inicio al marcar como "En Progreso"
   - Registra usuario y fecha al completar

## 🎓 Datos de Ejemplo

Para poblar el sistema con datos de ejemplo, puedes crear un script o usar el admin:

1. Crea algunos departamentos (IT, Ventas, Finanzas)
2. Crea puestos asociados
3. Crea empleados con el formulario de alta

## 📝 Próximas Mejoras

- [ ] Drag & drop en vista Kanban
- [ ] Notificaciones en tiempo real
- [ ] Reportes y exportación a PDF
- [ ] API REST
- [ ] App móvil
- [ ] Integración con sistemas de nómina
- [ ] Dashboard personalizable

## 📄 Licencia

Este proyecto es de uso interno para Rivcon.

## 👨‍💻 Desarrollado por

Sistema desarrollado para Rivcon - Gestión de Recursos Humanos

---

**¿Necesitas ayuda?** Contacta al equipo de desarrollo o consulta la documentación de Django en https://docs.djangoproject.com/

