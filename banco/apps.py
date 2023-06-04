from django.apps import AppConfig
import threading
import socket
import json
import calendar, time

class BancoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banco'

class LamportAlgorithm():
    """
    Algoritmo Lamport Timestamps.
    """
    def __init__(self, port=1743, bank_name="city slicker"):
        self.format = 'utf-8'
        self.host = "127.0.0.1"
        self.port = port

        self.host_header = 'Host: ' + self.host + ":" + str(self.port) + "\n"

        self.addr = (self.host, self.port)
        self.server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_tcp.bind(self.addr)

        self.bank_name = bank_name
        self.bank_conn = {}
        self.bank_addr = {"sneed": ("127.0.0.1", 4006), "chuck": ("127.0.0.1", 1459), "city slicker": ("127.0.0.1", 1743)}
        self.bank_timers = {}
        self.current_bank = None

        # socket_list = [("banco_y", "127.0.0.1", "9000"), ("banco_z", "127.0.0.1", "10000")]

        lamport_time = 0


    def start_server(self):
        """
        Cria o socket para ser or servidor do banco
        """
        self.server_tcp.listen()
        while True:
            conn, addr = self.server_tcp.accept()
            bank_thread = threading.Thread(target=self.treat_bank, args=[conn, addr])

    def link_bank(self, addr):
        """
        Cria um socket para se conectar com um servidor de outro banco
        """
        try:
            print(addr)
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_socket.connect(addr)
            self.bank_conn[addr[1]] = new_socket
            print("Conectado.")
        except Exception as e:
            print(e)

    def treat_bank(self, conn, addr):
        """
        Estabelece a comunicação entre o servidor deste banco e o socket de outro banco
        """
        print(conn)
        print(addr)
        session_vars = {}
        connected = True
        while connected:
            msg = conn.recv(1024).decode(self.format)
            msg = str(msg)
            if msg:
                print(f"\n==={addr} ENVIOU A REQUEST:===\n{msg}")
                route, param = self.translate(msg)
                api_method = hasattr(self, route)

                if api_method:
                    api_call = getattr(self, route)
                    response = api_call(param, session_vars)

    def alert_banks(self, message):
        """
        Envia mensagens com timestamp para todos os outros bancos
        """

        banks_alerted = 0

        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        time_stamp += 1

        for name, bank in self.bank_addr.items():
            if bank[1] != self.port:
                bank_socket = self.bank_conn.get(name)
                if bank_socket:
                    bank_socket.send(message.encode(self.format))


    def translate(self, message):
        if message.startswith("P"):  # POST OR PUT
            # print("decoding p")
            message = message.split("{")

            header = message[0]
            route = header.split("HTTP")[0]
            route = route.replace(" /", "_")
            route = route.replace(" ", "")

            param = message[1]
            param = "{" + param
            param = json.loads(param)

        elif message.startswith("G"):  # GET
            message = message.split("HTTP")
            header = message[0]
            route = header.split("HTTP")[0]
            route = route.replace(" /", "_")
            route = route.replace(" ", "")
            param = {}

        return route, param

    def POST_insertOperation(self, param, session):
        bank_name = param.get("bank_name")
        timestamp = param.get("timestamp")

        status = 'HTTP/1.1 200 OK\n'
        response_body = '{\"resultado\": \"Timestamp recebido.\"}'

        if timestamp and bank_name:
            pass

    def response_insertOperation(self, response):
        pass

    
    def calc_recv_timestamp(self, recv_timestamp, counter):
        """
        Calcula o novo timestamp quando um processo recebe uma mensagem.
        """
        return max(recv_timestamp, counter) + 1

    def send_messages(self, message):
        pass

    def main(self):
        pass
