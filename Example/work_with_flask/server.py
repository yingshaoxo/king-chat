from king_chat import Server
server = Server(ip="127.0.0.1", port=5920)

from flask import Flask
app = Flask(__name__)

count = 0
@server.on_received
def handle(protocol, text):
    if text != "hi":
        exit()

    global count
    count += 1
    print(text + str(count))

    server.send_to_one('qq', text)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    server.reactor.callInThread(app.run, debug=False)
    server.start(wait=True)
    #app.run(debug=True)
