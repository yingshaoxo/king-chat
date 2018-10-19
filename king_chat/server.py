import threading

from twisted.internet import protocol, reactor


class Client(protocol.Protocol):
    def __init__(self, factory):
        self.name = None
        self.state = "getname"

        self.factory = factory

    def connectionMade(self):
        self.transport.write("//**what's your name**//".encode("utf-8"))

    def connectionLost(self, reason):
        if self.name in self.factory.clients:
            del self.factory.clients[self.name]

    def dataReceived(self, data):
        try:
            text = data.decode("utf-8")
        except Exception as e:
            print(e)
            text = ""

        if self.state == "getname":
            self.handle_getname(text)
        elif self.state == "chat":
            #if "//**i'm connected**//" in text:
            if "**i'm connected**" in text:
                return
            else:
                self.handle_chat(text)

    def handle_getname(self, name):
        if name != "":
            if name in self.factory.clients:
                self.transport.loseConnection()
                return
            self.name = name
            self.factory.clients[name] = self # the self is a protocol, also a instance of connection
            self.state = "chat"
        else:
            self.transport.loseConnection()

    def handle_chat(self, msg):
        msg = msg.strip("\n ")
        self.factory.on_text_received_function(self, msg)

    def send(self, text):
        self.transport.write(text.encode("utf-8"))

    def send_to_one(self, name, text):
        if name in self.factory.clients:
            self.factory.clients[name].transport.write(text.encode("utf-8"))

    def send_to_all(self, text):
        for name, protocol in self.factory.clients.items():
            protocol.transport.write(text.encode("utf-8"))

    def send_to_all_except_sender(self, text):
        for name, protocol in self.factory.clients.items():
            if protocol != self:
                protocol.transport.write(text.encode("utf-8"))


class ClientFactory(protocol.Factory):
    def __init__(self, on_text_received_function):
        self.clients = {}
        self.on_text_received_function = on_text_received_function

    def buildProtocol(self, addr):
        return Client(self)

    def send_to_one(self, name, text):
        if name in self.clients:
            self.clients[name].transport.write(text.encode("utf-8"))
            return True
        else:
            return False

    def send_to_all(self, text):
        for name, protocol in self.clients.items():
            protocol.transport.write(text.encode("utf-8"))


class Server():
    def __init__(self, ip, port):
        port = int(port)

        self._ip = ip
        self._port = port

        self._factory = None
        self.reactor = reactor

        def default_handle_function(protocol, text):
            print("(default_action)You got msg: ", text)
        self._on_text_received_function = default_handle_function

        self._tip = "serving at tcp://{ip}:{port}".format(ip=self._ip, port=str(self._port))

    def on_received(self, func):
        self._on_text_received_function = func

    def start(self, wait=True):
        self._factory = ClientFactory(self._on_text_received_function)
        reactor.listenTCP(self._port, self._factory, interface=self._ip)
        self.Thread_Activity = threading.Thread(target=reactor.run, kwargs={"installSignalHandlers": False})
        self.Thread_Activity.start()
        print(self._tip)

        if wait == True:
            self.Thread_Activity.join()
        else:
            pass

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
            print('you must start the client first to send message!')
            exit()

    def _get_connected_clients(self):
        if self._factory:
            return self._factory.clients


if __name__ == '__main__':
    server = Server(ip='127.0.0.1', port=5920)

    @server.on_received
    def on_received(protocol, text):
        print(text)
        protocol.send_to_all_except_sender(text)

    server.start(wait=False)

    while 1:
        text = input("what you want to say: ")
        #server.send_to_one('qq', text)
        server.send_to_all(text)
        print(server._get_connected_clients())
