from django import forms
from .models import Area, Puerta

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'descripcion','activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la área'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción de la área' }),
            'activo': forms.CheckboxInput(attrs={'class':'form-check-input m-auto mt-1'})
        }

class PuertaForm(forms.ModelForm):
    class Meta:
        model = Puerta
        fields = ['nombre', 'descripcion', 'area', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la puerta'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción de la puerta' }),
            'area': forms.Select(attrs={'class':'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class':'form-check-input m-auto mt-1'})
        }