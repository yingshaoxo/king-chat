import threading

from twisted.internet import protocol, reactor


class Protocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.append(self)
        #print("connection made")

    def connectionLost(self, reason):
        if self in self.factory.clients:
            self.factory.clients.remove(self)
        #print("connection lost")

    def dataReceived(self, data):
        try:
            text = data.decode("utf-8")
        except Exception as e:
            print(e)
            text = ""

        if text == "//**what's your name**//":
            self.handle_setname()
        elif self.factory.state == "chat":
            self.handle_chat(text)

    def handle_setname(self):
        self.transport.write(f"{self.factory.name}".encode('utf-8'))
        self.factory.state = "chat"

    def handle_chat(self, msg):
        msg = msg.strip("\n ")
        self.factory.on_text_received_function(self, msg)

    def send(self, text):
        self.transport.write(text.encode("utf-8"))


class ProtocolFactory(protocol.ReconnectingClientFactory):
    def __init__(self, name, on_text_received_function):
        self.name = name
        self.state = "setname"

        self.clients = []
        self.on_text_received_function = on_text_received_function

    def buildProtocol(self, addr):
        self.resetDelay()
        return Protocol(self)

    def clientConnectionLost(self, connector, reason):
        print("Lost connection: \n", reason)
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed: \n", reason)
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def send(self, text):
        if self.clients:
            self.clients[-1].transport.write(text.encode('utf-8'))
            return True
        else:
            return False


class Client():
    def __init__(self, ip, port, name):
        port = int(port)

        self._ip = ip
        self._port = port
        self._name = name

        self.reactor = reactor
        self._factory = None
        def default_handle_function(protocol, text):
            print("(default_action)You got msg: ", text)
        self._on_text_received_function = default_handle_function

        self._tip = "connected with tcp://{ip}:{port}".format(ip=self._ip, port=str(self._port))

    def on_received(self, func):
        self._on_text_received_function = func

    def start(self, wait=False):
        self._factory = ProtocolFactory(self._name, self._on_text_received_function)
        reactor.connectTCP(self._ip, self._port, self._factory)
        self.Thread_Activity = threading.Thread(target=reactor.run, kwargs={"installSignalHandlers": False})
        self.Thread_Activity.start()

        self.Thread_Activity = threading.Thread(target=self._make_sure_connected)
        self.Thread_Activity.start()
        print(self._tip)

        if wait == True:
            self.Thread_Activity.join()
        else:
            pass

    def _make_sure_connected(self):
        from time import sleep
        while 1:
            sleep(10)
            if self._factory:
                if self._factory.state == "chat":
                    self.send("//**i'm connected**//")

    def send(self, text):
        if self._factory:
            return self._factory.send(text)
        else:
            print('you must start the client first to send message!')
            exit()



if __name__ == '__main__':
    client = Client(name='telegram', ip='127.0.0.1', port=5920)

    @client.on_received
    def on_received(protocol, text):
        print('\n', text)

    client.start(wait=False)

    while 1:
        text = input("what you want to say: ")
        client.send(text)
