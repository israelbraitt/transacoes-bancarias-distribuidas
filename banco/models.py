from django.db import models
from random import randint

class Conta(models.Model):
    '''
    Representa uma conta bancária

        Atributos:
            id (str): código de identificação da conta (também serve para identificar o banco responsável)
            titular (str): nome do titular da conta
            tipo (int): tipo da conta
                        1 -> individual
                        2 -> conjunta
            transacoes (list): lista de transações realizadas pela conta
    '''
    id = models.CharField(max_length=10)
    titular = models.CharField(max_length=70)
    tipo = models.IntegerField()
    transacoes = []
    
    def __init__(self, titular, tipo):
        self.id = "ABC" + str(randint(0000000, 9999999))
        self.titular = titular
        if (tipo == 1 or tipo == 2):
            self.tipo = tipo

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
    conta_origem = models.CharField(max_length=10)
    conta_destino = models.CharField(max_length=10)
    valor = models.IntegerField()
    data_hora = models.DateTimeField()
    
    def __init__(self, conta_origem, conta_destino, valor, data_hora):
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino
        self.valor = valor
        self.data_hora = data_hora
