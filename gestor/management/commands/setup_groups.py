"""
Comando de Django para configurar grupos y permisos del sistema de onboarding.

Uso:
    python manage.py setup_groups
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from gestor.models import Empleado, Documento, TareaOnboarding, Departamento, Puesto


class Command(BaseCommand):
    help = 'Configura los grupos y permisos para el sistema de onboarding de RRHH'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Configurando Grupos y Permisos del Sistema de Onboarding'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        # Limpiar grupos existentes (opcional, comentar si no se desea)
        # Group.objects.all().delete()
        # self.stdout.write(self.style.WARNING('✓ Grupos anteriores eliminados'))
        
        # ==========================================
        # GRUPO: RRHH (Recursos Humanos)
        # ==========================================
        self.stdout.write(self.style.HTTP_INFO('\n📋 Configurando grupo: RRHH'))
        
        grupo_rrhh, created = Group.objects.get_or_create(name='RRHH')
        
        # Permisos para RRHH - TODOS los permisos
        permisos_rrhh = []
        
        # Empleado - Todos los permisos
        ct_empleado = ContentType.objects.get_for_model(Empleado)
        permisos_rrhh.extend(Permission.objects.filter(content_type=ct_empleado))
        
        # Documento - Todos los permisos + permiso especial
        ct_documento = ContentType.objects.get_for_model(Documento)
        permisos_rrhh.extend(Permission.objects.filter(content_type=ct_documento))
        
        # Tarea - Todos los permisos
        ct_tarea = ContentType.objects.get_for_model(TareaOnboarding)
        permisos_rrhh.extend(Permission.objects.filter(content_type=ct_tarea))
        
        # Departamento - Todos los permisos
        ct_departamento = ContentType.objects.get_for_model(Departamento)
        permisos_rrhh.extend(Permission.objects.filter(content_type=ct_departamento))
        
        # Puesto - Todos los permisos
        ct_puesto = ContentType.objects.get_for_model(Puesto)
        permisos_rrhh.extend(Permission.objects.filter(content_type=ct_puesto))
        
        # Permisos personalizados
        permisos_custom_rrhh = Permission.objects.filter(
            codename__in=[
                'view_dashboard',
                'approve_documents',
                'manage_onboarding'
            ]
        )
        permisos_rrhh.extend(permisos_custom_rrhh)
        
        grupo_rrhh.permissions.set(permisos_rrhh)
        
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ Grupo "RRHH" {"creado" if created else "actualizado"}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ {len(permisos_rrhh)} permisos asignados')
        )
        
        # ==========================================
        # GRUPO: Supervisores
        # ==========================================
        self.stdout.write(self.style.HTTP_INFO('\n👔 Configurando grupo: Supervisores'))
        
        grupo_supervisores, created = Group.objects.get_or_create(name='Supervisores')
        
        permisos_supervisores = []
        
        # Ver empleados
        permisos_supervisores.append(
            Permission.objects.get(codename='view_empleado', content_type=ct_empleado)
        )
        
        # Ver y editar tareas de sus subordinados
        permisos_supervisores.extend([
            Permission.objects.get(codename='view_tareaonboarding', content_type=ct_tarea),
            Permission.objects.get(codename='change_tareaonboarding', content_type=ct_tarea),
        ])
        
        # Ver documentos
        permisos_supervisores.append(
            Permission.objects.get(codename='view_documento', content_type=ct_documento)
        )
        
        # Ver departamentos y puestos
        permisos_supervisores.extend([
            Permission.objects.get(codename='view_departamento', content_type=ct_departamento),
            Permission.objects.get(codename='view_puesto', content_type=ct_puesto),
        ])
        
        # Permiso de ver dashboard
        try:
            perm_dashboard = Permission.objects.get(codename='view_dashboard')
            permisos_supervisores.append(perm_dashboard)
        except Permission.DoesNotExist:
            pass
        
        grupo_supervisores.permissions.set(permisos_supervisores)
        
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ Grupo "Supervisores" {"creado" if created else "actualizado"}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ {len(permisos_supervisores)} permisos asignados')
        )
        
        # ==========================================
        # GRUPO: Empleados
        # ==========================================
        self.stdout.write(self.style.HTTP_INFO('\n👤 Configurando grupo: Empleados'))
        
        grupo_empleados, created = Group.objects.get_or_create(name='Empleados')
        
        permisos_empleados = []
        
        # Ver su propio perfil (ver empleado)
        permisos_empleados.append(
            Permission.objects.get(codename='view_empleado', content_type=ct_empleado)
        )
        
        # Ver sus tareas
        permisos_empleados.append(
            Permission.objects.get(codename='view_tareaonboarding', content_type=ct_tarea)
        )
        
        # Subir y ver sus documentos
        permisos_empleados.extend([
            Permission.objects.get(codename='add_documento', content_type=ct_documento),
            Permission.objects.get(codename='view_documento', content_type=ct_documento),
        ])
        
        grupo_empleados.permissions.set(permisos_empleados)
        
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ Grupo "Empleados" {"creado" if created else "actualizado"}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ {len(permisos_empleados)} permisos asignados')
        )
        
        # ==========================================
        # GRUPO: IT (Tecnología)
        # ==========================================
        self.stdout.write(self.style.HTTP_INFO('\n💻 Configurando grupo: IT'))
        
        grupo_it, created = Group.objects.get_or_create(name='IT')
        
        permisos_it = []
        
        # Ver empleados
        permisos_it.append(
            Permission.objects.get(codename='view_empleado', content_type=ct_empleado)
        )
        
        # Ver y editar tareas asignadas a IT
        permisos_it.extend([
            Permission.objects.get(codename='view_tareaonboarding', content_type=ct_tarea),
            Permission.objects.get(codename='change_tareaonboarding', content_type=ct_tarea),
        ])
        
        # Ver documentos
        permisos_it.append(
            Permission.objects.get(codename='view_documento', content_type=ct_documento)
        )
        
        grupo_it.permissions.set(permisos_it)
        
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ Grupo "IT" {"creado" if created else "actualizado"}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ {len(permisos_it)} permisos asignados')
        )
        
        # ==========================================
        # Resumen Final
        # ==========================================
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('✅ Configuración completada exitosamente'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        self.stdout.write(self.style.WARNING('\n📝 Resumen de Grupos Creados:'))
        self.stdout.write(f'  • RRHH: {grupo_rrhh.permissions.count()} permisos')
        self.stdout.write(f'  • Supervisores: {grupo_supervisores.permissions.count()} permisos')
        self.stdout.write(f'  • Empleados: {grupo_empleados.permissions.count()} permisos')
        self.stdout.write(f'  • IT: {grupo_it.permissions.count()} permisos')
        
        self.stdout.write(self.style.WARNING('\n💡 Próximos pasos:'))
        self.stdout.write('  1. Asignar usuarios a los grupos correspondientes desde el admin')
        self.stdout.write('  2. Los usuarios heredarán automáticamente los permisos de su grupo')
        self.stdout.write('  3. Puedes personalizar permisos individuales si es necesario')
        
        self.stdout.write(self.style.SUCCESS('\n✨ ¡Sistema listo para usar!\n'))

