# king-chat
This is a powerful chat center for all kinds of messages.

### Principles
json in, json out. 

> That is to say, don't send pure text, it's silly, send json instead.

### Installation
```bash
sudo pip3 install king-chat
```

### Usage
server
```python
from king_chat import Server

server = Server(ip="127.0.0.1", port=5920)


@server.on_received
def handle(protocol, text):
    print(f"Server got: {text}")
    protocol.send_to_all_except_sender(text)


server.start(wait=True)
```

client 1
```python
from king_chat import Client

client = Client(name="qq", ip="127.0.0.1", port=5920)


@client.on_received
def on_received(protocol, text):
    print(f"We got a msg: {text}")


client.start(wait=False)

while 1:
    client.send(input('What you wanna say: '))
```

client 2
```python
from king_chat import Client

client = Client(name="telegram", ip="127.0.0.1", port=5920)


@client.on_received
def on_received(protocol, text):
    print(f"We got a msg: {text}")


client.start(wait=False)

while 1:
    client.send(input('What you wanna say: '))
```
