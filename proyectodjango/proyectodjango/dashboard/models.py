from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, URLValidator, MaxLengthValidator


class Rol(models.Model):
    class Regiones(models.TextChoices):
        IMHN = 'IMHN', 'IMHN'
        IMGT = 'IMGT', 'IMGT'
        IMCR = 'IMCR', 'IMCR'
        IMSL = 'IMSL', 'IMSL'
        CA = 'CA', 'CA'
        
    rol = models.CharField(max_length=100)
    servicio = models.URLField(max_length=200)

    region = models.CharField(
        max_length=10,
        choices=Regiones.choices,    
        default=Regiones.IMHN,        
        help_text="Región"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return f"{self.rol} - {self.region}"


class Contacto(models.Model):
    nombre = models.CharField(max_length=200)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    telefono = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{3,4}[-\s]?\d{4,}$',
                message="Formato inválido. Ejemplo: +504 31821111"
            )
        ],
        help_text="Ejemplo: +504 31821111",
        blank=True, null=True, default=''
    )
    correo = models.EmailField(
        max_length=254,
        blank=True, null=True, default=''
    )
    idRol = models.PositiveIntegerField(
        help_text="Ingrese el ID de un rol existente",
        blank=True, null=True, default=0
    )
    descripcion = models.TextField(
        blank=True, null=True, default=''
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Conversacion(models.Model):
    contacto = models.ForeignKey('Contacto', on_delete=models.CASCADE, related_name='conversaciones')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_mensaje = models.DateTimeField(default=timezone.now)
    mensajes_enviados = models.PositiveIntegerField(default=0)
    conversacion_anterior = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='siguiente_conversacion')

    def __str__(self):
        return f"Conversación {self.id} - {self.contacto.nombre}"

    class Meta:
        verbose_name = "Conversación"
        verbose_name_plural = "Conversaciones"
        ordering = ['-fecha_creacion']


class Mensaje(models.Model):
    REMITENTE_CHOICES = [
        ('usuario', 'Usuario'),
        ('bot', 'Bot'),
    ]

    conversacion = models.ForeignKey('Conversacion', on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.CharField(max_length=10, choices=REMITENTE_CHOICES)
    texto = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.remitente}: {self.texto[:30]}"
    
    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"
        ordering = ['fecha_envio']


# === CAMPAÑAS ===
class Campania(models.Model):
    encabezado = models.CharField(max_length=200)
    descripcion = models.TextField()
    arte = models.FileField(upload_to='campanias/', null=True, blank=True)
    accion = models.URLField(max_length=300, null=True, blank=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)
    fechaProgramada = models.DateTimeField(null=True, blank=True)
    exclusiones = models.ManyToManyField(Contacto, blank=True, null=True)

    def __str__(self):
        return self.encabezado

