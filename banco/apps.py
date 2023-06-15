from django.apps import AppConfig
import threading
import socket
import json
import calendar, time

class BancoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banco'

class Transacao():
    def __init__(self, banco_origem, banco_destino, conta_origem, conta_destino, valor, timestamp):
        self.banco_origem = banco_origem
        self.banco_destino = banco_destino
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino
        self.valor = valor
        self.timestamp = timestamp

class Conta():
    def __init__(self, id, titular, saldo):
        self.id = id
        self.titular = titular
        self.saldo = saldo
        self.last_transfer = 0
    def cancel(self):
        self.saldo += self.last_transfer
        self.last_transfer = 0
    def transfer(self, valor):
        self.saldo += valor
        self.last_transfer = valor

accs = {"164": Conta("164", "Gui", 30.0), "10": Conta("10", "Hi", 78.5), "110": Conta("110", "George", 110.1)}
last_acc = None
transactions = []
my_port = 'http://172.16.103.8:8008/notificar'
banco_ports = {'7': 'http://172.16.103.7:8007/notificar', '5': 'http://172.16.103.5:8005/notificar', '8': 'http://172.16.103.8:8008/notificar'}
