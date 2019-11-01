from king_chat import Client

client = Client(name="telegram", ip="127.0.0.1", port=5920)


@client.on_received
def on_received(protocol, text):
    print(f"We got a msg: {text}")


client.start(wait=False)

while 1:
    client.send(input('What you wanna say: '))
