from django.contrib import admin
from django.utils.html import format_html
from .models import Departamento, Puesto, Empleado, Documento, TareaOnboarding


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    """Configuración del admin para Departamentos."""
    
    list_display = ['nombre', 'total_puestos', 'total_empleados', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_filter = ['fecha_creacion']
    ordering = ['nombre']
    
    def total_puestos(self, obj):
        return obj.puestos.count()
    total_puestos.short_description = 'Total Puestos'
    
    def total_empleados(self, obj):
        return Empleado.objects.filter(puesto__departamento=obj).count()
    total_empleados.short_description = 'Total Empleados'


@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    """Configuración del admin para Puestos."""
    
    list_display = [
        'titulo', 'departamento', 'nivel', 'salario_minimo', 
        'salario_maximo', 'total_empleados', 'activo', 'fecha_creacion'
    ]
    list_filter = ['departamento', 'nivel', 'activo', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'departamento__nombre']
    list_editable = ['activo']
    ordering = ['departamento', 'titulo']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'departamento', 'nivel', 'descripcion')
        }),
        ('Información Salarial', {
            'fields': ('salario_minimo', 'salario_maximo'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    def total_empleados(self, obj):
        count = obj.empleados.count()
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                count
            )
        return count
    total_empleados.short_description = 'Empleados'


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    """Configuración del admin para Empleados."""
    
    list_display = [
        'get_nombre_completo', 'cedula', 'puesto', 'estado_badge', 
        'progreso_bar', 'fecha_ingreso', 'supervisor', 'fecha_creacion'
    ]
    list_filter = [
        'estado', 'puesto__departamento', 'fecha_ingreso', 
        'supervisor', 'fecha_creacion'
    ]
    search_fields = [
        'cedula', 'usuario__username', 'usuario__email',
        'usuario__first_name', 'usuario__last_name',
        'puesto__titulo'
    ]
    readonly_fields = [
        'progreso', 'fecha_creacion', 'fecha_actualizacion', 'creado_por'
    ]
    list_per_page = 25
    date_hierarchy = 'fecha_ingreso'
    
    fieldsets = (
        ('Usuario', {
            'fields': ('usuario', 'creado_por')
        }),
        ('Información Personal', {
            'fields': (
                'cedula', 'telefono', 'telefono_emergencia',
                'fecha_nacimiento', 'direccion', 'tipo_sangre'
            )
        }),
        ('Información Laboral', {
            'fields': (
                'puesto', 'fecha_ingreso', 'salario', 'supervisor'
            )
        }),
        ('Estado del Onboarding', {
            'fields': ('estado', 'progreso', 'notas'),
            'classes': ('wide',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_nombre_completo(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username
    get_nombre_completo.short_description = 'Nombre'
    get_nombre_completo.admin_order_field = 'usuario__first_name'
    
    def estado_badge(self, obj):
        colors = {
            'pre_ingreso': '#FFC107',
            'en_proceso': '#2196F3',
            'completado': '#4CAF50',
            'cancelado': '#9E9E9E',
        }
        color = colors.get(obj.estado, '#9E9E9E')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    estado_badge.admin_order_field = 'estado'
    
    def progreso_bar(self, obj):
        progreso = obj.progreso
        color = '#4CAF50' if progreso >= 75 else '#FFC107' if progreso >= 50 else '#FF5722'
        return format_html(
            '<div style="width: 100px; background-color: #e0e0e0; border-radius: 10px; overflow: hidden;">'
            '<div style="width: {}%; background-color: {}; height: 20px; text-align: center; '
            'color: white; font-size: 11px; line-height: 20px;">{} %</div></div>',
            progreso,
            color,
            progreso
        )
    progreso_bar.short_description = 'Progreso'
    progreso_bar.admin_order_field = 'progreso'
    
    actions = ['marcar_en_proceso', 'marcar_completado', 'actualizar_progreso']
    
    def marcar_en_proceso(self, request, queryset):
        updated = queryset.update(estado='en_proceso')
        self.message_user(
            request,
            f'{updated} empleado(s) marcado(s) como En Proceso.'
        )
    marcar_en_proceso.short_description = 'Marcar como En Proceso'
    
    def marcar_completado(self, request, queryset):
        updated = queryset.update(estado='completado')
        self.message_user(
            request,
            f'{updated} empleado(s) marcado(s) como Completado.'
        )
    marcar_completado.short_description = 'Marcar como Completado'
    
    def actualizar_progreso(self, request, queryset):
        for empleado in queryset:
            empleado.actualizar_progreso()
        self.message_user(
            request,
            f'Progreso actualizado para {queryset.count()} empleado(s).'
        )
    actualizar_progreso.short_description = 'Actualizar Progreso'


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    """Configuración del admin para Documentos."""
    
    list_display = [
        'nombre', 'tipo', 'get_empleado', 'estado_badge',
        'obligatorio_badge', 'fecha_subida', 'revisado_por'
    ]
    list_filter = [
        'tipo', 'estado', 'obligatorio', 'fecha_subida',
        'empleado__puesto__departamento'
    ]
    search_fields = [
        'nombre', 'empleado__usuario__first_name',
        'empleado__usuario__last_name', 'empleado__cedula'
    ]
    readonly_fields = ['fecha_subida', 'fecha_actualizacion']
    date_hierarchy = 'fecha_subida'
    list_per_page = 30
    
    fieldsets = (
        ('Información del Documento', {
            'fields': ('empleado', 'tipo', 'nombre', 'archivo', 'obligatorio')
        }),
        ('Revisión', {
            'fields': ('estado', 'revisado_por', 'fecha_revision', 'comentarios')
        }),
        ('Metadatos', {
            'fields': ('fecha_subida', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_empleado(self, obj):
        return obj.empleado.usuario.get_full_name() or obj.empleado.usuario.username
    get_empleado.short_description = 'Empleado'
    get_empleado.admin_order_field = 'empleado__usuario__first_name'
    
    def estado_badge(self, obj):
        colors = {
            'pendiente': '#FFC107',
            'en_revision': '#2196F3',
            'aprobado': '#4CAF50',
            'rechazado': '#F44336',
        }
        color = colors.get(obj.estado, '#9E9E9E')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    estado_badge.admin_order_field = 'estado'
    
    def obligatorio_badge(self, obj):
        if obj.obligatorio:
            return format_html(
                '<span style="color: red; font-weight: bold;">✓ Sí</span>'
            )
        return format_html('<span style="color: gray;">No</span>')
    obligatorio_badge.short_description = 'Obligatorio'
    obligatorio_badge.admin_order_field = 'obligatorio'
    
    actions = ['aprobar_documentos', 'rechazar_documentos', 'marcar_en_revision']
    
    def aprobar_documentos(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(
            estado='aprobado',
            revisado_por=request.user,
            fecha_revision=timezone.now()
        )
        self.message_user(
            request,
            f'{updated} documento(s) aprobado(s).'
        )
    aprobar_documentos.short_description = 'Aprobar Documentos Seleccionados'
    
    def rechazar_documentos(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(
            estado='rechazado',
            revisado_por=request.user,
            fecha_revision=timezone.now()
        )
        self.message_user(
            request,
            f'{updated} documento(s) rechazado(s).'
        )
    rechazar_documentos.short_description = 'Rechazar Documentos Seleccionados'
    
    def marcar_en_revision(self, request, queryset):
        updated = queryset.update(estado='en_revision')
        self.message_user(
            request,
            f'{updated} documento(s) marcado(s) como En Revisión.'
        )
    marcar_en_revision.short_description = 'Marcar como En Revisión'


@admin.register(TareaOnboarding)
class TareaOnboardingAdmin(admin.ModelAdmin):
    """Configuración del admin para Tareas de Onboarding."""
    
    list_display = [
        'titulo', 'get_empleado', 'responsable', 'estado_badge',
        'prioridad_badge', 'fecha_limite', 'es_automatica'
    ]
    list_filter = [
        'estado', 'responsable', 'prioridad', 'es_automatica',
        'fecha_limite', 'empleado__puesto__departamento'
    ]
    search_fields = [
        'titulo', 'descripcion', 'empleado__usuario__first_name',
        'empleado__usuario__last_name'
    ]
    readonly_fields = [
        'fecha_creacion', 'fecha_actualizacion',
        'fecha_completado', 'completado_por'
    ]
    date_hierarchy = 'fecha_limite'
    list_per_page = 50
    
    fieldsets = (
        ('Información de la Tarea', {
            'fields': ('empleado', 'titulo', 'descripcion', 'orden')
        }),
        ('Responsabilidad', {
            'fields': ('responsable', 'responsable_usuario')
        }),
        ('Fechas y Prioridad', {
            'fields': (
                'fecha_limite', 'fecha_inicio', 'prioridad'
            )
        }),
        ('Estado', {
            'fields': ('estado', 'notas', 'es_automatica')
        }),
        ('Completado', {
            'fields': ('fecha_completado', 'completado_por'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_empleado(self, obj):
        return obj.empleado.usuario.get_full_name() or obj.empleado.usuario.username
    get_empleado.short_description = 'Empleado'
    get_empleado.admin_order_field = 'empleado__usuario__first_name'
    
    def estado_badge(self, obj):
        colors = {
            'pendiente': '#FFC107',
            'en_progreso': '#2196F3',
            'completado': '#4CAF50',
            'bloqueado': '#F44336',
            'cancelado': '#9E9E9E',
        }
        color = colors.get(obj.estado, '#9E9E9E')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    estado_badge.admin_order_field = 'estado'
    
    def prioridad_badge(self, obj):
        colors = {
            'urgente': '#F44336',
            'alta': '#FF9800',
            'media': '#FFC107',
            'baja': '#9E9E9E',
        }
        color = colors.get(obj.prioridad, '#9E9E9E')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 10px; font-size: 10px; font-weight: bold;">{}</span>',
            color,
            obj.get_prioridad_display()
        )
    prioridad_badge.short_description = 'Prioridad'
    prioridad_badge.admin_order_field = 'prioridad'
    
    actions = [
        'marcar_en_progreso', 'marcar_completado',
        'marcar_pendiente', 'aumentar_prioridad'
    ]
    
    def marcar_en_progreso(self, request, queryset):
        from django.utils import timezone
        for tarea in queryset:
            if not tarea.fecha_inicio:
                tarea.fecha_inicio = timezone.now().date()
            tarea.estado = 'en_progreso'
            tarea.save()
        self.message_user(
            request,
            f'{queryset.count()} tarea(s) marcada(s) como En Progreso.'
        )
    marcar_en_progreso.short_description = 'Marcar como En Progreso'
    
    def marcar_completado(self, request, queryset):
        from django.utils import timezone
        for tarea in queryset:
            tarea.estado = 'completado'
            tarea.fecha_completado = timezone.now().date()
            tarea.completado_por = request.user
            tarea.save()
        self.message_user(
            request,
            f'{queryset.count()} tarea(s) marcada(s) como Completada.'
        )
    marcar_completado.short_description = 'Marcar como Completado'
    
    def marcar_pendiente(self, request, queryset):
        updated = queryset.update(estado='pendiente')
        self.message_user(
            request,
            f'{updated} tarea(s) marcada(s) como Pendiente.'
        )
    marcar_pendiente.short_description = 'Marcar como Pendiente'
    
    def aumentar_prioridad(self, request, queryset):
        prioridades = {'baja': 'media', 'media': 'alta', 'alta': 'urgente'}
        for tarea in queryset:
            if tarea.prioridad in prioridades:
                tarea.prioridad = prioridades[tarea.prioridad]
                tarea.save()
        self.message_user(
            request,
            f'Prioridad aumentada para {queryset.count()} tarea(s).'
        )
    aumentar_prioridad.short_description = 'Aumentar Prioridad'


# Personalización del admin site
admin.site.site_header = 'Rivcon RRHH - Administración'
admin.site.site_title = 'Rivcon RRHH Admin'
admin.site.index_title = 'Panel de Administración de Recursos Humanos'
