from king_chat import Client

client = Client(name="qq", ip="127.0.0.1", port=5920)

@client.on_received
def on_received(protocol, text):
    print(text)

client.start(wait=False)

while 1:
    client.send(input('words: '))
