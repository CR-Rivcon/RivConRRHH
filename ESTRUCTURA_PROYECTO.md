# 📂 Estructura del Proyecto - Sistema de Onboarding Rivcon

```
RivconRRHH/
│
├── 📁 RivconRRHH/                    # Configuración del proyecto Django
│   ├── __init__.py
│   ├── __pycache__/
│   ├── asgi.py                       # Configuración ASGI
│   ├── settings.py                   # ⚙️ Configuración principal (App, DB, Email, Media)
│   ├── urls.py                       # 🔗 URLs principales del proyecto
│   └── wsgi.py                       # Configuración WSGI
│
├── 📁 gestor/                        # ⭐ App principal del sistema de onboarding
│   │
│   ├── 📁 management/                # Comandos personalizados
│   │   ├── __init__.py
│   │   └── 📁 commands/
│   │       ├── __init__.py
│   │       └── setup_groups.py       # 🔐 Comando para crear grupos y permisos
│   │
│   ├── 📁 migrations/                # Migraciones de la base de datos
│   │   └── __init__.py
│   │
│   ├── 📁 templates/                 # Templates HTML
│   │   └── 📁 gestor/
│   │       ├── 📁 partials/
│   │       │   └── _sidebar_content.html    # Sidebar del menú
│   │       │
│   │       ├── base.html             # 🎨 Template base (Tailwind + Alpine.js)
│   │       ├── dashboard.html        # 📊 Dashboard principal con KPIs
│   │       ├── kanban.html           # 📋 Vista Kanban
│   │       │
│   │       ├── empleado_list.html    # 👥 Lista de empleados
│   │       ├── empleado_detail.html  # 👤 Detalle de empleado
│   │       ├── empleado_form.html    # ✏️ Formulario de empleado
│   │       ├── empleado_confirm_delete.html
│   │       │
│   │       ├── documento_list.html   # 📄 Lista de documentos
│   │       ├── documento_form.html   # ⬆️ Subir documento
│   │       ├── documento_revisar.html # ✅ Revisar documento
│   │       │
│   │       ├── tarea_list.html       # ✔️ Lista de tareas
│   │       ├── tarea_form.html       # ➕ Crear tarea
│   │       ├── tarea_update.html     # 🔄 Actualizar tarea
│   │       │
│   │       ├── departamento_list.html
│   │       ├── departamento_form.html
│   │       ├── puesto_list.html
│   │       └── puesto_form.html
│   │
│   ├── __init__.py
│   ├── admin.py                      # 🛠️ Configuración del admin con filtros y badges
│   ├── apps.py                       # ⚙️ Configuración de la app (carga signals)
│   ├── forms.py                      # 📝 Formularios de Django
│   ├── models.py                     # 🗄️ Modelos y Signals (automatización)
│   ├── tests.py
│   ├── urls.py                       # 🔗 URLs de la app gestor
│   └── views.py                      # 🎯 Vistas basadas en clases (CBV)
│
├── 📁 media/                         # 📁 Archivos subidos por usuarios
│   └── documentos/                   # Documentos de empleados (PDFs, imágenes, etc.)
│       └── YYYY/MM/                  # Organizados por año/mes
│
├── 📁 static/                        # 📦 Archivos estáticos (CSS, JS, imágenes)
│
├── 📁 terminals/                     # Terminal states (Cursor IDE)
│
├── db.sqlite3                        # 💾 Base de datos SQLite
├── manage.py                         # 🚀 Script de gestión de Django
│
├── .gitignore                        # Git ignore file
├── README.md                         # 📖 Documentación principal
├── COMANDOS_UTILES.md               # 💻 Guía de comandos útiles
└── ESTRUCTURA_PROYECTO.md           # 📂 Este archivo

```

---

## 📋 Modelos de Datos

### 🏢 Departamento
- Nombre
- Descripción
- Fecha de creación

### 💼 Puesto
- Título
- Departamento (FK)
- Nivel (Junior, Semi Senior, Senior, Manager, Director, Ejecutivo)
- Descripción
- Salario mínimo/máximo
- Activo/Inactivo

### 👤 Empleado
**Usuario:**
- Usuario de Django (OneToOne)

**Información Personal:**
- Cédula
- Teléfono, teléfono emergencia
- Fecha de nacimiento
- Dirección
- Tipo de sangre

**Información Laboral:**
- Puesto (FK)
- Fecha de ingreso
- Salario
- Supervisor (FK a User)

**Estado del Onboarding:**
- Estado (Pre-ingreso, En Proceso, Completado, Cancelado)
- Progreso (0-100%)
- Notas internas

### 📄 Documento
- Empleado (FK)
- Tipo (Contrato, Cédula, NDA, Título, etc.)
- Nombre
- Archivo (FileField)
- Estado (Pendiente, En Revisión, Aprobado, Rechazado)
- Obligatorio (boolean)
- Revisado por (User)
- Fecha de revisión
- Comentarios

### ✅ TareaOnboarding
- Empleado (FK)
- Título
- Descripción
- Responsable (RRHH, IT, Supervisor, Finanzas, Empleado, Legal)
- Responsable usuario (FK a User - opcional)
- Fecha límite
- Fecha de inicio
- Fecha completado
- Estado (Pendiente, En Progreso, Completado, Bloqueado, Cancelado)
- Prioridad (Baja, Media, Alta, Urgente)
- Orden
- Es automática
- Notas

---

## 🔄 Signals (Automatización)

### 1. `crear_tareas_automaticas`
**Trigger:** Al crear un nuevo empleado  
**Acción:** Crea 10 tareas predeterminadas de onboarding

**Tareas creadas automáticamente:**
1. Crear cuenta de correo corporativo (IT, 3 días antes)
2. Preparar estación de trabajo (IT, 2 días antes)
3. Crear accesos a sistemas corporativos (IT, 1 día antes)
4. Firmar contrato de trabajo (RRHH, 5 días antes)
5. Firmar acuerdo de confidencialidad (Legal, 5 días antes)
6. Subir documentos personales (Empleado, 7 días antes)
7. Inscripción en sistema de nómina (Finanzas, 3 días antes)
8. Asignación de supervisor y equipo (Supervisor, día de ingreso)
9. Tour por las instalaciones (RRHH, día de ingreso)
10. Capacitación de inducción corporativa (RRHH, día de ingreso)

### 2. `enviar_email_bienvenida`
**Trigger:** Al crear un nuevo empleado  
**Acción:** 
- Genera contraseña temporal segura
- Envía email con credenciales (visible en consola en desarrollo)

### 3. `actualizar_progreso_empleado`
**Trigger:** Al cambiar estado de una tarea  
**Acción:** Recalcula el progreso del empleado (% de tareas completadas)

---

## 🔐 Sistema de Permisos

### Grupos Creados por `setup_groups`

#### 👥 RRHH
**Permisos:**
- ✅ CRUD completo en Empleados
- ✅ CRUD completo en Documentos + Aprobar/Rechazar
- ✅ CRUD completo en Tareas
- ✅ CRUD completo en Departamentos
- ✅ CRUD completo en Puestos
- ✅ Ver dashboard completo

**Uso:** Personal de Recursos Humanos con acceso administrativo total

#### 👔 Supervisores
**Permisos:**
- ✅ Ver empleados
- ✅ Ver y editar tareas de subordinados
- ✅ Ver documentos
- ✅ Ver dashboard

**Uso:** Jefes de departamento que supervisan el onboarding de su equipo

#### 👤 Empleados
**Permisos:**
- ✅ Ver su propio perfil
- ✅ Ver sus tareas
- ✅ Subir y ver sus documentos

**Uso:** Nuevos empleados en proceso de onboarding

#### 💻 IT
**Permisos:**
- ✅ Ver empleados
- ✅ Ver y editar tareas asignadas a IT
- ✅ Ver documentos

**Uso:** Departamento de IT para gestionar accesos y equipos

---

## 🎨 Stack Tecnológico

### Backend
- **Django 5.2.8** - Framework web
- **Python 3.x** - Lenguaje
- **SQLite** - Base de datos (desarrollo)

### Frontend
- **Tailwind CSS 3.x** (CDN) - Framework CSS
- **Alpine.js 3.x** (CDN) - Framework JS ligero
- **Font Awesome 6.x** (CDN) - Iconos

### Características
- Class Based Views (CBV)
- Mixins de permisos
- Signals para automatización
- Django Admin personalizado
- Templates modulares
- Responsive design

---

## 🌊 Flujo de Trabajo

### 1. Alta de Empleado
```
Usuario RRHH → Formulario → Crear Empleado
    ↓
Signal crea 10 tareas automáticas
    ↓
Signal envía email de bienvenida
    ↓
Empleado aparece en dashboard
```

### 2. Proceso de Onboarding
```
Empleado: Pre-ingreso (Progreso: 0%)
    ↓
RRHH/IT/Supervisor completan tareas
    ↓
Empleado sube documentos
    ↓
RRHH aprueba documentos
    ↓
Tareas completadas (Progreso actualiza automáticamente)
    ↓
Empleado: Completado (Progreso: 100%)
```

### 3. Gestión de Documentos
```
Empleado sube documento → Estado: Pendiente
    ↓
RRHH revisa documento
    ↓
Aprobar ✅ / Rechazar ❌ (con comentarios)
    ↓
Empleado notificado (próximamente)
```

---

## 📊 URLs Principales

| URL | Vista | Descripción |
|-----|-------|-------------|
| `/` | Dashboard | Panel principal con KPIs |
| `/empleados/` | Lista | Todos los empleados |
| `/empleados/nuevo/` | Crear | Alta de empleado |
| `/empleados/<id>/` | Detalle | Perfil y progreso |
| `/kanban/` | Kanban | Vista por estados |
| `/documentos/` | Lista | Gestión documental |
| `/tareas/` | Lista | Todas las tareas |
| `/departamentos/` | Lista | Departamentos |
| `/puestos/` | Lista | Puestos |
| `/admin/` | Admin | Panel de administración |

---

## 🎯 Próximas Mejoras Sugeridas

- [ ] API REST con Django REST Framework
- [ ] Notificaciones en tiempo real (Django Channels)
- [ ] Exportación de reportes a PDF
- [ ] Drag & Drop en vista Kanban
- [ ] Panel de analíticas avanzado
- [ ] Integración con sistemas de nómina
- [ ] App móvil (React Native + API)
- [ ] Tests automatizados
- [ ] Traducción i18n
- [ ] Dashboard personalizable por usuario

---

**Desarrollado para Rivcon - Sistema de Onboarding de RRHH**

