from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('conta')
        else:
            messages.success(request, ("Ocorreu um erro no login, tente novamente..."))
            return redirect('login')
    else:
        return render(request, 'usuarios/login.html')