from king_chat import Client

client = Client(name="qq", ip="127.0.0.1", port=5920)

count = 0
@client.on_received
def on_received(protocol, text):
    if text != "hi":
        exit()

    global count
    count += 1
    print(text + str(count))

    client.send(text)

client.start(wait=False)

while 1:
    input()
    successed = client.send('hi')
