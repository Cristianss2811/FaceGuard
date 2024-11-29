from django import forms
from .models import Roles, Profile


class RolesForm(forms.ModelForm):
    class Meta:
        model = Roles
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rol'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del rol'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto mt-1'})
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'nombre', 'apellido_p', 'apellido_m', 'fecha_nacimiento',
            'sexo', 'nss', 'telefono', 'direccion', 'estado', 'ciudad'
        ]