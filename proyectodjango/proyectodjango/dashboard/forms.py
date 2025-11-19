from django import forms
from .models import Campania, Rol, Contacto, Conversacion, Mensaje

tailwind_input_classes = 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'


class RoleForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['rol', 'servicio', 'region']  # ✅ se agrega 'region'

        widgets = {
            'rol': forms.TextInput(attrs={
                'class': tailwind_input_classes,
                'placeholder': 'Nombre del Rol'
            }),
            'servicio': forms.URLInput(attrs={
                'class': tailwind_input_classes,
                'placeholder': 'https://mi-servicio.com'
            }),
            'region': forms.Select(attrs={
                'class': tailwind_input_classes
            }),
        }


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'rol', 'telefono', 'correo', 'idRol', 'descripcion']  # ✅ nuevos campos

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': tailwind_input_classes,
                'placeholder': 'Nombre completo'
            }),
            'rol': forms.Select(attrs={
                'class': tailwind_input_classes
            }),
            'telefono': forms.TextInput(attrs={
                'class': tailwind_input_classes,
                'placeholder': 'Ej. +504 31821111'
            }),
            'correo': forms.EmailInput(attrs={
                'class': tailwind_input_classes,
                'placeholder': 'Correo electrónico'
            }),
            'idRol': forms.NumberInput(attrs={
                'class': tailwind_input_classes,
                'placeholder': 'ID del Rol existente'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': tailwind_input_classes,
                'placeholder': 'Descripción del contacto (opcional)',
                'rows': 3
            }),
        }


class ConversacionForm(forms.ModelForm):
    class Meta:
        model = Conversacion
        fields = ['contacto', 'ultimo_mensaje', 'mensajes_enviados', 'conversacion_anterior']
        widgets = {
            'ultimo_mensaje': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'mensajes_enviados': forms.NumberInput(attrs={'class': 'form-control'}),
            'contacto': forms.Select(attrs={'class': 'form-control'}),
            'conversacion_anterior': forms.Select(attrs={'class': 'form-control'}),
        }


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['texto']
        widgets = {
            'texto': forms.TextInput(attrs={
                'class': 'form-control w-full rounded-lg border-gray-300',
                'placeholder': 'Escribe un mensaje...',
                'autocomplete': 'off'
            }),
        }



class CampaniaForm(forms.ModelForm):
    class Meta:
        model = Campania
        fields = [
            'encabezado', 'descripcion', 'arte', 'accion',
            'fechaProgramada', 'exclusiones'
        ]
        widgets = {
            'encabezado': forms.TextInput(attrs={
                'class': tailwind_input_classes,
                'placeholder': 'Título de la campaña'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': tailwind_input_classes,
                'rows': 4,
                'placeholder': 'Escribe el contenido de la campaña'
            }),
            'arte': forms.ClearableFileInput(attrs={
                'class': tailwind_input_classes
            }),
            'accion': forms.URLInput(attrs={
                'class': tailwind_input_classes,
                'placeholder': 'https://mi-accion.com'
            }),
            'fechaProgramada': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': tailwind_input_classes
            }),
            'exclusiones': forms.SelectMultiple(attrs={
                'class': tailwind_input_classes
            }),
        }
