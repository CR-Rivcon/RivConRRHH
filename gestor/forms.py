from django import forms
from django.contrib.auth.models import User
from .models import Empleado, Documento, TareaOnboarding, Departamento, Puesto


class EmpleadoForm(forms.ModelForm):
    """Formulario para crear/editar empleados."""
    
    # Campos del usuario
    username = forms.CharField(
        max_length=150,
        label='Nombre de Usuario',
        help_text='Nombre de usuario para acceso al sistema'
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        help_text='Correo electrónico corporativo'
    )
    first_name = forms.CharField(
        max_length=150,
        label='Nombre(s)'
    )
    last_name = forms.CharField(
        max_length=150,
        label='Apellido(s)'
    )
    
    class Meta:
        model = Empleado
        fields = [
            'cedula', 'telefono', 'telefono_emergencia', 'fecha_nacimiento',
            'direccion', 'tipo_sangre', 'puesto', 'fecha_ingreso',
            'salario', 'supervisor', 'estado', 'notas'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'notas': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        # Si estamos editando un empleado existente
        instance = kwargs.get('instance')
        if instance and instance.pk:
            # Pre-rellenar campos del usuario
            initial = kwargs.get('initial', {})
            initial['username'] = instance.usuario.username
            initial['email'] = instance.usuario.email
            initial['first_name'] = instance.usuario.first_name
            initial['last_name'] = instance.usuario.last_name
            kwargs['initial'] = initial
        
        super().__init__(*args, **kwargs)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        # Si estamos editando, permitir el mismo username
        if self.instance.pk:
            if User.objects.exclude(pk=self.instance.usuario.pk).filter(username=username).exists():
                raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        else:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        # Si estamos editando, permitir el mismo email
        if self.instance.pk:
            if User.objects.exclude(pk=self.instance.usuario.pk).filter(email=email).exists():
                raise forms.ValidationError('Este correo electrónico ya está en uso.')
        else:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Este correo electrónico ya está en uso.')
        return email
    
    def save(self, commit=True, created_by=None):
        empleado = super().save(commit=False)
        
        # Si es un nuevo empleado, crear el usuario
        if not empleado.pk:
            user = User.objects.create(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
            )
            empleado.usuario = user
            if created_by:
                empleado.creado_por = created_by
        else:
            # Actualizar datos del usuario existente
            user = empleado.usuario
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
        
        if commit:
            empleado.save()
        
        return empleado


class DocumentoForm(forms.ModelForm):
    """Formulario para subir documentos."""
    
    class Meta:
        model = Documento
        fields = ['tipo', 'nombre', 'archivo', 'obligatorio']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Cédula escaneada'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El campo obligatorio solo es editable por RRHH
        if not kwargs.get('user_is_staff'):
            self.fields['obligatorio'].widget = forms.HiddenInput()


class DocumentoRevisionForm(forms.ModelForm):
    """Formulario para que RRHH revise documentos."""
    
    class Meta:
        model = Documento
        fields = ['estado', 'comentarios']
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': 3}),
        }


class TareaOnboardingForm(forms.ModelForm):
    """Formulario para crear/editar tareas de onboarding."""
    
    class Meta:
        model = TareaOnboarding
        fields = [
            'titulo', 'descripcion', 'responsable', 'responsable_usuario',
            'fecha_limite', 'prioridad', 'estado', 'notas', 'orden'
        ]
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'notas': forms.Textarea(attrs={'rows': 2}),
        }


class TareaEstadoForm(forms.ModelForm):
    """Formulario simple para actualizar el estado de una tarea."""
    
    class Meta:
        model = TareaOnboarding
        fields = ['estado', 'notas']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 2}),
        }


class DepartamentoForm(forms.ModelForm):
    """Formulario para crear/editar departamentos."""
    
    class Meta:
        model = Departamento
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class PuestoForm(forms.ModelForm):
    """Formulario para crear/editar puestos."""
    
    class Meta:
        model = Puesto
        fields = [
            'titulo', 'departamento', 'nivel', 'descripcion',
            'salario_minimo', 'salario_maximo', 'activo'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        salario_min = cleaned_data.get('salario_minimo')
        salario_max = cleaned_data.get('salario_maximo')
        
        if salario_min and salario_max and salario_min > salario_max:
            raise forms.ValidationError(
                'El salario mínimo no puede ser mayor que el salario máximo.'
            )
        
        return cleaned_data


class FiltroEmpleadosForm(forms.Form):
    """Formulario para filtrar la lista de empleados."""
    
    buscar = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre, cédula, email...',
            'class': 'form-control'
        })
    )
    
    estado = forms.ChoiceField(
        required=False,
        label='Estado',
        choices=[('', 'Todos')] + Empleado.ESTADO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    departamento = forms.ModelChoiceField(
        required=False,
        label='Departamento',
        queryset=Departamento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    supervisor = forms.ModelChoiceField(
        required=False,
        label='Supervisor',
        queryset=User.objects.filter(empleados_supervisados__isnull=False).distinct(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

