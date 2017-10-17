import message
import threading
import socket
import pickle
import copy
import time
import os


class update_thread (threading.Thread):

    def __init__(self, vetor, id, did):

        threading.Thread.__init__(self)
        self.vetor = vetor
        self.id = id
        self.did = did

    def run(self):
        if self.did == 0:
            update0(self.vetor, self.id)

        elif self.did == 1:
            update1(self.vetor, self.id)

        elif self.did == 2:
            update2(self.vetor, self.id)

        elif self.did == 3:
            update3(self.vetor, self.id)

class MyThread2 (threading.Thread):

    def __init__(self, nd):

        threading.Thread.__init__(self)
        self.nd = nd

    def run(self):
        send_request(self.nd)



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


class MyThread3 (threading.Thread):

    def __init__(self, nd):

        threading.Thread.__init__(self)
        self.nd = nd
        # self.name = name
        # self.counter = counter

    def run(self):
        Node.receive(self.nd)

class Node:

    def __init__(self, pid, host, port):
        self.pid = pid
        self.vizinhos = []
        self.distancias = []
        self.host = host
        self.port = port
        thread = MyThread3(self)
        thread.start()


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
            con, cliente = tcp.accept()

            while True:
                msg = con.recv(1024)
                if msg:
                    msg_loaded = pickle.loads(msg)
                    new_m = copy.copy(msg_loaded)

                if not msg: break

                t1 = update_thread(new_m.distancias, new_m.sid, new_m.did)
                t1.start()
            con.close()



host = '127.0.0.1'
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

    send_request(p[0])

def rtinit1(nd):
    print("Entrou no init 1")
    nd.set_distancias([1, 0, 1, 999])
    nd.set_vizinhos([0, 2])

    print("Distância de 1 até o vizinho 0 é: " , p[1].distancias[0])
    print("Distância de 1 até o vizinho 2 é: " , p[1].distancias[2])
    print("Distância de 1 até o vizinho 3 é: " , p[1].distancias[3])

    send_request(p[1])

def rtinit2(nd):
    print("Entrou no init 2")
    nd.set_distancias([3, 1, 0, 2])
    nd.set_vizinhos([0, 1, 3])

    print("Distância de 2 até o vizinho 0 é: " , p[2].distancias[0])
    print("Distância de 2 até o vizinho 1 é: " , p[2].distancias[1])
    print("Distância de 2 até o vizinho 3 é: " , p[2].distancias[3])

    send_request(p[2])

def rtinit3(nd):
    print("Entrou no init 3")
    nd.set_distancias([7, 999, 2, 0])
    nd.set_vizinhos([0, 2])

    print("Distância de 3 até o vizinho 0 é: " , p[3].distancias[0])
    print("Distância de 3 até o vizinho 1 é: " , p[3].distancias[1])
    print("Distância de 3 até o vizinho 2 é: " , p[3].distancias[2])

    send_request(p[3])

def send_request(node):
    for no in node.vizinhos:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        tcp.connect((host, p[no].port))
        mensagem = message.Message(node.pid, no, node.distancias)
        m_dumped = pickle.dumps(mensagem)
        tcp.send(m_dumped)
        tcp.close()


def update0(vetor, id):
    time.sleep(2)
    change_control = False
    i = 0
    for no in p[0].distancias:
        if no > (vetor[i] + p[0].distancias[id]):
            p[0].distancias[i] = vetor[i] + p[0].distancias[id]
            change_control = True
        i+=1

    if change_control:
        print("Distância update de 0 até o vizinho 1 é: ", p[0].distancias[1])
        print("Distância update de 0 até o vizinho 2 é: ", p[0].distancias[2])
        print("Distância update de 0 até o vizinho 3 é: ", p[0].distancias[3])
        print("")
        send_request(p[0])


def update1(vetor, id):
    time.sleep(2)
    change_control = False
    i = 0
    for no in p[1].distancias:
        if no > (vetor[i] + p[1].distancias[id]):
            p[1].distancias[i] = vetor[i] + p[1].distancias[id]
            change_control = True
        i+=1

    if change_control:
        print("Distância update de 1 até o vizinho 0 é: ", p[1].distancias[0])
        print("Distância update de 1 até o vizinho 2 é: ", p[1].distancias[2])
        print("Distância update de 1 até o vizinho 3 é: ", p[1].distancias[3])
        print("")
        send_request(p[1])

def update2(vetor, id):
    time.sleep(2)
    change_control = False
    i = 0
    for no in p[2].distancias:
        if no > (vetor[i] + p[2].distancias[id]):
            p[2].distancias[i] = vetor[i] + p[2].distancias[id]
            change_control = True
        i+=1

    if change_control:
        print("Distância update de 2 até o vizinho 0 é: ", p[2].distancias[0])
        print("Distância update de 2 até o vizinho 1 é: ", p[2].distancias[1])
        print("Distância update de 2 até o vizinho 3 é: ", p[2].distancias[3])
        print("")
        send_request(p[2])

def update3(vetor, id):
    time.sleep(2)
    change_control = False
    i = 0
    for no in p[3].distancias:
        if no > (vetor[i] + p[3].distancias[id]):
            p[3].distancias[i] = vetor[i] + p[3].distancias[id]
            change_control = True
        i+=1

    if change_control:
        print("Distância update de 3 até o vizinho 0 é: ", p[3].distancias[0])
        print("Distância update de 3 até o vizinho 1 é: ", p[3].distancias[1])
        print("Distância update de 3 até o vizinho 2 é: ", p[3].distancias[2])
        print("")
        send_request(p[3])

rtinit0(p[0])
rtinit1(p[1])
rtinit2(p[2])
rtinit3(p[3])



