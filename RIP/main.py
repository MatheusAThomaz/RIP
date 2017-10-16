import message
import threading
import socket
import pickle
import copy
import time
import os

class MyThread (threading.Thread):

    def __init__(self, nd):

        threading.Thread.__init__(self)
        self.nd = nd
        self.id = id
        # self.name = name
        # self.counter = counter

    def run(self):
        if self.nd.pid == 0:
            rtinit0(self.nd)

        elif self.nd.pid == 1:
            rtinit1(self.nd)

        elif self.nd.pid == 2:
            rtinit2(self.nd)

        elif self.nd.pid == 3:
            rtinit3(self.nd)

class Node:

    def __init__(self, pid, host, port):
        self.pid = pid
        self.vizinhos = []
        self.distancias = []
        self.host = host
        self.port = port


    def set_vizinhos(self, distancia):
        self.vizinhos = distancia

    def set_distancias(self, distancia):
        self.distancias = [distancia[0], distancia[1], distancia[2], distancia[3]]

    def receive(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (self.host, self.port)
        tcp.bind(orig)
        tcp.listen(1)


        while True:

                    con, cliente = self.tcp_accept(tcp)

                    while True:
                        msg = con.recv(1024)
                        if msg:
                            msg_loaded = pickle.loads(msg)
                            new_m = copy.copy(msg_loaded)

                        if not msg: break

                    con.close()



host = '192.168.0.101'
process_number = 0
p = [Node(process_number, host, 5000),
     Node(process_number + 1, host, 5001),
     Node(process_number + 2, host, 5002),
     Node(process_number + 3, host, 5004)]


def rtinit0(nd):
    print("Entrou no init 0")
    nd.set_distancias([0, 1, 3, 7])
    nd.set_vizinhos([1, 2, 3])

    print("Distância de 0 até o vizinho 1 é: " , p[0].distancias[1])
    print("Distância de 0 até o vizinho 2 é: " , p[0].distancias[2])
    print("Distância de 0 até o vizinho 3 é: " , p[0].distancias[3])

def rtinit1(nd):
    print("Entrou no init 1")
    nd.set_distancias([1, 0, 1, 999])
    nd.set_vizinhos([0, 2])

    print("Distância de 1 até o vizinho 0 é: " , p[0].distancias[0])
    print("Distância de 1 até o vizinho 2 é: " , p[0].distancias[2])
    print("Distância de 1 até o vizinho 3 é: " , p[0].distancias[3])

def rtinit2(nd):
    print("Entrou no init 2")
    nd.set_distancias([3, 1, 0, 2])
    nd.set_vizinhos([0, 1, 3])

    print("Distância de 2 até o vizinho 0 é: " , p[0].distancias[0])
    print("Distância de 2 até o vizinho 1 é: " , p[0].distancias[1])
    print("Distância de 2 até o vizinho 3 é: " , p[0].distancias[3])

def rtinit3(nd):
    print("Entrou no init 3")
    nd.set_distancias([7, 999, 2, 0])
    nd.set_vizinhos([0, 2])


    print("Distância de 3 até o vizinho 0 é: " , p[0].distancias[0])
    print("Distância de 3 até o vizinho 1 é: " , p[0].distancias[1])
    print("Distância de 3 até o vizinho 2 é: " , p[0].distancias[2])

def send_request(nd):

        for nos in nd.vizinhos:
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp.connect((host, p[nos].port))
                mensagem = message.Message(nd.pid, nos, nd.distancias)
                m_dumped = pickle.dumps(mensagem)
                tcp.send(m_dumped)

                tcp.close()

thread1 = MyThread(p[0])
thread2 = MyThread(p[1])
thread3 = MyThread(p[2])
thread4 = MyThread(p[3])

thread1.start()
thread2.start()
thread3.start()
thread4.start()





