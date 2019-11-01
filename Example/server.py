from king_chat import Server

server = Server(ip="127.0.0.1", port=5920)


@server.on_received
def handle(protocol, text):
    print(f"Server got: {text}")
    protocol.send_to_all_except_sender(text)


server.start(wait=True)
