# king-chat
This is a powerful chat center for all kinds of messages.

#### design principles
* json in, json out

#### usage
server
```python
from king_chat import Server

server = Server(ip="127.0.0.1", port=5920)

@server.on_received
def handle(protocol, text)
    protocol.send_to_all_except_sender(text)

server.start(wait=True)
```

client
```python
from king_chat import Client

client = Client(name="qq", ip="127.0.0.1", port=5920)

@client.on_received
def on_received(protocol, text):
    print(text)

client.start(wait=False)

while 1:
    client.send(input('words: '))
```
