# 📝 Comandos Útiles - Sistema de Onboarding Rivcon

## 🚀 Comandos de Inicio Rápido

### 1. Configuración Inicial (IMPORTANTE)

```bash
# Crear las migraciones
python manage.py makemigrations

# Aplicar las migraciones a la base de datos
python manage.py migrate

# Configurar grupos y permisos automáticamente
python manage.py setup_groups

# Crear un superusuario (administrador)
python manage.py createsuperuser

# Ejecutar el servidor de desarrollo
python manage.py runserver
```

**¡Listo!** Accede a http://127.0.0.1:8000/

⚠️ **Nota:** Al acceder serás redirigido automáticamente a `/login/`. Usa las credenciales del superusuario que creaste.

---

## 🔧 Comandos de Gestión

### Migraciones

```bash
# Ver el SQL que se ejecutará en las migraciones
python manage.py sqlmigrate gestor 0001

# Ver las migraciones aplicadas
python manage.py showmigrations

# Revertir migraciones (cuidado en producción)
python manage.py migrate gestor 0001  # Volver a una migración específica
python manage.py migrate gestor zero  # Revertir todas las migraciones de la app
```

### Base de Datos

```bash
# Abrir shell de Django (para ejecutar código Python)
python manage.py shell

# Vaciar la base de datos (CUIDADO: elimina todos los datos)
python manage.py flush

# Crear datos de prueba (desde el shell)
python manage.py shell
>>> from gestor.models import Departamento
>>> Departamento.objects.create(nombre='IT', descripcion='Tecnología')
>>> exit()
```

### Usuarios y Permisos

```bash
# Cambiar contraseña de un usuario
python manage.py changepassword nombre_usuario

# Crear un usuario desde shell
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('empleado1', 'empleado1@rivcon.com', 'password123')
>>> user.first_name = 'Juan'
>>> user.last_name = 'Pérez'
>>> user.save()
>>> exit()

# Asignar un usuario a un grupo
python manage.py shell
>>> from django.contrib.auth.models import User, Group
>>> user = User.objects.get(username='empleado1')
>>> grupo = Group.objects.get(name='RRHH')
>>> user.groups.add(grupo)
>>> exit()
```

---

## 🗂️ Comandos del Modelo

### Desde el Shell de Django

```bash
python manage.py shell
```

#### Crear Departamento
```python
from gestor.models import Departamento

dept_it = Departamento.objects.create(
    nombre='Tecnología',
    descripcion='Departamento de IT'
)
```

#### Crear Puesto
```python
from gestor.models import Departamento, Puesto

dept = Departamento.objects.get(nombre='Tecnología')
puesto = Puesto.objects.create(
    titulo='Desarrollador Backend',
    departamento=dept,
    nivel='senior',
    descripcion='Desarrollo de aplicaciones web',
    salario_minimo=50000,
    salario_maximo=80000
)
```

#### Crear Empleado
```python
from django.contrib.auth.models import User
from gestor.models import Empleado, Puesto
from datetime import date

# Crear usuario
user = User.objects.create_user(
    username='jperez',
    email='jperez@rivcon.com',
    first_name='Juan',
    last_name='Pérez',
    password='temporal123'
)

# Crear empleado
puesto = Puesto.objects.first()
empleado = Empleado.objects.create(
    usuario=user,
    cedula='001-1234567-8',
    telefono='809-555-1234',
    fecha_nacimiento=date(1990, 5, 15),
    puesto=puesto,
    fecha_ingreso=date.today(),
    estado='pre_ingreso'
)
```

#### Ver Tareas de un Empleado
```python
from gestor.models import Empleado

empleado = Empleado.objects.first()
tareas = empleado.tareas.all()

for tarea in tareas:
    print(f"{tarea.titulo} - {tarea.get_estado_display()}")
```

---

## 📊 Comandos de Consulta

```bash
python manage.py shell
```

```python
from gestor.models import *

# Contar registros
print(f"Empleados: {Empleado.objects.count()}")
print(f"Tareas: {TareaOnboarding.objects.count()}")
print(f"Documentos: {Documento.objects.count()}")

# Empleados por estado
for estado, _ in Empleado.ESTADO_CHOICES:
    count = Empleado.objects.filter(estado=estado).count()
    print(f"{estado}: {count}")

# Tareas pendientes
pendientes = TareaOnboarding.objects.filter(
    estado__in=['pendiente', 'en_progreso']
).count()
print(f"Tareas pendientes: {pendientes}")

# Documentos sin aprobar
sin_aprobar = Documento.objects.filter(
    estado__in=['pendiente', 'en_revision']
).count()
print(f"Documentos sin aprobar: {sin_aprobar}")
```

---

## 🧪 Comandos de Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de una app específica
python manage.py test gestor

# Ejecutar tests con verbosidad
python manage.py test --verbosity=2

# Ejecutar un test específico
python manage.py test gestor.tests.TestEmpleadoModel
```

---

## 🔍 Comandos de Depuración

```bash
# Ver todas las URLs configuradas
python manage.py show_urls  # Requiere django-extensions

# Verificar la configuración
python manage.py check

# Verificar problemas con migraciones
python manage.py makemigrations --check --dry-run

# Ver la configuración actual
python manage.py diffsettings
```

---

## 📦 Comandos de Producción

```bash
# Recolectar archivos estáticos
python manage.py collectstatic

# Comprimir archivos estáticos (requiere django-compressor)
python manage.py compress

# Limpiar sesiones expiradas
python manage.py clearsessions

# Crear un backup de la base de datos (SQLite)
# En Windows:
copy db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3

# En Linux/Mac:
cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3
```

---

## 🎨 Comandos Personalizados

### Re-ejecutar setup_groups (si necesitas resetear permisos)

```bash
python manage.py setup_groups
```

---

## 💡 Tips Útiles

### Crear varios departamentos de una vez

```python
python manage.py shell

from gestor.models import Departamento

departamentos = [
    {'nombre': 'Recursos Humanos', 'descripcion': 'Gestión de personal'},
    {'nombre': 'Tecnología', 'descripcion': 'Desarrollo y soporte IT'},
    {'nombre': 'Finanzas', 'descripcion': 'Contabilidad y finanzas'},
    {'nombre': 'Ventas', 'descripcion': 'Equipo comercial'},
    {'nombre': 'Marketing', 'descripcion': 'Publicidad y marketing'},
]

for dept_data in departamentos:
    Departamento.objects.get_or_create(**dept_data)

print("Departamentos creados!")
```

### Actualizar progreso de todos los empleados

```python
python manage.py shell

from gestor.models import Empleado

for empleado in Empleado.objects.all():
    empleado.actualizar_progreso()
    print(f"{empleado.usuario.get_full_name()}: {empleado.progreso}%")
```

### Listar usuarios sin grupo asignado

```python
python manage.py shell

from django.contrib.auth.models import User

usuarios_sin_grupo = User.objects.filter(groups__isnull=True)
for user in usuarios_sin_grupo:
    print(f"{user.username} - {user.email}")
```

---

## 🆘 Solución de Problemas Comunes

### Error: "Table doesn't exist"
```bash
python manage.py migrate
```

### Error: "No module named 'gestor'"
```bash
# Verifica que 'gestor' esté en INSTALLED_APPS en settings.py
# Verifica que estés en el directorio correcto
```

### Los archivos media no se sirven
```bash
# Verifica que en settings.py tengas:
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# Y en urls.py (solo en desarrollo):
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Resetear la base de datos completamente
```bash
# CUIDADO: Esto elimina TODOS los datos
rm db.sqlite3
rm -rf gestor/migrations/*.py  # Excepto __init__.py
# Mantén el __init__.py

python manage.py makemigrations
python manage.py migrate
python manage.py setup_groups
python manage.py createsuperuser
```

---

¿Necesitas más ayuda? Consulta el README.md o la documentación de Django.

