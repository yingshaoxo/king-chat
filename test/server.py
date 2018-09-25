from king_chat import Server

server = Server(ip="127.0.0.1", port=5920)
server.start(wait=False)

while 1:
    #server.send_to_one("qq", input("word: "))
    server.send_to_all(input("word: "))
