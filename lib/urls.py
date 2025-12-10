"""
URL configuration for lib project.

Este archivo controla todas las rutas (URLs) del proyecto.
Cada path() conecta una URL con una vista específica.
"""

from django.contrib import admin
from django.urls import path
from app_lib.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL del panel de administración de Django
    path('admin/', admin.site.urls),

    # Página principal (home)
    path('', home, name='home'),

    # Registrar nuevo usuario
    path('agregarUsuario/', agregar_usuario, name="agregar_usuario"),

    # Subir un apunte
    path('subir_apunte/', subir_apunte, name="subir_apunte"),

    # Login y logout
    path('login/', login_vista, name="login"),
    path('logout/', logout_vista, name='logout'),

    # Ver detalle de un apunte (por id)
    path('apunte/<int:apunte_id>/', detalle_apunte, name='detalle_apunte'),

    # Perfil de usuario
    path('perfil/<int:usuario_id>/', perfil_vista, name='perfil_vista'),

    # Eliminar y editar apuntes
    path('eliminar_apunte/<int:apunte_id>', eliminar_apunte, name='eliminar_apunte'),
    path('editar_apunte/<int:apunte_id>', editar_apunte, name='editar_apunte'),

    # Ver o generar el PDF de un apunte
    path("apunte/<int:apunte_id>/pdf/", pdf_apunte, name="pdf_apunte"),

    # Página "Nosotros"
    path("nosotros/", nosotros, name="nosotros"),

    # Compartir apuntes con otros usuarios
    path("compartir/<int:apunte_id>/", compartir_apunte, name="compartir_apunte"),
    path("compartir/<int:apunte_id>/<int:usuario_id>/hacer/", hacer_compartido, name="hacer_compartido"),

    # Eliminar un apunte compartido
    path('eliminar_compartido/<int:apunte_id>/', eliminar_compartido, name='eliminar_compartido'),

    # Rutas del panel de administrador personalizado
    path('login_admin/', login_admin, name='login_admin'),
    path('admin_home/', admin_home, name='admin_home'),
    path('todos_usuarios/', todos_usuarios, name='todos_usuarios'),
    path('eliminar_usuario/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),
]

# Configuración para servir archivos estáticos y media en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))
