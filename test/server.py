from king_chat import Server
server = Server(ip="127.0.0.1", port=5920)

from flask import Flask
app = Flask(__name__)

@server.on_received
def handle(protocol, text):
    print(text)
    server.send_to_all(text)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    server.reactor.callInThread(app.run, debug=False)
    server.start(wait=True)
    #app.run(debug=True)
