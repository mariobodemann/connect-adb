#!/usr/bin/env python3
import http.server

SERVER_ADDRESS = "http://192.168.178.147:65535"

def reverseConnectFromPhoneToDevMachineToPhone():
    class StartADBConnectServerHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            """
            Inform user about which script to install in .shortcuts in termux....
            :return:
            """
            response = """#!/data/data/com.termux/files/usr/bin/env bash
# script to tell the developer machine to connect to the phone calling this script. Yolo.
#
# Put me under .shortcuts/ in termux and create a shortcut on desktop or something
#
# install missing commands if needed with `$0 install`

# update with dev machine ip address
server='SERVER_ADDRESS'

if [[ ${1} == "install" ]]; then
    command termux-clipboard-get 2> /dev/null && pkg install termux-api
    command curl 2> /dev/null && pkg install curl
    command jq 2> /dev/null && pkg install jq
fi

client="$(termux-clipboard-get)"
echo "(clipboard) client= ${client}."

if ! [[ "${client}" =~ ":" ]]; then
        client="$(termux-dialog text -t 'Enter Wireless Debug Address' -i 'ip:port' | jq -r .text)"
        echo "User dialog provided client '${client}'."

        if ! [[ "${client}" =~ ":" ]]; then
                termux-dialog confirm -t 'Failure' -i "'${client}' is an invalid IP." > /dev/null 2>&1
                exit
        fi
fi

result="$(curl --silent "${server}" -d "${client}")"
echo "${result}"

termux-dialog confirm -t 'Result' -i "${result}" > /dev/null 2>&1

""".replace("SERVER_ADDRESS", SERVER_ADDRESS)

            print(f"GET request from {self.client_address}.")

            self.wfile.write(
                f'HTTP/1.1 200 OK\n'
                f'Server: adb-yolo.py/0.0.01-SNAPSHOT\n'
                f'Content-Type: application/json; charset=UTF-8\n'
                f'Content-Length: {len(response)}\n'
                f'\n{response}'
                .encode('utf-8')
            )

        def do_POST(self):
            req_len = self.headers['Content-Length']
            request = self.rfile.read(int(req_len)).decode()

            print(f"Received {request} from {self.client_address}.")

            if ':' in request:
                response = call_adb(request)
                response_code = 200
            else:
                response = "Invalid payload. Please provide a body of 'ip:port' as POST payload."
                response_code = 400

            print(f"adb says: {response}")
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

    # start adb with that connectio
    ip, port = request.split(":")
    adb_command = ('adb', 'connect', f'{ip}:{port}',)

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
