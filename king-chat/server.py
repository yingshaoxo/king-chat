import threading

from twisted.internet import protocol, reactor


class Client(protocol.Protocol):
    def __init__(self, clients, on_text_received_function):
        self.clients = clients
        self.on_text_received_function = on_text_received_function
        self.name = None
        self.state = "getname"

    def connectionMade(self):
        self.transport.write("//**what's your name**//".encode("utf-8"))

    def connectionLost(self, reason):
        if self.name in self.clients:
            del self.clients[self.name]

    def dataReceived(self, data):
        try:
            text = data.decode("utf-8")
        except Exception as e:
            print(e)
            text = ""

        if self.state == "getname":
            self.handle_getname(text)
        elif self.state == "chat":
            self.handle_chat(text)

    def handle_getname(self, name):
        if name != "":
            if name in self.clients:
                self.transport.loseConnection()
                return
            self.name = name
            self.clients[name] = self # the self is a protocol, also a instance of connection
            self.state = "chat"
        else:
            self.transport.loseConnection()

    def handle_chat(self, msg):
        msg = msg.strip("\n ")
        self.on_text_received_function(self, msg)

    def send(self, text):
        self.transport.write(text.encode("utf-8"))

    def send_to_one(self, name, text):
        if name in self.clients:
            self.clients[name].transport.write(text.encode("utf-8"))

    def send_to_all(self, text):
        for name, protocol in self.clients.items():
            protocol.transport.write(text.encode("utf-8"))

    def send_to_all_except_sender(self, text):
        for name, protocol in self.clients.items():
            if protocol != self:
                protocol.transport.write(text.encode("utf-8"))


class ClientFactory(protocol.Factory):
    def __init__(self, on_text_received_function):
        self.clients = {}
        self.on_text_received_function = on_text_received_function

    def buildProtocol(self, addr):
        return Client(self.clients, self.on_text_received_function)

    def send_to_one(self, name, text):
        if name in self.clients:
            self.clients[name].transport.write(text.encode("utf-8"))

    def send_to_all(self, text):
        for name, protocol in self.clients.items():
            protocol.transport.write(text.encode("utf-8"))


class Server():
    def __init__(self, ip, port):
        port = int(port)

        self._ip = ip
        self._port = port

        self._factory = None
        self.on_text_received_function = None

        self._tip = "serving at tcp://{ip}:{port}".format(ip=self._ip, port=str(self._port))

    def start(self, wait=True):
        if (self.on_text_received_function):
            self._factory = ClientFactory(self.on_text_received_function)
            reactor.listenTCP(self._port, self._factory, interface=self._ip)
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

    def send_to_one(self, name, text):
        if self._factory:
            self._factory.send_to_one(name, text)
        else:
            print('you must start the client firest to send message!')
            exit()

    def send_to_all(self, text):
        if self._factory:
            self._factory.send_to_all(text)
        else:
            print('you must start the client firest to send message!')
            exit()

    def get_connected_clients(self):
        if self._factory:
            return self._factory.clients


if __name__ == '__main__':
    server = Server(ip='127.0.0.1', port=5920)

    def on_received(protocol, text):
        print(text)
    server.on_text_received_function = on_received

    server.start(wait=False)

    while 1:
        text = input("what you want to say: ")
        server.send_to_one('qq', text)
        print(server.get_connected_clients())
