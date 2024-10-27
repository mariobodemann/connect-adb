#!/usr/bin/env python3
import http.server

SERVER_ADDRESS = "http://192.168.178.147:65535"

def reverseConnectFromPhoneToDevMachineToPhone():
    class StartADBConnectServerHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            print(f"GET request from {self.client_address}.")

            response = open("index.html").read()
            
            self.wfile.write(
                f'HTTP/1.1 200 OK\n'
                f'Server: adb-yolo.py/0.0.01-SNAPSHOT\n'
                f'Content-Type: text/html; charset=UTF-8\n'
                f'Content-Length: {len(response)}\n'
                f'\n{response}'
                .encode('utf-8')
            )

        def do_POST(self):
            req_len = self.headers['Content-Length']
            request = self.rfile.read(int(req_len)).decode()

            print(f"Received {request} from {self.client_address}.")

            if ':' in request:
                try:
                    response = call_adb(request)
                    response_code = 200
                except Exception as e:
                    response = f"Error: {e}."
                    response_code = 400
            else:
                response = "Invalid payload. Please provide a body of 'ip=host:port' as POST payload."
                response_code = 400

            print(response)
            self.wfile.write(
                f'HTTP/1.1 {response_code} OK\n'
                f'Server: adb-yolo.py/0.0.01-SNAPSHOT\n'
                f'Content-Type: text/plain charset=UTF-8\n'
                f'Content-Length: {len(response)}\n'
                f'\n{response}'
                .encode('utf-8')
            )

    def creator(a, b, c) -> http.server.BaseHTTPRequestHandler:
        return StartADBConnectServerHandler(a, b, c)

    print("ready")
    http.server.HTTPServer(
        server_address=("", 65535),
        bind_and_activate=True,
        RequestHandlerClass=creator
    ).serve_forever()


def call_adb(request):
    import subprocess
    name, value = request.split('=')

    if name != 'ip':
        return f'Wrong parameter name, excpected "ip", not "{name}".'

    # start adb with that connection
    host, port = value.split(":") # check user input? nah!
    adb_command = ('adb', 'connect', f'{host}:{port}',)

    process = subprocess.Popen(
        adb_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    process.wait()

    output = process.stdout.read().decode('utf-8')
    response = f"Output: {output}."
    return response


if __name__ == '__main__':
    print("Starting ...")
    reverseConnectFromPhoneToDevMachineToPhone()
