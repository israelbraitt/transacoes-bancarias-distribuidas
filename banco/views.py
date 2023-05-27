from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'banco/home.html')

def login(request):
    return render(request, 'banco/home.html')

def conta(request):
    context = {
        # fazer conexão da lista de transações de uma conta
        'transacoes': 123,
        'conta': "A"
    }
    return render(request, 'banco/conta.html', context)
