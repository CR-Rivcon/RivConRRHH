from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import secrets


class Departamento(models.Model):
    """Modelo para representar los departamentos de la empresa."""
    
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del Departamento',
        help_text='Nombre del departamento (ej: Recursos Humanos, IT, Ventas)'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Descripción breve del departamento y sus funciones'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Puesto(models.Model):
    """Modelo para representar los puestos de trabajo."""
    
    NIVEL_CHOICES = [
        ('junior', 'Junior'),
        ('semi_senior', 'Semi Senior'),
        ('senior', 'Senior'),
        ('manager', 'Manager'),
        ('director', 'Director'),
        ('ejecutivo', 'Ejecutivo'),
    ]
    
    titulo = models.CharField(
        max_length=150,
        verbose_name='Título del Puesto',
        help_text='Nombre del puesto (ej: Desarrollador Backend, Contador)'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        related_name='puestos',
        verbose_name='Departamento',
        help_text='Departamento al que pertenece este puesto'
    )
    nivel = models.CharField(
        max_length=20,
        choices=NIVEL_CHOICES,
        default='junior',
        verbose_name='Nivel',
        help_text='Nivel jerárquico del puesto'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Responsabilidades y requisitos del puesto'
    )
    salario_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Salario Mínimo',
        help_text='Rango salarial mínimo para este puesto'
    )
    salario_maximo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Salario Máximo',
        help_text='Rango salarial máximo para este puesto'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el puesto está actualmente disponible'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        verbose_name = 'Puesto'
        verbose_name_plural = 'Puestos'
        ordering = ['departamento', 'titulo']
        unique_together = ['titulo', 'departamento']
    
    def __str__(self):
        return f"{self.titulo} - {self.departamento.nombre}"


class Empleado(models.Model):
    """Modelo para representar a los empleados en proceso de onboarding."""
    
    ESTADO_CHOICES = [
        ('pre_ingreso', 'Pre-ingreso'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    TIPO_SANGRE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    # Relación con usuario de Django
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='empleado',
        verbose_name='Usuario',
        help_text='Usuario de Django asociado al empleado'
    )
    
    # Datos personales
    cedula = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Cédula de Identidad',
        help_text='Número de cédula de identidad del empleado'
    )
    telefono = models.CharField(
        max_length=20,
        verbose_name='Teléfono',
        help_text='Número de teléfono de contacto'
    )
    telefono_emergencia = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono de Emergencia',
        help_text='Contacto de emergencia'
    )
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de Nacimiento',
        help_text='Fecha de nacimiento del empleado'
    )
    direccion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Dirección',
        help_text='Dirección de residencia'
    )
    tipo_sangre = models.CharField(
        max_length=3,
        choices=TIPO_SANGRE_CHOICES,
        blank=True,
        null=True,
        verbose_name='Tipo de Sangre'
    )
    
    # Datos laborales
    puesto = models.ForeignKey(
        Puesto,
        on_delete=models.SET_NULL,
        null=True,
        related_name='empleados',
        verbose_name='Puesto',
        help_text='Puesto que ocupará el empleado'
    )
    fecha_ingreso = models.DateField(
        verbose_name='Fecha de Ingreso',
        help_text='Fecha en que el empleado inicia labores'
    )
    salario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Salario',
        help_text='Salario mensual del empleado'
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='empleados_supervisados',
        verbose_name='Supervisor',
        help_text='Supervisor directo del empleado'
    )
    
    # Estado del onboarding
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pre_ingreso',
        verbose_name='Estado',
        help_text='Estado actual del proceso de onboarding'
    )
    progreso = models.IntegerField(
        default=0,
        verbose_name='Progreso (%)',
        help_text='Porcentaje de avance en el proceso de onboarding'
    )
    
    # Notas internas
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas',
        help_text='Notas internas de RRHH sobre el empleado'
    )
    
    # Metadatos
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='empleados_creados',
        verbose_name='Creado Por'
    )
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['-fecha_creacion']
        permissions = [
            ('view_dashboard', 'Puede ver el dashboard de RRHH'),
            ('approve_documents', 'Puede aprobar documentos'),
            ('manage_onboarding', 'Puede gestionar el proceso de onboarding'),
        ]
    
    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} - {self.estado}"
    
    def calcular_progreso(self):
        """Calcula el progreso del onboarding basado en tareas completadas."""
        total_tareas = self.tareas.count()
        if total_tareas == 0:
            return 0
        tareas_completadas = self.tareas.filter(estado='completado').count()
        return int((tareas_completadas / total_tareas) * 100)
    
    def actualizar_progreso(self):
        """Actualiza el campo progreso."""
        self.progreso = self.calcular_progreso()
        self.save(update_fields=['progreso'])


class Documento(models.Model):
    """Modelo para gestionar los documentos del empleado."""
    
    TIPO_CHOICES = [
        ('contrato', 'Contrato de Trabajo'),
        ('cedula', 'Cédula de Identidad'),
        ('nda', 'Acuerdo de Confidencialidad (NDA)'),
        ('titulo', 'Título Académico'),
        ('certificado_medico', 'Certificado Médico'),
        ('carta_recomendacion', 'Carta de Recomendación'),
        ('foto', 'Fotografía'),
        ('antecedentes', 'Certificado de Antecedentes'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='documentos',
        verbose_name='Empleado',
        help_text='Empleado al que pertenece el documento'
    )
    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Documento',
        help_text='Tipo de documento que se está subiendo'
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre del Documento',
        help_text='Nombre descriptivo del documento'
    )
    archivo = models.FileField(
        upload_to='documentos/%Y/%m/',
        verbose_name='Archivo',
        help_text='Archivo del documento (PDF, Word, Imagen, etc.)'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado',
        help_text='Estado de verificación del documento'
    )
    obligatorio = models.BooleanField(
        default=False,
        verbose_name='Obligatorio',
        help_text='Indica si el documento es obligatorio para completar el onboarding'
    )
    
    # Revisión
    revisado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documentos_revisados',
        verbose_name='Revisado Por',
        help_text='Usuario de RRHH que revisó el documento'
    )
    fecha_revision = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Revisión'
    )
    comentarios = models.TextField(
        blank=True,
        null=True,
        verbose_name='Comentarios',
        help_text='Comentarios sobre el documento (razón de rechazo, observaciones, etc.)'
    )
    
    # Metadatos
    fecha_subida = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Subida'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-fecha_subida']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.empleado.usuario.get_full_name() or self.empleado.usuario.username}"


class TareaOnboarding(models.Model):
    """Modelo para gestionar las tareas del proceso de onboarding."""
    
    RESPONSABLE_CHOICES = [
        ('rrhh', 'Recursos Humanos'),
        ('it', 'Tecnología (IT)'),
        ('supervisor', 'Jefe Directo'),
        ('finanzas', 'Finanzas'),
        ('empleado', 'Empleado'),
        ('legal', 'Legal'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
        ('bloqueado', 'Bloqueado'),
        ('cancelado', 'Cancelado'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='tareas',
        verbose_name='Empleado',
        help_text='Empleado al que pertenece esta tarea'
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título breve de la tarea'
    )
    descripcion = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada de lo que debe realizarse'
    )
    responsable = models.CharField(
        max_length=20,
        choices=RESPONSABLE_CHOICES,
        verbose_name='Responsable',
        help_text='Departamento o persona responsable de completar la tarea'
    )
    responsable_usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tareas_asignadas',
        verbose_name='Usuario Responsable',
        help_text='Usuario específico asignado a la tarea'
    )
    
    # Fechas
    fecha_limite = models.DateField(
        verbose_name='Fecha Límite',
        help_text='Fecha en que debe completarse la tarea'
    )
    fecha_inicio = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Inicio',
        help_text='Fecha en que se comenzó a trabajar en la tarea'
    )
    fecha_completado = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Completado'
    )
    
    # Estado y prioridad
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_CHOICES,
        default='media',
        verbose_name='Prioridad'
    )
    
    # Configuración
    es_automatica = models.BooleanField(
        default=True,
        verbose_name='Tarea Automática',
        help_text='Indica si la tarea fue creada automáticamente por el sistema'
    )
    orden = models.IntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de ejecución de la tarea'
    )
    
    # Notas
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas',
        help_text='Notas adicionales sobre la tarea'
    )
    
    # Metadatos
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    completado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tareas_completadas',
        verbose_name='Completado Por'
    )
    
    class Meta:
        verbose_name = 'Tarea de Onboarding'
        verbose_name_plural = 'Tareas de Onboarding'
        ordering = ['orden', 'fecha_limite', '-prioridad']
    
    def __str__(self):
        return f"{self.titulo} - {self.empleado.usuario.get_full_name() or self.empleado.usuario.username}"


# ======================
# SIGNALS (Automatización)
# ======================

@receiver(post_save, sender=Empleado)
def crear_tareas_automaticas(sender, instance, created, **kwargs):
    """
    Signal que crea automáticamente las tareas de onboarding
    cuando se crea un nuevo empleado.
    """
    if created:
        from datetime import timedelta
        from django.utils import timezone
        
        fecha_base = instance.fecha_ingreso
        
        # Lista de tareas predeterminadas
        tareas_predeterminadas = [
            {
                'titulo': 'Crear cuenta de correo electrónico corporativo',
                'descripcion': 'Configurar cuenta de correo con dominio @rivcon.com y acceso a herramientas corporativas.',
                'responsable': 'it',
                'prioridad': 'alta',
                'dias_antes': 3,
                'orden': 1,
            },
            {
                'titulo': 'Preparar estación de trabajo',
                'descripcion': 'Configurar computadora, periféricos y acceso a red.',
                'responsable': 'it',
                'prioridad': 'alta',
                'dias_antes': 2,
                'orden': 2,
            },
            {
                'titulo': 'Crear accesos a sistemas corporativos',
                'descripcion': 'Configurar permisos y accesos a ERP, CRM y sistemas internos.',
                'responsable': 'it',
                'prioridad': 'media',
                'dias_antes': 1,
                'orden': 3,
            },
            {
                'titulo': 'Firmar contrato de trabajo',
                'descripcion': 'Revisar y firmar el contrato de trabajo junto con RRHH.',
                'responsable': 'rrhh',
                'prioridad': 'urgente',
                'dias_antes': 5,
                'orden': 4,
            },
            {
                'titulo': 'Firmar acuerdo de confidencialidad (NDA)',
                'descripcion': 'Revisar y firmar el acuerdo de confidencialidad de la empresa.',
                'responsable': 'legal',
                'prioridad': 'alta',
                'dias_antes': 5,
                'orden': 5,
            },
            {
                'titulo': 'Subir documentos personales',
                'descripcion': 'Subir cédula, títulos académicos, certificados médicos y otros documentos requeridos.',
                'responsable': 'empleado',
                'prioridad': 'alta',
                'dias_antes': 7,
                'orden': 6,
            },
            {
                'titulo': 'Inscripción en sistema de nómina',
                'descripcion': 'Registrar datos bancarios y información para procesamiento de nómina.',
                'responsable': 'finanzas',
                'prioridad': 'alta',
                'dias_antes': 3,
                'orden': 7,
            },
            {
                'titulo': 'Asignación de supervisor y equipo',
                'descripcion': 'Presentar al empleado con su supervisor y equipo de trabajo.',
                'responsable': 'supervisor',
                'prioridad': 'media',
                'dias_antes': 0,
                'orden': 8,
            },
            {
                'titulo': 'Tour por las instalaciones',
                'descripcion': 'Realizar recorrido por oficinas, áreas comunes y presentación del personal.',
                'responsable': 'rrhh',
                'prioridad': 'media',
                'dias_antes': 0,
                'orden': 9,
            },
            {
                'titulo': 'Capacitación de inducción corporativa',
                'descripcion': 'Asistir a sesión de inducción sobre valores, políticas y procedimientos de la empresa.',
                'responsable': 'rrhh',
                'prioridad': 'alta',
                'dias_antes': 0,
                'orden': 10,
            },
        ]
        
        # Crear las tareas
        for tarea_data in tareas_predeterminadas:
            dias_antes = tarea_data.pop('dias_antes')
            fecha_limite = fecha_base - timedelta(days=dias_antes) if dias_antes > 0 else fecha_base
            
            TareaOnboarding.objects.create(
                empleado=instance,
                fecha_limite=fecha_limite,
                es_automatica=True,
                **tarea_data
            )


@receiver(post_save, sender=Empleado)
def enviar_email_bienvenida(sender, instance, created, **kwargs):
    """
    Signal que envía un email de bienvenida cuando se crea un empleado.
    En desarrollo, se mostrará en la consola.
    """
    if created:
        # Generar contraseña temporal
        password_temporal = secrets.token_urlsafe(12)
        instance.usuario.set_password(password_temporal)
        instance.usuario.save()
        
        # Enviar email
        asunto = f'Bienvenido a Rivcon - {instance.usuario.first_name}'
        mensaje = f"""
        ¡Hola {instance.usuario.first_name}!
        
        Bienvenido a Rivcon. Tu cuenta ha sido creada exitosamente.
        
        Detalles de acceso:
        - Usuario: {instance.usuario.username}
        - Contraseña temporal: {password_temporal}
        - Correo: {instance.usuario.email}
        
        Fecha de ingreso: {instance.fecha_ingreso.strftime('%d/%m/%Y')}
        Puesto: {instance.puesto}
        
        Por favor, ingresa al sistema y cambia tu contraseña en tu primer acceso.
        
        Si tienes alguna pregunta, no dudes en contactar a Recursos Humanos.
        
        ¡Bienvenido al equipo!
        
        Equipo de Recursos Humanos
        Rivcon
        """
        
        try:
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [instance.usuario.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error enviando email: {e}")


@receiver(post_save, sender=TareaOnboarding)
def actualizar_progreso_empleado(sender, instance, **kwargs):
    """
    Signal que actualiza el progreso del empleado cuando cambia el estado de una tarea.
    """
    instance.empleado.actualizar_progreso()
