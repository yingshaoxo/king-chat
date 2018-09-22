import threading

from twisted.internet import protocol, reactor


class Protocol(protocol.Protocol):
    def __init__(self, name, clients, on_text_received_function):
        self.clients = clients
        self.name = name
        self.state = "setname"

        self.on_text_received_function = on_text_received_function

    def connectionMade(self):
        self.clients.append(self)
        #print("connection made")

    def connectionLost(self, reason):
        if self in self.clients:
            self.clients.remove(self)
        #print("connection lost")

    def dataReceived(self, data):
        try:
            text = data.decode("utf-8")
        except Exception as e:
            print(e)
            text = ""

        if text == "//**what's your name**//":
            self.handle_setname()
        elif self.state == "chat":
            self.handle_chat(text)

    def handle_setname(self):
        self.transport.write(f"{self.name}".encode('utf-8'))
        self.state = "chat"

    def handle_chat(self, msg):
        msg = msg.strip("\n ")
        self.on_text_received_function(self, msg)

    def send(self, text):
        self.transport.write(text.encode("utf-8"))


class ProtocolFactory(protocol.ClientFactory):
    def __init__(self, name, on_text_received_function):
        self.name = name
        self.clients = []
        self.on_text_received_function = on_text_received_function

    def buildProtocol(self, addr):
        return Protocol(name=self.name, clients=self.clients, on_text_received_function=self.on_text_received_function)

    def send(self, text):
        if self.clients:
            self.clients[-1].transport.write(text.encode('utf-8'))
            print(self.clients[-1].transport.connected)
            py.help(self.clients[-1].transport)


class Client():
    def __init__(self, ip, port, name):
        port = int(port)

        self._ip = ip
        self._port = port
        self._name = name

        self._factory = None
        self.on_text_received_function = None

        self._tip = "connected at tcp://{ip}:{port}".format(ip=self._ip, port=str(self._port))

    def start(self, wait=True):
        if (self.on_text_received_function):
            self._factory = ProtocolFactory(self._name, self.on_text_received_function)
            reactor.connectTCP(self._ip, self._port, self._factory)
            self.Thread_Activity = threading.Thread(target=reactor.run, kwargs={"installSignalHandlers": False})
            self.Thread_Activity.start()
            print(self._tip)

            if wait == True:
                self.Thread_Activity.join()
            else:
                pass
        else:
            print('You must specify self.on_text_received_function to hanle incoming text')
            exit()

    def send(self, text):
        if self._factory:
            self._factory.send(text)
        else:
            print('you must start the client firest to send message!')
            exit()



if __name__ == '__main__':
    client = Client(name='qq', ip='127.0.0.1', port=5920)

    def on_received(protocol, text):
        print('\n', text)
    client.on_text_received_function = on_received

    client.start(wait=False)

    while 1:
        text = input("what you want to say: ")
        client.send(text)
