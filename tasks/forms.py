from django.forms import ModelForm #Aqui se crean formularios a partir de las tablas(modelos)
from .models import Task
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','importnat']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write a title'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Write a description' }),
            'importnat':forms.CheckboxInput(attrs={'class':'form-check-input m-auto mt-1'})
        }