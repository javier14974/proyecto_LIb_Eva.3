from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.text import slugify

# ============================================================
#   MODELO: Usuario
#   Extiende el modelo User de Django con datos adicionales.
# ============================================================
class Usuario(models.Model):  # alumno/docente

    # Relación 1 a 1 con el usuario de Django (username, password, email)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Información adicional del usuario
    carrera = models.CharField(max_length=50, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    universidad = models.CharField(max_length=100, null=True, blank=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)  # Fecha en que se registró

    # Roles permitidos dentro de la plataforma
    ROL_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
    ]

    # Campo obligatorio que define el rol del usuario
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        # Lo que aparece cuando se imprime o lista el usuario
        return self.user.username



# ============================================================
#   Funciones de rutas personalizadas para guardar archivos
# ============================================================

# Ruta donde se guardan los apuntes subidos
def ruta_subida_apuntes(instance, filename):
    email = instance.usuario.user.email
    safe_email = slugify(email)  # Convierte el email en texto seguro para URLs
    safe_filename = slugify(os.path.splitext(filename)[0]) + os.path.splitext(filename)[1]
    return f"apuntes/{safe_email}/{safe_filename}"

# Ruta donde se guardan las imágenes asociadas al apunte
def ruta_subida_imagen(instance, filename):
    email = instance.usuario.user.email
    safe_email = slugify(email)
    safe_filename = slugify(os.path.splitext(filename)[0]) + os.path.splitext(filename)[1]
    return f"apuntes/{safe_email}/imagenes/{safe_filename}"



# ============================================================
#   MODELO: Apunte
#   Representa un archivo subido por el usuario (PDF o Word),
#   con información como título, descripción y categorización.
# ============================================================
class Apunte(models.Model):

    # Usuario al que pertenece el apunte
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    titulo = models.CharField(max_length=40)
    descripcion = models.TextField(blank=True, null=True, max_length=100)
    carrera = models.TextField(blank=True, null=True, max_length=30)     # Carrera asociada al apunte
    asignatura = models.TextField(blank=True, null=True, max_length=40)  # Materia correspondiente

    # Archivos asociados
    archivo = models.FileField(upload_to=ruta_subida_apuntes)
    imagen = models.ImageField(upload_to=ruta_subida_imagen, default="default_apunte.jpg")

    fecha_subida = models.DateTimeField(auto_now_add=True)  # Fecha automática de subida



# ============================================================
#   MODELO: ApunteCompartido
#   Guarda con quién fue compartido un apunte.
# ============================================================
class ApunteCompartido(models.Model):

    apunte = models.ForeignKey(Apunte, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuario que recibe el apunte
    fecha_compartido = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Impide que un mismo apunte sea compartido 2 veces con la misma persona
        unique_together = ('apunte', 'usuario')

    def __str__(self):
        return f"{self.apunte.titulo} → {self.usuario.user.username}"



# ============================================================
#   MODELO: ApunteCalificacion
#   Sistema de calificación (1 a 5) de los apuntes.
# ============================================================
class ApunteCalificacion(models.Model):

    apunte = models.ForeignKey(Apunte, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    calificacion = models.PositiveIntegerField()  # Valor entre 1 y 5
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Un usuario solo puede calificar una vez cada apunte
        unique_together = ('apunte', 'usuario')

    def __str__(self):
        return f"{self.usuario.user.username} califica {self.apunte.titulo}: {self.calificacion}"
