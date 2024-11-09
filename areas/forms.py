from django import forms
from .models import Area, Puerta, Zona

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'descripcion','zonas','activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la área'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción de la área' }),
            'zonas': forms.SelectMultiple(attrs={'class':'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class':'form-check-input m-auto mt-1'})
        }

class PuertaForm(forms.ModelForm):
    class Meta:
        model = Puerta
        fields = ['nombre', 'descripcion', 'areas', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la puerta'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción de la puerta' }),
            'areas': forms.SelectMultiple(attrs={'class':'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class':'form-check-input m-auto mt-1'})
        }

class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ['nombre', 'descripcion','activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la zona'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción de la zona' }),
            'activo': forms.CheckboxInput(attrs={'class':'form-check-input m-auto mt-1'})
        }