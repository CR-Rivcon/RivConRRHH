# 🚀 Guía para Subir el Proyecto a GitHub

## 📋 Repositorio
**URL:** https://github.com/CR-Rivcon/RivConRRHH.git

---

## 🔧 Pasos para Subir el Proyecto

### 1️⃣ Inicializar Git (si no está inicializado)

```bash
# Inicializar repositorio local
git init

# Configurar tu información (primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```

### 2️⃣ Agregar el Repositorio Remoto

```bash
# Agregar el repositorio remoto de GitHub
git remote add origin https://github.com/CR-Rivcon/RivConRRHH.git

# Verificar que se agregó correctamente
git remote -v
```

### 3️⃣ Preparar los Archivos

```bash
# Ver el estado de los archivos
git status

# Agregar todos los archivos al staging area
git add .

# O agregar archivos específicos
git add README.md
git add gestor/
git add RivconRRHH/
```

### 4️⃣ Hacer el Primer Commit

```bash
# Crear el commit inicial con un mensaje descriptivo
git commit -m "🎉 Commit inicial - Sistema de Onboarding Rivcon RRHH

- Modelos completos (Empleado, Documento, Tarea, Departamento, Puesto)
- Sistema de autenticación con login/logout
- Dashboard con KPIs y estadísticas
- Gestión de empleados con CRUD completo
- Sistema de documentos con aprobación
- Vista Kanban para visualización de estados
- Admin personalizado con filtros y acciones
- Signals para automatización de tareas
- Sistema de permisos con 4 grupos (RRHH, Supervisores, Empleados, IT)
- Templates con Tailwind CSS y Alpine.js
- Documentación completa"
```

### 5️⃣ Subir a GitHub

```bash
# Subir al repositorio remoto (primera vez)
git push -u origin main

# Si la rama principal se llama 'master' en lugar de 'main':
# git push -u origin master
```

**⚠️ Nota:** Si el repositorio está vacío en GitHub, puede que necesites crear la rama principal primero:

```bash
# Renombrar la rama actual a 'main' (si es necesario)
git branch -M main

# Luego hacer push
git push -u origin main
```

---

## 🔐 Autenticación con GitHub

### Opción 1: HTTPS con Token (Recomendado)

1. Ve a GitHub → Settings → Developer settings → Personal access tokens
2. Genera un nuevo token con permisos de 'repo'
3. Usa el token como contraseña cuando hagas `git push`

### Opción 2: SSH

```bash
# Generar clave SSH (si no tienes una)
ssh-keygen -t ed25519 -C "tu.email@ejemplo.com"

# Agregar la clave a tu cuenta de GitHub
# Copia el contenido de ~/.ssh/id_ed25519.pub
cat ~/.ssh/id_ed25519.pub

# Cambia la URL del remoto a SSH
git remote set-url origin git@github.com:CR-Rivcon/RivConRRHH.git
```

---

## 📝 Comandos Git Útiles

### Ver el Estado

```bash
# Ver archivos modificados
git status

# Ver diferencias
git diff

# Ver historial de commits
git log --oneline
```

### Actualizar el Repositorio

```bash
# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Subir cambios
git push
```

### Trabajar con Ramas

```bash
# Crear una nueva rama
git branch feature/nueva-funcionalidad

# Cambiar a esa rama
git checkout feature/nueva-funcionalidad

# O crear y cambiar en un solo comando
git checkout -b feature/nueva-funcionalidad

# Subir la rama a GitHub
git push -u origin feature/nueva-funcionalidad

# Volver a la rama principal
git checkout main
```

### Descargar Cambios

```bash
# Descargar cambios del repositorio remoto
git pull origin main
```

---

## 🚨 Solución de Problemas Comunes

### Error: "failed to push some refs"

```bash
# Descargar cambios primero
git pull origin main --rebase

# Luego intenta push de nuevo
git push origin main
```

### Error: "remote: Permission denied"

- Verifica que tienes permisos de escritura en el repositorio
- Asegúrate de estar autenticado correctamente (token o SSH)

### Quiero deshacer el último commit (sin perder cambios)

```bash
git reset --soft HEAD~1
```

### Quiero eliminar archivos del staging area

```bash
# Quitar todos los archivos
git reset

# Quitar un archivo específico
git reset archivo.py
```

---

## 📂 Archivos que NO se Subirán (gracias al .gitignore)

✅ El `.gitignore` está configurado para excluir:

- ❌ `db.sqlite3` - Base de datos (contiene datos sensibles)
- ❌ `media/` - Archivos subidos por usuarios
- ❌ `__pycache__/` - Archivos compilados de Python
- ❌ `*.pyc` - Archivos compilados
- ❌ `venv/` - Entorno virtual
- ❌ `.env` - Variables de entorno
- ❌ `*.log` - Logs del sistema

---

## 🌟 Buenas Prácticas

### Mensajes de Commit

Usa mensajes descriptivos:

```bash
# ✅ Bien
git commit -m "Agregar validación de cédula en formulario de empleado"
git commit -m "Corregir error en cálculo de progreso"
git commit -m "Actualizar diseño del dashboard con nuevos KPIs"

# ❌ Mal
git commit -m "fix"
git commit -m "cambios"
git commit -m "wip"
```

### Estructura de Commits

```bash
# Tipo: Descripción breve
git commit -m "feat: Agregar exportación de reportes a PDF"
git commit -m "fix: Corregir error en envío de emails"
git commit -m "docs: Actualizar README con instrucciones de instalación"
git commit -m "style: Mejorar diseño del formulario de empleados"
git commit -m "refactor: Optimizar consultas de base de datos"
```

### Tipos comunes:
- `feat` - Nueva funcionalidad
- `fix` - Corrección de bug
- `docs` - Documentación
- `style` - Cambios de estilo/formato
- `refactor` - Refactorización de código
- `test` - Agregar/modificar tests
- `chore` - Tareas de mantenimiento

---

## 🔄 Flujo de Trabajo Recomendado

### Para Desarrollar una Nueva Funcionalidad

```bash
# 1. Actualizar la rama principal
git checkout main
git pull origin main

# 2. Crear una rama para la funcionalidad
git checkout -b feature/nombre-funcionalidad

# 3. Desarrollar y hacer commits
git add .
git commit -m "feat: Agregar nueva funcionalidad"

# 4. Subir la rama
git push -u origin feature/nombre-funcionalidad

# 5. Crear un Pull Request en GitHub

# 6. Una vez aprobado, fusionar a main (desde GitHub)

# 7. Actualizar tu rama local
git checkout main
git pull origin main

# 8. Eliminar la rama local (opcional)
git branch -d feature/nombre-funcionalidad
```

---

## 📊 Verificar el Repositorio

Después de hacer push, verifica en GitHub:

1. Ve a https://github.com/CR-Rivcon/RivConRRHH
2. Deberías ver todos los archivos del proyecto
3. Verifica que aparezca el README.md formateado
4. Revisa que no haya archivos sensibles (db.sqlite3, etc.)

---

## 🎉 ¡Listo!

Tu proyecto está ahora en GitHub y puede ser:
- ✅ Clonado por otros desarrolladores
- ✅ Versionado correctamente
- ✅ Colaborativo (con ramas y pull requests)
- ✅ Respaldado en la nube

---

## 📞 Contacto

Si tienes problemas, consulta:
- [Documentación oficial de Git](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com)
- O pregunta al equipo de desarrollo

---

**Desarrollado para Rivcon - Sistema de Onboarding de RRHH**

