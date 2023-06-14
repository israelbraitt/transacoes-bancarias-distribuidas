from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import banco.apps as my_apps
import calendar, time
import json
import requests


@csrf_protect
def home(request):
    return render(request, 'banco/home.html')

@csrf_protect
def cadastro(request):
    return render(request, 'banco/cadastro.html')

@csrf_protect
def conta(request):

    context = {
        "id": 1,
        "titular": "sneed",
        "saldo": 300.60
    }
    return render(request, 'banco/conta.html', context)

@csrf_protect
def form_transferencia(request):

    context = {

    }
    return render(request, 'banco/transferencia.html', context)


@csrf_protect
def efetuar_transferencia(request):

    context = {}

    current_GMT = time.gmtime()
    timestamp = calendar.timegm(current_GMT)
    timestamp += 1
    erros = {}

    if request.method == "POST":

        notified = True
        conta_origem = request.POST.get('conta_origem', None)
        origem_split = conta_origem.split("-")

        if len(origem_split) > 2:
            erros['origem'] = "Conta de origem inválida."

        banco_origem = origem_split[0]
        addr_1 = my_apps.banco_ports.get(banco_origem)

        conta_destino = request.POST.get('conta_destino', None)
        destino_split = conta_destino.split("-")
        banco_destino = destino_split[0]
        addr_2 = my_apps.banco_ports.get(banco_destino)

        valor = request.POST.get('valor', None)

        if addr_1 and addr_2:
            payload = {'operation': "new", 'timestamp': timestamp}
            for port in my_apps.banco_ports.values():
                if port != my_apps.my_port:
                    response = request.post(port, data=payload)
                    if response != "Success":
                        notified = False
                        break
            if notified:
                    my_apps.transactions.append(timestamp)
                    my_apps.transactions.sort()
                    for i in range(3):
                        if my_apps.transactions[0] == timestamp:
                            payload_o = {'operation': "sub", 'acc': origem_split[1], 'valor': valor}
                            port_o = my_apps.banco_ports.get(addr_1)
                            response_o = request.post(port_o, data=payload_o)

                            payload_d = {'operation': "sub", 'acc': origem_split[1], 'valor': valor}
                            port_d = my_apps.banco_ports.get(addr_2)
                            response_d = request.post(port_d, data=payload_d)

                            if response_o == "Success" and response_d == "Success":
                                my_apps.transactions.remove(timestamp)
                                context['mensagem'] = "Transferência feita com sucesso."
                        else:
                            time.sleep(1)
        else:
            pass

        return render(request, 'banco/transferencia.html', context)

    else:

        return render(request, 'banco/transferencia.html', context)
@csrf_protect
def notificar(request):
    body = request.body.decode('utf-8')
    payload = json.loads(body)
    operation = payload.get('operation')
    rp = HttpResponse("Invalid operation.")

    match operation:
        case "new":
            new_time = payload.get('timestamp')
            if new_time:
                my_apps.transactions.append(new_time)
                my_apps.transactions.sort()
                rp = HttpResponse("Success.")
            else:
                rp = HttpResponse("No timestamp.")
        case "add":
            acc = payload.get('acc')
            valor = payload.get('valor')
            if acc and valor:
                rp = HttpResponse("Sucess.")
        case "sub":
            acc = payload.get('acc')
            valor = payload.get('valor')
            if acc and valor:
                rp = HttpResponse("Sucess.")


    print(rp)
    return rp

