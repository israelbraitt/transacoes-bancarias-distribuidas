from django.db import models
from django.utils import timezone
from random import randint
import calendar, time

class Conta(models.Model):
    '''
    Representa uma conta bancária

        Atributos:
            id (str): código de identificação da conta (também serve para identificar o banco responsável)
            titular (str): nome do titular da conta
            tipo (int): tipo da conta
                        1 -> individual
                        2 -> conjunta
            saldo (float): valor disponível na conta
            transacoes (list): lista de transações realizadas pela conta
            banco (str): banco no qual a conta está associada
    '''
    id = models.CharField(max_length=10, primary_key=True)
    titular = models.CharField(max_length=70)
    tipo = models.IntegerField()
    saldo = models.FloatField()
    transacoes = []
    banco = models.CharField(max_length=5)
    
    def __init__(self, titular, tipo):
        self.id = "ABC" + str(randint(0000000, 9999999))
        self.titular = titular
        if (tipo == 1 or tipo == 2):
            self.tipo = tipo
        self.banco = "A"

    def __str__(self):
        return self.id
    
class Transacao(models.Model):
    '''
    Transação bancária realizada entre contas

        Atributos:
            conta_origem (str): id da conta de origem da transação
            conta_destino (str): id da conta de destino da transação
            valor (int): valor da transferência realizada
            data_hora (datetime): data e hora da transação
    '''
    banco_inicial = models.IntegerField(default=100)
    banco_origem = models.IntegerField(default=100)
    banco_destino = models.IntegerField(default=100)
    conta_origem = models.CharField(max_length=10)
    conta_destino = models.CharField(max_length=10)
    valor = models.FloatField(default=0.1)
    timestamp = models.IntegerField(default=1)

    '''
    def __init__(self, banco_inicial, banco_origem, banco_destino, conta_origem, conta_destino, valor, timestamp):
        self.banco_inicial = banco_inicial
        self.banco_origem = banco_origem
        self.banco_destino = banco_destino
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino
        self.valor = valor
        self.timestamp = timestamp
    '''