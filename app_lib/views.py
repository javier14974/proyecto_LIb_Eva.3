from django.shortcuts import render, get_object_or_404
from .forms import *
import os
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, 'login.html')


# Create your views here.

def home(request):
    apuntes = Apunte.objects.all()  # todos los apuntes
    return render(request, 'template/home.html', {'apuntes': apuntes})


def agregar_usuario(request):
    if request.method == 'POST':
        form = registrarUsuario(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = registrarUsuario()

    return render(request, 'template/agregar_usuario.html', {'form': form})



@login_required
def subir_apunte(request):
    if request.method == 'POST':
        form = subir_apuntes_forms(request.POST, request.FILES)
        if form.is_valid():
            apunte = form.save(commit=False)
            apunte.usuario = request.user.usuario  # asigna el usuario logiado
            apunte.save()
            return redirect('home')
    else:
        form = subir_apuntes_forms()

    return render(request, 'template/subir_apunte.html', {'form': form})

def login_vista(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, 'template/login.html')


def logout_vista(request):
    logout(request)
    return redirect('login')




def detalle_apunte(request, apunte_id):
    apunte = get_object_or_404(Apunte, id=apunte_id)
    usuario_actual = request.user.usuario  # tu usuario logueado

    if request.method == "POST":
        calificacion = int(request.POST.get("calificacion", 0))
        if 1 <= calificacion <= 5:
            # Crear o actualizar calificación
            obj, created = ApunteCalificacion.objects.update_or_create(
                apunte=apunte,
                usuario=usuario_actual,
                defaults={"calificacion": calificacion}
            )
        return redirect('detalle_apunte', apunte_id=apunte.id)

    # Promedio de calificaciones
    promedio = ApunteCalificacion.objects.filter(apunte=apunte).aggregate(models.Avg('calificacion'))['calificacion__avg']

    return render(request, 'template/detalle_apunte.html', {
        'apunte': apunte,
        'promedio': promedio or 0
    })




