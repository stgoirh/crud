from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.template import loader
from django.contrib.auth.models import User

def index(request):
    return render(request, 'crud/index.html')

def registro(request):
    return render(request, 'crud/registro.html')

def registrarUsuario(request):
    usuario = request.POST['usuario']
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.create_user(username=usuario, email=email, password=password)
    return render(request, 'crud/index.html')