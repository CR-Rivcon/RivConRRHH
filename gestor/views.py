from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Empleado, Documento, TareaOnboarding, Departamento, Puesto
from .forms import (
    EmpleadoForm, DocumentoForm, DocumentoRevisionForm,
    TareaOnboardingForm, TareaEstadoForm, FiltroEmpleadosForm,
    DepartamentoForm, PuestoForm
)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Vista principal del dashboard con KPIs y estadísticas."""
    
    template_name = 'gestor/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular fechas
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # KPIs principales
        context['total_empleados'] = Empleado.objects.count()
        context['empleados_este_mes'] = Empleado.objects.filter(
            fecha_creacion__gte=inicio_mes,
            fecha_creacion__lte=fin_mes
        ).count()
        context['tareas_pendientes'] = TareaOnboarding.objects.filter(
            estado__in=['pendiente', 'en_progreso']
        ).count()
        context['documentos_pendientes'] = Documento.objects.filter(
            estado__in=['pendiente', 'en_revision']
        ).count()
        
        # Empleados por estado
        context['empleados_por_estado'] = Empleado.objects.values(
            'estado'
        ).annotate(
            total=Count('id')
        ).order_by('estado')
        
        # Empleados recientes
        context['empleados_recientes'] = Empleado.objects.select_related(
            'usuario', 'puesto', 'puesto__departamento'
        ).order_by('-fecha_creacion')[:5]
        
        # Tareas urgentes (próximas a vencer en 7 días)
        fecha_limite = hoy + timedelta(days=7)
        context['tareas_urgentes'] = TareaOnboarding.objects.filter(
            fecha_limite__lte=fecha_limite,
            estado__in=['pendiente', 'en_progreso']
        ).select_related('empleado', 'empleado__usuario').order_by('fecha_limite')[:10]
        
        # Documentos sin verificar
        context['documentos_sin_verificar'] = Documento.objects.filter(
            estado='pendiente'
        ).select_related('empleado', 'empleado__usuario').order_by('-fecha_subida')[:5]
        
        # Gráficos - Empleados por mes (últimos 6 meses)
        meses_data = []
        for i in range(6):
            mes = (hoy - timedelta(days=30*i)).replace(day=1)
            mes_siguiente = (mes + timedelta(days=32)).replace(day=1)
            count = Empleado.objects.filter(
                fecha_creacion__gte=mes,
                fecha_creacion__lt=mes_siguiente
            ).count()
            meses_data.append({
                'mes': mes.strftime('%b'),
                'count': count
            })
        context['empleados_por_mes'] = reversed(meses_data)
        
        return context


class EmpleadoListView(LoginRequiredMixin, ListView):
    """Vista para listar todos los empleados con filtros."""
    
    model = Empleado
    template_name = 'gestor/empleado_list.html'
    context_object_name = 'empleados'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Empleado.objects.select_related(
            'usuario', 'puesto', 'puesto__departamento', 'supervisor'
        ).order_by('-fecha_creacion')
        
        # Aplicar filtros
        form = FiltroEmpleadosForm(self.request.GET)
        if form.is_valid():
            buscar = form.cleaned_data.get('buscar')
            if buscar:
                queryset = queryset.filter(
                    Q(usuario__first_name__icontains=buscar) |
                    Q(usuario__last_name__icontains=buscar) |
                    Q(usuario__email__icontains=buscar) |
                    Q(cedula__icontains=buscar)
                )
            
            estado = form.cleaned_data.get('estado')
            if estado:
                queryset = queryset.filter(estado=estado)
            
            departamento = form.cleaned_data.get('departamento')
            if departamento:
                queryset = queryset.filter(puesto__departamento=departamento)
            
            supervisor = form.cleaned_data.get('supervisor')
            if supervisor:
                queryset = queryset.filter(supervisor=supervisor)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filtros'] = FiltroEmpleadosForm(self.request.GET)
        return context


class EmpleadoDetailView(LoginRequiredMixin, DetailView):
    """Vista detallada del proceso de onboarding de un empleado."""
    
    model = Empleado
    template_name = 'gestor/empleado_detail.html'
    context_object_name = 'empleado'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empleado = self.object
        
        # Tareas del empleado
        context['tareas'] = empleado.tareas.all().order_by('orden', 'fecha_limite')
        context['tareas_por_estado'] = empleado.tareas.values('estado').annotate(
            total=Count('id')
        )
        
        # Documentos del empleado
        context['documentos'] = empleado.documentos.all().order_by('-fecha_subida')
        context['documentos_por_estado'] = empleado.documentos.values('estado').annotate(
            total=Count('id')
        )
        
        # Progreso
        context['progreso'] = empleado.calcular_progreso()
        
        return context


class EmpleadoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista para crear un nuevo empleado (Alta de RRHH)."""
    
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'gestor/empleado_form.html'
    success_url = reverse_lazy('gestor:empleado_list')
    permission_required = 'gestor.add_empleado'
    
    def form_valid(self, form):
        # Guardar el empleado con el usuario que lo creó
        form.save(created_by=self.request.user)
        messages.success(
            self.request,
            f'Empleado {form.instance.usuario.get_full_name()} creado exitosamente. '
            'Se han generado las tareas automáticas de onboarding y se ha enviado un email de bienvenida.'
        )
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrige los errores en el formulario.')
        return super().form_invalid(form)


class EmpleadoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Vista para editar un empleado existente."""
    
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'gestor/empleado_form.html'
    permission_required = 'gestor.change_empleado'
    
    def get_success_url(self):
        return reverse_lazy('gestor:empleado_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Empleado actualizado exitosamente.')
        return super().form_valid(form)


class EmpleadoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Vista para eliminar un empleado."""
    
    model = Empleado
    template_name = 'gestor/empleado_confirm_delete.html'
    success_url = reverse_lazy('gestor:empleado_list')
    permission_required = 'gestor.delete_empleado'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Empleado eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


class DocumentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Vista para gestionar documentos (RRHH)."""
    
    model = Documento
    template_name = 'gestor/documento_list.html'
    context_object_name = 'documentos'
    paginate_by = 30
    permission_required = 'gestor.approve_documents'
    
    def get_queryset(self):
        queryset = Documento.objects.select_related(
            'empleado', 'empleado__usuario', 'revisado_por'
        ).order_by('-fecha_subida')
        
        # Filtrar por estado si se especifica
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estado_filtro'] = self.request.GET.get('estado', '')
        return context


class DocumentoCreateView(LoginRequiredMixin, CreateView):
    """Vista para que un empleado suba sus documentos."""
    
    model = Documento
    form_class = DocumentoForm
    template_name = 'gestor/documento_form.html'
    
    def get_success_url(self):
        return reverse_lazy('gestor:empleado_detail', kwargs={'pk': self.kwargs['empleado_pk']})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_is_staff'] = self.request.user.is_staff
        return kwargs
    
    def form_valid(self, form):
        empleado = get_object_or_404(Empleado, pk=self.kwargs['empleado_pk'])
        form.instance.empleado = empleado
        messages.success(self.request, 'Documento subido exitosamente.')
        return super().form_valid(form)


class DocumentoRevisarView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Vista para que RRHH apruebe/rechace documentos."""
    
    model = Documento
    form_class = DocumentoRevisionForm
    template_name = 'gestor/documento_revisar.html'
    permission_required = 'gestor.approve_documents'
    
    def get_success_url(self):
        return reverse_lazy('gestor:documento_list')
    
    def form_valid(self, form):
        documento = form.save(commit=False)
        documento.revisado_por = self.request.user
        documento.fecha_revision = timezone.now()
        documento.save()
        
        estado_text = documento.get_estado_display()
        messages.success(
            self.request,
            f'Documento "{documento.nombre}" marcado como {estado_text}.'
        )
        return super().form_valid(form)


class TareaListView(LoginRequiredMixin, ListView):
    """Vista para listar tareas de onboarding."""
    
    model = TareaOnboarding
    template_name = 'gestor/tarea_list.html'
    context_object_name = 'tareas'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = TareaOnboarding.objects.select_related(
            'empleado', 'empleado__usuario', 'responsable_usuario'
        ).order_by('fecha_limite', '-prioridad')
        
        # Filtros
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        responsable = self.request.GET.get('responsable')
        if responsable:
            queryset = queryset.filter(responsable=responsable)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estado_filtro'] = self.request.GET.get('estado', '')
        context['responsable_filtro'] = self.request.GET.get('responsable', '')
        return context


class TareaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista para crear una nueva tarea de onboarding."""
    
    model = TareaOnboarding
    form_class = TareaOnboardingForm
    template_name = 'gestor/tarea_form.html'
    permission_required = 'gestor.add_tareaonboarding'
    
    def get_initial(self):
        initial = super().get_initial()
        empleado_pk = self.kwargs.get('empleado_pk')
        if empleado_pk:
            initial['empleado'] = empleado_pk
        return initial
    
    def get_success_url(self):
        empleado_pk = self.kwargs.get('empleado_pk')
        if empleado_pk:
            return reverse_lazy('gestor:empleado_detail', kwargs={'pk': empleado_pk})
        return reverse_lazy('gestor:tarea_list')
    
    def form_valid(self, form):
        empleado_pk = self.kwargs.get('empleado_pk')
        if empleado_pk:
            form.instance.empleado_id = empleado_pk
        messages.success(self.request, 'Tarea creada exitosamente.')
        return super().form_valid(form)


class TareaUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para actualizar el estado de una tarea."""
    
    model = TareaOnboarding
    form_class = TareaEstadoForm
    template_name = 'gestor/tarea_update.html'
    
    def get_success_url(self):
        return reverse_lazy('gestor:empleado_detail', kwargs={'pk': self.object.empleado.pk})
    
    def form_valid(self, form):
        tarea = form.save(commit=False)
        
        # Si se marca como completada, registrar fecha y usuario
        if tarea.estado == 'completado' and not tarea.fecha_completado:
            tarea.fecha_completado = timezone.now().date()
            tarea.completado_por = self.request.user
        
        # Si se pone en progreso por primera vez, registrar fecha de inicio
        if tarea.estado == 'en_progreso' and not tarea.fecha_inicio:
            tarea.fecha_inicio = timezone.now().date()
        
        tarea.save()
        messages.success(self.request, 'Tarea actualizada exitosamente.')
        return super().form_valid(form)


class DepartamentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Vista para listar departamentos."""
    
    model = Departamento
    template_name = 'gestor/departamento_list.html'
    context_object_name = 'departamentos'
    permission_required = 'gestor.view_departamento'
    
    def get_queryset(self):
        return Departamento.objects.annotate(
            total_puestos=Count('puestos'),
            total_empleados=Count('puestos__empleados')
        )


class DepartamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista para crear un departamento."""
    
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'gestor/departamento_form.html'
    success_url = reverse_lazy('gestor:departamento_list')
    permission_required = 'gestor.add_departamento'
    
    def form_valid(self, form):
        messages.success(self.request, 'Departamento creado exitosamente.')
        return super().form_valid(form)


class PuestoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Vista para listar puestos."""
    
    model = Puesto
    template_name = 'gestor/puesto_list.html'
    context_object_name = 'puestos'
    permission_required = 'gestor.view_puesto'
    
    def get_queryset(self):
        return Puesto.objects.select_related('departamento').annotate(
            total_empleados=Count('empleados')
        )


class PuestoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista para crear un puesto."""
    
    model = Puesto
    form_class = PuestoForm
    template_name = 'gestor/puesto_form.html'
    success_url = reverse_lazy('gestor:puesto_list')
    permission_required = 'gestor.add_puesto'
    
    def form_valid(self, form):
        messages.success(self.request, 'Puesto creado exitosamente.')
        return super().form_valid(form)


# Vista adicional para tablero Kanban
class KanbanView(LoginRequiredMixin, TemplateView):
    """Vista tipo Kanban para visualizar el proceso de onboarding."""
    
    template_name = 'gestor/kanban.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Empleados organizados por estado
        context['empleados_pre_ingreso'] = Empleado.objects.filter(
            estado='pre_ingreso'
        ).select_related('usuario', 'puesto')
        
        context['empleados_en_proceso'] = Empleado.objects.filter(
            estado='en_proceso'
        ).select_related('usuario', 'puesto')
        
        context['empleados_completados'] = Empleado.objects.filter(
            estado='completado'
        ).select_related('usuario', 'puesto')
        
        return context
