"""
URLs de la aplicación gestor - Sistema de Onboarding de RRHH
"""
from django.urls import path
from . import views

app_name = 'gestor'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Empleados
    path('empleados/', views.EmpleadoListView.as_view(), name='empleado_list'),
    path('empleados/nuevo/', views.EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleados/<int:pk>/', views.EmpleadoDetailView.as_view(), name='empleado_detail'),
    path('empleados/<int:pk>/editar/', views.EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleados/<int:pk>/eliminar/', views.EmpleadoDeleteView.as_view(), name='empleado_delete'),
    
    # Vista Kanban
    path('kanban/', views.KanbanView.as_view(), name='kanban'),
    
    # Documentos
    path('documentos/', views.DocumentoListView.as_view(), name='documento_list'),
    path('documentos/<int:pk>/revisar/', views.DocumentoRevisarView.as_view(), name='documento_revisar'),
    path('empleados/<int:empleado_pk>/documentos/nuevo/', views.DocumentoCreateView.as_view(), name='documento_create'),
    
    # Tareas
    path('tareas/', views.TareaListView.as_view(), name='tarea_list'),
    path('tareas/<int:pk>/actualizar/', views.TareaUpdateView.as_view(), name='tarea_update'),
    path('empleados/<int:empleado_pk>/tareas/nueva/', views.TareaCreateView.as_view(), name='tarea_create'),
    
    # Departamentos
    path('departamentos/', views.DepartamentoListView.as_view(), name='departamento_list'),
    path('departamentos/nuevo/', views.DepartamentoCreateView.as_view(), name='departamento_create'),
    
    # Puestos
    path('puestos/', views.PuestoListView.as_view(), name='puesto_list'),
    path('puestos/nuevo/', views.PuestoCreateView.as_view(), name='puesto_create'),
]

