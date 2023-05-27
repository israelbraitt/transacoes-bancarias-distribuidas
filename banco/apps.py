from django.apps import AppConfig
import threading
import socket
import json

class BancoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banco'

class LamportAlgorithm():
    """
    Algoritmo Lamport Timestamps.
    """
    my_socket = None
    my_host = "127.0.0.1"
    my_port = "8000"
    socket_list = [("banco_y", "127.0.0.1", "9000"), ("banco_z", "127.0.0.1", "10000")]

    lamport_time = 0

    def __init__(self):
        my_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        server_address = (self.my_host, self.my_port)
        socket.bind(server_address)
        socket.listen()
    
    def connections(self):
        socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)

        for banco_address in self.socket_list:
            banco = banco_address[0]
            host = banco_address[1]
            port = banco_address[2]
            try:
                socket.bind((host, port))
                socket.listen()
            except:
                return print("Não foi possível se conectar ao banco: " + banco)

            conn_client_tcp, addr_client_tcp = socket.accept()
            print("Conectado com um banco em: ", addr_client_tcp)

            thread_tcp = threading.Thread(target=self.threat_messages, args=[conn_client_tcp])
            thread_tcp.start()
    
    def calc_recv_timestamp(self, recv_timestamp, counter):
        """
        Calcula o novo timestamp quando um processo recebe uma mensagem.
        """
        return max(recv_timestamp, counter) + 1

    def send_messages(self, message):
        pass

    def threat_messages(self, connection):
        message = connection.recv(1024).decode(self.format)
        message = str(message)
        
        if message:
            message = json.loads(message)
            print("MENSAGEM RECEBIDA")
            print(message)
            response = None

            if message.get("timestamp"):
                timestamp = message.get("timestamp")
                self.calc_recv_timestamp(timestamp, self.lamport_time)
                self.send_messages(msg)
            
            elif message.get("payload"):
                payload = message.get("payload")
                response = self.updateStation(message)

            if response:
                print(f"ENVIANDO RESPOSTA: \n{response}")
                connection.send(response.encode(self.format))

    def main(self):
        pass