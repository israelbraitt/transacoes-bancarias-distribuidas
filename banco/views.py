from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import banco.models
import banco.apps as my_apps
import calendar, time
import json
import requests


@csrf_exempt
def home(request):
    return render(request, 'banco/home.html')

@csrf_exempt
def cadastro(request):
    return render(request, 'banco/cadastro.html')

@csrf_exempt
def conta(request):

    acc = my_apps.accs.get("164")
    context = {
        "id": acc.id,
        "titular": acc.titular,
        "saldo": acc.saldo
    }
    return render(request, 'banco/conta.html', context)

@csrf_exempt
def form_transferencia(request):

    context = {

    }
    return render(request, 'banco/transferencia.html', context)


@csrf_exempt
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

        valor = int(request.POST.get('valor', None))

        if addr_1 and addr_2:
            print("NOTIFICANDO OUTROS BANCOS")
            payload = {'operation': 'new', 'timestamp': timestamp}
            for port in my_apps.banco_ports.values():
                if port != my_apps.my_port:
                    response = requests.post(port, json=payload)
                    response = response.content.decode('utf-8')
                    print("RESPOSTA DE OUTRO BANCO")
                    print(response)
                    if response != "Sucesso.":
                        print("FALHA NA NOTIFICAÇÃO")
                        notified = False

            if notified:
                    print("BANCOS NOTIFICADOS")
                    my_apps.transactions.append(timestamp)
                    my_apps.transactions.sort()
                    print(my_apps.transactions)
                    for i in range(3):
                        if my_apps.transactions[0] == timestamp:
                            print("RETIRANDO DINHEIRO DA PRIMEIRA CONTA")
                            print(origem_split)
                            port_o = my_apps.banco_ports.get(origem_split[0])
                            print(port_o)
                            payload_o = {'operation': 'sub', 'acc': origem_split[1], 'valor': valor}

                            if port_o != my_apps.my_port:
                                response_o = requests.post(port_o, json=payload_o)
                                response_o = response_o.content.decode('utf-8')
                            else:
                                acc = my_apps.accs.get(origem_split[1])
                                sub_transaction(acc, valor)
                                response_o = "Sucesso."

                            print("ADICIONANDO DINHEIRO NA SEGUNDA CONTA")
                            print(destino_split)
                            port_d = my_apps.banco_ports.get(destino_split[0])
                            print(port_d)
                            payload_d = {'operation': 'add', 'acc': destino_split[1], 'valor': valor}

                            if port_d != my_apps.my_port:
                                response_d = requests.post(port_d, json=payload_d)
                                response_d = response_d.content.decode('utf-8')
                            else:
                                acc = my_apps.accs.get(destino_split[1])
                                add_transaction(acc, valor)
                                response_d = "Sucesso."

                            if response_o == "Sucesso." and response_d == "Sucesso.":
                                print("SUCESSO")
                                context['mensagem'] = "Transferência feita com sucesso."
                                for port in my_apps.banco_ports.values():
                                    if port != my_apps.my_port:
                                        payload_finish = {'operation': 'done', 'timestamp': timestamp}
                                        response_finish = requests.post(port, json=payload_finish)
                                        response_finish = response_finish.content.decode('utf-8')
                            else:
                                print("FALHA")
                                context['mensagem'] = "Transferência não realizada."
                                for port in my_apps.banco_ports.values():
                                    if port != my_apps.my_port:
                                        payload_cancel = {'operation': 'cancel', 'timestamp': timestamp}
                                        response_cancel = requests.post(port, json=payload_cancel)
                                        response_cancel = response_cancel.content.decode('utf-8')
                            break
                        else:
                            print("FILA CHEIA.")
                            time.sleep(1)
                    my_apps.transactions.remove(timestamp)
                    my_apps.transactions.sort()
        else:
            erros['bancos'] = "Conta inválida."

        return render(request, 'banco/transferencia.html', context)

    else:

        return render(request, 'banco/transferencia.html', context)

@csrf_exempt
def notificar(request):
    body = request.body.decode('utf-8')
    print("BODY")
    print(body)
    payload = json.loads(body)
    print("PAYLOAD")
    print(payload)
    operation = payload.get('operation')
    rp = HttpResponse("Invalid operation.")

    match operation:
        case 'new':
            new_time = payload.get('timestamp')
            if new_time:
                new_transaction(new_time)
                rp = HttpResponse("Sucesso.")
            else:
                rp = HttpResponse("Sem timestamp.")
        case 'add':
            acc_id = payload.get('acc')
            valor = payload.get('valor')
            if acc_id and valor:
                acc = my_apps.accs.get(acc_id)
                if acc:
                    add_transaction(acc, valor)
                    rp = HttpResponse("Sucesso.")
                else:
                    rp = HttpResponse("Conta não existe.")
        case 'sub':
            acc_id = payload.get('acc')
            valor = payload.get('valor')
            if acc_id and valor:
                acc = my_apps.accs.get(acc_id)
                if acc:
                    if acc.saldo >= valor:
                        sub_transaction(acc, valor)
                        rp = HttpResponse("Sucesso.")
                    else:
                        rp = HttpResponse("Saldo insuficiente.")
                else:
                    rp = HttpResponse("Conta não existe.")
        case 'done':
            old_time = payload.get('timestamp')
            if old_time:
                if old_time in my_apps.transactions:
                    my_apps.transactions.remove(old_time)
                    my_apps.transactions.sort()
                my_apps.last_acc = None
                rp = HttpResponse("Sucesso.")
            else:
                rp = HttpResponse("Sem timestamp.")
        case 'cancel':
            old_time = payload.get('timestamp')
            if old_time:
                if old_time in my_apps.transactions:
                    my_apps.transactions.remove(old_time)
                    my_apps.transactions.sort()
                if my_apps.last_acc:
                    my_apps.last_acc.cancel()
                    my_apps.transactions.sort()
                    my_apps.last_acc = None
                rp = HttpResponse("Operação cancelada por erro em um dos bancos.")
            else:
                rp = HttpResponse("Sem timestamp.")

    print("RESPONSE")
    print(rp)
    return rp

def new_transaction(timestamp):
    my_apps.transactions.append(timestamp)
    my_apps.transactions.sort()

def add_transaction(acc, valor):
    acc.transfer(abs(valor))
    my_apps.last_acc = acc

def sub_transaction(acc, valor):
    acc.transfer(-abs(valor))
    my_apps.last_acc = acc



@csrf_exempt
def inserir_conta(request):
    if request.method == "POST":
        id = request.POST.get("id")
        titular = request.POST.get("titular")
        saldo = request.POST.get("saldo")

        if id and titular and saldo:
            new_conta = my_apps.Conta(id, titular, saldo)
            my_apps.accs[id] = new_conta
            print(my_apps.accs)
            return HttpResponse("Success.")
        else:
            return HttpResponse("Campo faltando.")