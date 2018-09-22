# king-chat
This is a powerful chat center for all kinds of messages.

#### design principles
* json in, json out

#### Usage
server
```
server = Server(ip='127.0.0.1', port=5920)

def on_received(protocol, text):
    protocol.send_to_all_except_sender(text)
server.on_text_received_function = on_received

server.start(wait=True)
```

client
```
client = Client(name='qq', ip='127.0.0.1', port=5920)

def on_received(protocol, text):
    print(text)
client.on_text_received_function = on_received

client.start(wait=False)

while 1:
    text = input("what you want to say: ")
    client.send(text)
```
