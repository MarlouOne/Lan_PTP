import socketserver
import json

user_names = []
massages = {}

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip()

        resp = json.loads(data.decode())
        response_text = ''

        if resp.get('user_name') is not None:
            user_names.append(resp.get('user_name'))
        if resp.get('get') is not None:
            response_text = massages.pop(resp.get('get'), '')
        if resp.get("for") is not None:
            massages.update([(resp.get('for'),resp.get('text'))])

        if response_text != '':
            print(response_text)

        self.request.sendall(bytes(response_text, 'utf-8'))

with ThreadingTCPServer(('127.0.0.1', 15000),MyTCPHandler) as server:
    server.serve_forever()


