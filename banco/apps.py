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

accs = {}
transactions = []
my_port = "http://localhost:8000/notificar"
banco_ports = {"164": "http://localhost:8000/notificar", "649": "http://localhost:8000/notificar", "114": "http://localhost:8000/notificar"}