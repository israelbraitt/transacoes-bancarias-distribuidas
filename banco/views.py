from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def home(request):
    return render(request, 'banco/home.html')

@csrf_protect
def conta(request):
    
    context = {
        
    }

    return render(request, 'banco/conta.html', context)

@csrf_protect
def form_transferencia(request):

    context = {}

    if request.method == "POST":

        erros = {}

        conta_origem = request.POST.get('conta_origem', None)
        conta_destino = request.POST.get('conta_destino', None)
        valor = request.POST.get('valor', None)

        if not isinstance(valor, int):
            erros['valor'] = "O valor não possui o tipo esperado"

        if erros:
            context['erros'] = erros
            context['conta_origem'] = conta_origem
            context['conta_destino'] = conta_destino
            context['valor'] = valor
        else:
            context['mensagem'] = "Os dados foram salvos com sucesso"
        
        return render(request, 'banco/transferencia.html', context)