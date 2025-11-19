# en dashboard/admin.py

from django.contrib import admin
from .models import Rol, Contacto  # <-- 1. Importa tus modelos

# 2. Registra los modelos para que aparezcan en el admin
admin.site.register(Rol)
admin.site.register(Contacto)