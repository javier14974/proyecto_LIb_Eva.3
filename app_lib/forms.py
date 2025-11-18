from django import forms
from .models import *
from django.contrib.auth.models import User



class registrarUsuario(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  #solo djgango no se reflejaran en la base de datos
    email = forms.CharField()



    class Meta:
        model = Usuario
        fields = ['carrera', 'ciudad', 'universidad', 'edad', 'rol']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este usuario ya existe.")
        return username

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
        )
        usuario = super().save(commit=False)
        usuario.user = user
        if commit:
            usuario.save()
        return usuario








class subir_apuntes_forms(forms.ModelForm):
    class Meta:
        model = Apunte
        fields = ['titulo', 'descripcion', 'archivo', 'asignatura', 'carrera']


